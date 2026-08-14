---
id: tool-codex
type: tool-profile
title: OpenAI Codex
status: observed
tags:
  - knowledge-base
  - tool
  - coding-agent
  - app-server
  - windows
official_upstream: https://github.com/openai/codex
license: Apache-2.0-with-NOTICE
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 7c194ff24b3aa0e3beaf03b526db2d0b4f708794
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 1c4f42863c1f84eb5175a1a0cfffe84641a63df3
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# OpenAI Codex

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

OpenAI Codex는 로컬 repository에서 명령·파일 변경·도구 호출을 수행하고 CLI/TUI/IDE/app-server surface로 session과 approval을 노출하는 primary coding-agent runtime 후보다.

## ToolVersion과 공식 최신 관찰

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/openai/codex` |
| 조사일 기본 브랜치 HEAD | `main` · `7c194ff24b3aa0e3beaf03b526db2d0b4f708794` |
| 고정 버전 | `1c4f42863c1f84eb5175a1a0cfffe84641a63df3` |
| pin과 최신 HEAD | 조사일 최신 HEAD가 pin보다 3 commits 앞섬. 주장은 pin에 고정 |
| 로컬 gitlink | [`multi-agent-tools/codex`](../../multi-agent-tools/codex/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | `I2`: parent gitlink와 공식 fixed tree 일치 |
| 유지보수 관찰 | archived/disabled가 아니고 조사일 push 관찰. 특정 release/model/API availability 보장은 아님 |
| license | fixed [`LICENSE`](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/LICENSE#L1-L18) Apache-2.0, [`NOTICE`](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/NOTICE#L1-L6) 포함 |

## 기술 구조

| 구성 | 책임 | fixed-SHA 근거 |
|---|---|---|
| CLI/TUI | local coding-agent 대화와 작업 실행 | [README](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/README.md#L1-L7) |
| Core/tool runtime | command/file/MCP tool dispatch와 sandbox policy 적용 | [sandbox adapter](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/sandboxing/mod.rs#L1-L28) |
| App server | bidirectional JSON-RPC로 thread/turn/item lifecycle과 approval surface 제공 | [protocol](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L20-L29), [lifecycle](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L68-L83) |
| MCP integration | external MCP server tool을 registry/handler에 연결 | [MCP handler](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/tools/handlers/mcp.rs#L23-L45) |
| Windows sandbox | Windows sandbox identity, filesystem/network/proxy와 process 경로 | [core fields](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/sandboxing/mod.rs#L51-L60), [Windows crate](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/windows-sandbox-rs/src/lib.rs#L11-L43) |

## 역할과 연동

- AgentRole: Worker, Executor, Reviewer 보조, interactive coding agent
- Capability: `repository-edit`, `command-exec`, `thread-resume`, `streaming-items`, `approval-policy`, `sandbox-policy`, `mcp-tools`
- Integration: CLI/TUI, IDE, app-server JSON-RPC/JSONL, experimental WebSocket, Unix socket, MCP
- SecurityOperationalRequirement: workspace scope, approval policy, sandbox/network profile, MCP trust, credential audience, independent verifier/committer

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `codex-local-coding-runtime` | capability | 로컬 컴퓨터에서 실행되는 coding agent이며 CLI와 editor/app surface를 제공한다. | [README](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/README.md#L1-L7) | `I2` | `V2` | `W0` | pass(정적). 실제 작업 성공 미검증 |
| `codex-appserver-lifecycle` | interface | app-server가 JSON-RPC의 thread→turn→item lifecycle과 streaming notification을 제공한다. | [protocol/transports](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L20-L29), [lifecycle](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L68-L83) | `I2` | `V2` | `W0` | pass(정적). WebSocket은 문서상 experimental/unsupported |
| `codex-turn-policy` | security | turn 시작 시 cwd, sandbox/permission profile, approval policy를 선택할 수 있다. | [turn start](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L78-L83), [sandbox request fields](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/sandboxing/mod.rs#L51-L60) | `I2` | `V2` | `W0` | pass(정적). 선택 정책의 enforcement E2E 미검증 |
| `codex-streamed-evidence-surface` | capability | item lifecycle이 command/file edit/tool progress와 final status를 streaming event로 노출한다. | [turn streaming](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L81-L83), [event lifecycle](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L1583-L1588) | `I2` | `V2` | `W0` | pass(정적). event는 독립 verification verdict가 아님 |
| `codex-windows-sandbox-source` | platform | Windows sandbox level, workspace root, private desktop, proxy/network provisioning 코드 경로가 있다. | [core Windows policy](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/sandboxing/mod.rs#L51-L60), [Windows provisioning](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/windows-sandbox-rs/src/lib.rs#L11-L43) | `I2` | `V2` | `W1` | pass(정적). Windows sandbox setup/runtime 미실행 |
| `codex-worker-not-verifier` | limitation | agent의 completed turn과 tool success는 독립 verifier·fresh-base merge·production 성공이 아니다. | [item/turn state](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L68-L83), [completed statuses](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L1583-L1588) | `I2` | `V2` | `W0` | architectural limitation; external verifier/committer 필요 |

## Interface와 protocol

| 표면 | 계약 | 상태·권한 경계 | 근거 |
|---|---|---|---|
| CLI/TUI/IDE | interactive coding-agent client | local user와 workspace authority | [README](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/README.md#L1-L7) |
| app-server stdio | newline-delimited JSON-RPC-like messages | local adapter primary transport | [transport list](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L20-L29) |
| WebSocket/Unix socket | frame/socket transport | WebSocket experimental; origin/remote exposure 별도 검토 | [transport warning](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/app-server/README.md#L31-L39) |
| MCP | external server tools | MCP server별 tool/credential/egress trust | [handler](https://github.com/openai/codex/blob/1c4f42863c1f84eb5175a1a0cfffe84641a63df3/codex-rs/core/src/tools/handlers/mcp.rs#L23-L45) |

## 운영·보안·trust boundary

- Codex를 primary worker adapter로 사용하되 planning acceptance와 독립 verification, merge authority는 외부 역할로 둔다.
- model output·turn completion은 proposal/evidence input이며 `proposal → policy/verifier/human → committer` 경계를 통과해야 외부 write나 merge가 된다.
- app-server client, workspace, MCP server, model provider, sandbox/network policy를 각각 식별 가능한 principal/config로 기록한다.
- credential은 provider/MCP/action audience와 expiry가 붙은 opaque handle로 주입하고 durable session/event에 원문을 남기지 않는다.

## 플랫폼과 Windows

- README가 Windows 설치 경로를 제공하고 fixed source에 전용 sandbox crate와 policy fields가 있어 `W1`이다.
- static Windows source는 ACL/network/process enforcement가 실제 환경에서 작동했다는 뜻이 아니다.
- Windows build, sandbox setup, cancellation/process-tree, CRLF/long-path 회귀를 수행하지 않아 `W2/W3`가 아니다.

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `codex-origin-20260814` | parent gitlink와 GitHub repo/branch/compare/license metadata | pass | `openai/codex@1c4f42863c1f84eb5175a1a0cfffe84641a63df3` | origin과 ToolVersion |
| `codex-fixed-static-20260814` | fixed README/app-server/core/Windows source 정적 검토 | partial pass | 위 fixed permalinks | `V2`, `W1` Claims |
| `codex-v3plus-none` | build/runtime/agent task/Windows sandbox/E2E 미실행 | unknown | 없음 | `V3+`, `W2+` 없음 |

병렬 조사 worktree submodule 본문은 비어 있어 로컬 본문을 읽지 않았다. parent `.gitmodules`+`git ls-tree`로 gitlink를 확인하고 official GitHub fixed-SHA tree/metadata에서만 정적 근거를 수집했다.

## 강점과 한계

- 강점: `codex-appserver-lifecycle`과 `codex-turn-policy`는 primary worker adapter의 structured lifecycle·approval surface로 적합하다.
- 강점: `codex-windows-sandbox-source`는 Windows-first local executor의 직접 비교 기준이다.
- 한계: `codex-worker-not-verifier`처럼 completed event가 correctness/merge authority를 증명하지 않는다.
- 한계: transport와 feature 일부가 experimental이며 provider/API availability는 fixed repository source와 별도다.

## AX 설계 재료

| 구분 | 연결 Claim | 사내 AX 플랫폼에서의 사용 |
|---|---|---|
| Borrow | `codex-appserver-lifecycle`, `codex-turn-policy` | structured worker adapter와 명시적 sandbox/approval profile |
| Adapt | `codex-streamed-evidence-surface`, `codex-windows-sandbox-source` | event를 evidence input으로 보존하고 Windows capability를 실제 conformance로 협상 |
| Avoid | `codex-worker-not-verifier` | completed turn이나 tool success를 검증·merge 승인으로 자동 승격 |
| Build | `codex-worker-not-verifier`, `codex-turn-policy` | independent verifier, human/policy gate, scoped committer와 audience-bound opaque credential broker |

회사 코드·데이터 분류, 허용 model/provider, sandbox baseline, MCP allowlist, 승인 역할과 merge authority는 `unknown/decision item`이다. Codex 채택은 primary adapter 설계 재료이지 단독 AX 플랫폼의 최종 답이 아니다.

## 도입 판단

- 결정: 채택
- 적용 범위: 첫 primary coding worker adapter와 app-server lifecycle; 외부 verifier/policy/committer를 필수로 결합
- 이유: structured session/turn/item, approval/sandbox, MCP, Windows 구현 경로가 핵심 요구와 맞는다.
- 재검토 조건: fixed version adapter conformance, Windows W2/W3, cancel/process cleanup, MCP malicious server, stale-head verification/merge E2E

## 다음 검증

| Item ID | 목표 Claim/등급 | 환경·시나리오 | 통과 기준 | 보존 artifact |
|---|---|---|---|---|
| `codex-v4-adapter` | `codex-appserver-lifecycle` / `V4` | stdio initialize→thread→turn→interrupt/resume | schema/state ordering 일치 | transcript, schema version, exit codes |
| `codex-w2-sandbox` | `codex-windows-sandbox-source` / `W2` | Windows 11 workspace-write/read-only/network/cancel | 허용 범위 밖 write/egress 0, process tree 회수 | logs, ACL/network snapshot |
| `codex-v5-worker-gate` | `codex-worker-not-verifier` / `V5` | false-complete/stale-head/malicious MCP failure injection | verifier·committer가 부적합 proposal 100% 차단 | run/evidence/decision chain |

## 관계와 변경 이력

- `ToolVersion FITS_ROLE Worker/Executor`
- `ToolVersion PROVIDES repository-edit/thread-lifecycle/approval-policy`
- `ToolVersion SUPPORTS app-server-JSON-RPC/MCP`
- `Project SELECTS ToolVersion`
- 2026-08-14: official GitHub fixed-SHA 정적 프로필 작성. `I2 / V2 / W1`; runtime 미수행.
