---
id: tool-vercel-sandbox
type: tool-profile
title: Vercel Sandbox
status: observed
tags:
  - knowledge-base
  - tool
  - remote-executor
  - microvm
  - sdk
official_upstream: https://github.com/vercel/sandbox
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 2c2c942239fd9ef47bed0b9295389b702ce6c0ff
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Vercel Sandbox

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Vercel Sandbox는 persistent Linux MicroVM을 SDK/CLI에서 생성·재개하고 command/files/interactive session, network policy, snapshot/fork를 다루는 remote executor 후보이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/vercel/sandbox` |
| 기본 브랜치와 고정 버전 | `main` · `2c2c942239fd9ef47bed0b9295389b702ce6c0ff` |
| 조사일 현재 관찰 | 2026-08-14 GitHub API 기준 current `main`은 `adf41df4eb10fff4836e0ac70951200f2ba2f851`로 pin보다 앞섬. 아래 Claim은 pin에만 적용 |
| 로컬 gitlink | [`multi-agent-tools/vercel-sandbox`](../../multi-agent-tools/vercel-sandbox/) |
| 출처 무결성 | `I2`: parent URL/gitlink SHA와 official fixed-SHA tree를 대조 |
| license | root [`LICENSE`](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/LICENSE#L1-L5)의 Apache-2.0 text와 GitHub SPDX metadata가 일치 |

## 조사 provenance와 ceiling

병렬 조사 worktree의 submodule 본문이 비어 local checkout body를 근거로 읽을 수 없었다. parent `.gitmodules`·`git ls-tree`로 `I2` pin을 확정하고 official GitHub fixed-SHA README/source를 `V2`로 검토했다. local body, npm install/build, Vercel login/API runtime, MicroVM E2E, Windows 실행은 수행하지 않았다.

## 목적과 기술 구조

- `@vercel/sandbox` SDK와 `sandbox` CLI가 Vercel control API에서 project-scoped Linux MicroVM을 관리한다.
- Sandbox object는 persistent sandbox identity와 current session을 구분하며 stopped/snapshotting session에서 새 session을 resume하고 요청을 retry한다.
- command API는 foreground/detached 실행, output stream, signal/kill을 제공하고 filesystem API는 Node `fs`에 가까운 read/write/mkdir/readdir/rename/copy surface를 제공한다.
- snapshot은 current session을 중지해 filesystem snapshot을 만들고 fork는 source의 config와 persistent state lineage를 새 sandbox로 복제한다.
- network policy는 default allow-all, deny-all, domain/CIDR allow/deny와 일부 request transformer를 표현한다.

## 역할과 연동

- AgentRole: Remote executor, Workspace/runtime provider
- Capability: `persistent-microvm`, `command-execution`, `file-operation`, `interactive-session`, `snapshot`, `fork`, `network-policy`
- Integration: TypeScript SDK, CLI, HTTPS control/data API, OIDC/access token, streaming logs
- SecurityOperationalRequirement: project/team scope, OIDC/token lifecycle, deny-by-default egress, snapshot retention, sudo policy, timeout/cost, stale session fencing, audit logs

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|
| `vercel-microvm-sandbox` | sandbox는 isolated ephemeral Linux Firecracker MicroVM이고 SDK/CLI surface를 제공한다. | [README](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/README.md#L1-L15) | `I2` | `V2` | `W0` | 문서+structure pass. isolation/runtime은 미실행 |
| `vercel-persistent-session` | SDK는 persistent sandbox와 current session을 분리하고 첫 operation 또는 stopped session에서 resume한다. | [persistent/resume options](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/sandbox.ts#L115-L148), [resume fencing/retry](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/sandbox.ts#L993-L1070) | `I2` | `V2` | `W0` | 정적 pass. duplicate command/idempotency와 concurrent resume는 미검증 |
| `vercel-command-files` | SDK가 command 실행/kill/output과 filesystem read/write/directory/rename/copy를 제공한다. | [runCommand](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/sandbox.ts#L1083-L1122), [filesystem](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/filesystem.ts#L237-L390) | `I2` | `V2` | `W0` | 정적 pass. stdin/PTY parity, atomicity, large stream은 미검증 |
| `vercel-snapshot-fork` | CLI/SDK가 filesystem snapshot과 source config를 복제하는 fork를 제공하며 persistent restore를 선택할 수 있다. | [fork CLI contract](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/sandbox/src/commands/fork.ts#L19-L75), [snapshot stop contract](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/sandbox/src/commands/snapshot.ts#L11-L80), [SDK fork](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/sandbox.ts#L739-L803) | `I2` | `V2` | `W0` | 정적 pass. running process/memory continuity는 주장하지 않음 |
| `vercel-network-policy` | network policy는 allow-all(default), deny-all, domain/CIDR allow/deny를 표현하며 denied CIDR가 우선한다. | [network policy type](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/network-policy.ts#L91-L175), [CLI builder](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/sandbox/src/util/network-policy.ts#L25-L62) | `I2` | `V2` | `W0` | 정적 pass. DNS rebinding·IPv6·redirect·policy enforcement는 미검증 |
| `vercel-auth-sudo-boundary` | SDK는 OIDC/access token과 project/team scope에 의존하고 default image는 passwordless sudo를 허용한다. | [authentication](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/README.md#L108-L148), [sudo behavior](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/README.md#L165-L192) | `I2` | `V2` | `W0` | confirmed trust boundary. guest root와 platform control plane isolation을 혼동하면 안 됨 |
| `vercel-service-limits-observation` | pin README는 sandbox duration/resource limits를 명시하지만 이는 변동 가능한 서비스 관찰값이다. | [README limits](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/README.md#L159-L163) | `I2` | `V1` | `W0` | TTL 필요. 가격·현재 quota를 이 프로필에서 보장하지 않음 |

## 인터페이스와 protocol

- Programmatic: `@vercel/sandbox` TypeScript SDK over authenticated HTTPS.
- Operator: `sandbox` CLI create/list/connect/exec/fork/snapshot/stop.
- Identity: project/team scope + sandbox name/metadata + session/command/snapshot IDs.
- Interactive: SDK interactive URL/token 및 CLI shell; typed API를 우선하고 PTY heuristic은 보조 adapter로 둔다.
- platform은 caller run ID와 sandbox/session/command generation을 저장해 auto-resume 후 stale output을 차단해야 한다.

## 운영·보안 trust boundary

- Vercel identity/project, client credential, platform API, MicroVM guest root, snapshot, published port/network policy를 분리한다.
- default allow-all network를 agent workload 기본값으로 쓰지 말고 explicit allowlist/deny CIDR와 secret audience를 policy gate로 둔다.
- snapshot/fork가 config/env를 복제할 수 있으므로 raw long-lived secret이 lineage에 전파되지 않게 opaque handle로 교환한다.
- SDK auto-resume/retry는 편리하지만 non-idempotent command 재실행 위험을 verifier fixture로 확인해야 한다.

## 플랫폼과 Windows

remote client를 Windows에서 실행할 수 있는 가능성은 있지만 실제 sandbox는 Linux MicroVM이고 Windows 전용 source/build/runtime evidence를 이번 조사에서 확보하지 않았다. 따라서 `W0`; Windows control host와 remote Linux guest를 분리한다.

## 강점과 한계

- 강점: persistent sandbox identity와 session resume, snapshot/fork, command/files, network policy가 agent workspace에 잘 맞는다.
- 강점: E2B와 같은 executor contract로 A/B 가능한 독립 provider 후보이다.
- 한계: hosted service credential·quota·duration·cost·availability에 의존하고 pin의 서비스 제한은 쉽게 stale해진다.
- 한계: default allow-all egress와 passwordless guest sudo는 별도 policy 없이 secret-safe 기본값이 아니다.
- 한계: pin은 current upstream main보다 뒤처져 최신 변경을 자동 반영하지 않는다.

## AX 설계 재료

- **Borrow**: `vercel-persistent-session`, `vercel-command-files`, `vercel-snapshot-fork`의 persistent identity/session 분리와 fork/resume surface.
- **Adapt**: `vercel-network-policy`를 deny-by-default 사내 policy로 좁히고 auto-resume/retry에 run/session generation과 idempotency key를 결합한다.
- **Avoid**: `vercel-microvm-sandbox` 문서만으로 isolation을 승인하거나 `vercel-auth-sudo-boundary`의 default allow-all/passwordless sudo를 production 기본값으로 사용하지 않는다.
- **Build**: provider-neutral conformance, secret broker, stale output fence, snapshot lineage/retention ledger, cost/timeout governor와 승인 gate를 AX control plane에 둔다.
- **Unknown / decision items**: 회사 업종, data classification, 규정, 승인자는 미정이다. remote sandbox 허용 data, token/secret TTL, network allowlist, snapshot/log retention·deletion 및 sudo 승인 기준을 결정해야 한다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정의 최종 답이 아니라 사내 AX 플랫폼의 E2B 대비 remote executor conformance A/B 설계 재료; persistent resume/fork 후보
- 이유: `vercel-persistent-session`, `vercel-command-files`, `vercel-snapshot-fork`가 run continuity에 유용하지만 `vercel-auth-sudo-boundary`와 enforcement 미검증 때문에 production default는 아님.
- 재검토 조건: pin update/diff, V3 SDK build, V4 command/files/session resume/fork, V5 concurrent resume/idempotency/network/secret/retention failure injection

## Evidence와 다음 검증

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `vercel-pin-static-20260814` | parent `.gitmodules`/gitlink와 official fixed-SHA docs/source 정적 검토 | partial pass | `vercel/sandbox@2c2c942239fd9ef47bed0b9295389b702ce6c0ff` | 위 `V1/V2` Claim |
| `vercel-head-drift-20260814` | GitHub default branch metadata | observed drift | `main@adf41df4eb10fff4836e0ac70951200f2ba2f851` | pin 최신성 한계 |
| `vercel-v3plus-none` | local body/build/runtime/API/E2E/Windows 미실행 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

다음 검증은 explicit 비용 승인을 전제로 SDK build V3, command/files/interactive/session resume/fork V4, concurrent resume와 non-idempotent retry·stale generation·deny-all/allowlist·snapshot secret retention V5를 수행하고 provider request ID와 sandbox/session/command/snapshot lineage를 보존한다.

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE RemoteExecutor`
- `ToolVersion PROVIDES persistent-microvm/command-execution/file-operation/snapshot-fork`
- `ToolVersion SUPPORTS TypeScript-SDK/CLI/HTTPS`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: fixed pin/current head를 분리해 `I2 / V2 / W0` persistent remote executor 후보로 기록. build/runtime/E2E 미수행.
