#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import kb_link_intake


class UrlValidationTests(unittest.TestCase):
    def test_accepts_public_https_and_removes_fragment(self) -> None:
        self.assertEqual(
            kb_link_intake.validate_public_https_url(
                "https://example.com/article?q=1#section"
            ),
            "https://example.com/article?q=1",
        )

    def test_rejects_non_https_and_local_targets(self) -> None:
        invalid = (
            "http://example.com",
            "https://localhost/page",
            "https://127.0.0.1/page",
            "https://10.0.0.1/page",
            "https://user:secret@example.com/page",
            "https://example.com:8443/page",
            "https://example.com/a|b",
        )
        for url in invalid:
            with self.subTest(url=url), self.assertRaises(kb_link_intake.IntakeError):
                kb_link_intake.validate_public_https_url(url)

    def test_extracts_first_acceptable_url(self) -> None:
        body = "내부 https://127.0.0.1/a 다음 공개 https://example.com/post."
        self.assertEqual(
            kb_link_intake.first_public_https_url(body),
            "https://example.com/post",
        )


class PrepareTests(unittest.TestCase):
    def test_prepares_trusted_issue_event_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event_path = root / "event.json"
            intake_path = root / ".gemini" / "kb-link-intake.json"
            output_path = root / "github-output.txt"
            event_path.write_text(
                json.dumps(
                    {
                        "issue": {
                            "number": 42,
                            "title": "[KB 링크] 문서",
                            "body": "### 링크\nhttps://example.com/post\n\n### 메모\n검토",
                            "user": {"login": "owner"},
                        },
                        "repository": {
                            "html_url": "https://github.com/example/repo"
                        },
                    }
                ),
                encoding="utf-8",
            )

            environment = {
                "GITHUB_EVENT_NAME": "issues",
                "GITHUB_EVENT_PATH": str(event_path),
                "GITHUB_REPOSITORY": "example/repo",
                "GITHUB_RUN_ID": "100",
                "GITHUB_ACTOR": "owner",
                "GITHUB_OUTPUT": str(output_path),
            }
            with (
                patch.object(kb_link_intake, "INTAKE_PATH", intake_path),
                patch.dict(os.environ, environment, clear=True),
            ):
                kb_link_intake.prepare_intake()

            payload = json.loads(intake_path.read_text(encoding="utf-8"))
            outputs = output_path.read_text(encoding="utf-8")
            self.assertEqual(payload["source_url"], "https://example.com/post")
            self.assertEqual(payload["source_id"], "issue-42")
            self.assertIn("record_name", outputs)
            self.assertIn("kb-link-issue-42.md", outputs)


class AnalyzeTests(unittest.TestCase):
    def test_html_extractor_omits_script_and_style(self) -> None:
        parser = kb_link_intake._TextExtractor()
        parser.feed("<h1>제목</h1><script>secret()</script><style>x{}</style><p>본문</p>")
        self.assertEqual(parser.parts, ["제목", "본문"])

    @patch("kb_link_intake.socket.getaddrinfo")
    def test_rejects_hostname_resolving_to_private_address(self, resolve) -> None:
        resolve.return_value = [(2, 1, 6, "", ("10.0.0.1", 443))]
        with self.assertRaisesRegex(kb_link_intake.IntakeError, "non-public"):
            kb_link_intake.validate_resolved_host("https://example.com/post")

    def test_analyze_calls_gemini_once_and_keeps_key_out_of_url(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            intake_path = root / ".gemini" / "kb-link-intake.json"
            response_path = root / "gemini-artifacts" / "response.json"
            (root / "knowledge-base").mkdir(parents=True)
            intake_path.parent.mkdir(parents=True)
            intake_path.write_text(
                json.dumps(
                    {
                        "source_url": "https://example.com/post",
                        "note": "검토",
                    }
                ),
                encoding="utf-8",
            )
            (root / "knowledge-base" / "tools").mkdir()
            for name in (
                "ax-platform-context.md",
                "knowledge-graph-schema.md",
                "index.md",
            ):
                (root / "knowledge-base" / name).write_text("context", encoding="utf-8")
            (root / "knowledge-base" / "tools" / "catalog.md").write_text(
                "catalog", encoding="utf-8"
            )

            decision = RenderTests.decision()
            api_body = json.dumps(
                {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": json.dumps(decision, ensure_ascii=False)}
                                ]
                            }
                        }
                    ]
                }
            ).encode("utf-8")
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.return_value = api_body
            opener = MagicMock()
            opener.open.return_value = response

            with (
                patch.object(kb_link_intake, "REPO_ROOT", root),
                patch.object(kb_link_intake, "INTAKE_PATH", intake_path),
                patch.object(kb_link_intake, "fetch_source_text", return_value="본문"),
                patch.object(kb_link_intake, "build_opener", return_value=opener),
                patch.dict(
                    os.environ,
                    {"GEMINI_API_KEY": "test-secret", "GEMINI_MODEL": "gemini-test"},
                    clear=True,
                ),
            ):
                result_path = kb_link_intake.analyze_once(
                    Path("gemini-artifacts/response.json")
                )

            opener.open.assert_called_once()
            self.assertEqual(result_path, response_path)
            request = opener.open.call_args.args[0]
            self.assertNotIn("test-secret", request.full_url)
            self.assertEqual(request.get_header("X-goog-api-key"), "test-secret")
            self.assertEqual(
                json.loads(response_path.read_text(encoding="utf-8"))["response"],
                json.dumps(decision, ensure_ascii=False),
            )


class RenderTests(unittest.TestCase):
    @staticmethod
    def decision(**overrides: object) -> dict[str, object]:
        value: dict[str, object] = {
            "decision": "add",
            "title": "테스트 링크",
            "reason": "새로운 근거가 있어 추가합니다.",
            "summary": "링크의 핵심 내용을 간략히 분석했습니다.",
            "key_points": ["새로운 [근거](relative.md)"],
            "kb_relevance": "AX 플랫폼 설계와 관련됩니다.",
            "limitations": ["런타임은 검증하지 않았습니다."],
        }
        value.update(overrides)
        return value

    def test_add_decision_renders_record_and_neutralizes_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            intake_path = root / ".gemini" / "kb-link-intake.json"
            record_root = root / "knowledge-base" / "execution-records"
            response_path = root / "response.json"
            output_path = root / "github-output.txt"
            intake_path.parent.mkdir(parents=True)
            intake_path.write_text(
                json.dumps(
                    {
                        "source_url": "https://example.com/post",
                        "note": "see [local](missing.md)",
                        "source_id": "issue-42",
                        "source_ref": "https://github.com/example/repo/issues/42",
                        "title": "테스트",
                        "submitter": "owner",
                        "repository": "example/repo",
                        "submitted_at": "2026-08-15T00:00:00+00:00",
                        "github_run_id": "100",
                    }
                ),
                encoding="utf-8",
            )
            response_path.write_text(
                json.dumps(
                    {"response": json.dumps(self.decision(), ensure_ascii=False)}
                ),
                encoding="utf-8",
            )

            with (
                patch.object(kb_link_intake, "REPO_ROOT", root),
                patch.object(kb_link_intake, "INTAKE_PATH", intake_path),
                patch.object(kb_link_intake, "RECORD_ROOT", record_root),
                patch.dict(
                    os.environ,
                    {
                        "GEMINI_MODEL": "gemini-test",
                        "GITHUB_OUTPUT": str(output_path),
                    },
                ),
            ):
                decision, result = kb_link_intake.render_result(response_path)

            rendered = result.read_text(encoding="utf-8")
            self.assertEqual(decision, "add")
            self.assertIn("execution-run-kb-link-issue-42", rendered)
            self.assertIn("intake_decision: add", rendered)
            self.assertIn("requested model: `gemini-test`", rendered)
            self.assertNotIn("[근거](relative.md)", rendered)
            self.assertIn("&#91;근거&#93;(relative.md)", rendered)
            self.assertIn("\nadd\n", output_path.read_text(encoding="utf-8"))

    def test_skip_decision_writes_reason_without_kb_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            intake_path = root / ".gemini" / "kb-link-intake.json"
            record_root = root / "knowledge-base" / "execution-records"
            result_root = root / "gemini-artifacts"
            skip_path = result_root / "kb-link-skip-comment.md"
            response_path = root / "response.json"
            output_path = root / "github-output.txt"
            intake_path.parent.mkdir(parents=True)
            intake_path.write_text(
                json.dumps(
                    {
                        "source_url": "https://example.com/post",
                        "note": "검토",
                        "source_id": "issue-43",
                        "source_ref": "https://github.com/example/repo/issues/43",
                    }
                ),
                encoding="utf-8",
            )
            response_path.write_text(
                json.dumps(
                    {
                        "response": json.dumps(
                            self.decision(
                                decision="skip",
                                reason="기존 내용과 중복됩니다. @team #42",
                                summary="새로운 근거가 없습니다.",
                            ),
                            ensure_ascii=False,
                        )
                    }
                ),
                encoding="utf-8",
            )

            with (
                patch.object(kb_link_intake, "REPO_ROOT", root),
                patch.object(kb_link_intake, "INTAKE_PATH", intake_path),
                patch.object(kb_link_intake, "RECORD_ROOT", record_root),
                patch.object(kb_link_intake, "RESULT_ROOT", result_root),
                patch.object(kb_link_intake, "SKIP_COMMENT_PATH", skip_path),
                patch.dict(os.environ, {"GITHUB_OUTPUT": str(output_path)}),
            ):
                decision, result = kb_link_intake.render_result(response_path)

            self.assertEqual(decision, "skip")
            self.assertEqual(result, skip_path)
            self.assertFalse(record_root.exists())
            comment = skip_path.read_text(encoding="utf-8")
            self.assertIn("추가하지 않음", comment)
            self.assertIn("기존 내용과 중복됩니다.", comment)
            self.assertIn("&#64;team &#35;42", comment)
            self.assertNotIn("@team #42", comment)
            self.assertIn("\nskip\n", output_path.read_text(encoding="utf-8"))

    def test_rejects_invalid_decision_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            response_path = Path(directory) / "response.json"
            response_path.write_text(
                json.dumps({"response": '{"decision":"maybe"}'}),
                encoding="utf-8",
            )
            with self.assertRaises(kb_link_intake.IntakeError):
                kb_link_intake.parse_model_decision(response_path)


if __name__ == "__main__":
    unittest.main()
