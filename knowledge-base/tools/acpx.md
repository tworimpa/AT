---
id: tool-acpx
type: tool-profile
title: acpx
status: observed
tags:
  - knowledge-base
  - tool
  - acp
  - session-runtime
  - orchestration
official_upstream: https://github.com/openclaw/acpx
license: MIT
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# acpx

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md) · [ACP](./agent-client-protocol.md)

## 한 줄 역할

acpx는 ACP-compatible coding agent를 persistent session, queue owner, permission policy, NDJSON event와 flow trace/replay 표면으로 제어하는 headless CLI·embeddable runtime이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/openclaw/acpx` |
| 기본 브랜치와 고정 버전 | `main` · `5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3` |
| 로컬 gitlink | [`multi-agent-tools/acpx`](../../multi-agent-tools/acpx/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 현재 upstream 관찰 | GitHub `main`은 조사 시 `5897733ce5aa4d8e94a6f4de6ab62089c1dd0bcc`로 고정 버전보다 앞서 있었다. archived/disabled가 아니고 같은 날 push가 관찰됐다. |
| 출처 무결성 | `I2`: parent [`.gitmodules`](../../.gitmodules) URL과 `git ls-tree` gitlink SHA를 확인하고 official fixed-SHA tree/blob를 대조했다. |
| license | fixed SHA root [`LICENSE`](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/LICENSE#L1-L13)의 MIT text와 GitHub metadata가 일치한다. |

## 기술 구조

- Node.js/TypeScript headless CLI가 ACP agent subprocess를 시작하고 `@agentclientprotocol/sdk` connection을 통해 capability, session, filesystem, terminal, permission request를 처리한다.
- local session record, ACP wire session ID, optional inner agent/provider session ID를 분리해 reconnect/fallback 후 identity 혼동을 줄이는 모델을 둔다.
- session별 queue owner record에 PID, socket path, heartbeat, generation, queue depth를 기록하고 active turn/control mutation을 한 owner에 직렬화한다.
- persistent sessions와 stateless `exec`, NDJSON ACP event output, multi-step flow 및 append-only trace/replay bundle을 함께 제공한다.

## 역할과 연동

- AgentRole: ACP client adapter, Session owner, Executor supervisor 보조, Workflow runner
- Capability: `persistent-acp-session`, `session-identity`, `warm-owner`, `generation-lease`, `prompt-queue`, `structured-event-output`, `flow-trace-replay`
- Integration: ACP/JSON-RPC over stdio, CLI, NDJSON, local IPC/socket, TypeScript runtime API
- SecurityOperationalRequirement: cwd·filesystem·terminal·permission mode 분리, credential environment scope, stale owner fencing, trace artifact의 secret/redaction·retention 정책

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `acpx-structured-client` | one-shot와 persistent session을 동일 ACP client surface로 제공하고 terminal escape text 대신 structured event를 출력한다. | [README role](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/README.md#L13-L25), [sessions/output](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/README.md#L62-L78) | `V2` | `W0` | pass(정적). 실제 agent 호환성·event completeness는 미검증 |
| `acpx-session-identity` | local record ID, ACP session ID, optional provider session ID를 서로 다른 identity로 다루고 provider ID를 합성하지 않는 규칙을 둔다. | [identity model](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/docs/2026-02-23-session-identity-spec.md#L36-L55), [persistence requirements](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/docs/2026-02-23-session-identity-spec.md#L89-L95) | `V2` | `W0` | partial pass. 문서는 Draft이므로 actual CLI output compatibility는 별도 fixture 필요 |
| `acpx-warm-owner-lease` | queue owner record가 session ID, heartbeat, generation과 queue depth를 보존하고 stale heartbeat를 판정한다. | [lease types](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/cli/queue/lease-store.ts#L17-L49), [generation/staleness](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/cli/queue/lease-store.ts#L99-L120) | `V2` | `W0` | pass(정적). crash/restart 경쟁과 ABA fencing은 runtime failure injection 미실행 |
| `acpx-owner-turn-control` | active turn의 cancel/mode/model/config 변경을 owner controller가 상태와 timeout을 통해 직렬화한다. | [owner state](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/cli/queue/owner-turn-controller.ts#L4-L35), [cancel/control](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/cli/queue/owner-turn-controller.ts#L79-L147) | `V2` | `W0` | pass(정적). exactly-once execution이나 cross-host lease는 보장하지 않음 |
| `acpx-load-replay` | ACP load/resume을 감싸고 replay update suppression/drain budget을 명시하며, flow trace는 append-only log를 source of truth로 둔다. | [client replay controls](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/acp/client.ts#L125-L130), [load/replay path](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/acp/client.ts#L976-L1030), [flow trace model](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/docs/2026-03-26-acpx-flow-trace-replay.md#L16-L53) | `V2` | `W0` | pass(정적). replay는 재실행 correctness나 side-effect idempotency를 자동 보장하지 않음 |
| `acpx-permission-boundary` | API에 permission/auth/fs/terminal 옵션이 있으나 선택된 mode와 agent credential로 subprocess를 구동하므로 sandbox·secret broker로 간주할 수 없다. | [session option contract](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/cli/session/contracts.ts#L41-L83), [ACP client authority](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/src/acp/client.ts#L1-L65) | `V2` | `W0` | confirmed limitation. secrets는 audience-scoped opaque handle로 별도 전달 필요 |
| `acpx-pre1-compatibility` | 이 fixed version은 pre-1.0이며 CLI/runtime interface가 변할 수 있다고 공식 README가 경고한다. | [pre-1.0 note](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/README.md#L24-L25) | `V1` | `W0` | confirmed limitation. adapter pin과 conformance regression 필요 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `acpx-origin-20260814` | parent `.gitmodules` + `git ls-tree`, official metadata와 fixed commit 비교 | pass | `openclaw/acpx@5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3` | origin과 ToolVersion |
| `acpx-static-20260814` | official fixed-SHA README/docs/TypeScript source 정적 검토 | partial pass | 위 fixed-SHA permalink | `V1/V2` Claim |
| `acpx-local-body-v3plus-none` | 조사 worktree submodule 본문이 비어 로컬 본문을 읽지 못했고 install/build/runtime/agent E2E/failure injection을 실행하지 않음 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

## 강점과 한계

- 강점: ACP를 automation-friendly CLI/runtime으로 감싸고 명시적 session identity, warm owner, queue, cancel과 replay를 제공한다.
- 강점: owner generation과 heartbeat는 session-local stale owner 회수와 fence 설계의 구체적인 참고 구현이다.
- 한계: pre-1.0이고 adapter가 설치·인증된 upstream agent 및 그 ACP 품질에 의존한다.
- 한계: local owner lease는 distributed consensus나 side-effect exactly-once가 아니다. trace replay도 derived UI보다 강한 기록이지만 외부 side effect 재현을 증명하지 않는다.
- 한계: Windows 전용 source/runtime evidence를 이번 fixed-SHA 조사에서 확정하지 않아 `W0`이다.

## AX 설계 재료

- `Borrow`: `acpx-session-identity`, `acpx-warm-owner-lease`, `acpx-load-replay`의 local/wire/provider identity 분리, heartbeat+generation owner record, append-only trace 원칙을 차용한다.
- `Adapt`: `acpx-owner-turn-control`을 AX run/attempt state machine에 맞춰 owner generation fence와 idempotency key를 모든 mutation에 요구하도록 강화한다.
- `Avoid`: local lease를 distributed consensus·exactly-once로, replay bundle을 외부 side-effect 재현 proof로, permission mode를 sandbox로 해석하지 않는다(`acpx-permission-boundary`).
- `Build`: `acpx-warm-owner-lease`, `acpx-load-replay`, `acpx-permission-boundary`를 검증하는 ACP conformance, stale-owner/ABA/duplicate-prompt failure injection, evidence append-only store와 audience-scoped opaque secret handle 전달 계층을 별도 구축한다.
- `unknown / decision item`: 회사별 session retention, trace 안의 prompt/tool artifact 데이터 분류, credential audience, 자동 승인 가능 작업과 필수 사람 승인 주체는 확인되지 않았다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정이나 최종 구현 답이 아니라, 사내 AX의 ACP persistent client, explicit run/session identity, warm owner generation fence, append-only replay/conformance fixture를 설계하기 위한 재료
- 이유: `acpx-session-identity`, `acpx-warm-owner-lease`, `acpx-load-replay`가 local orchestration kernel에 직접 유용하다. pre-1.0·runtime 미검증 때문에 production dependency 채택은 보류한다.
- 재검토 조건: current upstream pin 갱신, Node build `V3`, two-session queue/cancel/load/reconnect `V4`, owner crash·stale generation·duplicate prompt failure injection `V5`, Windows process/socket lifecycle `W2`

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE ACPClient/SessionOwner/WorkflowRunner`
- `ToolVersion PROVIDES persistent-acp-session/session-identity/generation-lease/flow-trace-replay`
- `ToolVersion SUPPORTS ACP/CLI/NDJSON/local-IPC`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA tree/blob를 대조해 `I2 / V2 / W0` 프로필 작성. local submodule body와 build/runtime/E2E는 미검증으로 보존.
