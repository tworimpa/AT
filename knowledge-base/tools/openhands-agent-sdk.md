---
id: tool-openhands-agent-sdk
type: tool-profile
title: OpenHands Agent SDK
status: observed
profile_schema_version: 2
tool_key: openhands-agent-sdk
tool_version_id: tool-version:openhands-agent-sdk@ceda00b478a41b64c2f259c096e08977ca7ea4dd
tags: [knowledge-base, tool, sdk, agent-server, workspace]
official_upstream: https://github.com/OpenHands/software-agent-sdk
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 2f7e8ed8216ecfec45de6691cbfc0586af304e40
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: ceda00b478a41b64c2f259c096e08977ca7ea4dd
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# OpenHands Agent SDK

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

OpenHands Agent SDK는 Python Agent/Conversation/Tool/Workspace 추상화와 REST/WebSocket/MCP Agent Server를 제공해 local·remote·Docker·Kubernetes workspaces에서 agent runtime을 구성하는 SDK다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/OpenHands/software-agent-sdk` · `main` / `2f7e8ed8216ecfec45de6691cbfc0586af304e40` (2026-08-15) |
| 고정 버전 / gitlink | `ceda00b478a41b64c2f259c096e08977ca7ea4dd` (agent-server package `1.42.1` 관찰) · [`multi-agent-tools/openhands-agent-sdk`](../../multi-agent-tools/openhands-agent-sdk/) |
| pin 관계 | upstream이 pin 이후 이동; package version/current HEAD는 fixed ToolVersion과 분리 |
| license | [MIT LICENSE](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/LICENSE#L1-L21) |
| provenance limitation | parent gitlink + official fixed-SHA README/source 정적 검토. lease 등 일부 locator는 package directory-level; build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| SDK core | Agent, Conversation, Tool, Workspace composition | [README](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/README.md#L45-L83) |
| Agent Server | SDK를 REST/WebSocket service로 호스팅 | [agent-server tree](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) |
| Workspace backends | local/remote/container/Kubernetes execution context | [README](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/README.md#L32-L43) |
| Conversation lease | file lock, owner generation, TTL/stale fencing | [agent-server fixed source](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) |

## 역할과 연동

- AgentRole: Agent Runtime, Conversation Service, Workspace Executor Adapter.
- Capability: `agent-conversation-kernel`, `tool-workspace-abstraction`, `agent-server-api`, `conversation-lease-generation`.
- Integration: Python API, REST, WebSocket, MCP, local/remote/Docker/Kubernetes workspace.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `ohsdk-core-abstractions` | architecture | Agent/Conversation/Tool/Workspace를 별도 추상화로 제공한다. | [README](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/README.md#L45-L83) | `I2` | `V2` | `W1` | 정적 pass; backend parity 미검증 |
| `ohsdk-server-api` | interface | Agent Server가 SDK runtime을 REST/WebSocket/MCP surface로 노출한다. | [agent-server source](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) | `I2` | `V2` | `W1` | exact endpoint/auth conformance runtime 미검증 |
| `ohsdk-conversation-lease` | capability | conversation owner generation/TTL/stale fencing을 포함한 file-lock lease pattern이 있다. | [agent-server source](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) | `I2` | `V2` | `W1` | 유용한 reference지만 distributed/host-failure 보장은 아님 |
| `ohsdk-auth-bind-risk` | security | API auth가 optional이고 server bind 기본이 `0.0.0.0`일 수 있어 deployment policy가 필요하다. | [server details](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server/server_details_router.py#L1), [init router](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server/init_router.py#L1) | `I2` | `V2` | `W1` | 조직 인증·TLS·network policy를 기본값에 위임 금지 |
| `ohsdk-codex-home` | security | ACP Codex path는 run-scoped mode-0700 `CODEX_HOME` pattern을 사용한다. | [agent-server fixed tree](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) | `I2` | `V2` | `W1` | directory isolation은 credential audience/egress 전체 보장이 아님 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Python SDK | in-process objects/events | embedding process authority | [README](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/README.md#L45-L83) |
| Agent Server | REST/WebSocket/MCP | network caller → conversation/workspace | bind/auth/TLS/tenant scope fail-closed 필요 | [server tree](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server) |

## 운영·보안·trust boundary

- conversation lease는 ownership concurrency control이고 sandbox/secret/network policy가 아니다.
- server network exposure, optional auth, workspace backend, telemetry/secret lifecycle을 별도 policy/evidence layer로 분리해야 한다.

## 플랫폼과 Windows

- `W1 narrow`: cross-platform Python/source 및 Windows 관련 정적 경로만 관찰했다. native Windows workspace/process-tree/sandbox 실행 증거는 없다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `ohsdk-static-20260815` | `I2/V2/W1` | parent pin + official fixed source | partial pass | 일부 directory-level locator; runtime 없음 |
| `ohsdk-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: conversation lease/generation과 workspace abstraction은 AX event kernel/executor 분리에 직접 참고할 수 있다.
- 한계: optional auth/bind, secret/telemetry lifecycle, distributed recovery와 Windows isolation은 별도 구현·검증이 필요하다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | owner generation/TTL/stale fencing lease | `ohsdk-conversation-lease` | `AX-N-DURABLE-OWNERSHIP` |
| Adapt | Agent/Conversation/Tool/Workspace를 event-sourced kernel contract로 변형 | `ohsdk-core-abstractions` | deterministic receipts와 replay 필요 |
| Avoid | optional auth/default bind와 directory-only secret isolation | `ohsdk-auth-bind-risk`, `ohsdk-codex-home` | fail-closed network/secret policy |
| Build | event kernel + secret/egress broker + crash recovery/conformance | 위 Claims | `AD-LEASE-FENCING` / `RM-EVIDENCE-KERNEL` |

## 도입 판단

- 결정: SDK/server architecture reference. 최종 vendor 선택이 아니다.
- 재검토: exact lease/auth locator 보강, pinned build, concurrent crash recovery, Windows workspace, secret/egress failure injection.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `ohsdk-v3-build` | fixed packages | `V3/W2` | pinned Python/Node dependency build/test |
| `ohsdk-v5-lease` | conversation lease | `V5` | owner crash/TTL/stale writer에서 중복 side effect 0 |
| `ohsdk-v5-security` | server/secret | `V5` | unauthenticated remote request 차단, secret log/egress leakage 0 |

## 관계와 변경 이력

- `Capability conversation-lease-generation ADDRESSES AXNeed AX-N-DURABLE-OWNERSHIP`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
