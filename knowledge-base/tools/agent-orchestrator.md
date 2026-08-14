---
id: tool-agent-orchestrator
type: tool-profile
title: Agent Orchestrator
status: observed
tags:
  - knowledge-base
  - tool
  - daemon
  - desktop
  - worktree
  - status-projection
official_upstream: https://github.com/Untrivial-ai/agent-orchestrator
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Agent Orchestrator

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Agent Orchestrator(AO)는 coding-agent worker, branch/worktree, terminal, PR·CI·review fact를 local daemon에 모으고 desktop Kanban과 orchestrator conversation으로 계획·위임·감독하는 control plane이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/Untrivial-ai/agent-orchestrator` |
| 기본 브랜치와 고정 버전 | `main` · `12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3` |
| 로컬 gitlink | [`multi-agent-tools/agent-orchestrator`](../../multi-agent-tools/agent-orchestrator/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 현재 upstream 관찰 | GitHub `main`은 조사 시 `452743579207829b63720ad25746c368ecc74532`로 고정 버전보다 앞서 있었다. archived/disabled가 아니고 같은 날 push가 관찰됐다. |
| 출처 무결성 | `I2`: parent [`.gitmodules`](../../.gitmodules) URL과 `git ls-tree` gitlink SHA, official fixed-SHA GitHub tree/blob를 대조했다. |
| license | fixed SHA root [`LICENSE`](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/LICENSE#L1-L5)의 Apache-2.0 text와 GitHub metadata가 일치한다. |

## 기술 구조

- Go local daemon이 loopback HTTP, SQLite durable store, change-data-capture fan-out, agent runtime, terminal manager, SCM/review service와 lifecycle wiring을 소유한다.
- Electron/React desktop이 daemon status와 event/API surface를 읽어 session별 task, terminal, changed files, PR, CI, review를 Kanban에 투영한다.
- Windows build-tagged runtime은 detached ConPTY host와 per-instance named pipe supervisor 경로를 별도로 구현한다.
- worker는 task+agent+workspace 실행 단위이고 Git-backed worker에는 branch/worktree가 연결된다. project orchestrator는 별도 persistent planning/coordination conversation이다.
- display status는 agent activity signal과 stored PR facts에서 파생된다. source signal이 끊기거나 daemon downtime reconciliation이 실패하면 stale/unknown을 보존해야 한다.

## 역할과 연동

- AgentRole: Planner/Orchestrator, Worker supervisor, Worktree manager, Human control surface, Review feedback relay
- Capability: `project-orchestration`, `worker-session`, `worktree-isolation`, `terminal-supervision`, `derived-kanban-status`, `pr-ci-review-projection`, `feedback-loop`
- Integration: local daemon HTTP/events, SQLite/CDC, Electron desktop, native TUI/structured chat, Git/GitHub, terminal runtime, mobile
- SecurityOperationalRequirement: loopback daemon authority, browser runtime token, per-worker workspace/process isolation, PR/CI/review freshness, human approval before commit/merge/external write

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `ao-daemon-desktop` | local daemon이 durable store·CDC·terminal/runtime/service를 구성하고 desktop이 이를 operational workspace로 표시한다. | [README architecture](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L29-L35), [daemon package](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/daemon/daemon.go#L1-L50), [store/CDC startup](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/daemon/daemon.go#L98-L105) | `V2` | `W0` | pass(정적). daemon/desktop runtime은 미실행 |
| `ao-worker-worktree` | worker가 task, agent, isolated workspace를 묶고 Git-backed work에는 branch/worktree를 연결한다. | [worker model](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L39-L44), [workflow isolation](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L70-L78) | `V2` | `W0` | pass(정적). worktree는 OS sandbox나 merge collision 방지 보장이 아님 |
| `ao-project-orchestrator` | project-scoped persistent orchestrator가 계획·위임을 맡고 worker가 구현·test·commit·PR을 맡는 역할 분리를 문서화한다. | [orchestrator model](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L47-L54) | `V2` | `W0` | pass(정적 문서+구조). 실제 역할 권한 강제와 task DAG correctness는 미검증 |
| `ao-derived-kanban-status` | Kanban 위치는 session, PR, CI, review fact로부터 파생되며 working/needs-you/in-review/ready-to-merge를 표시한다. | [derived board semantics](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L57-L66), [status derivation](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/service/session/status.go#L10-L30) | `V2` | `W0` | pass(정적). UI card는 underlying provider fact의 freshness/proof가 아님 |
| `ao-pr-fact-snapshot` | stored PR fact에는 CI, review, mergeability, comments, head SHA와 update time이 포함되며 display status는 snapshot을 사용한다. | [PR fact store](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/storage/sqlite/store/pr_facts.go#L13-L53) | `V2` | `W0` | pass(정적). provider API 지연·webhook loss·head drift에서 stale할 수 있음 |
| `ao-freshness-fail-closed` | silent session은 grace 뒤 `no_signal`로 낮추지만, daemon downtime reconciliation 실패는 stale notification row를 남길 수 있다. | [no-signal rule](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/service/session/status.go#L10-L25), [best-effort reconcile limitation](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/daemon/daemon.go#L155-L160) | `V2` | `W0` | partial. status마다 observed-at/source-head를 노출하고 commit/CI/review를 직접 재확인해야 함 |
| `ao-ui-not-proof` | desktop의 ready-to-merge나 review 상태는 derived projection이며 merge authorization·commit identity·CI freshness의 독립 evidence가 아니다. | [board derivation](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/README.md#L57-L66), [PR fact snapshot](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/storage/sqlite/store/pr_facts.go#L27-L53) | `V2` | `W0` | confirmed limitation. external write는 proposal→policy/verifier→human→committer로 분리 필요 |
| `ao-windows-runtime-source` | Windows build-tagged source가 detached ConPTY host process group과 loopback readiness handshake, per-instance named pipe supervisor listener를 구현한다. | [ConPTY spawn](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/adapters/runtime/conpty/spawn_windows.go#L1-L25), [process flags/readiness](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/adapters/runtime/conpty/spawn_windows.go#L60-L100), [named-pipe supervisor](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/daemon/supervisor/listen_windows.go#L13-L39) | `V2` | `W1` | pass(좁은 정적 경로). native daemon/desktop/ConPTY workflow 실행·cleanup 회귀는 없어 `W2/W3` 아님 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `ao-origin-20260814` | parent `.gitmodules` + `git ls-tree`, official GitHub metadata와 fixed commit 비교 | pass | `Untrivial-ai/agent-orchestrator@12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3` | origin과 ToolVersion |
| `ao-static-20260814` | official fixed-SHA README/Go daemon·status·SQLite·Windows source 정적 검토 | partial pass | 위 fixed-SHA permalink | `V1/V2`, `W1` Claim |
| `ao-local-body-v3plus-none` | 조사 worktree submodule 본문이 비어 로컬 본문을 읽지 못했고 build/daemon/desktop/agent E2E/Windows 실행을 수행하지 않음 | unknown | 없음 | `V3+`, `W2+` Claim 없음 |

## 강점과 한계

- 강점: persistent project planner와 focused worker, worktree, terminal, PR/CI/review feedback loop를 하나의 daemon/desktop model에 결합한다.
- 강점: activity signal이 없을 때 confident idle을 주장하지 않는 `no_signal` 처리와 head SHA/update time 보존은 fail-closed projection 설계에 유용하다.
- 한계: Kanban status는 파생 상태다. stale provider snapshot이나 reconciliation failure가 있으면 ready/review/CI 표시는 실제 원격 head와 어긋날 수 있다.
- 한계: worktree·browser profile 분리는 credential/network/process sandbox가 아니며, orchestrator 역할 설명만으로 worker의 commit/PR 권한이 강제되지 않는다.
- 한계: Windows source는 detached ConPTY/named-pipe 경로에 한정된 `W1`이다. native daemon·desktop workflow와 process cleanup을 실행하지 않아 `W2/W3` 성공을 주장하지 않는다.

## AX 설계 재료

- `Borrow`: `ao-daemon-desktop`, `ao-worker-worktree`, `ao-project-orchestrator`의 durable daemon, explicit worker ownership, planner/worker 책임 분리 구조를 차용한다.
- `Adapt`: `ao-derived-kanban-status`, `ao-freshness-fail-closed`, `ao-pr-fact-snapshot`에 provider cursor, source head, observed-at, staleness budget을 결합하고 unknown을 ready보다 우선한다.
- `Avoid`: Kanban ready/review/CI를 merge authorization이나 current remote proof로 사용하거나 worktree를 sandbox로 해석하지 않는다(`ao-ui-not-proof`).
- `Build`: `ao-freshness-fail-closed`, `ao-ui-not-proof`, `ao-pr-fact-snapshot`에 대응해 read-only proposal → policy/verifier → human approval → scoped committer를 분리하고, event reconciliation·stale head rejection·append-only evidence를 daemon 밖의 독립 gate로 구축한다.
- `unknown / decision item`: 회사의 SCM/CI provider, merge 승인 체계, data classification, worker credential scope, notification·conversation 보존 규정은 확인되지 않았다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정이나 최종 구현 답이 아니라, 사내 AX의 daemon+desktop fleet model, explicit worker ownership, derived-state freshness/fail-closed UI를 설계하기 위한 재료
- 이유: `ao-daemon-desktop`, `ao-derived-kanban-status`, `ao-freshness-fail-closed`는 control plane 설계에 가치가 크다. UI를 proof로 오인하지 않고 read-only proposal→policy/verifier/human→committer 단계를 분리해야 한다.
- 재검토 조건: current upstream pin 갱신, Go/Electron build `V3`, daemon+desktop session `V4`, webhook loss·stale PR head·CI/review drift·restart E2E `V5`, Windows terminal/process lifecycle `W2/W3`

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE ProjectOrchestrator/WorkerSupervisor/HumanControlSurface`
- `ToolVersion PROVIDES worker-session/derived-kanban-status/pr-ci-review-projection`
- `ToolVersion SUPPORTS daemon-HTTP/events/SQLite-CDC/Electron/terminal/GitHub`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA tree/blob를 대조해 `I2 / V2 / W1` 프로필 작성. derived UI와 source proof를 분리하고 local body/build/runtime/E2E 및 Windows native 실행 미검증을 보존.
