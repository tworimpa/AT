---
id: tool-beads
type: tool-profile
title: Beads
status: observed
profile_schema_version: 2
tool_key: beads
tool_version_id: tool-version:beads@d1e725d9f35ba307518551b4e61b3d504fb41ec5
tags: [knowledge-base, tool, issue-graph, claim, identity]
official_upstream: https://github.com/gastownhall/beads
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 185b339be6d5bf7553dc4af0e8a535055f02de4e
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: d1e725d9f35ba307518551b4e61b3d504fb41ec5
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-14
---

# Beads

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Beads는 dependency graph 기반 ready-work 탐색, issue identity와 transaction/CAS-style claim을 제공하는 분산형 issue/task substrate다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/gastownhall/beads` |
| 기본 브랜치와 조사일 HEAD | `main` / [`185b339be6d5bf7553dc4af0e8a535055f02de4e`](https://github.com/gastownhall/beads/commit/185b339be6d5bf7553dc4af0e8a535055f02de4e) (2026-08-14) |
| 고정 버전 | `d1e725d9f35ba307518551b4e61b3d504fb41ec5` |
| pin과 최신 관찰 관계 | 조사 시 `main`이 2 commits ahead, pin은 behind 0. profile은 fixed SHA를 유지한다. |
| 로컬 gitlink | [`multi-agent-tools/beads`](../../multi-agent-tools/beads/) |
| 출처 무결성 | `I2`: parent `.gitmodules`/gitlink와 official fixed-SHA tree 일치 |
| license | fixed SHA [`LICENSE`](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/LICENSE#L1-L20)의 MIT |
| provenance limitation | 통합 조사 worktree submodule body가 비어 parent gitlink와 official fixed-SHA GitHub source/metadata로 `V2`를 수집했다. local build, DB runtime, concurrent claim, E2E, Windows 실행은 미수행이다. |
| source 관리 | claim/identity/dependency semantics가 core scheduler 설계에 직접 영향을 주므로 fixed-SHA submodule 유지 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Issue graph | dependencies에서 ready 후보 계산 | persisted issues/edges → ready IDs → hydrated issues | [ready query](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/ready_work.go#L31-L84) |
| Claim transaction | status/row lock 조건으로 owner 설정 | ready candidate → conditional UPDATE → event/lease | [CAS update](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim.go#L107-L138), [conflict/lease/event](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim.go#L138-L225) |
| Identity derivation | issue/auxiliary row collision 저감 | content → hash-derived ID | [derived IDs](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/derivedid.go#L10-L28) |
| Storage mode | embedded single-writer 또는 server multi-writer | DB source of truth; JSONL은 export | [storage modes](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/README.md#L127-L142) |

## 역할과 연동

- AgentRole: Issue planner, Ready-work scheduler, Claiming worker, Audit observer
- Capability: `dependency-ready-work`, `atomic-ish-task-claim`, `issue-identity`, `claim-event-journal`
- Integration: `bd` CLI, embedded/server database, JSONL export, HTTP API
- SecurityOperationalRequirement: transaction isolation, claim generation/fencing, authenticated network API, schema compatibility gate, safe process ownership

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `beads-ready-graph` | capability | dependency predicates로 ready issue IDs를 구하고 hydrate한다. | [current upstream](https://github.com/gastownhall/beads/commit/185b339be6d5bf7553dc4af0e8a535055f02de4e), 2026-08-14 | [ready_work.go](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/ready_work.go#L31-L144) | `I2` | `V2` | `W0` | pass(정적). graph scale/performance와 stale dependency runtime은 미검증. |
| `beads-claim-cas` | capability | claim은 transaction 안에서 row_lock/status 조건부 update와 affected-row 확인을 사용한다. | 동일 | [claim.go](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim.go#L18-L36), [CAS](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim.go#L107-L225) | `I2` | `V2` | `W0` | pass(atomic-ish 정적). 실제 concurrent claimant/DB backend에서 atomicity를 실행 검증하지 않았다. |
| `beads-claim-ready-tx` | architecture | ready 후보 계산과 claim을 한 transaction에서 수행하는 경로가 있다. | 동일 | [claim ready](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim.go#L244-L299), [claim next](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/claim_next.go#L44-L75) | `I2` | `V2` | `W0` | pass(정적). isolation level/failure injection은 unknown. |
| `beads-derived-identity-limit` | limitation | auxiliary content-derived ID는 collision 저감을 제공하지만 동일 content의 concurrent single-replica write 직렬화를 가정한다. | 동일 | [derivedid caveat](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/storage/issueops/derivedid.go#L55-L92) | `I2` | `V2` | `W0` | confirmed limitation. multi-writer identity/fencing 설계가 별도 필요하다. |
| `beads-auth-fail-closed` | security | loopback 밖 listen은 token 또는 명시적 insecure override가 필요하다. | 동일 | [auth.go](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/httpapi/auth.go#L243-L260) | `I2` | `V2` | `W0` | pass(정적 fail-closed default). `--insecure-no-auth` escape hatch와 loopback trust는 정책으로 제한해야 한다. |
| `beads-schema-bypass` | limitation | schema version guard가 있으나 환경변수로 무시할 수 있다. | 동일 | [schema skew](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/README.md#L144-L175) | `I2` | `V1` | `W0` | documented limitation. 사내 authoritative store에서는 bypass 금지 또는 승인·감사 필요. |
| `beads-windows-source` | platform | Windows process identity/liveness/terminate와 Dolt server lifecycle source, Windows workflow 정의가 있다. | 동일 | [procid](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/procid/procid_windows.go#L30-L138), [dolt lifecycle](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/doltserver/doltserver_windows.go#L31-L127), [Windows job](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/.github/workflows/pr.yml#L253-L303) | `I2` | `V2` | `W1` | pass(좁은 source). canonical port의 untracked server 처리 위험이 있으며 실제 Windows 실행 증거가 아니다. |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| `bd` CLI | command + DB transaction | planner/worker → issue store | local DB authority, process identity | [workflow](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/README.md#L49-L79) |
| HTTP API | HTTP + token | remote client → server | non-loopback token required unless insecure override | [auth](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/internal/httpapi/auth.go#L243-L260) |
| JSONL export | line-delimited records | DB → Git/interchange | export는 source of truth 아님 | [storage note](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/README.md#L127-L142) |

## 운영·보안·trust boundary

- DB transaction과 backend isolation이 claim authority다. CLI 성공/self-report만으로 concurrent exclusivity를 증명하지 않는다.
- loopback은 no-token으로 허용되므로 local hostile process 모델과 OS ACL을 결정해야 한다. non-loopback insecure override와 schema bypass는 production profile에서 fail-closed로 차단한다.
- Windows Dolt cleanup은 process ownership 확인 한계 때문에 unrelated process 종료 위험을 검증해야 한다.
- 회사 업종, 데이터 분류, 규정, 승인, 망분리, DB topology는 unknown Decision Item이다.

## 플랫폼과 Windows

- fixed source의 Windows process creation-time token/liveness와 workflow config로 `W1`을 부여한다.
- CI YAML 존재는 조사자가 실행한 CI가 아니며, build/runtime/process cleanup을 수행하지 않아 `W2/W3`이 아니다.
- server/embedded mode 각각의 Windows locking, port ownership, crash recovery를 별도로 검증해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `beads-origin-static-20260814` | `I2/V2/W1` | `d1e725d9...` | gitlink/upstream/fixed source inspection; exit 0 | Windows/PowerShell, parent `984cac0...` | partial pass | 위 permalinks | 모든 Claim | local body/runtime 미사용 |
| `beads-v3plus-none` | `V3~V6/W2~W3` | 동일 | build/runtime/concurrent claim/E2E 미실행 | unknown | unknown | 없음 | 없음 | atomicity runtime claim 금지 |

실행 기록: task/run `/root/implement_deep_collaboration_profiles`; profile `implement-deep` revision unknown; role `profile author`; model `OpenAI/gpt-5.6-sol`, exact build unknown; effort `high`; 시간·cost·latency unknown(2026-08-14 session); base/head `984cac0634b83d10af91d8e1814680816e67c53b`; artifact는 이 프로필뿐이다.

## 강점과 한계

- 강점: ready graph와 conditional claim/event를 같은 storage model에서 연결해 scheduler 설계 reference가 명확하다.
- 확인된 한계: derived identity는 특정 concurrency 가정을 가지며 auth/schema guard에는 명시적 bypass가 있다.
- 미확인: 실제 backend별 atomicity, deadlock/retry, lease expiry/fencing, server failover와 Windows process safety는 unknown이다.

## AX 설계 재료

이 표는 최종 vendor selection이 아니라 사내 AX 설계 재료다. 회사 조건은 추정하지 않는다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | issue identity, dependency-ready query, conditional claim/event pattern | `beads-ready-graph`, `beads-claim-cas` | `AXN-TASK-OWNERSHIP` |
| Adapt | backend-neutral transaction contract에 generation lease/fencing와 idempotency key 추가 | `beads-claim-ready-tx`, `beads-derived-identity-limit` | multi-executor/replica 조건 |
| Avoid | V2 source를 실제 atomicity로 주장, auth/schema bypass 허용, port만으로 process 종료 | `beads-claim-cas`, `beads-schema-bypass`, `beads-windows-source` | fail-open/data-loss 방지 |
| Build | transaction conformance suite, append-only claim evidence, lease heartbeat/reclaim, safe Windows ownership cleanup | 모든 Claim | `AD-DURABLE-TASK-CLAIM` → `RM-CLAIM-CONTENTION-MATRIX` (proposed) |

관계: `atomic-ish-task-claim` → `AXN-TASK-OWNERSHIP` → `AD-DURABLE-TASK-CLAIM` → `RM-CLAIM-CONTENTION-MATRIX`; evidence는 fixed-SHA Claims/Evidence다.

## 도입 판단

- 결정: 참고/adapter 실험 후보
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: graph-ready와 task identity/claim transaction pattern
- 재검토 조건: `V3` build, backend별 concurrent `V4/V5`, auth/schema escape 정책, Windows `W2/W3`

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `beads-claim-contention` | `beads-claim-cas`, `beads-claim-ready-tx` | `V4/V5` | embedded/server isolated DB | simultaneous claims, crash between CAS/event, lease expiry | one fenced owner, replayable audit, deterministic reclaim | DB/event/log bundle | DB runtime 승인 |
| `beads-windows-process` | `beads-windows-source` | `W2/W3` | native Windows | owned/unowned Dolt processes, crash/restart | unrelated process 미종료, owned child cleanup | process/port logs | process execution 승인 |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion PROVIDES dependency-ready-work/atomic-ish-task-claim/issue-identity`
- `Capability ADDRESSES AXNeed`
- `AXNeed DRIVES ArchitectureDecision`
- `ArchitectureDecision CREATES RoadmapItem`
- `RoadmapItem IMPLEMENTS Capability`

## 변경 이력

- 2026-08-14: official fixed-SHA source로 `I2/V2/W1` 작성. concurrent atomicity는 미검증으로 제한.
