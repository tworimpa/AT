---
id: tool-warren
type: tool-profile
title: Warren
status: observed
profile_schema_version: 2
tool_key: warren
tool_version_id: tool-version:warren@bb9a4f1ced640f220b062c1ddfb9ba778e990bfa
tags:
  - knowledge-base
  - tool
  - control-plane
  - sandbox
  - governance
official_upstream: https://github.com/jayminwest/warren
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: ae3d9c633dacf3d79a1a93ad01d09cc9bed85f9c
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: bb9a4f1ced640f220b062c1ddfb9ba778e990bfa
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Warren

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Warren은 agent run을 runtime-provider contract 뒤의 local sandbox 또는 Kubernetes pod로 dispatch하고 event·workspace·credential·admission·human governance 경계를 설계한 self-hosted control-plane reference다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/jayminwest/warren` |
| 기본 브랜치와 조사일 HEAD | `main` / `ae3d9c633dacf3d79a1a93ad01d09cc9bed85f9c` (2026-08-14) |
| 고정 버전 | `bb9a4f1ced640f220b062c1ddfb9ba778e990bfa` |
| pin과 최신 관찰 관계 | current HEAD가 pin보다 6 commits 앞섬. 아래 Claims는 fixed pin에만 적용하며 latest release와 같다고 보지 않음 |
| 로컬 gitlink | [`multi-agent-tools/warren`](../../multi-agent-tools/warren/) |
| 유지보수 관찰 | GitHub metadata상 archived/disabled가 아니고 `pushed_at=2026-08-13T18:53:39Z`; 지원 SLA/운영 상태와 분리 |
| 출처 무결성 | `I2`: parent gitlink와 official fixed commit/tree, current HEAD compare 대조 |
| license | fixed [`LICENSE`](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/LICENSE#L1-L21)의 MIT text와 GitHub SPDX metadata 일치 |
| provenance limitation | local submodule body가 비어 official GitHub fixed-SHA code/docs만 검토. build/runtime/E2E는 미실행이며 Docker/bwrap/Kubernetes, agent run, acceptance, recovery, production도 실행하지 않음 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| HTTP/UI control plane | project/run/plan dispatch, stream, steer, cancel | client→HTTP API→domain composition→runtime provider | [architecture/API](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L224-L295) |
| RuntimeProvider seam | domain intent를 provider-native sandbox/pod identity와 분리 | `RunSpec`→opaque `RunHandle`→events/status/finalize | [contract boundary](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L1-L46), [capabilities](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L204-L230) |
| Local/K8s runtime | local Burrow/bwrap 또는 pod-per-run 실행 | provider create→sandbox/pod→normalized events/status | [topology](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L224-L250), [local create](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/local/provider.ts#L108-L148) |
| Workspace/worktree | host clone에서 per-run branch/worktree materialization helper | clone/worktree→run workspace→cleanup | [helper contract](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/workspace/git/worktree.ts#L1-L20), [CRUD](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/workspace/git/worktree.ts#L25-L115) |
| Governance/admission | protected policy changes, proposal boundary, capacity rejection | agent proposal→human/CI gate; counts/caps→admit/reject | [constitution](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/docs/CONSTITUTION.md#L75-L112), [admission gate](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/k8s/admission.ts#L169-L205) |
| Forge credential seam | git operation 직전 credential mint | forge→single-op secret→git child env | [credential contract](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/forge/credentials.ts#L1-L18), [fail behavior](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/forge/credentials.ts#L23-L65) |

## 역할과 연동

- AgentRole: Control Plane, Scheduler/Admission, Executor/Runtime Provider, Worker, Verifier, Policy, Human Approver, scoped Committer.
- Capability: `runtime-provider-contract`, `sandbox-per-run`, `opaque-run-handle`, `normalized-event-stream`, `worktree-materialization`, `capacity-admission`, `per-operation-credential`, `proposal-governance`.
- Integration: HTTP/NDJSON, CLI/UI, Unix socket/Bearer, Kubernetes API, git/worktree, GitHub App/PAT, SQLite/Postgres.
- SecurityOperationalRequirement: multi-tenant auth, audit, secret rotation, TLS, per-repo allowlist, sandbox/egress verification, generation fencing and approval separation이 필요하다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `wr-runtime-seam` | architecture | domain에서 provider-native sandbox/pod/path identity를 opaque contract 뒤로 숨긴다. | [contract](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L1-L46), [workspace semantics](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L239-L259) | `I2` | `V2` | `W0` | pass(정적 interface). provider conformance/runtime 미검증 |
| `wr-sandbox-topologies` | architecture | local Burrow/bwrap와 K8s pod를 provider topology로 분리한다. | [topology](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L224-L250), [local provider](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/local/provider.ts#L84-L148) | `I2` | `V2` | `W0` | partial. README의 sandbox/운영 주장을 이 조사에서 실행 확인하지 않음 |
| `wr-worktree-helper-unwired` | limitation | worktree helper는 clone/worktree CRUD를 제공하지만 fixed source 주석상 domain에 아직 wiring되지 않은 reference seam이다. | [explicit unwired note](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/workspace/git/worktree.ts#L1-L20), [operations](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/workspace/git/worktree.ts#L62-L115) | `I2` | `V2` | `W0` | confirmed limitation. reference implementation이지 active runtime path proof가 아님 |
| `wr-capability-degradation` | capability | provider가 preview/network/steering/resource/archive/GC capability를 명시적으로 광고한다. | [capability contract](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L204-L230), [local declaration](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/local/provider.ts#L84-L99) | `I2` | `V2` | `W0` | interface/declaration only; enforcement와 actual egress coverage unknown |
| `wr-governed-proposal` | security | agent finding은 durable tracker proposal이며 protected policy/self-schedule change는 human review 대상으로 둔다. | [human protected changes](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/docs/CONSTITUTION.md#L81-L99), [reporting boundary](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/docs/CONSTITUTION.md#L103-L112) | `I2` | `V2` | `W0` | strong reference pattern; repository-specific governance이며 platform-wide enforcement 미검증 |
| `wr-admission-fail-closed` | security | K8s capacity counters가 cap에 도달하면 machine-readable 429용 rejection을 만든다. | [gate](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/k8s/admission.ts#L169-L205) | `I2` | `V2` | `W0` | partial. cap `0`은 control disable이므로 config policy 필요; race/cluster runtime 미검증 |
| `wr-credential-mint` | security | forge-owned clone URL에 대해 git operation 직전 secret을 mint하고 non-no-credential failure는 loud error로 만든다. | [credential seam](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/forge/credentials.ts#L1-L18), [mint](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/forge/credentials.ts#L48-L65) | `I2` | `V2` | `W0` | partial. foreign URL/no credential는 anonymous fallback이어서 policy별 fail-closed 결정 필요 |
| `wr-v1-security-gaps` | limitation | single bearer, no rotation/revocation, no multi-tenant RBAC/audit 등 V1 한계를 공식 문서가 명시한다. | [known limitations](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/SECURITY.md#L29-L48) | `I2` | `V2` | `W0` | confirmed limitation; 사내 baseline으로 직접 채택 금지 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| HTTP API/CLI/UI | HTTP + Bearer + NDJSON stream | operator/client→control plane→run | health/version 외 bearer; TLS는 edge 책임 | [API auth](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L252-L295) |
| RuntimeProvider | typed in-process interface | domain→local/K8s provider | opaque handle과 capability contract; provider enforcement 별도 | [RunHandle/RunSpec](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L24-L46) |
| event stream/status | ordered normalized events + reconcile snapshot | provider→domain/evidence consumers | origin classification과 cursor가 필요 | [events/status](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/runtime/contract.ts#L108-L180) |
| forge credential | typed secret mint→git env | control plane→single git child | anonymous fallback 조건을 policy에서 제한해야 함 | [mint semantics](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/src/forge/credentials.ts#L34-L65) |

## 운영·보안·trust boundary

- Warren README의 “sandboxed”, “stable”, “continuous use”는 공식 문서 `V1` 관찰이다. 이 profile의 runtime ceiling은 `V2`이며 보안/운영 성공으로 승격하지 않는다.
- quickstart는 outer container에 unconfined security flags와 `SYS_ADMIN`을 요구한다. nested sandbox가 outer host boundary를 대체하지 않으므로 deployment threat model을 별도 검증해야 한다.
- `SECURITY.md`가 밝힌 single bearer/no audit/no RBAC는 사내 AX 최소 코어 요구와 충돌한다.
- credential mint의 anonymous fallback은 public repo 편의일 수 있으나 private/regulated project에서는 allowlist와 explicit denial이 필요하다.

## 플랫폼과 Windows

- `W0`: local topology는 Linux bwrap/Unix socket이고 hosted path는 Kubernetes pod다. Windows control client 가능성과 Windows executor/runtime를 구분한다.
- fixed source에 native Windows sandbox/executor path 또는 실행 artifact가 없어 cross-platform native core 전체의 구현 후보가 아니라 governed Linux sandbox/control-plane reference로만 사용한다. Linux host runtime도 이 조사에서는 실행하지 않았다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | 지원 Claim | limitation |
|---|---|---|---|---|---|---|---|
| `wr-origin-20260814` | `I2` | `bb9a4f1ced640f220b062c1ddfb9ba778e990bfa` | parent gitlink + official fixed/current compare/license, exit 0 | Windows PowerShell 5.1; git 2.51.0.windows.1; gh 2.95.0 | pass | ToolVersion identity | current HEAD 6 commits ahead |
| `wr-static-20260814` | `V2/W0` | same | official fixed README/contracts/provider/worktree/governance/security 정적 검토, exit 0 | same | partial pass | 위 Claims | local/k8s runtime 없음 |
| `wr-v3plus-none` | `V3~V6/W2~W3` | same | build/Docker/bwrap/K8s/agent E2E 미실행 | unknown | unknown | 없음 | upstream CI/demo/운영 주장을 재검증하지 않음 |

수집 실행 기록: `run_id=implement-deep-orchestration-profiles-20260814`, `profile_id=implement-deep@1`, role=`Documenter`, provider=`OpenAI`, model slug=`gpt-5.6-sol`, model version=`unknown`, requested/actual effort=`high/high`, base/head=`984cac0634b83d10af91d8e1814680816e67c53b`, started_at=`not-captured`, ended_at=`2026-08-14T23:54:03+09:00`, cost/latency=`unknown`, external write=`none`.

## 강점과 한계

- 강점: domain/runtime identity 분리, capability degradation, admission, credential mint와 agent proposal governance를 명시적 contract로 만든다.
- 강점: sandbox/worktree를 control-plane architecture와 연결하는 풍부한 reference다.
- 한계: worktree helper가 pinned source에서 아직 domain에 unwired이고 runtime/security enforcement를 이 조사에서 실행하지 않았다.
- 한계: V1 auth/audit/RBAC posture는 사내 multi-user governance baseline에 부족하다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | opaque runtime handle, provider capability matrix, agent output→durable proposal→human protected change | `wr-runtime-seam`, `wr-capability-degradation`, `wr-governed-proposal` | `AX-N-EXECUTOR-ABSTRACTION`, `AX-N-GOVERNANCE` |
| Adapt | per-operation credential mint와 admission을 company policy/ABAC, repo allowlist, immutable caps로 강화 | `wr-credential-mint`, `wr-admission-fail-closed` | `AX-D002~D005` 결정 필요 |
| Avoid | single bearer/no audit posture, unconfined outer container를 production-safe로 간주, unwired helper를 active path로 주장 | `wr-v1-security-gaps`, `wr-worktree-helper-unwired` | fail-closed·감사·provenance 위반 |
| Build | Windows-native executor, lease/generation fencing, secret broker, append-only evidence/audit, policy decision point와 scoped committer | 위 전체 | `AD-WINDOWS-EXECUTOR`, `AD-POLICY-EVIDENCE`, `RM-MINIMAL-CORE` |

회사 업종, 데이터 분류, 규정, 승인 체계, 망분리, cloud/Kubernetes 허용, secret store와 tenancy는 `unknown/decision-needed`다.

## 도입 판단

- 결정: 참고/격리 파일럿 후보.
- 성격: vendor selection이 아니라 governed sandbox/worktree/control-plane 설계 재료.
- 적용 범위: runtime contract, provider capability, governance/admission/credential patterns; Windows executor와 사내 auth/audit는 직접 구현.
- 재검토 조건: current pin 갱신, build `V3`, local/K8s controlled runtime `V4`, sandbox escape/egress/credential/recovery `V5`, Windows executor 별도 `W2/W3`.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|
| `wr-v3-build` | fixed ToolVersion | `V3` | pinned Bun/dependencies build/test | exit 0와 artifact hash | lock/env/log/hash | dependency/network approval |
| `wr-v4-local` | `wr-sandbox-topologies` | `V4` | disposable Linux VM에서 local runtime | isolation/resource/network/status contract 관찰 | runtime trace, mount/net/process snapshot | Docker/secret/cost approval |
| `wr-v5-boundary` | governance/credential/admission | `V5` | malicious worker, anonymous URL, cap race, crash/restart | forbidden write/secret/egress 0; stale run fenced | audit/event/cluster/git artifacts | security-owned testbed |

## 관계와 변경 이력

- `ToolVersion PROVIDES runtime-provider-contract/sandbox-per-run/capacity-admission/proposal-governance`.
- `Capability ADDRESSES AXNeed AX-N-EXECUTOR-ABSTRACTION/AX-N-GOVERNANCE`.
- `ArchitectureDecision AD-POLICY-EVIDENCE ADAPTS wr-governed-proposal`.
- 2026-08-14: `I2/V2/W0` fixed-SHA 프로필 작성. current HEAD 6 commits ahead, unwired worktree seam, V1 security gaps와 runtime 미검증을 보존.
