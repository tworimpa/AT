---
id: tool-gastown
type: tool-profile
title: Gas Town
status: observed
profile_schema_version: 2
tool_key: gastown
tool_version_id: tool-version:gastown@649b832b7672bc7a2dbef26f5983aba6198b819b
tags:
  - knowledge-base
  - tool
  - orchestration
  - tmux
  - wsl
official_upstream: https://github.com/gastownhall/gastown
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 649b832b7672bc7a2dbef26f5983aba6198b819b
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 649b832b7672bc7a2dbef26f5983aba6198b819b
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Gas Town

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Gas Town은 Mayor/Deacon/Witness/Refinery/Polecat 역할, Beads/Dolt 작업 상태, git worktree와 tmux session을 결합해 여러 coding agent를 장기 조율하는 workspace orchestration reference다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/gastownhall/gastown` |
| 기본 브랜치와 조사일 HEAD | `main` / `649b832b7672bc7a2dbef26f5983aba6198b819b` (2026-08-14) |
| 고정 버전 | `649b832b7672bc7a2dbef26f5983aba6198b819b` |
| pin과 최신 관찰 관계 | 조사일 default-branch HEAD와 같음. repository `pushed_at`은 `2026-08-13T01:48:44Z`이나 latest release와 동일하다는 뜻은 아님 |
| 로컬 gitlink | [`multi-agent-tools/gastown`](../../multi-agent-tools/gastown/) |
| 유지보수 관찰 | GitHub metadata상 archived/disabled가 아님; activity observation일 뿐 지원·운영 보장 아님 |
| 출처 무결성 | `I2`: parent `.gitmodules`/gitlink와 official fixed commit/tree 대조 |
| license | fixed [`LICENSE`](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/LICENSE#L1-L21)의 MIT text와 GitHub SPDX metadata 일치 |
| provenance limitation | submodule 본문이 비어 official GitHub fixed-SHA blob/tree만 읽음. local build, tmux/WSL/runtime, agent E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Town/Rig role hierarchy | cross-rig coordination과 per-project workers/merge/watchdog 분리 | Mayor→rig→Polecat, Witness, Refinery | [core concepts](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L46-L104) |
| Beads/Dolt ledger | town/rig task, identity, mail과 work state 보존 | shared Dolt SQL server와 prefix routing | [two-level storage](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L5-L60), [transaction discipline](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L148-L173) |
| Worktree/tmux execution | worker workspace와 long-lived role session | mayor clone→polecat/refinery worktree→tmux role | [directory/worktree model](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L82-L146) |
| Monitoring/merge | Witness/Deacon/Dog health, Refinery merge queue | observed worker state→recovery/escalation/merge gate | [monitoring/refinery](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L86-L104) |

## 역할과 연동

- AgentRole: Coordinator(Mayor), Scheduler/Watchdog(Deacon/Witness), Worker(Polecat), Verifier/Merger(Refinery), Operator(Crew).
- Capability: `role-hierarchy`, `persistent-work-ledger`, `tmux-role-session`, `worktree-worker`, `merge-queue`, `capacity-governor`.
- Integration: CLI, git/worktree, tmux, Beads CLI, Dolt/MySQL protocol, agent runtime, ACP proxy components.
- SecurityOperationalRequirement: role authority enforcement, credential audience, durable lease/fencing, terminal provenance, merge approval, recovery and data retention을 별도 검증해야 한다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `gt-role-orchestration` | architecture | town/rig 범위에 coordinator, worker, watchdog, verifier/merge 역할을 분리한다. | [agent taxonomy](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L62-L80) | `I2` | `V2` | `W0` | pass(정적). 역할 설명이 실제 권한 강제를 증명하지 않음 |
| `gt-persistent-ledger` | capability | agent identity와 task/work state를 Beads/Dolt ledger로 보존한다. | [README](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L5-L16), [storage](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L148-L171) | `I2` | `V2` | `W0` | partial. crash consistency와 concurrent claim은 runtime 미검증 |
| `gt-worktree-tmux` | capability | polecat/refinery는 worktree, full-stack roles는 tmux session에 의존한다. | [worktree](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L120-L146), [tmux requirement](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L125-L137) | `I2` | `V2` | `W0` | partial. worktree/tmux는 sandbox가 아님 |
| `gt-refinery-merge` | capability | Refinery가 verification gate와 batch/bisect merge queue를 담당한다. | [README](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L94-L104), [design status](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L206-L235) | `I2` | `V2` | `W0` | partial. design 문서 자체에 단계별 in-progress/blocked가 있어 완성·runtime claim 금지 |
| `gt-native-windows-limit` | platform | native Windows는 minimal CLI-only로 안내되고 full tmux workflow는 WSL/Linux 환경을 요구한다. | [Windows install boundary](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/INSTALLING.md#L90-L102), [workspace boundary](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/INSTALLING.md#L149-L152) | `I2` | `V2` | `W0` | confirmed scope limit. 일부 Windows source/CI를 full native workflow로 승격하지 않음 |
| `gt-windows-components-not-proof` | limitation | Windows-specific ACP process code와 MSYS2 build CI가 있어도 tmux-backed orchestration의 native runtime evidence는 아니다. | [Windows ACP process](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/internal/acp/proxy_windows.go#L1-L47), [Windows CI](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/.github/workflows/windows-ci.yml#L12-L49) | `I2` | `V2` | `W0` | narrow component source only; current target인 full native workflow는 W0 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| `gt` CLI | process CLI + structured Beads operations | operator/agent→Town/Rig | shell identity와 stored credentials의 scope 별도 | [command concepts](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L46-L84) |
| Beads/Dolt | CLI + MySQL protocol | all roles→shared ledger | direct-main transaction discipline이 actor authorization을 대신하지 않음 | [Dolt flow](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/docs/design/architecture.md#L148-L173) |
| tmux | local terminal sessions | role supervisor↔agent panes | session attachment와 process rights는 host user boundary | [install requirement](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L125-L137) |
| ACP proxy component | process/stdin-stdout adapter | orchestrator↔agent runtime | process lifecycle code만 확인; auth/session E2E 없음 | [Windows adapter fragment](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/internal/acp/proxy_windows.go#L13-L47) |

## 운영·보안·trust boundary

- worktree, tmux, shared ledger, agent runtime credential과 merge queue는 서로 다른 trust boundary다. 동일 host user 아래 worktree/tmux는 hostile worker 격리가 아니다.
- Polecat self-managed completion은 throughput에 유리하지만 worker 자기보고를 verifier/merge authorization으로 쓰면 fail-open이다. independent evidence와 Refinery gate가 필요하다.
- Dolt transaction 원자성은 actor authorization, task generation fencing, duplicate external effect 방지를 자동 보장하지 않는다.
- UI/ledger status는 current git head, CI/review, approval과 observed-at를 함께 reconcile해야 한다.

## 플랫폼과 Windows

- 최종 등급은 `W0`. native Windows build fragments와 ACP process path는 있지만 공식 install boundary가 full tmux-backed workflow에 WSL/Linux를 요구한다.
- Windows-first AX baseline은 Gas Town 전체를 native dependency로 삼지 않고 role hierarchy와 ledger/merge patterns만 clean-room reference로 사용한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | 지원 Claim | limitation |
|---|---|---|---|---|---|---|---|
| `gt-origin-20260814` | `I2` | `649b832b7672bc7a2dbef26f5983aba6198b819b` | parent gitlink + official commit/tree/license metadata, exit 0 | Windows PowerShell 5.1; git 2.51.0.windows.1; gh 2.95.0 | pass | ToolVersion identity | local body 없음 |
| `gt-static-20260814` | `V2/W0` | same | official fixed README/docs/Go/CI 정적 검토, exit 0 | same | partial pass | 위 Claims | CI 실행 artifact를 수집하지 않음 |
| `gt-v3plus-none` | `V3~V6/W2~W3` | same | build/runtime/tmux/agent E2E 미실행 | unknown | unknown | 없음 | 실행 성공 claim 금지 |

수집 실행 기록: `run_id=implement-deep-orchestration-profiles-20260814`, `profile_id=implement-deep@1`, role=`Documenter`, provider=`OpenAI`, model slug=`gpt-5.6-sol`, model version=`unknown`, requested/actual effort=`high/high`, base/head=`984cac0634b83d10af91d8e1814680816e67c53b`, started_at=`not-captured`, ended_at=`2026-08-14T23:54:03+09:00`, cost/latency=`unknown`, external write=`none`.

## 강점과 한계

- 강점: 조직적 role hierarchy, persistent ledger, watchdog, merge queue를 한 workspace model로 연결한다.
- 한계: terminology와 운영 surface가 크고 role 설명과 enforced authority 사이에 별도 검증이 필요하다.
- 한계: full workflow는 tmux/Linux 중심이며 native Windows reference baseline으로 사용할 수 없다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | coordinator/worker/watchdog/verifier-merger 역할 분리와 two-level ledger | `gt-role-orchestration`, `gt-persistent-ledger` | `AX-N-ROLE-SEPARATION`, `AX-N-DURABLE-STATE` |
| Adapt | self-managed worker completion을 independent verifier와 merge approval 뒤 proposal로 제한 | `gt-refinery-merge` | 조직 승인·SCM 정책이 결정돼야 함 |
| Avoid | WSL/tmux full stack을 Windows native core로 채택하거나 shared ledger status를 proof로 사용 | `gt-native-windows-limit`, `gt-windows-components-not-proof` | Windows-first 및 evidence 분리 위반 |
| Build | native Windows control plane/executor, generation-fenced ownership, append-only evidence와 scoped committer | `gt-worktree-tmux`, `gt-refinery-merge` | `AD-WINDOWS-EXECUTOR` / `RM-CORE-CONTROL-PLANE` |

회사 업종, 데이터 분류, 규정, 승인 체계, 망분리, credential/merge authority는 모두 `unknown/decision-needed`다.

## 도입 판단

- 결정: 참고.
- 성격: 최종 vendor selection이 아니라 사내 AX role/state/merge governance 설계 재료.
- 적용 범위: role taxonomy, ledger, watchdog, merge queue의 clean-room pattern; full native Windows runtime baseline에서는 제외.
- 재검토 조건: 고정 ToolVersion 갱신, native Windows full-stack `W2`, crash/recovery/merge failure injection `V5`.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|
| `gt-v3-build` | fixed source | `V3` | pinned Go/MSYS2와 Linux build를 분리 | 각 환경 exit와 artifact hash 보존 | logs, toolchain, binary hashes | dependency/network approval |
| `gt-v5-ledger-recovery` | `gt-persistent-ledger` | `V5` | concurrent writes, daemon crash, stale worker, restart | lost/duplicate assignment 0 또는 명시 fail state | Dolt/event/git trace | isolated fixture |
| `gt-w2-native-scope` | `gt-native-windows-limit` | `W2` | native Windows CLI-only 범위와 WSL full workflow 분리 | 두 환경 artifact가 섞이지 않고 지원 matrix 확정 | Windows/WSL logs | Windows host + WSL |

## 관계와 변경 이력

- `ToolVersion PROVIDES role-hierarchy/persistent-work-ledger/worktree-worker/merge-queue`.
- `Capability ADDRESSES AXNeed AX-N-ROLE-SEPARATION/AX-N-DURABLE-STATE`.
- `ArchitectureDecision AD-WINDOWS-EXECUTOR AVOIDS gt-native-windows-limit`.
- 2026-08-14: `I2/V2/W0` fixed-SHA 프로필 작성. Windows component source와 full native workflow evidence를 분리하고 runtime 미검증을 보존.
