---
id: tool-buzz
type: tool-profile
title: Buzz
status: observed
profile_schema_version: 2
tool_key: buzz
tool_version_id: tool-version:buzz@8abc2baf0b71844fc4ff7222aab5027c862b7d1f
tags:
  - knowledge-base
  - tool
  - collaboration
  - signed-event
  - relay
official_upstream: https://github.com/block/buzz
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 8b8445f5ef3338c58825194ebc008b98111a0962
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 8abc2baf0b71844fc4ff7222aab5027c862b7d1f
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-14
---

# Buzz

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Buzz는 사람과 에이전트가 키 기반 신원으로 서명된 이벤트를 relay에 게시하고 채널·작업·검토 맥락을 공유하는 협업 control surface다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/block/buzz` |
| 기본 브랜치와 조사일 HEAD | `main` / [`8b8445f5ef3338c58825194ebc008b98111a0962`](https://github.com/block/buzz/commit/8b8445f5ef3338c58825194ebc008b98111a0962) (2026-08-14) |
| 고정 버전 | `8abc2baf0b71844fc4ff7222aab5027c862b7d1f` |
| pin과 최신 관찰 관계 | 조사 시 `main`이 18 commits ahead, pin은 behind 0인 선조 관계. 이 프로필은 자동 갱신하지 않는다. |
| 로컬 gitlink | [`multi-agent-tools/buzz`](../../multi-agent-tools/buzz/) |
| 출처 무결성 | `I2`: parent `.gitmodules` 공식 URL과 `git ls-tree` gitlink SHA 일치, official fixed-SHA tree/blob 교차 확인 |
| license | fixed SHA [`LICENSE`](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/LICENSE#L1-L12)의 Apache-2.0과 GitHub metadata가 일치한다. 의존성 license는 별도 검토 대상이다. |
| provenance limitation | 병렬 조사 통합 worktree에서는 submodule body가 비어 있어 parent gitlink와 official GitHub fixed-SHA tree/metadata로 `V2`를 수집했다. local body build, relay/desktop runtime, agent E2E는 실행하지 않았다. |
| source 관리 | 설계의 signed-event envelope와 relay adapter에 직접 영향을 주므로 fixed-SHA submodule 유지 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| CLI client | event 구성·서명·publish, relay `OK` 응답 처리 | local key → signed event → WebSocket relay | [서명](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-cli/src/client.rs#L583-L605), [publish/OK](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-cli/src/client.rs#L1070-L1095) |
| Relay event handler | 인증, channel visibility, 저장, fan-out | authenticated event → policy/filter → durable accept → best-effort downstream | [인증 거부](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L608-L665), [accept 의미](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L338-L346) |
| Membership/visibility filter | private channel 수신자 축소 | lookup 실패 시 recipient 없음 | [private filter](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L99-L115), [lookup failure](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L194-L220) |
| Desktop managed-agent runtime | 설치와 child-process lifecycle | Windows installer → process/job cleanup | [installer](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/desktop/src-tauri/src/managed_agents/discovery/windows_install.rs#L25-L78), [process lifecycle](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/desktop/src-tauri/src/managed_agents/process_lifecycle.rs#L17-L60) |

## 역할과 연동

- AgentRole: Human collaborator, Agent identity, Relay operator, Review participant
- Capability: `signed-collaboration-event`, `relay-publish-ack`, `channel-membership-filter`, `auditable-identity`
- Integration: CLI, WebSocket relay, signed event log, desktop/Tauri managed-agent process
- SecurityOperationalRequirement: signing key custody, authenticated relay connection, explicit membership enforcement, delivery/replay evidence, external-write approval

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `buzz-signed-event` | capability | client는 event에 auth tag를 넣고 local key로 서명한다. | [current upstream](https://github.com/block/buzz/commit/8b8445f5ef3338c58825194ebc008b98111a0962), 2026-08-14 | [client.rs](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-cli/src/client.rs#L583-L605) | `I2` | `V2` | `W0` | pass(정적). 서명은 무결성·키 소유 증거이지 업무 권한·내용 기밀성·업무 완료 증거가 아니다. |
| `buzz-accepted-boundary` | interface | publish의 `accepted:true`는 relay가 해당 event를 durable accepted 했다는 범위다. | 동일 | [client OK](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-cli/src/client.rs#L1070-L1095), [relay semantics](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L338-L346) | `I2` | `V2` | `W0` | pass(정적). recipient delivery, Redis fan-out, workflow trigger, 상대의 실제 조치는 증명하지 않는다. |
| `buzz-private-fail-closed` | security | private visibility lookup 실패 시 수신자를 만들지 않는 경로가 있다. | 동일 | [visibility failure](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L194-L220) | `I2` | `V2` | `W0` | pass(정적, fail-closed path). 전체 배포 구성의 기밀성 보장은 아니다. |
| `buzz-membership-default` | limitation | auth token, pubkey allowlist, relay membership enforcement 기본값이 비활성인 구성 경로가 있다. | 동일 | [config defaults](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/config.rs#L582-L607), [membership default test](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/config.rs#L1118-L1137) | `I2` | `V2` | `W0` | confirmed limitation. 사내 배포는 명시적 fail-closed policy와 startup assertion이 필요하다. |
| `buzz-windows-source` | platform | Windows 전용 설치 및 Job Object/process-tree 종료 경로가 존재한다. | 동일 | [Windows install](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/desktop/src-tauri/src/managed_agents/discovery/windows_install.rs#L100-L160), [Job Object/fallback](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/desktop/src-tauri/src/managed_agents/process_lifecycle.rs#L108-L157) | `I2` | `V2` | `W1` | pass(좁은 source). Job assignment race/fallback가 있고 Windows build/runtime/E2E 미실행이므로 `W2/W3` 아님. |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| CLI publish | WebSocket, signed event/NIP-style `OK` | client → relay, event 단위 | key signature + connection auth; channel 권한은 별도 | [publish](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-cli/src/client.rs#L1070-L1095) |
| Relay ingest/fan-out | signed event + persistent store + subscriber fan-out | producer → relay → permitted recipients | unauthenticated/pubkey mismatch reject; membership은 구성 의존 | [auth](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/crates/buzz-relay/src/handlers/event.rs#L608-L665) |

## 운영·보안·trust boundary

- 보호 자산은 signing key, channel membership, event body, relay store, workflow/external-write authority다. signed event와 실제 승인 주체를 분리해야 한다.
- relay accept와 downstream delivery를 분리하고, subscriber cursor·replay·freshness를 evidence layer가 기록해야 한다.
- private recipient lookup은 fail-closed이나 enforcement 기본값은 fail-open 쪽이므로, 사내 adapter는 보안 옵션 미설정 시 시작 자체를 거부해야 한다.
- 회사 업종, 데이터 분류, 규정, 승인 체계, 망분리/relay 배치 방식은 `unknown` Decision Item이다.

## 플랫폼과 Windows

- `buzz-windows-source`가 설치 및 process lifecycle의 좁은 `W1` 근거다.
- process Job assignment와 fallback의 race는 source에 드러난 한계이며 native Windows 실제 종료·잔존 child 검증은 하지 않았다.
- desktop host와 relay server, managed agent guest를 분리해 평가해야 하며 Windows source 존재를 전체 native workflow 지원으로 확대하지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `buzz-origin-static-20260814` | `I2/V2/W1` | `8abc2baf...` | parent `git ls-tree`, `.gitmodules`, official GitHub fixed-SHA source/metadata inspection; exit 0 | Windows/PowerShell, parent `984cac0...` | pass/partial | 위 immutable links | 모든 Claim | 통합 조사 worktree local body 미사용, 실행 없음 |
| `buzz-v3plus-none` | `V3~V6/W2~W3` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

실행 기록: task/run `/root/implement_deep_collaboration_profiles`; profile `implement-deep` (revision unknown); role `profile author`; model provider `OpenAI`, slug `gpt-5.6-sol`, exact build/version unknown; effort `high`; 시작·종료 시각은 미계측(2026-08-14 session); base/head `984cac0634b83d10af91d8e1814680816e67c53b`; cost/latency unknown; 변경 artifact는 이 프로필뿐이다.

## 강점과 한계

- 강점: `buzz-signed-event`는 사람/에이전트의 이벤트 출처를 일관된 envelope로 연결하고 `buzz-accepted-boundary`는 relay acceptance를 좁게 구분한다.
- 확인된 한계: `buzz-membership-default` 때문에 secure-by-configuration이 필요하며 accepted/signature를 authorization 또는 delivery로 오독하면 fail-open이 된다.
- 미확인·추론: relay 장애 replay, key rotation/revocation, 다중 relay ordering, Windows process cleanup, 실제 recipient delivery는 unknown이다.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계는 추정하지 않는다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | canonical signed event envelope와 relay acceptance receipt | `buzz-signed-event`, `buzz-accepted-boundary` | `AXN-COLLAB-AUDIT` |
| Adapt | relay를 선택적 collaboration adapter로 두고 identity를 사내 IAM/승인 주체에 매핑 | `buzz-private-fail-closed`, `buzz-membership-default` | 명시적 membership, key custody, 망분리 결정 필요 |
| Avoid | signature=authorization, accepted=delivered/completed, relay=필수 control-plane kernel로 해석 | `buzz-accepted-boundary`, `buzz-membership-default` | 근거 범위 초과와 fail-open 방지 |
| Build | local evidence ledger, policy gate, offline queue/replay/cursor, freshness, secret/key broker | 모든 Claim | `AD-COLLAB-EVIDENCE-SEPARATION` → `RM-COLLAB-REPLAY-POLICY` (proposed) |

관계: `signed-collaboration-event` → `AXN-COLLAB-AUDIT` → `AD-COLLAB-EVIDENCE-SEPARATION` → `RM-COLLAB-REPLAY-POLICY`; evidence source는 위 fixed-SHA Claim과 Evidence ID다.

## 도입 판단

- 결정: 참고/제한적 파일럿 후보
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: signed collaboration envelope와 relay adapter의 clean-room/reference pattern
- 재검토 조건: fixed ToolVersion 갱신, license/identity 변화, `V3` build, relay failure/replay `V4/V5`, Windows `W2/W3`

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `buzz-relay-runtime` | `buzz-accepted-boundary`, `buzz-private-fail-closed` | `V4` | 격리된 relay+2 clients | publish, disconnect, lookup failure, replay | acceptance/delivery/cursor가 분리되고 unauthorized recipient 0 | event/relay logs | network/key test 승인 |
| `buzz-windows-lifecycle` | `buzz-windows-source` | `W2/W3` | native Windows | install/spawn/kill/crash/reboot | child 잔존 0, exit/cleanup evidence 보존 | ETW/process/log bundle | installer 실행 승인 |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion PROVIDES signed-collaboration-event/relay-publish-ack`
- `Capability ADDRESSES AXNeed`
- `AXNeed DRIVES ArchitectureDecision`
- `ArchitectureDecision CREATES RoadmapItem`
- `RoadmapItem IMPLEMENTS Capability`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA 근거로 `I2/V2/W1` 프로필 작성. build/runtime/E2E와 Windows 실행은 미수행.
