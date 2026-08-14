---
id: tool-agent-client-protocol
type: tool-profile
title: Agent Client Protocol (ACP)
status: observed
tags:
  - knowledge-base
  - tool
  - protocol
  - json-rpc
  - agent-adapter
official_upstream: https://github.com/agentclientprotocol/agent-client-protocol
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 25ce6f77d6a81b452e5579cf710e25c1c3922b4a
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Agent Client Protocol (ACP)

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

ACP는 editor·IDE 같은 client와 coding agent 사이의 초기화, capability 협상, session lifecycle, prompt/update, tool·permission 흐름을 typed JSON-RPC 계약으로 표준화하는 protocol이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/agentclientprotocol/agent-client-protocol` |
| 기본 브랜치와 고정 버전 | `main` · `25ce6f77d6a81b452e5579cf710e25c1c3922b4a` |
| 로컬 gitlink | [`multi-agent-tools/agent-client-protocol`](../../multi-agent-tools/agent-client-protocol/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 현재 upstream 관찰 | GitHub `main`은 조사 시 `16879d6217e5a213099e540b1ddc2088fdcbfe35`로 고정 버전보다 앞서 있었다. archived/disabled가 아니고 같은 날 push가 관찰됐지만 support SLA를 뜻하지 않는다. |
| 출처 무결성 | `I2`: parent [`.gitmodules`](../../.gitmodules) URL과 `git ls-tree` gitlink SHA를 확인하고, 공식 GitHub의 fixed-SHA tree/blob를 대조했다. |
| license | fixed SHA root [`LICENSE`](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/LICENSE#L1-L5)의 Apache-2.0 text와 GitHub metadata가 일치한다. |

## 기술 구조

- Rust schema crate가 request/response/notification, JSON-RPC envelope, protocol-version type을 정의하고 versioned JSON Schema를 생성한다.
- client가 agent subprocess를 띄우는 newline-delimited UTF-8 stdio가 권장 transport이며, Streamable HTTP는 이 버전에서 draft다.
- `initialize`가 protocol major version, client/agent capability, authentication method를 협상한 뒤 `session/new`, `session/load` 또는 `session/resume`으로 대화 단위를 만든다.
- agent가 tool 실행 주체이고 client는 filesystem·terminal capability와 permission response를 제공할 수 있다. 따라서 protocol과 executor/security policy는 별도 계층이다.

## 역할과 연동

- AgentRole: Adapter contract, Client/Gateway, Agent runtime boundary
- Capability: `typed-agent-contract`, `capability-negotiation`, `session-identity`, `prompt-stream`, `tool-progress`, `permission-request`, `session-cancel`
- Integration: JSON-RPC 2.0, stdio, custom bidirectional transport, draft Streamable HTTP, MCP descriptor forwarding
- SecurityOperationalRequirement: unadvertised capability fail-closed, absolute-path validation, permission decision authority, subprocess/credential isolation은 구현체가 별도로 제공

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `acp-typed-jsonrpc` | repository가 ACP wire message의 typed Rust model과 JSON-RPC 2.0 envelope/schema를 제공한다. | [README schema surface](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/README.md#L11-L29), [JSON-RPC type](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/agent-client-protocol-schema/src/rpc.rs#L134-L151) | `V2` | `W0` | pass(정적). SDK 상호운용 실행은 미검증 |
| `acp-capability-negotiation` | `initialize`에서 protocol major version과 양방향 capability를 교환하며, 생략된 capability는 unsupported로 다뤄야 한다. | [initialization](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/initialization.mdx#L24-L29), [capability rules](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/initialization.mdx#L84-L112) | `V2` | `W0` | pass(정적). extension namespace 충돌·downgrade fixture는 미실행 |
| `acp-session-contract` | session은 독립 context/state 단위이며 new/load/resume, prompt, update, cancel lifecycle과 session ID를 정의한다. | [session setup](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/session-setup.mdx#L6-L40), [load/replay rules](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/session-setup.mdx#L83-L104) | `V2` | `W0` | pass(정적). session persistence durability는 agent 구현 책임 |
| `acp-permission-surface` | agent가 tool call을 알리고 client에 permission을 요청할 수 있으나 client가 자동 allow/reject 정책을 선택할 수도 있다. | [tool reporting](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/tool-calls.mdx#L6-L10), [permission request](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/tool-calls.mdx#L108-L168) | `V2` | `W0` | pass(정적). 사용자 승인 진위·policy engine·secret redaction을 protocol 자체가 보장하지 않음 |
| `acp-stdio-transport` | 권장 stdio transport는 client가 agent subprocess를 시작하고 newline-delimited JSON-RPC만 stdin/stdout으로 교환하도록 규정한다. | [transport contract](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/transports.mdx#L6-L27) | `V2` | `W0` | pass(정적). HTTP는 draft이고 framing/backpressure/runtime은 미검증 |
| `acp-not-executor-isolation` | ACP는 I/O·lifecycle 계약이지 process, filesystem, network, credential sandbox가 아니다. | [client responsibility](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/overview.mdx#L114-L125), [client capabilities](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/initialization.mdx#L114-L130) | `V2` | `W0` | confirmed limitation. 별도 executor policy와 audience-scoped secret handle 필요 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `acp-origin-20260814` | parent `.gitmodules` + `git ls-tree`와 official GitHub metadata/fixed commit 비교 | pass | `agentclientprotocol/agent-client-protocol@25ce6f77d6a81b452e5579cf710e25c1c3922b4a` | origin과 ToolVersion |
| `acp-static-20260814` | official fixed-SHA docs/schema/source blob 정적 검토 | partial pass | 위 fixed-SHA permalink | 모든 `V2` Claim |
| `acp-local-body-v3plus-none` | 조사 worktree의 submodule 본문이 비어 로컬 본문을 읽지 못했고 build/runtime/conformance/E2E를 실행하지 않음 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

## 강점과 한계

- 강점: terminal text 추측보다 method, ID, capability, session, permission, progress를 기계 검증 가능한 계약으로 교환한다.
- 강점: capability omission을 unsupported로 처리하므로 adapter가 선택 기능을 fail-closed로 협상할 수 있다.
- 한계: protocol 준수는 agent가 작업을 정확히 수행했다거나 permission UI가 실제 사람 승인을 받았음을 증명하지 않는다.
- 한계: stdio subprocess와 client filesystem/terminal capability는 host authority를 넓힐 수 있다. 인증, secret scope, egress, sandbox, audit 보존은 외부 정책이 필요하다.
- 한계: fixed SHA의 Windows 전용 implementation 또는 Windows 실행 evidence를 조사하지 않았으므로 `W0`이다.

## AX 설계 재료

- `Borrow`: `acp-typed-jsonrpc`, `acp-capability-negotiation`, `acp-session-contract`의 typed message, explicit session ID, capability omission fail-closed 규칙을 adapter kernel의 기본 계약으로 차용한다.
- `Adapt`: `acp-permission-surface`를 사내 policy/verifier와 연결하고 run ID·owner generation·attempt/fence를 ACP `_meta` 또는 상위 envelope에 명시한다.
- `Avoid`: `acp-not-executor-isolation`을 무시한 채 protocol 연결 성공을 sandbox, 사람 승인, task correctness 또는 운영 성공으로 해석하지 않는다.
- `Build`: `acp-capability-negotiation`, `acp-session-contract`, `acp-permission-surface`를 검증하는 malformed frame·version downgrade·cancel·permission·load/replay executor conformance fixture와 audience-scoped opaque secret handle broker를 별도 구축한다.
- `unknown / decision item`: 회사의 데이터 분류, 허용 agent/MCP 목록, filesystem·terminal 권한, 승인 주체·보존 기간·audit 요구는 확인되지 않았다. 실제 policy binding 전에 소유자가 결정해야 한다.

## 도입 판단

- 결정: 채택
- 적용 범위: 벤더 선정이나 최종 구현 답이 아니라, 사내 AX adapter 우선순위의 primary typed protocol(`typed API → ACP → JSON CLI → PTY heuristic`) 및 executor conformance fixture를 설계하기 위한 재료
- 이유: `acp-typed-jsonrpc`, `acp-capability-negotiation`, `acp-session-contract`가 run/session identity와 structured progress를 제공한다. 다만 execution proof와 security boundary는 분리한다.
- 재검토 조건: current upstream pin 갱신, protocol v1/v2 matrix 확인, client/agent pair build `V3`, cancel·permission·load/replay·malformed frame conformance `V4/V5`, Windows stdio process-tree `W2`

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE AdapterContract/Gateway`
- `ToolVersion PROVIDES typed-agent-contract/capability-negotiation/session-identity`
- `ToolVersion SUPPORTS JSON-RPC/stdio`
- `Project SELECTS ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA tree/blob를 대조해 `I2 / V2 / W0` 프로필 작성. local submodule body와 build/runtime/E2E는 미검증으로 보존.
