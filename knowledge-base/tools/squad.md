---
id: tool-squad
type: tool-profile
title: squad
status: observed
profile_schema_version: 2
tool_key: squad
tool_version_id: tool-version:squad@8146bcc1c38c439aedaf3ff44548c830654c8621
tags: [knowledge-base, tool, collaboration, task-queue, sqlite]
official_upstream: https://github.com/mco-org/squad
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 8146bcc1c38c439aedaf3ff44548c830654c8621
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 8146bcc1c38c439aedaf3ff44548c830654c8621
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-14
---

# squad

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

squad는 daemon 없이 공유 SQLite store를 통해 에이전트 메시지, task 상태, lease와 history를 조정하는 terminal collaboration/task-memory queue다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/mco-org/squad` |
| 기본 브랜치와 조사일 HEAD | `main` / [`8146bcc1c38c439aedaf3ff44548c830654c8621`](https://github.com/mco-org/squad/commit/8146bcc1c38c439aedaf3ff44548c830654c8621) (2026-08-14) |
| 고정 버전 | `8146bcc1c38c439aedaf3ff44548c830654c8621` (조사일 HEAD와 동일) |
| 로컬 gitlink | [`multi-agent-tools/squad`](../../multi-agent-tools/squad/) |
| 출처 무결성 | `I2`: parent `.gitmodules` URL + `git ls-tree` gitlink SHA + official fixed tree 교차 확인 |
| license | fixed SHA [`LICENSE`](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/LICENSE#L1-L20)의 MIT. 의존성은 별도 검토한다. |
| provenance limitation | 통합 조사 worktree submodule body가 비어 parent gitlink와 official GitHub fixed-SHA tree/metadata로 `V2`를 수집했다. local build/runtime/contention/E2E/Windows 실행은 하지 않았다. |
| source 관리 | task/lease/message 구조가 control-plane 설계에 직접 영향을 주므로 fixed-SHA submodule 유지 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| SQLite store | agent, message, task, lease persistence | CLI transaction → WAL DB → peer CLI | [open/schema](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L44-L107) |
| Message queue | unread 조회와 read 표시 | receive transaction 안에서 select + mark-read | [receive](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L330-L374) |
| Task lifecycle | create, ack, complete, requeue | conditional update + lease owner/status | [ack](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L624-L650), [complete/requeue](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L653-L718) |
| Session file | local agent/token continuity | file absent 시 backward-compatible 허용 | [session validation](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/session.rs#L47-L58) |

## 역할과 연동

- AgentRole: Collaborator, Task producer, Task assignee, Queue consumer
- Capability: `task-memory-queue`, `conditional-task-transition`, `local-message-bus`, `task-lease`
- Integration: native CLI, shared SQLite/WAL, shell/tmux launcher
- SecurityOperationalRequirement: host filesystem ACL, authenticated identity, durable delivery acknowledgement, lease fencing/reclaim, database backup

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `squad-shared-store` | architecture | agent/messages/tasks가 공유 SQLite DB에 저장되고 daemon은 필수가 아니다. | [current pin](https://github.com/mco-org/squad/commit/8146bcc1c38c439aedaf3ff44548c830654c8621), 2026-08-14 | [README](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/README.md#L1-L16), [schema](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L44-L107) | `I2` | `V2` | `W0` | pass(정적). host-local filesystem과 SQLite 동시성 경계를 넘지 않는다. |
| `squad-message-consume` | capability | receive는 unread select와 read 표시를 한 transaction에서 수행한다. | 동일 | [store.rs](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L330-L374) | `I2` | `V2` | `W0` | pass(정적). commit 후 출력 전 crash 시 소비됐으나 관찰되지 않은 메시지가 생길 수 있어 end-to-end ack가 아니다. |
| `squad-task-cas` | capability | ack/complete/requeue는 status·assignee·lease 조건과 affected-row 확인을 사용한다. | 동일 | [ack](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L624-L650), [requeue](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L681-L718) | `I2` | `V2` | `W0` | pass(정적, atomic-ish). 실제 concurrent claim/lease contention은 미검증이다. |
| `squad-session-fail-open` | limitation | local session file이 없으면 backward compatibility를 위해 validation이 성공한다. | 동일 | [session.rs](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/session.rs#L47-L58) | `I2` | `V2` | `W0` | confirmed limitation. 이 token을 사내 보안 인증으로 간주하면 fail-open이다. |
| `squad-windows-source` | platform | Windows command 처리와 Windows CI/release target 정의가 fixed source에 존재한다. | 동일 | [setup Windows branch](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/setup.rs#L422-L443), [CI matrix](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/.github/workflows/ci.yml#L12-L49), [release target](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/.github/workflows/release.yml#L77-L87) | `I2` | `V2` | `W1` | pass(좁은 source). upstream workflow 정의는 이 조사에서 실행한 증거가 아니며 shell smoke는 Windows에서 skip된다. |
| `squad-crlf-unknown` | limitation | fixed source에서 명시적 CRLF 계약/fixture를 확인하지 못했다. | 동일 | [line parser](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/setup.rs#L232-L246) | `I2` | `V2` | `W1` | unknown/보수적 결론. 일반 `lines()/trim()` 사용을 Windows CRLF 검증으로 승격하지 않는다. |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| CLI message | command → SQLite rows | sender → recipients, unread/read lifecycle | DB/file ACL와 session identity 의존 | [commands](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/README.md#L128-L140) |
| CLI task | create/ack/complete/requeue | producer ↔ assignee, 15-minute lease constant | conditional status/owner check; cryptographic auth 아님 | [lease/status](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L1-L13) |

## 운영·보안·trust boundary

- 공유 DB에 접근 가능한 host user/process가 핵심 authority다. session token은 `squad-session-fail-open` 때문에 security boundary가 아니다.
- message read marking과 실제 consumer 처리 증거를 분리하고, task lease에는 generation/fencing, heartbeat, reclaim audit를 추가해야 한다.
- static review에서 자동 heartbeat/reclaim runtime을 입증하지 못했다. 없음으로 단정하지 않고 `unknown`으로 둔다.
- 회사 업종, 데이터 분류, 규정, 승인, 망분리, cross-host DB 운영은 Decision Item이다.

## 플랫폼과 Windows

- Windows code branch와 upstream CI/release definitions가 있어 기본 결론은 `W1`이다.
- shell launcher smoke가 Windows에서 제외되고 CRLF-specific fixture가 없어 full native workflow 또는 CRLF correctness를 입증하지 못한다.
- build/runtime/E2E 미실행이므로 `W2/W3`은 부여하지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `squad-origin-static-20260814` | `I2/V2/W1` | `8146bcc1...` | gitlink/upstream/fixed source inspection; exit 0 | Windows/PowerShell, parent `984cac0...` | partial pass | 위 permalinks | 모든 Claim | local body/runtime 미사용 |
| `squad-v3plus-none` | `V3~V6/W2~W3` | 동일 | build/runtime/E2E/contention 미실행 | unknown | unknown | 없음 | 없음 | CI YAML을 실행 증거로 보지 않음 |

실행 기록: task/run `/root/implement_deep_collaboration_profiles`; profile `implement-deep` revision unknown; role `profile author`; model `OpenAI/gpt-5.6-sol`, exact build unknown; effort `high`; 시간·cost·latency unknown(2026-08-14 session); base/head `984cac0634b83d10af91d8e1814680816e67c53b`; artifact는 이 프로필뿐이다.

## 강점과 한계

- 강점: 작은 CLI/SQLite 모델 안에서 task와 message memory, conditional transition을 명시적으로 보여준다.
- 확인된 한계: `squad-session-fail-open`, receive-after-commit gap, host-local store trust가 사내 auth/durable delivery 요구를 충족하지 않는다.
- 미확인: 실제 multi-process contention, lease expiry/reclaim, crash recovery, Windows shell/tmux와 CRLF correctness는 unknown이다.

## AX 설계 재료

이 표는 최종 vendor selection이 아니라 사내 AX 설계 재료다. 회사 조건은 추정하지 않는다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | typed task/message memory와 conditional lifecycle | `squad-message-consume`, `squad-task-cas` | `AXN-TASK-OWNERSHIP` |
| Adapt | lease에 durable ack, consumer cursor, generation/fencing, heartbeat/reclaim 추가 | `squad-task-cas` | multi-executor·crash recovery 조건 |
| Avoid | absent-session 허용을 인증으로 사용하거나 local DB를 cross-host authoritative ledger로 사용 | `squad-session-fail-open`, `squad-shared-store` | fail-open 및 split-brain 방지 |
| Build | append-only event ledger, durable delivery ack, lease generation/reclaim audit, Windows/CRLF conformance | 모든 Claim | `AD-DURABLE-TASK-CLAIM` → `RM-TASK-LEASE-CONFORMANCE` (proposed) |

관계: `task-memory-queue` → `AXN-TASK-OWNERSHIP` → `AD-DURABLE-TASK-CLAIM` → `RM-TASK-LEASE-CONFORMANCE`; evidence는 fixed-SHA Claims/Evidence다.

## 도입 판단

- 결정: 참고/조건부 adapter 후보
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: task-memory queue와 conditional transition pattern
- 재검토 조건: `V3` Windows build, `V4` contention/crash/lease, `W2/W3` shell·process·CRLF 실행

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `squad-contention` | `squad-task-cas` | `V4` | isolated temp DB | N workers simultaneous ack/requeue/crash | single owner, fencing, deterministic recovery | DB snapshot/log | local runtime 승인 |
| `squad-windows-crlf` | `squad-windows-source`, `squad-crlf-unknown` | `W2/W3` | native Windows | build/test + CRLF fixtures + launcher lifecycle | exit 0, no parse drift, cleanup complete | test/log bundle | toolchain 설치 |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion PROVIDES task-memory-queue/conditional-task-transition`
- `Capability ADDRESSES AXNeed`
- `AXNeed DRIVES ArchitectureDecision`
- `ArchitectureDecision CREATES RoadmapItem`
- `RoadmapItem IMPLEMENTS Capability`

## 변경 이력

- 2026-08-14: official fixed-SHA source로 `I2/V2/W1` 작성. CRLF는 explicit evidence 부족을 fail-closed로 기록.
