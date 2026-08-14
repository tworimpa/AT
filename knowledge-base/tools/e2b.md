---
id: tool-e2b
type: tool-profile
title: E2B SDK
status: observed
tags:
  - knowledge-base
  - tool
  - remote-executor
  - sandbox
  - sdk
official_upstream: https://github.com/e2b-dev/E2B
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: f5d702a520de52ac0e5d4dda3ca0d5fca01d7993
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# E2B SDK

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

E2B SDK는 API key로 remote Linux sandbox를 생성·재연결하고 command/PTY/files/git와 pause/fork/snapshot lifecycle을 제어하는 remote executor adapter 후보이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/e2b-dev/E2B` |
| 기본 브랜치와 고정 버전 | `main` · `f5d702a520de52ac0e5d4dda3ca0d5fca01d7993` |
| 조사일 현재 관찰 | 2026-08-14 GitHub API 기준 `main` HEAD도 위 SHA이며 archived/disabled가 아님 |
| 로컬 gitlink | [`multi-agent-tools/e2b`](../../multi-agent-tools/e2b/) |
| 출처 무결성 | `I2`: parent URL/gitlink와 official fixed-SHA tree를 대조 |
| license | root [`LICENSE`](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/LICENSE#L1-L5)의 Apache-2.0 text와 GitHub SPDX metadata가 일치. package별 LICENSE도 통합 전 재확인 필요 |

## 조사 provenance와 ceiling

병렬 조사 worktree의 submodule 본문이 비어 local checkout body를 읽지 못했으므로 parent `.gitmodules`·`git ls-tree`로 pin을 `I2` 확인하고 공식 GitHub fixed-SHA tree/blob를 `V2` 근거로 사용했다. 이 프로필에서 local body, package install/build, E2B API runtime, agent E2E, Windows 실행은 수행하지 않았다. 따라서 서비스 격리·지속성·latency·비용은 검증된 운영 사실이 아니다.

## 목적과 기술 구조

- JavaScript/Python SDK와 CLI가 E2B control API에서 sandbox lifecycle을 관리하고, sandbox 내부 `envd`에 Connect RPC/HTTP2로 process·filesystem 요청을 전달한다.
- JS `Sandbox`는 `sandboxId`, sandbox domain, envd access token, traffic access token을 결합하고 `Commands`, `Pty`, `Filesystem`, `Git` client를 제공한다.
- command는 foreground/background, stdin, stdout/stderr callback, timeout을 지원하고 PTY는 PID 기반 create/connect/input/resize/kill surface를 가진다.
- pause는 memory 포함 또는 filesystem-only snapshot을 선택하며, snapshot으로 새 sandbox 생성과 fork를 표현한다.

## 역할과 연동

- AgentRole: Remote executor, Workspace/runtime provider
- Capability: `remote-command`, `remote-pty`, `remote-files`, `sandbox-identity`, `pause-resume`, `fork`, `snapshot`
- Integration: JS/Python SDK, CLI, E2B REST control API, Connect RPC/HTTP2 to envd
- SecurityOperationalRequirement: API key audience/scope, sandbox/traffic token 보호, egress policy, retention/deletion, tenant isolation, timeout/cost budget, audit artifact 보존

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|
| `e2b-remote-sandbox-sdk` | JS/Python SDK가 cloud sandbox를 만들고 command를 실행하는 공식 surface를 제공한다. | [README](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/README.md#L19-L61) | `I2` | `V2` | `W0` | 정적 pass. service 호출·격리 효과는 미실행 |
| `e2b-typed-client-surface` | JS Sandbox가 files, commands, PTY, git 모듈과 stable sandbox identity/token을 결합한다. | [Sandbox fields and clients](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/index.ts#L54-L121), [client construction](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/index.ts#L161-L228) | `I2` | `V2` | `W0` | 정적 pass. token rotation·cross-tenant negative test는 미실행 |
| `e2b-command-contract` | command API는 background, cwd/user/env, stdout/stderr, stdin, timeout과 PID 정보를 표현한다. | [commands API](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/commands/index.ts#L37-L130) | `I2` | `V2` | `W0` | 정적 pass. exit/cancel/timeout conformance는 미검증 |
| `e2b-pty-contract` | PTY API는 interactive bash를 생성하고 PID로 reconnect하며 input/resize/kill을 제공한다. | [PTY implementation](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/commands/pty.ts#L80-L174), [PTY input/resize](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/commands/pty.ts#L226-L318) | `I2` | `V2` | `W0` | 정적 pass. replay ordering, disconnect/reconnect, backpressure는 미검증 |
| `e2b-files-contract` | filesystem API는 text/bytes/blob/stream read, write, list, rename, remove, watch를 노출한다. | [Filesystem read/write](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/filesystem/index.ts#L369-L452), [list/rename/remove/watch](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/filesystem/index.ts#L827-L1044) | `I2` | `V2` | `W0` | 정적 pass. path traversal·large stream·atomicity fixture는 미실행 |
| `e2b-snapshot-fork` | pause는 memory 또는 filesystem-only 상태를 선택하고 snapshot/fork로 상태 계보를 만든다. | [fork semantics](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/index.ts#L393-L432), [pause/snapshot semantics](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/index.ts#L633-L690) | `I2` | `V2` | `W0` | 정적 pass. memory/process continuity와 snapshot deletion/retention은 미검증 |
| `e2b-remote-trust-boundary` | SDK는 remote service credential과 remote Linux runtime에 의존하므로 client API 존재만으로 tenant isolation, secret safety, retention, egress를 증명하지 않는다. | [API key requirement](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/README.md#L36-L42), [access-token transport](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/index.ts#L108-L121) | `I2` | `V2` | `W0` | confirmed limitation. service-side policy와 V5 security test 필요 |

## 인터페이스와 protocol

- Control plane: JS/Python SDK와 CLI가 E2B API로 create/list/connect/fork/pause/snapshot/kill을 요청한다.
- Data plane: client가 sandbox ID headers와 access token을 사용해 `envd` HTTP/Connect RPC에 접근한다.
- Process: command event stream과 PID handle; PTY는 reconnect 가능한 별도 surface.
- Files: HTTP/Connect RPC 기반 read/write/list/watch와 streaming payload.
- platform adapter에는 외부 request ID와 project run/session ID를 E2B `sandboxId`/PID/snapshot ID에 명시적으로 매핑하고 stale response fence를 두어야 한다.

## 운영·보안 trust boundary

- control API credential, envd access token, traffic access token, sandbox network, snapshot storage와 user code를 별도 trust domain으로 취급한다.
- agent secret은 raw env 전달보다 audience-scoped opaque handle과 workload별 short-lived exchange를 우선한다.
- sandbox API가 “secure/isolated”라고 문서화돼도 이번 V2는 구현 surface만 확인했으며 실제 tenant escape/egress/retention을 증명하지 않는다.

## 플랫폼과 Windows

client SDK를 Windows에서 호출할 수 있다는 가능성과 remote Linux sandbox가 Windows executor라는 주장은 다르다. 고정 소스의 Windows 전용 실행 경로 또는 Windows runtime evidence를 이번 조사에서 확인하지 않았으므로 `W0`이다.

## 강점과 한계

- 강점: command, PTY, files, lifecycle과 snapshot/fork를 단일 remote SDK에서 제공해 executor contract adapter 후보로 적합하다.
- 강점: sandbox ID와 PID/snapshot ID가 run/session identity 설계의 concrete mapping 대상이 된다.
- 한계: hosted control/data plane, network latency, API key, service quota와 비용에 의존한다.
- 한계: retry/idempotency, pause 중 in-flight I/O, fork consistency, kill semantics를 정적으로만 확인했다.
- 한계: 서비스의 security/availability/SLA를 repository client code로 증명할 수 없다.

## AX 설계 재료

- **Borrow**: `e2b-command-contract`, `e2b-pty-contract`, `e2b-files-contract`의 typed remote executor surface와 `e2b-snapshot-fork`의 state lineage.
- **Adapt**: `e2b-typed-client-surface`의 sandbox/PID/snapshot ID를 사내 run/session/generation과 매핑하고 모든 retry에 idempotency/fence를 추가한다.
- **Avoid**: `e2b-remote-sandbox-sdk`의 isolation 문구나 `e2b-remote-trust-boundary`의 hosted credential을 그대로 사내 security proof로 사용하지 않는다.
- **Build**: provider-neutral conformance fixture, audience-scoped secret broker, egress policy, retention/deletion evidence, cost/timeout governor를 AX control plane에 둔다.
- **Unknown / decision items**: 업종, data classification, 규정, 승인자는 미정이다. 어떤 data를 remote sandbox에 보낼지, secret scope/TTL, network destination, snapshot/log retention·deletion과 사람 승인 지점을 결정해야 한다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정의 최종 답이 아니라 사내 AX 플랫폼의 첫 remote executor adapter 설계 재료; local Container Use와 Vercel Sandbox에 동일 conformance fixture를 적용하는 기준 구현
- 이유: `e2b-command-contract`, `e2b-pty-contract`, `e2b-files-contract`, `e2b-snapshot-fork`가 요구 surface를 폭넓게 제공한다. 다만 `e2b-remote-trust-boundary` 때문에 credential·egress·retention gate 전 production 사용은 보류한다.
- 재검토 조건: new pin, service terms/license change, V3 client build, V4 command/files/PTY/pause-resume, V5 cancel/reconnect/fork/secret/egress failure injection

## Evidence와 다음 검증

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `e2b-pin-static-20260814` | parent `.gitmodules` + gitlink, official GitHub fixed-SHA README/source 정적 검토 | partial pass | `e2b-dev/E2B@f5d702a520de52ac0e5d4dda3ca0d5fca01d7993` | 위 `V2` Claim |
| `e2b-v3plus-none` | local body/build/runtime/API/E2E/Windows 미실행 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

다음 검증은 SDK build V3 후 executor conformance V4(command exit/stdout/stderr/stdin/timeout/cancel, PTY reconnect, files atomicity, snapshot resume)와 V5(stale session fencing, fork consistency, credential/egress/retention negative test)를 수행하고 command log·request ID·sandbox/snapshot ID를 evidence로 보존한다.

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE RemoteExecutor`
- `ToolVersion PROVIDES remote-command/remote-pty/remote-files/snapshot-fork`
- `ToolVersion SUPPORTS JS-SDK/Python-SDK/CLI/REST/Connect-RPC`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA source를 대조해 `I2 / V2 / W0` remote executor 후보로 기록. build/runtime/E2E 미수행.
