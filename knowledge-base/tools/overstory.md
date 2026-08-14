---
id: tool-overstory
type: tool-profile
title: Overstory
status: observed
profile_schema_version: 2
tool_key: overstory
tool_version_id: tool-version:overstory@ff38f3f76f084abcc34f519bcaa69580f6e53cf1
tags:
  - knowledge-base
  - tool
  - orchestration
  - archived
  - reference-only
official_upstream: https://github.com/jayminwest/overstory
license: MIT
maintenance_status: archived
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: ff38f3f76f084abcc34f519bcaa69580f6e53cf1
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: ff38f3f76f084abcc34f519bcaa69580f6e53cf1
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Overstory

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Overstory는 worktree, SQLite mail, runtime adapters와 coordinator/worker/reviewer/merger 역할을 결합했던 multi-agent orchestration reference지만, 공식 archived/EOL 상태이므로 신규 advanced baseline에서 제외한다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/jayminwest/overstory` |
| 기본 브랜치와 조사일 HEAD | `main` / `ff38f3f76f084abcc34f519bcaa69580f6e53cf1` (2026-08-14) |
| 고정 버전 | `ff38f3f76f084abcc34f519bcaa69580f6e53cf1` |
| pin과 최신 관찰 관계 | archived repository의 조사일 HEAD와 같음. active successor는 공식 README가 Warren을 가리키지만 이 ToolVersion에 소급하지 않음 |
| 로컬 gitlink | [`multi-agent-tools/overstory`](../../multi-agent-tools/overstory/) |
| 유지보수 관찰 | GitHub `archived=true`; README가 “No longer maintained”와 read-only를 명시 |
| 출처 무결성 | `I2`: parent gitlink와 official fixed commit/tree 대조 |
| license | fixed [`LICENSE`](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/LICENSE#L1-L21)의 MIT text와 package/GitHub metadata 일치 |
| provenance limitation | local body가 비어 official fixed-SHA tree/blob만 읽음. Bun install/build/test, agent runtime, tmux/WSL2, merge/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Role hierarchy | orchestrator→coordinator→lead/workers 역할 분리 | task/objective→delegation→review/merge | [roles](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L219-L242) |
| Worktree/session layer | agent별 branch/worktree와 headless/tmux session | sling→worktree→runtime→merge | [architecture](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L195-L217), [worktree validation](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/manager.ts#L38-L119) |
| Runtime adapters | agent CLI별 spawn/guard/readiness/transcript 변환 | runtime registry→adapter→process/events | [adapter matrix](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L199-L217) |
| SQLite mail/merge/watchdog | typed inter-agent messages, FIFO merge, liveness | agent events/mail→coordination→merge/recovery | [key architecture](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L244-L254) |
| Agent manifest | model/tools/capability/canSpawn/constraints validation | JSON manifest→validated role definitions→capability index | [manifest validation](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/agents/manifest.ts#L58-L135) |

## 역할과 연동

- AgentRole: Orchestrator, Coordinator, Supervisor/Lead, Scout, Builder, Reviewer, Merger, Monitor.
- Capability: `role-manifest`, `runtime-adapter`, `worktree-worker`, `typed-agent-mail`, `merge-queue`, `watchdog`, `headless-event-stream`.
- Integration: Bun CLI, agent CLIs, git/worktree, SQLite, headless process/NDJSON, tmux, HTTP/WebSocket UI.
- SecurityOperationalRequirement: supported-maintainer gate, runtime guard coverage, atomic claim/lease, credential/network sandbox, merge approval와 evidence provenance가 필요하다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `ov-archived-eol` | limitation | 공식 repository는 archived/read-only이며 더 이상 유지되지 않는다. | [README notice](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L1-L13) | `I2` | `V2` | `W0` | confirmed. 신규 production/advanced baseline 제외 |
| `ov-role-manifest` | capability | manifest가 agent tools/capabilities/canSpawn/constraints를 검증하고 capability index를 만든다. | [field validation](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/agents/manifest.ts#L58-L135), [file validation](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/agents/manifest.ts#L175-L219) | `I2` | `V2` | `W0` | pass(정적). declarations가 runtime enforcement를 자동 증명하지 않음 |
| `ov-worktree-validation` | capability | worktree 생성 후 git registration과 tracked file 존재를 검증하고 실패 시 rollback한다. | [create/validate](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/manager.ts#L38-L119), [best-effort rollback](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/manager.ts#L121-L155) | `I2` | `V2` | `W0` | partial. rollback은 best-effort이고 sandbox가 아님 |
| `ov-runtime-guards-vary` | security | runtime별 guard가 hooks/extensions/OS sandbox/approval 또는 none으로 달라 동일 보안 contract가 아니다. | [adapter matrix](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L199-L217) | `I2` | `V2` | `W0` | confirmed design risk; several adapters explicitly `none`/allow-all/yolo |
| `ov-typed-mail-merge-watchdog` | architecture | SQLite typed mail, FIFO merge, tiered watchdog를 한 orchestration model로 둔다. | [architecture](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L244-L254) | `I2` | `V2` | `W0` | static design only; concurrency/recovery/merge E2E 없음 |
| `ov-wsl2-posix-path` | platform | tmux path가 `which`, `/bin/bash`, `export/unset`, `$PATH`에 의존하고 WSL2 race retry만 명시한다. | [POSIX shell path](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/tmux.ts#L45-L85), [bash/WSL2 path](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/tmux.ts#L123-L181) | `I2` | `V2` | `W0` | WSL2-oriented source뿐이며 native Windows implementation/evidence 없음 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| `ov` CLI | Bun process CLI/JSON | human/coordinator/worker→local orchestration | host user credential와 runtime guard에 의존 | [commands](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L92-L193) |
| SQLite mail | typed local messages | agents↔coordinator/watchdog | actor identity와 delivery atomicity runtime 미검증 | [messaging design](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L244-L252) |
| headless process | Bun.spawn + NDJSON/stdin | runtime adapter↔agent child | full env 전달; credential audience 별도 통제 | [headless process](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/process.ts#L76-L130) |
| tmux | CLI + bash wrapper | coordinator/operator↔agent pane | POSIX/WSL host process boundary | [tmux create](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/src/worktree/tmux.ts#L106-L181) |

## 운영·보안·trust boundary

- archived/EOL은 단순 activity score가 아니라 patch, dependency, vulnerability와 agent runtime drift를 받을 owner가 없다는 governance risk다.
- runtime guard matrix에 `none`, `--allow-all-tools`, `--yolo`가 포함돼 있으므로 role의 read-only 선언을 공통 enforcement로 간주하면 fail-open이다.
- worktree validation은 filesystem correctness에 유용하지만 process, credential, network, external write 격리가 아니다.
- agent mail/status/merge queue는 derived state이며 independent verifier, git head, CI, approval evidence가 필요하다.

## 플랫폼과 Windows

- `W0`: fixed source는 POSIX shell/tmux와 WSL2 race 대응만 확인된다. native Windows ConPTY/Job Object/process cleanup implementation과 실행 evidence가 없다.
- archived 도구에 Windows port를 새로 의존시키지 않는다. 필요한 patterns는 clean-room으로 가져오고 active maintained components로 구현한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | 지원 Claim | limitation |
|---|---|---|---|---|---|---|---|
| `ov-origin-20260814` | `I2` | `ff38f3f76f084abcc34f519bcaa69580f6e53cf1` | parent gitlink + official GitHub archived/tree/license metadata, exit 0 | Windows PowerShell 5.1; git 2.51.0.windows.1; gh 2.95.0 | pass | ToolVersion/archived identity | local body 없음 |
| `ov-static-20260814` | `V2/W0` | same | official fixed README/TypeScript/package/license 정적 검토, exit 0 | same | partial pass | 위 Claims | WSL2/runtime 실행 없음 |
| `ov-v3plus-none` | `V3~V6/W2~W3` | same | build/runtime/E2E 미실행 | unknown | unknown | 없음 | archived CI badge를 실행 증거로 사용하지 않음 |

수집 실행 기록: `run_id=implement-deep-orchestration-profiles-20260814`, `profile_id=implement-deep@1`, role=`Documenter`, provider=`OpenAI`, model slug=`gpt-5.6-sol`, model version=`unknown`, requested/actual effort=`high/high`, base/head=`984cac0634b83d10af91d8e1814680816e67c53b`, started_at=`not-captured`, ended_at=`2026-08-14T23:54:03+09:00`, cost/latency=`unknown`, external write=`none`.

## 강점과 한계

- 강점: role manifest, runtime adapter, typed mail, worktree validation과 watchdog/merge patterns가 밀도 높은 historical reference다.
- 한계: archived/EOL이고 runtime guard strength가 adapter별로 다르다.
- 한계: Windows는 WSL2/POSIX 경로뿐이며 build/runtime/E2E를 검증하지 않았다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | role manifest validation, runtime adapter capability declaration, worktree post-create validation/rollback | `ov-role-manifest`, `ov-worktree-validation` | `AX-N-ROLE-CONTRACT`, `AX-N-ADAPTER-CONFORMANCE` |
| Adapt | typed mail/watchdog/merge를 durable event log, generation fencing, verifier evidence로 재설계 | `ov-typed-mail-merge-watchdog` | Windows/사내 감사·보존 규칙 필요 |
| Avoid | archived dependency를 advanced baseline으로 채택하거나 `none/yolo/allow-all` adapter를 동일 read-only policy로 취급 | `ov-archived-eol`, `ov-runtime-guards-vary` | maintenance와 fail-closed 위반 |
| Build | maintained Windows-native executor/adapter conformance suite와 central policy/evidence layer | `ov-wsl2-posix-path`, `ov-runtime-guards-vary` | `AD-ACTIVE-BASELINE`, `RM-ADAPTER-CONFORMANCE` |

회사 업종, 데이터 분류, 규정, 승인자, 망분리, agent runtime allowlist는 `unknown/decision-needed`다.

## 도입 판단

- 결정: 역사/reference only.
- 성격: final vendor selection이 아니라 사내 AX 설계를 위한 historical pattern과 anti-pattern 재료.
- 적용 범위: clean-room role/adapter/worktree/mail patterns. 신규 advanced baseline, production dependency, Windows runtime 후보에서는 제외.
- 재검토 조건: 공식 unarchive와 maintenance owner 복귀가 없는 한 도입 판단은 유지; successor 평가는 별도 Warren ToolVersion에서 수행.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|
| `ov-reference-extract` | Borrow patterns | `V2` | active AX design과 contract crosswalk | source/claim/decision trace 완성 | mapping document | runtime 없음 |
| `ov-runtime-none` | archived product | 없음 | 제품 runtime 검증은 기본 계획에서 제외 | 별도 사람 결정 전 실행하지 않음 | decision log | EOL risk acceptance 필요 |
| `ov-successor-check` | `ov-archived-eol` | `V2+` | Warren fixed/current ToolVersion 별도 검토 | successor claim을 Overstory에 소급하지 않음 | Warren profile/evidence | separate profile |

## 관계와 변경 이력

- `ToolVersion PROVIDES historical role-manifest/runtime-adapter/worktree-validation patterns`.
- `Project EVALUATES ToolVersion AS reference-only`.
- `ArchitectureDecision AD-ACTIVE-BASELINE AVOIDS ov-archived-eol`.
- 2026-08-14: `I2/V2/W0` profile 작성. MIT/archived/EOL, WSL2/POSIX-only static path, advanced baseline 제외와 runtime 미검증을 보존.
