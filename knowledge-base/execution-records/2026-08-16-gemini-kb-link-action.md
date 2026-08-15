---
id: execution-run-gemini-kb-link-action-2026-08-16
type: execution-record
title: Gemini 모바일 링크 수집 GitHub Action 구현 기록
status: historical-snapshot
observed_at: 2026-08-16
profile_id: implement-deep
profile_revision: 1
verification_ceiling: V2
tags:
  - knowledge-base
  - execution-record
  - github-actions
  - gemini
  - link-intake
---

# Gemini 모바일 링크 수집 GitHub Action 구현 기록

[지식 베이스 홈](../index.md) · [실행 프로파일](../agent-profiles.md) ·
[지속 컨텍스트](../ax-platform-context.md)

이 문서는 모바일 Issue 또는 수동 입력으로 공개 링크를 받아 Gemini API로 분석하고,
추가 여부에 따라 검토용 KB execution record PR 또는 원본 Issue의 미추가 사유 댓글로
분기하는 자동화 구현 시점의 기록이다.

## Run identity

| 필드 | 실제 기록 |
|---|---|
| task/run ID | `gemini-kb-link-action-2026-08-16` |
| 역할 | worker / workflow implementer |
| profile | requested/actual `implement-deep@1` |
| model provider | OpenAI |
| requested model tier | `deep` |
| actual model slug/version | `unknown` — 실행 telemetry에서 관찰하지 못함 |
| requested/actual effort | `high` / `unknown` |
| 시작 시각 | exact `unknown`; 2026-08-15 KST |
| 종료·최종 검증 시각 | `2026-08-16T00:15+09:00` |
| base/head SHA | `148e1c51ec5bf4fe16968abe94c83d2f89f65550` / uncommitted HEAD 동일 |
| branch | `main` |
| cost/latency | `unknown` / `unknown` |

## Environment fingerprint

| 항목 | 값 |
|---|---|
| workspace | `/home/sh-cat-lee/workspaces/AT` |
| kernel | Linux `6.18.33.2-microsoft-standard-WSL2`, x86_64 |
| shell | GNU bash |
| Git | `2.53.0` |
| validation runtime | Python `3.14.4`, PyYAML `6.0.3` |

## 구현 범위와 결과

- 전용 Issue form과 `workflow_dispatch` 입력을 추가했다.
- Issue 자동 실행은 `[KB 링크]` 제목과 `OWNER|MEMBER|COLLABORATOR` author association을
  동시에 요구한다.
- URL은 HTTPS·공개 hostname·기본 포트만 허용하며 literal 사설/로컬 IP, credentials와
  Markdown에 위험한 미인코딩 문자를 거부한다.
- Gemini job은 `contents: read`만 받고 core tool allowlist에서 file write, shell,
  GitHub 도구와 검색을 제외했다. 정확한 제출 URL의 `web_fetch`만 승인한다.
- Gemini 출력은 Action step output을 사용하지 않고 JSON log를 결정론적 Python renderer가
  엄격한 JSON schema로 검사한다. 불명확하거나 schema 밖의 출력은 fail-closed 처리한다.
- 분석 결과가 `add`이면 간략 분석 `execution-record`를 만들고, `skip`이면 KB 파일을 만들지
  않은 채 사유·판단 요약을 안전하게 중립화한 Issue 댓글 artifact만 만든다.
- 별도 publish job만 `contents/issues/pull-requests: write`를 받고 자동화 branch와 검토용
  PR을 생성한다. 별도 skip-report job은 `issues: write`만 받고 원본 Issue에 사유를 남긴다.
  merge는 수행하지 않는다.
- 모든 직접 사용 Action을 전체 commit SHA로 고정하고 Gemini CLI를 `0.53.0`으로 고정했다.
- `GEMINI_MODEL` repository variable이 없으면 기본 요청 모델은 `gemini-3.7-flash`다.

## Upstream 정적 확인

| 대상 | 고정값·관찰 | 증거 범위 |
|---|---|---|
| `run-gemini-cli` | [`v0.1.22` commit `f77273f4c914e4bf38440cf36a0369cb64a37489`](https://github.com/google-github-actions/run-gemini-cli/commit/f77273f4c914e4bf38440cf36a0369cb64a37489) | 입력 `gemini_api_key`, `gemini_model`, `gemini_cli_version`, `settings`와 JSON log 생성 경로를 fixed-SHA `action.yml`에서 정적 확인 |
| Gemini CLI | [`v0.53.0`](https://github.com/google-gemini/gemini-cli/releases/tag/v0.53.0) | release 존재와 버전 고정만 확인; 이 저장소 CI 실행은 미수행 |

공식 Action은 pinned version에서도 Gemini CLI를 `--yolo`로 실행하므로, prompt 지시만이 아니라
`tools.core` allowlist로 모델에 노출되는 도구 자체를 제한했다. Action의 고정 `EOF` multiline
output delimiter는 모델 출력과 충돌할 수 있어 후속 단계가 Action output을 소비하지 않게 했고,
모델에도 단독 `EOF` 행을 출력하지 말도록 요구했다.

## Validation record

| 검사 | 명령·방법 | exit/result | 해석 |
|---|---|---|---|
| 기준 상태 | `git status --short --branch`; `git rev-parse HEAD` | exit `0`; clean `main`, base SHA 확인 | 사용자 기존 변경 없음 |
| 첫 단위검사 | `python3 scripts/test_kb_link_intake.py` | exit `1`; 임시 test root와 출력 경로의 상대화 불일치 | 기능 코드가 아닌 test fixture 경로를 보정 |
| 단위검사 재실행 | 같은 명령 | exit `0`; 4 tests | URL·renderer 기본 경계 통과 |
| 확장 단위검사 | 같은 명령 | exit `0`; 5 tests | Issue event prepare, URL 제한, 응답 중립화 통과 |
| 통합 shell 첫 시도 | 단위검사와 후속 검사를 한 shell command로 구성 | nonzero; shell quote의 예상치 못한 EOF로 검사 시작 전 종료 | 제품 코드 결과가 아니며 명령 quoting을 분리해 재시도 |
| 분기 단위검사 | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_kb_link_intake.py` | exit `1`; 7 tests 중 2 failures | HTML entity를 순차 치환해 entity 내부 `#`를 다시 치환하는 결함 발견 |
| 중립화 수정 후 단위검사 | 같은 명령 | exit `0`; 7 tests | add/skip 분기, KB 파일 유무, strict schema, 링크·멘션 중립화 통과 |
| Python syntax | `python3 -m py_compile scripts/kb_link_intake.py scripts/test_kb_link_intake.py scripts/validate_knowledge_base.py` | exit `0` | 세 Python 파일 compile 통과 |
| YAML parse | PyYAML `BaseLoader`로 workflow와 Issue form parse | exit `0` | YAML 구문·최상위 구조 확인; GitHub runner 실행 증거는 아님 |
| 확장 YAML gate 첫 시도 | jobs·권한·분기·Action SHA assertion | exit `1`; 잘못 이스케이프한 검사 regex가 `uses:`를 0개로 탐지 | 검사 harness를 수정해 같은 source에 재시도 |
| Action pin gate | `rg`로 `uses:` 전수 확인 후 mutable tag pattern 검사 | exit `0`; 5개 사용 모두 full SHA | 직접 참조 Action의 정적 pin 확인 |
| KB structural gate | `python3 scripts/validate_knowledge_base.py` | exit `0`; 중간 57 Markdown 통과 | frontmatter, lifecycle, ID, relative link `V2` 검사 |
| whitespace | `git diff --check` | exit `0` | 중간 diff 오류 없음 |
| 최종 통합 검사 | 단위검사, KB validator, 두 YAML 구조 검사, jobs·권한·분기·Action SHA assertion, `git diff --check` | exit `0`; 7 tests, 58 Markdown, 3 jobs, 7개 `uses:` full-SHA, clean diff check | 이 execution record 포함 최종 로컬 정적 gate 통과 |

## Evidence and authority boundary

- 로컬 증거 상한은 workflow·script·문서 정적 검사 `V2`다.
- `GEMINI_API_KEY` 원문을 읽거나 출력하지 않았고 Gemini API, GitHub-hosted runner,
  artifact 전달, branch push, Issue comment와 PR 생성은 실행하지 않았다. 따라서 실제 모델
  가용성, 웹 fetch, 비용, PR·댓글 생성은 `unknown`이다.
- DNS rebinding과 원격 redirect 뒤의 대상은 로컬 URL 문자열 검사만으로 완전히 보장하지 않는다.
  자동 실행자를 trusted repository association으로 제한한 이유다.
- GitHub 조직·저장소 정책이 Actions의 branch push 또는 PR 생성을 금지하면 publish job은 실패한다.
- stage, commit, push, merge, deploy, external message, credential·permission 변경과 비용 발생
  service 실행은 수행하지 않았다.
