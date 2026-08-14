---
id: tool-taskplane
type: tool-profile
title: Taskplane
status: observed
profile_schema_version: 2
tool_key: taskplane
tool_version_id: tool-version:taskplane@504ee6888239c511d69cd36479abf4ccfabe253f
tags:
  - knowledge-base
  - tool
  - orchestration
  - dag
  - wave-lane
official_upstream: https://github.com/HenryLach/taskplane
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 504ee6888239c511d69cd36479abf4ccfabe253f
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 504ee6888239c511d69cd36479abf4ccfabe253f
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Taskplane

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Taskplane은 file-based task packet에서 dependency DAG를 만들고 순차 wave·병렬 lane·git worktree로 실행 계획을 구성하는 coding-agent batch planner/orchestrator다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/HenryLach/taskplane` |
| 기본 브랜치와 조사일 HEAD | `main` / `504ee6888239c511d69cd36479abf4ccfabe253f` (2026-08-14) |
| 고정 버전 | `504ee6888239c511d69cd36479abf4ccfabe253f` |
| pin과 최신 관찰 관계 | 조사일 default-branch HEAD와 같음. latest npm/release 여부는 확인하지 않았고 ToolVersion과 분리 |
| 로컬 gitlink | [`multi-agent-tools/taskplane`](../../multi-agent-tools/taskplane/) |
| 유지보수 관찰 | GitHub metadata상 archived/disabled가 아니며 `pushed_at=2026-07-18T14:12:28Z`; 운영 지원 보장은 아님 |
| 출처 무결성 | `I2`: parent `.gitmodules`와 mode `160000` gitlink, official fixed commit/tree 대조 |
| license | fixed [`LICENSE`](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/LICENSE#L1-L21)의 MIT text와 GitHub SPDX metadata 일치 |
| provenance limitation | submodule body가 비어 official GitHub fixed-SHA source만 검토. package install, Node/pi runtime, dashboard, agent E2E와 실제 Windows 실행 미수행 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Task packet | `PROMPT.md` mission/dependency와 `STATUS.md` progress를 durable context로 사용 | file packet→discovery/parser→DAG | [README](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L15-L31) |
| DAG/wave planner | dependency graph 검증과 topological waves 계산 | pending/completed task→validated DAG→wave sequence | [graph build/validation](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/waves.ts#L30-L88), [wave contract](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/waves.ts#L200-L210) |
| Lane allocator | affinity/round-robin/load strategy로 parallel slot 배치 | wave tasks→repo/file-scope grouping→lanes | [wave/lane model](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/docs/explanation/waves-lanes-and-worktrees.md#L55-L132) |
| Worktree/branch layer | batch/lane별 branch와 checkout 격리 | orch branch→lane worktrees→merge worktree | [path/branch model](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/worktree.ts#L28-L65), [batch paths](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/worktree.ts#L83-L175) |
| Lane runner | headless Node process가 worker loop와 status/mailbox snapshot 관리 | execution unit→agent host→STATUS/event/mailbox | [lane runner boundary](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/lane-runner.ts#L1-L54) |

## 역할과 연동

- AgentRole: Planner/Scheduler, Supervisor, Worker, Reviewer, Merger.
- Capability: `task-packet`, `dependency-dag`, `wave-scheduler`, `lane-affinity`, `worktree-isolation`, `file-mailbox`, `dashboard-projection`.
- Integration: pi extension/commands, CLI, Node process, git/worktree, file packets, mailbox files, SSE dashboard.
- SecurityOperationalRequirement: atomic task ownership, generation fencing, file-state locking, worker tool policy, verifier independence, merge approval and event provenance가 필요하다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `tp-task-packet` | capability | PROMPT/STATUS file pair를 task definition과 persistent progress store로 사용한다. | [README](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L15-L31) | `I2` | `V2` | `W0` | pass(정적). concurrent writer/atomic file persistence는 미검증 |
| `tp-dag-wave` | capability | dependency graph를 검증하고 Kahn-style wave로 순차 실행 순서를 계산한다. | [validation](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/waves.ts#L75-L198), [documented semantics](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/docs/explanation/waves-lanes-and-worktrees.md#L36-L67) | `I2` | `V2` | `W0` | pass(정적). 실제 scheduler/runtime 결과 없음 |
| `tp-lane-affinity` | capability | 동일 file scope task를 같은 lane에 두어 serialize하고 max lane 범위에서 병렬화한다. | [assignment strategies](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/docs/explanation/waves-lanes-and-worktrees.md#L86-L114) | `I2` | `V2` | `W0` | partial. declared file scope가 실제 dynamic write set을 완전히 예측하지 못함 |
| `tp-orch-branch-worktree` | architecture | user branch를 직접 수정하지 않고 batch orch branch와 lane worktree를 사용한다. | [branch model](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/docs/explanation/waves-lanes-and-worktrees.md#L136-L175), [worktree paths](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/worktree.ts#L111-L175) | `I2` | `V2` | `W0` | partial. worktree는 process/network/credential sandbox가 아님 |
| `tp-windows-narrow-source` | platform | Windows path normalization과 MAX_PATH cleanup fallback을 다루는 fixed source/test가 있다. | [path normalization](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/worktree.ts#L111-L150), [mocked Windows behavioral test](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/tests/windows-worktree-cleanup-behavioral.test.ts#L1-L42) | `I2` | `V2` | `W1` | narrow static evidence. 실제 Windows host 실행이 아니며 W2/W3 아님 |
| `tp-derived-progress-limit` | limitation | STATUS/dashboard/worker completion은 file/event projection이며 commit·test·approval의 독립 proof가 아니다. | [runner responsibility](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/lane-runner.ts#L1-L15), [README claims](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L33-L42) | `I2` | `V2` | `W0` | confirmed evidence boundary; runtime success unknown |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| pi commands | extension command surface | operator/supervisor→planner/runtime | pi session authority와 repo credential에 의존 | [commands](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L134-L180) |
| task packet | Markdown files | planner/worker/reviewer↔durable state | filesystem write race와 provenance를 별도 통제 | [task definition](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L27-L31) |
| lane runner | child process + file/mailbox event | scheduler→worker/reviewer | tool allowlist와 process credential enforcement 미검증 | [runner imports/responsibility](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/extensions/taskplane/lane-runner.ts#L1-L54) |
| dashboard | local HTTP/SSE | persisted/runtime projection→human | observation surface이며 approval authority가 아님 | [dashboard claim](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md#L33-L42) |

## 운영·보안·trust boundary

- task packet은 이해하기 쉽지만 multi-writer update, partial write, stale resume에 대한 atomicity/generation fencing이 별도 필요하다.
- file-scope affinity는 merge-conflict heuristic이다. undeclared/generated files, repo metadata와 external side effects를 보호하지 않는다.
- worker, reviewer, merger가 논리적으로 분리돼도 credential과 process sandbox가 같다면 enforced separation of duties가 아니다.
- batch status와 dashboard 표시는 source head, last event cursor, verifier result, approval을 함께 보존해야 fail-closed다.

## 플랫폼과 Windows

- `W1`은 `path.resolve` 사용과 Windows MAX_PATH cleanup branch/test의 좁은 static evidence다.
- 해당 test는 process/platform을 mock한다. 이 조사에서 Windows runtime을 실행하지 않았으므로 `W2/W3`로 승격하지 않는다.
- ConPTY process tree, Ctrl+C/cancel, CRLF, long path, antivirus/file locking, simultaneous git worktree cleanup은 향후 Windows suite 대상이다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | 지원 Claim | limitation |
|---|---|---|---|---|---|---|---|
| `tp-origin-20260814` | `I2` | `504ee6888239c511d69cd36479abf4ccfabe253f` | parent gitlink + official GitHub metadata/tree, exit 0 | Windows PowerShell 5.1; git 2.51.0.windows.1; gh 2.95.0 | pass | ToolVersion identity | local body 없음 |
| `tp-static-20260814` | `V2/W1` | same | official fixed README/docs/TypeScript/test 정적 검토, exit 0 | same | partial pass | 위 Claims | test 파일을 읽었을 뿐 실행하지 않음 |
| `tp-v3plus-none` | `V3~V6/W2~W3` | same | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 실행 성공 claim 없음 |

수집 실행 기록: `run_id=implement-deep-orchestration-profiles-20260814`, `profile_id=implement-deep@1`, role=`Documenter`, provider=`OpenAI`, model slug=`gpt-5.6-sol`, model version=`unknown`, requested/actual effort=`high/high`, base/head=`984cac0634b83d10af91d8e1814680816e67c53b`, started_at=`not-captured`, ended_at=`2026-08-14T23:54:03+09:00`, cost/latency=`unknown`, external write=`none`.

## 강점과 한계

- 강점: dependency graph를 wave와 lane이라는 설명 가능한 scheduling model로 낮추고 worktree branch lifecycle과 연결한다.
- 강점: file-based task packet은 사람 review와 context handoff에 유리하다.
- 한계: affinity는 heuristic이고 file state/dashboard는 completion evidence가 아니다.
- 한계: Windows evidence는 cleanup/path의 좁은 static branch뿐이다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | validated DAG→sequential waves→bounded lanes 계획과 dry-run 설명 가능성 | `tp-dag-wave`, `tp-lane-affinity` | `AX-N-EXPLAINABLE-SCHEDULING` |
| Adapt | Markdown task packet을 versioned spec + append-only event/evidence projection으로 변형 | `tp-task-packet`, `tp-derived-progress-limit` | 감사·동시성·retention 결정 필요 |
| Avoid | declared file scope만으로 충돌 없음 또는 sandbox를 보장 | `tp-lane-affinity`, `tp-orch-branch-worktree` | fail-open merge와 credential leakage 위험 |
| Build | Windows-native executor, atomic claim/lease/generation, actual write-set conflict detector와 independent verifier | `tp-windows-narrow-source`, `tp-derived-progress-limit` | `AD-WINDOWS-EXECUTOR` / `RM-SCHEDULER-FENCING` |

회사 업종, 데이터 분류, 규정, 승인자, 망분리와 보존 정책은 `unknown/decision-needed`다.

## 도입 판단

- 결정: 참고/파일럿 후보.
- 성격: final vendor selection이 아니라 AX scheduler/task-contract 설계 재료.
- 적용 범위: wave/lane planning과 task packet; Windows executor 및 enforced governance는 자체 구현/검증.
- 재검토 조건: pinned build `V3`, controlled batch `V4`, crash/merge/race `V5`, Windows lifecycle `W2/W3`.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|
| `tp-v3-planner` | `tp-dag-wave` | `V3` | fixed Node/pi deps, graph fixtures | deterministic plan hash와 exit 0 | env, lock hash, plan/log | network/dependency approval |
| `tp-v5-race` | task packet/lanes | `V5` | two workers, stale resume, undeclared write, merge conflict | duplicate ownership 0; fail-closed conflict | event/file/git trace | isolated repos |
| `tp-w2-windows` | `tp-windows-narrow-source` | `W2` | native Windows worktree create/remove/cancel | long-path cleanup과 process tree 종료 관찰 | Windows logs, fs/git snapshot | Windows test host |

## 관계와 변경 이력

- `ToolVersion PROVIDES task-packet/dependency-dag/wave-scheduler/lane-affinity`.
- `Capability ADDRESSES AXNeed AX-N-EXPLAINABLE-SCHEDULING`.
- `ArchitectureDecision AD-WINDOWS-EXECUTOR ADAPTS tp-windows-narrow-source`.
- 2026-08-14: `I2/V2/W1` fixed-SHA 프로필 작성. Windows static source와 actual runtime을 분리하고 build/runtime/E2E 미수행을 보존.
