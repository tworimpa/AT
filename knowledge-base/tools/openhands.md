---
id: tool-openhands
type: tool-profile
title: OpenHands Agent Canvas
status: observed
profile_schema_version: 2
tool_key: openhands
tool_version_id: tool-version:openhands@4f465f3ccada5271a3bbe4a0148941b0c40d243b
tags: [knowledge-base, tool, control-plane, backend-registry, acp]
official_upstream: https://github.com/OpenHands/OpenHands
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 86472bfbdd2a37a4239d7e469d10689ee5702119
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 4f465f3ccada5271a3bbe4a0148941b0c40d243b
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# OpenHands Agent Canvas

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

OpenHands Agent Canvas는 local/Docker/VM/cloud Agent Server backends를 등록하고 conversation·terminal·files·automation을 보여 주는 self-hosted control center다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/OpenHands/OpenHands` · `main` / `86472bfbdd2a37a4239d7e469d10689ee5702119` (2026-08-15) |
| 고정 버전 / gitlink | `4f465f3ccada5271a3bbe4a0148941b0c40d243b` (`v1.13.0` 관찰) · [`multi-agent-tools/openhands`](../../multi-agent-tools/openhands/) |
| pin 관계 | upstream이 pin 이후 이동; release label/current HEAD와 fixed ToolVersion을 분리 |
| license | [MIT LICENSE](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/LICENSE#L1-L21) |
| provenance limitation | parent gitlink + official fixed-SHA docs/source 정적 검토. Agent Server는 별도 pinned SDK profile이며 runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Canvas UI | conversation, terminal, browser, files, settings, automation projection | [architecture](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/architecture.md#L7-L21) |
| Backend registry | 하나 이상의 Agent Server를 등록·전환 | [runtime services](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/architecture.md#L21-L31) |
| Runtime modes | host-direct 또는 Docker/remote backend | [README](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/README.md#L33-L43), [host/sandbox](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/README.md#L63-L109) |
| ACP agent configuration | Canvas conversation이 Agent Server-managed ACP process를 선택 | [ACP docs](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/ACP_AGENTS.md#L1-L24) |

## 역할과 연동

- AgentRole: Human Control Surface, Backend Registry, Automation UI.
- Capability: `multi-backend-registry`, `conversation-projection`, `runtime-capability-selection`, `acp-agent-control`.
- Integration: REST/WebSocket to Agent Server, ACP JSON-RPC stdio behind server, Docker/VM/cloud backends.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `openhands-backend-registry` | architecture | Canvas는 하나 이상의 Agent Server를 등록하고 전환하는 control plane이다. | [architecture](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/architecture.md#L21-L31) | `I2` | `V2` | `W1` | UI는 process/credential owner가 아님 |
| `openhands-host-risk` | security | sandbox 없이 실행하면 agent server가 host filesystem에 접근한다. | [README](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/README.md#L63-L109) | `I2` | `V2` | `W1` | 명시적 trust boundary; Docker도 secret/egress 보장을 자동 제공하지 않음 |
| `openhands-acp-process-owner` | interface | ACP agent process와 credentials는 Canvas가 아니라 Agent Server가 관리한다. | [ACP docs](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/ACP_AGENTS.md#L24-L64) | `I2` | `V2` | `W1` | UI/backend authority 분리 필요 |
| `openhands-shared-cli-state` | limitation | 같은 provider의 concurrent conversations가 HOME/CLI config를 공유할 수 있어 collision 위험이 있다. | [ACP isolation caveat](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/ACP_AGENTS.md#L205-L209) | `I2` | `V2` | `W1` | data-dir isolation이 모든 경로에 노출·강제된다는 증거 없음 |
| `openhands-windows-doc` | platform | Windows는 Docker Desktop/PowerShell 설치 경로가 문서화된다. | [README](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/README.md#L82-L103), [Windows guide](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/README.windows.md#L1) | `I2` | `V2` | `W1` | Docker/Linux guest와 native executor를 구분; runtime 미검증 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Canvas↔Agent Server | REST/WebSocket; backend info→conversation | Agent Server가 process/workspace/credential owner | [architecture](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/architecture.md#L21-L31) |
| Agent Server↔ACP agent | JSON-RPC stdio process | server resolves secrets/spawns process; per-run scope 필요 | [ACP docs](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/ACP_AGENTS.md#L133-L167) |

## 운영·보안·trust boundary

- Canvas는 registry/projection이고 Agent Server 및 workspace backend가 실행 authority를 가진다. UI 표시를 runtime completion/evidence로 사용하지 않는다.
- global secrets의 subprocess 전달과 shared HOME은 per-conversation audience/TTL/data-dir/lease로 대체해야 한다.

## 플랫폼과 Windows

- `W1 narrow`: Windows Docker Desktop/PowerShell 문서만 있다. Linux guest의 동작을 native Windows agent host 증거로 표현하지 않는다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `openhands-static-20260815` | `I2/V2/W1` | parent pin + official fixed docs/source | partial pass | server/runtime 미실행 |
| `openhands-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: backend registry와 UI/process-owner 분리가 Windows-first control plane 구조에 유용하다.
- 한계: host-direct 위험, shared CLI config/secret, backend별 capability·isolation parity가 미검증이다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | multi-backend registry와 capability negotiation | `openhands-backend-registry` | `AX-N-EXECUTOR-FEDERATION` |
| Adapt | Canvas를 evidence-backed derived projection으로 제한 | `openhands-acp-process-owner` | UI와 execution authority 분리 |
| Avoid | host-direct 기본·global secret·shared CLI HOME | `openhands-host-risk`, `openhands-shared-cli-state` | secret/data isolation |
| Build | per-run credential/data-dir/lease + backend conformance | 위 Claims | `AD-EXECUTOR-CONTRACT` / `RM-BACKEND-REGISTRY` |

## 도입 판단

- 결정: control-plane/backend registry 참고. 최종 vendor 선택이 아니다.
- 재검토: pinned Canvas+Server pair, backend capability negotiation, secret/concurrency, Windows Docker/native 구분 E2E.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `openhands-v3-pair` | Canvas/Server | `V3/W2` | pinned compatible pair build/launch |
| `openhands-v5-concurrency` | shared state | `V5` | concurrent runs의 credential/config collision 0 |
| `openhands-v5-backend` | registry | `V5` | stale/unhealthy backend가 schedulable로 표시되지 않음 |

## 관계와 변경 이력

- `Capability multi-backend-registry ADDRESSES AXNeed AX-N-EXECUTOR-FEDERATION`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
