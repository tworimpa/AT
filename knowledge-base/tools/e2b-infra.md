---
id: tool-e2b-infra
type: tool-profile
title: E2B Infrastructure
status: observed
tags:
  - knowledge-base
  - tool
  - sandbox-infra
  - firecracker
  - self-host
official_upstream: https://github.com/e2b-dev/infra
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 035b7eda0e5d5a007489535686df9a7f087c154c
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# E2B Infrastructure

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

E2B Infrastructure는 Firecracker 기반 remote sandbox control/data plane과 self-host 배포 구조를 보여 주는 참조 구현이며, Windows desktop에서 직접 agent command를 실행하는 executor SDK가 아니다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/e2b-dev/infra` |
| 기본 브랜치와 고정 버전 | `main` · `035b7eda0e5d5a007489535686df9a7f087c154c` |
| 조사일 현재 관찰 | 2026-08-14 GitHub API 기준 current `main`은 `aeab31df792a293066a28286a80829e75db28463`으로 pin보다 앞섬. 이 프로필의 Claim은 pin에만 적용 |
| 로컬 gitlink | [`multi-agent-tools/e2b-infra`](../../multi-agent-tools/e2b-infra/) |
| 출처 무결성 | `I2`: parent `.gitmodules` URL/gitlink SHA와 official fixed-SHA tree를 대조 |
| license | root [`LICENSE`](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/LICENSE#L1-L5)의 Apache-2.0 text와 GitHub SPDX metadata가 일치 |

## 조사 provenance와 ceiling

병렬 조사 worktree의 submodule 본문이 비어 local checkout body를 읽을 수 없었다. parent `.gitmodules`와 `git ls-tree`를 `I2` pin evidence로, 공식 GitHub fixed-SHA tree/blob를 `V2` Claim evidence로 사용했다. local body, Terraform plan/apply, image/kernel build, Firecracker runtime, hosted API, E2E, Windows 실행은 모두 미수행이다.

## 목적과 기술 구조

- public REST API가 auth/quota/lifecycle/placement를 처리하고 node orchestrator에 gRPC create/delete/pause/resume 요청을 보낸다.
- sandbox node의 root orchestrator가 Firecracker microVM, cgroup, network namespace, COW rootfs, snapshot lazy loading을 관리한다.
- VM 내부 `envd`가 process/PTY/filesystem API를 제공하고 client proxy가 sandbox-to-node routing을 수행한다.
- Postgres는 durable entity, Redis는 running/routing state, ClickHouse는 telemetry, GCS/S3는 template/snapshot artifact를 담당한다.
- Terraform/Nomad 기반 GCP, AWS beta self-host deployment를 목표로 하며 일반 Linux host와 Azure는 fixed README상 미지원이다.

## 역할과 연동

- AgentRole: Sandbox infrastructure provider, Executor data-plane reference, Policy/operations reference
- Capability: `microvm-isolation`, `snapshot-resume`, `placement`, `network-policy`, `process-files-api`, `self-host-control-plane`
- Integration: REST/OpenAPI, gRPC, Connect RPC/HTTP, Firecracker API, Terraform/Nomad, Postgres/Redis/ClickHouse/GCS/S3
- SecurityOperationalRequirement: root orchestrator hardening, multi-tenant auth, workload identity audience, node isolation, egress, snapshot encryption/retention, disaster recovery, capacity/SLO

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|
| `e2b-infra-backend-scope` | repo가 control-plane API, Firecracker data plane, in-VM agent, routing, template build와 IaC를 포함한다. | [architecture overview](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L11-L28), [service map](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L85-L99) | `I2` | `V2` | `W0` | 정적 pass. 배포·서비스 readiness 미검증 |
| `e2b-infra-firecracker-snapshot` | sandbox는 Firecracker microVM이며 snapshot restore, lazy memory, COW rootfs로 상태를 구성한다. | [snapshot model](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L13-L28), [orchestrator mechanisms](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L131-L162) | `I2` | `V2` | `W0` | 정적 pass. boot latency·memory correctness·escape resistance 미검증 |
| `e2b-infra-control-data-split` | API control plane과 node orchestrator data plane이 분리되고 API가 placement/state, orchestrator가 VM 실행을 소유한다. | [control/data split](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L20-L28), [API and orchestrator](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L101-L148) | `I2` | `V2` | `W0` | 정적 pass. failover·split-brain·stale placement injection 미실행 |
| `e2b-infra-envd-contract` | VM 내부 envd가 process/stdin/signals/PTY와 filesystem API를 노출하고 access token을 검사한다. | [envd responsibilities](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L170-L192) | `I2` | `V2` | `W0` | 정적 pass. auth bypass·token rotation·stream recovery 미검증 |
| `e2b-infra-workload-identity` | API가 exact audience/tokenType definitions를 admission하고 authoritative sandbox identity로 workload identity를 파생한다. | [workload identity design](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L101-L123) | `I2` | `V2` | `W0` | 유용한 opaque/audience pattern. 실제 issuer·revocation·fork negative test는 미실행 |
| `e2b-infra-self-host-scope` | self-host는 Terraform으로 GCP와 AWS(beta)를 배포하며 Azure·general Linux machine은 지원 표기가 없다. | [README self-host matrix](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/README.md#L14-L22), [Firecracker Linux build note](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/self-host.md#L215-L220) | `I2` | `V2` | `W0` | 정적 pass. deployment 실행·비용·운영성 미검증 |
| `e2b-infra-not-desktop-executor` | 이 repo는 infrastructure/backend reference이며 Windows desktop agent adapter 또는 direct local executor가 아니다. | [repo scope](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/README.md#L4-L16), [node roles](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md#L131-L148) | `I2` | `V2` | `W0` | confirmed limitation. platform은 E2B SDK adapter를 별도로 사용해야 함 |

## 인터페이스와 protocol

- Client/API: REST/OpenAPI lifecycle·auth·quota·metrics.
- API/node: gRPC sandbox lifecycle, template build, capacity/health.
- VM guest: envd의 Connect RPC/HTTP process/filesystem/health/file transfer.
- Runtime: Firecracker Unix-socket API, cgroup/netns/NBD/object-storage snapshot.
- Deployment: Terraform, Nomad, cloud provider services. 이 복잡한 control plane을 desktop agent executor interface와 동일시하지 않는다.

## 운영·보안 trust boundary

- public API/auth DB, Redis routing, node orchestrator(root), Firecracker guest, envd token, object-store snapshot, telemetry store를 독립 authority로 나눈다.
- workload identity의 exact audience와 authoritative ID derivation은 secret handle 설계의 reference가 되지만 실제 credential delivery·revocation은 별도 검증 대상이다.
- Redis running state와 Postgres snapshots의 transition에는 generation/lease/idempotency와 stale owner fencing이 필요하다.
- self-host는 VM 한 개를 실행하는 문제가 아니라 cloud/IaC, DB/cache/object storage, root node, monitoring/upgrade까지 운영하는 범위다.

## 플랫폼과 Windows

Firecracker/node orchestration은 Linux-only 성격이고 fixed self-host 문서는 Firecracker build에 Linux machine이 필요하다고 명시한다. Windows는 remote SDK client/control host일 수 있을 뿐 이 data plane의 runtime host 근거가 없어 `W0`이다.

## 강점과 한계

- 강점: remote sandbox의 placement, snapshot lineage, node/runtime 경계, workload identity와 observability를 end-to-end 구조로 참조할 수 있다.
- 강점: control/data plane 분리와 Firecracker/COW/lazy restore는 remote executor readiness 기준 설계에 구체적이다.
- 한계: 운영 구성요소와 root authority가 많아 초기 Windows-first desktop platform의 직접 dependency로는 과도하다.
- 한계: pin은 조사일 current main보다 뒤처졌으며 fixed profile Claim을 최신 head에 자동 전이할 수 없다.
- 한계: static architecture는 실제 isolation, recovery, performance, SLO를 증명하지 않는다.

## AX 설계 재료

- **Borrow**: `e2b-infra-control-data-split`, `e2b-infra-firecracker-snapshot`의 control/data plane 및 snapshot lineage, `e2b-infra-workload-identity`의 exact audience pattern.
- **Adapt**: `e2b-infra-envd-contract`와 placement/state model을 provider-neutral executor contract, generation fence, readiness probe로 축소해 적용한다.
- **Avoid**: `e2b-infra-self-host-scope`의 전체 cloud stack을 초기 AX desktop executor로 복제하거나 `e2b-infra-not-desktop-executor`를 무시하지 않는다.
- **Build**: 사내 policy/verifier/human gate, opaque credential exchange, routing ownership fence, evidence/telemetry retention과 recovery drill을 별도 구현한다.
- **Unknown / decision items**: 업종, data classification, 규정, 승인 체계는 미정이다. self-host 필요성, tenant isolation 수준, secret issuer/audience, network/region, snapshot·telemetry retention 및 삭제 권한을 결정해야 한다.

## 도입 판단

- 결정: 참고
- 적용 범위: 벤더 선정의 최종 답이 아니라 사내 AX 플랫폼의 remote data-plane·snapshot·placement·workload identity·readiness/fencing 설계 재료; 직접 desktop executor로 채택하지 않음
- 이유: `e2b-infra-control-data-split`, `e2b-infra-firecracker-snapshot`, `e2b-infra-workload-identity`가 blueprint에 가치가 크지만 `e2b-infra-not-desktop-executor`와 높은 운영 복잡도로 직접 도입은 부적절하다.
- 재검토 조건: pin 업데이트 및 diff audit, isolated self-host lab V3/V4, node loss·Redis/Postgres drift·snapshot corruption·stale placement V5, security architecture review

## Evidence와 다음 검증

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `e2b-infra-pin-static-20260814` | parent `.gitmodules`/gitlink와 official fixed-SHA architecture/source 정적 대조 | partial pass | `e2b-dev/infra@035b7eda0e5d5a007489535686df9a7f087c154c` | 위 `V2` Claim |
| `e2b-infra-head-drift-20260814` | GitHub default branch metadata | observed drift | `main@aeab31df792a293066a28286a80829e75db28463` | pin 최신성 한계 |
| `e2b-infra-v3plus-none` | local body/build/deploy/runtime/E2E/Windows 미실행 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

다음 검증은 pin diff/license 재검사 후, 별도 비용 승인된 isolated cloud lab에서 Terraform plan V3, single-tenant create/command/pause/resume V4, node loss·stale routing·snapshot corruption·credential audience/fork V5를 수행한다. desktop platform Phase 1에는 실행하지 않는다.

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE SandboxInfrastructure/OperationsReference`
- `ToolVersion PROVIDES microvm-isolation/snapshot-resume/placement`
- `ToolVersion SUPPORTS REST/gRPC/Connect-RPC/Firecracker/Terraform/Nomad`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: fixed pin과 current main drift를 분리해 `I2 / V2 / W0` self-host infrastructure reference로 기록. deploy/runtime/E2E 미수행.
