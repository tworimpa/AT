---
id: execution-run-cq-answer-research-2026-08-21
type: execution-record
title: Mozilla AI cq와 Apache Answer 고정 버전 조사 기록
status: historical-snapshot
observed_at: 2026-08-21
profile_id: implement-deep
profile_revision: 1
verification_ceiling: V2
tags:
  - knowledge-base
  - execution-record
  - cq
  - apache-answer
---

# Mozilla AI cq와 Apache Answer 고정 버전 조사 기록

[지식 베이스 홈](../index.md) · [실행 프로파일](../agent-profiles.md) · [지속 컨텍스트](../ax-platform-context.md) · [cq 프로필](../tools/cq.md) · [Apache Answer 프로필](../tools/apache-answer.md)

## 작업 계약

- 범위: 두 official upstream의 immutable commit, license/activity/clone cost, architecture/interface/security/platform 경계를 조사하고 template v3 프로필과 파생 index를 추가한다.
- 비범위: dependency 설치, build/runtime/E2E, hosted service/model 호출, submodule 등록, commit/push/merge/deploy와 외부 write.
- 기준: local base/head `42f4f2d6a0b07bcb28cb782ac89ca6210f06abde`; 기존 사용자 변경은 보존한다.
- 성공 기준: 두 `I2/V2` profile, catalog/coverage/context/index 연결, KB validator와 `git diff --check` green, 증거 상한과 미수행 범위 기록.

## Run identity

| 필드 | 실제 기록 |
|---|---|
| task/run ID | `cq-answer-research-2026-08-21` |
| 역할·profile | worker/documenter / `implement-deep@1` |
| model provider·slug·version | OpenAI / `unknown` / `unknown` |
| requested/actual effort | `high` / `unknown` |
| 시작·종료 시각 | 시작 exact `unknown`; 종료 `2026-08-21T22:04:31+09:00` |
| base/head SHA | `42f4f2d6a0b07bcb28cb782ac89ca6210f06abde` / uncommitted working tree, commit SHA 없음 |
| environment | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; Git 2.53.0; Python 3.14.4 |
| cost/latency | provider cost `unknown`; 개별 network/local command latency만 도구 출력에 관찰, aggregate `unknown` |
| retry budget | 2; network/source inspection retry 0 |

## Source와 선택

| 대상 | official pin과 metadata | source 관리 판단 |
|---|---|---|
| Mozilla AI cq | `mozilla-ai/cq@4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd`; `main`; Apache-2.0; active; GitHub source size 약 2.8 MB | knowledge-plane 비교 대상이라 manifest-only. 직접 adapter/schema 구현 차용 시 gitlink 재검토 |
| Apache Answer | `apache/answer@3b9f1370612e690a0b7f230f05e688930db4c6d3`; `main`; Apache-2.0+NOTICE; active; GitHub source size 약 15.8 MB | knowledge portal 비교 대상이라 manifest-only. 직접 connector/plugin 구현 차용 시 gitlink 재검토 |

GitHub repository metadata의 `pushed_at`은 default branch HEAD timestamp와 다를 수 있어 activity observation으로만 기록했다. immutable pin은 branch API, `git ls-remote`와 shallow clone HEAD의 일치를 확인했다.

## 핵심 분석 결과

- cq는 query-before-retry, typed KU와 local-first MCP/SQLite가 유용하지만 confidence는 truth/freshness proof가 아니다. architecture의 human graduation 설명과 configured remote에서 direct `propose`가 즉시 shared publish될 수 있다는 skill 지침 사이의 authority boundary를 사내 policy가 강제해야 한다.
- Answer는 human-curated Q&A를 REST/MCP/AI tool loop와 search/vector plugins에 재사용한다. 그러나 MCP auth와 Web content ACL parity, in-process plugin 격리, model/embedding egress는 별도 검증·정책 대상이다.
- 두 대상 모두 agent knowledge plane 후보지만 cq는 operational learning feedback loop, Answer는 human knowledge portal이므로 자동 fallback이나 동일 schema로 취급하지 않는다.

## Validation record

| 명령·방법 | exit | 증거 범위 |
|---|---:|---|
| GitHub repository/branch API, `git ls-remote`, `git clone --depth 1` | 0 | official origin, default HEAD, activity/license metadata, immutable clone identity `I2` |
| fixed clone의 `rg`, `sed`, `nl` 정적 inspection | 0 | README/license/schema/client/plugin/MCP/AI/vector source Claims `V1/V2` |
| `python3 scripts/validate_knowledge_base.py` | 0; `PASS: 62 Markdown files` | 최종 frontmatter/lifecycle/중복 ID/repository-relative link 구조 `V2` |
| `git diff --check` | 0 | whitespace/static diff |

## 제한과 외부 동작

- build/runtime/E2E/native Windows/Linux, DB/model/plugin/hosted cq service를 실행하지 않아 `V3+`와 `P2+` evidence는 없다.
- component dependency license/SBOM/CVE, external URL availability와 production suitability는 검증하지 않았다.
- 외부 동작은 public GitHub metadata/source read와 임시 shallow clone뿐이다. credential을 읽거나 출력하지 않았고 external write, 비용 발생 API, commit/push/merge/deploy는 수행하지 않았다.
