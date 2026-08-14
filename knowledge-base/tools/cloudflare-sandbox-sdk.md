---
id: tool-cloudflare-sandbox-sdk
type: tool-profile
title: Cloudflare Sandbox SDK
status: observed
tags:
  - knowledge-base
  - tool
  - remote-executor
  - durable-object
  - container
  - fencing
official_upstream: https://github.com/cloudflare/sandbox-sdk
license: Apache-2.0-package-text-metadata-NOASSERTION
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 2dd1476e32769656da97d5a8daf75e2f92b57e71
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Cloudflare Sandbox SDK

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Cloudflare Sandbox SDK는 Durable Object가 hosted container lifecycle을 소유하고 command/files/process/preview surface를 제공하는 remote executor 후보이며, runtime identity와 sandbox lifetime generation fence의 정적 참조 구현이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/cloudflare/sandbox-sdk` |
| 기본 브랜치와 고정 버전 | `main` · `2dd1476e32769656da97d5a8daf75e2f92b57e71` |
| 조사일 현재 관찰 | 2026-08-14 GitHub API 기준 `main` HEAD도 위 SHA이며 archived/disabled가 아님 |
| 로컬 gitlink | [`multi-agent-tools/cloudflare-sandbox-sdk`](../../multi-agent-tools/cloudflare-sandbox-sdk/) |
| 출처 무결성 | repository/version은 parent URL/gitlink와 official fixed-SHA tree를 대조해 `I2` |
| license | root [`LICENSE`](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/LICENSE)는 package file을 가리키고 [`packages/sandbox/LICENSE`](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/LICENSE#L1-L5)는 Apache-2.0 text다. 그러나 GitHub repository metadata는 `NOASSERTION`이므로 repository 전체 license 결론은 `I1`; component 재사용 전 package별 license/NOTICE 확인 필요 |

## 조사 provenance와 ceiling

병렬 조사 worktree에서는 submodule 본문이 비어 local checkout body를 근거로 읽지 못했다. parent `.gitmodules`·`git ls-tree`로 official URL과 pin을 `I2` 확정하고 official GitHub fixed-SHA tree/blob로 `V2` Claim을 수집했다. local body, npm build/test, Wrangler/Docker runtime, hosted Cloudflare deployment, agent E2E, Windows 실행은 수행하지 않았다. license만 GitHub `NOASSERTION`과 root indirection 때문에 repository-wide `I1`로 낮춘다.

## 목적과 기술 구조

- Worker code가 `getSandbox()`로 Durable Object identity를 선택하고, DO가 Cloudflare Container lifecycle/state와 container HTTP/RPC client를 관리한다.
- public SDK, shared DTO/error package, in-container runtime의 3개 층으로 나뉜다.
- control plane은 command, files, processes, ports, git, interpreter, backup, watch, tunnel domain을 nested RPC targets로 제공한다.
- streaming exec/log는 SSE, newer container control plane은 capnweb RPC를 사용하며 route transport와 RPC transport의 capability 차이가 있다.
- Durable Object storage에 current runtime identity와 logical sandbox lifetime ID/generation을 저장하고 restore/tunnel 같은 장기 operation에서 stale runtime/lifetime을 fence한다.

## 역할과 연동

- AgentRole: Remote executor, Edge runtime provider, Lifecycle/fencing reference
- Capability: `remote-command`, `remote-files`, `background-process`, `session`, `preview-url`, `runtime-generation`, `lifetime-fence`, `backup-restore`
- Integration: Workers/Durable Objects, Cloudflare Containers, HTTP/JSON, SSE, capnweb RPC, TypeScript SDK, Wrangler/Docker local dev
- SecurityOperationalRequirement: DO namespace/auth, container identity, preview token, egress, secret mount/proxy, lifetime/runtime fence, backup retention, deployment/version rollout

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|
| `cloudflare-three-layer-runtime` | SDK는 Durable Object public layer, shared types, in-container runtime으로 나뉘고 HTTP/JSON으로 command/files/process를 중계한다. | [architecture overview](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/docs/ARCHITECTURE.md#L5-L27), [three layers](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/docs/ARCHITECTURE.md#L29-L68) | `I2` | `V2` | `W0` | 정적 pass. hosted container isolation/runtime은 미검증 |
| `cloudflare-executor-surface` | control API가 commands/files/processes/ports/git/interpreter/session/backup/watch/tunnels domain을 제공한다. | [SandboxControlAPI](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox-container/src/control-plane/api.ts#L41-L119) | `I2` | `V2` | `W0` | 정적 pass. 모든 domain의 deployed compatibility는 미검증 |
| `cloudflare-command-stream` | command는 sessionId/cwd/env/timeout을 받고 result 또는 SSE start/stdout/stderr/complete stream을 만든다. | [command RPC](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox-container/src/control-plane/api.ts#L121-L165), [stream RPC](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox-container/src/control-plane/api.ts#L167-L260) | `I2` | `V2` | `W0` | 정적 pass. disconnect/backpressure/event replay/cancel은 미검증 |
| `cloudflare-session-persistence-limit` | session metadata는 DO storage로 restart를 견디지만 active container의 files/processes는 sleeping 시 사라지는 ephemeral state다. | [session and lifecycle](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/docs/ARCHITECTURE.md#L123-L155) | `I2` | `V2` | `W0` | confirmed boundary. durable metadata와 runtime state를 동일시하면 안 됨 |
| `cloudflare-runtime-identity-fence` | current runtime identity는 DO storage에 저장되고 container health/running state와 ID가 모두 일치할 때만 active로 인정한다. | [runtime identity storage/status](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/current-runtime-identity.ts#L57-L106), [active assertion](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/current-runtime-identity.ts#L118-L138) | `I2` | `V2` | `W0` | 정적 pass. DO/container crash race와 storage consistency V5 미실행 |
| `cloudflare-lifetime-generation-fence` | explicit destroy는 logical lifetime ID를 rotate하고 generation을 올려 이전 operation이 새 sandbox lifetime에 복구되는 것을 차단한다. | [lifetime contract](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/sandbox-lifetime.ts#L1-L25), [rotate/assert](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/sandbox-lifetime.ts#L74-L127) | `I2` | `V2` | `W0` | 정적 pass. platform run/session generation 설계의 clean-room reference |
| `cloudflare-restore-double-fence` | restore runner가 runtime active와 lifetime current를 함께 확인하고 retryable interruption을 제한된 횟수로 복구한다. | [restore lifecycle](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/backup/restore-lifecycle.ts#L24-L45), [fence and retry](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/backup/restore-lifecycle.ts#L69-L142), [assert fences](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/backup/restore-lifecycle.ts#L174-L230) | `I2` | `V2` | `W0` | 정적 pass. crash/reorder/failure injection 미실행 |
| `cloudflare-license-boundary` | package license text는 Apache-2.0이나 repository metadata가 `NOASSERTION`이라 전체 tree 재사용 license를 자동 확정할 수 없다. | [root pointer](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/LICENSE), [package license](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/LICENSE#L1-L5) | `I1` | `V2` | `W0` | license limitation. component 단위 review 필요 |

## 인터페이스와 protocol

- Application: TypeScript Worker/Durable Object RPC object.
- DO → container: modular HTTP clients 또는 capnweb RPC; streaming command/log는 SSE.
- Interactive/preview: WebSocket/preview proxy/tunnel surface가 있고 runtime-local authorization을 요구한다.
- Identity: DO namespace+sanitized sandbox ID, session ID, runtime identity ID, sandbox lifetime ID/generation, operation record.
- 플랫폼 adapter는 runtime identity와 logical lifetime을 별도 fence로 유지하고 UI status는 이 authoritative state의 derived projection으로만 사용한다.

## 운영·보안 trust boundary

- caller Worker, Durable Object storage/identity, Cloudflare Container runtime, in-container code, preview/tunnel URL, backup object와 external credential proxy를 구분한다.
- runtime identity는 container start마다 교체되고 lifetime은 explicit destroy 때만 rotate된다. 이 이중 fence가 restart와 destroy의 의미를 분리한다.
- container isolation·security 문구는 official claim이지만 이번 V2는 구현 구조만 확인했다. tenant escape, egress, credential exfiltration은 V5가 필요하다.
- public preview/tunnel은 token·current-runtime activation·DNS/TLS/retention을 별도 검증해야 한다.

## 플랫폼과 Windows

local development prerequisite에 Docker가 있고 hosted runtime은 Cloudflare Container/VM이다. Windows-specific implementation 또는 Windows execution evidence를 이번 조사에서 확보하지 않았으므로 `W0`; Windows는 Worker client 개발 host일 수 있을 뿐 sandbox runtime이 아니다.

## 강점과 한계

- 강점: Durable Object identity와 container runtime 사이에 명시적 runtime/lifetime fence를 둔 점이 multi-executor orchestration에 직접 참고 가치가 있다.
- 강점: command/files/process/session/preview를 edge-native control surface로 제공한다.
- 한계: Cloudflare Workers/Containers/DO platform에 강하게 결합하며 local desktop executor가 아니다.
- 한계: container sleep에서 runtime files/processes가 사라져 persistence를 DO metadata와 backup/restore로 별도 설계해야 한다.
- 한계: repository-wide license metadata가 `NOASSERTION`이며 package/component별 license gate가 필요하다.
- 한계: beta/active development와 platform limits/cost/rollout은 TTL이 있는 외부 관찰값이다.

## AX 설계 재료

- **Borrow**: `cloudflare-runtime-identity-fence`, `cloudflare-lifetime-generation-fence`, `cloudflare-restore-double-fence`의 runtime replacement와 logical destroy를 분리한 이중 fence.
- **Adapt**: `cloudflare-executor-surface`와 `cloudflare-command-stream`을 provider-neutral adapter로 감싸고 UI status는 authoritative runtime/lifetime state의 derived projection으로 제한한다.
- **Avoid**: `cloudflare-three-layer-runtime`의 platform isolation 문구를 V5 proof로 승격하거나 `cloudflare-license-boundary`의 `NOASSERTION`을 무시한 전체 tree 재사용을 하지 않는다.
- **Build**: 사내 run/session generation store, policy/verifier/human gate, secret audience broker, preview/egress control, backup/operation retention ledger를 구현한다.
- **Unknown / decision items**: 업종, data classification, 규정, 승인 체계는 미정이다. hosted container 허용 data, secret/mount audience, network·preview 공개 범위, DO/backup/log retention과 삭제 승인자를 결정해야 한다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정의 최종 답이 아니라 사내 AX 플랫폼의 세 번째 remote executor adapter와 runtime generation/lifetime fencing·restore recovery 설계 재료
- 이유: `cloudflare-runtime-identity-fence`, `cloudflare-lifetime-generation-fence`, `cloudflare-restore-double-fence`는 platform kernel의 stale owner 방지에 가치가 높다. platform coupling, ephemeral state, license `I1`, V3+ 부재로 직접 기본 provider 채택은 보류한다.
- 재검토 조건: package license audit, new pin, V3 build/test, local Docker/Workers V4, hosted command/files/restart V4, destroy-vs-restart/race/restore/credential/preview V5

## Evidence와 다음 검증

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `cloudflare-pin-static-20260814` | parent `.gitmodules`/gitlink와 official fixed-SHA architecture/source 정적 검토 | partial pass | `cloudflare/sandbox-sdk@2dd1476e32769656da97d5a8daf75e2f92b57e71` | 위 `V2` Claim |
| `cloudflare-license-20260814` | root/package license blob + GitHub repository metadata | partial | package Apache-2.0, repository `NOASSERTION` | `cloudflare-license-boundary` |
| `cloudflare-v3plus-none` | local body/build/runtime/deploy/E2E/Windows 미실행 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

다음 검증은 package별 license/NOTICE audit 후 V3 build/unit test, local Docker+Workers command/files/SSE V4, hosted runtime restart와 session recovery V4, concurrent restore·destroy/lifetime rotate·stale runtime·preview authorization·secret proxy/egress V5를 수행한다. 각 attempt에 DO ID, runtime ID, lifetime generation, operation ID와 platform request ID를 보존한다.

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE RemoteExecutor/LifecycleReference`
- `ToolVersion PROVIDES remote-command/remote-files/runtime-generation/lifetime-fence`
- `ToolVersion SUPPORTS Durable-Objects/Containers/HTTP/SSE/capnweb-RPC`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: fixed pin과 official source를 대조해 repository `I2`, license conclusion `I1`, 기능 `V2 / W0`으로 기록. build/runtime/E2E 미수행.
