---
id: tool-agtx
type: tool-profile
title: agtx
status: observed
profile_schema_version: 2
tool_key: agtx
tool_version_id: tool-version:agtx@6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04
tags:
  - knowledge-base
  - tool
  - orchestration
  - kanban
  - mcp
official_upstream: https://github.com/fynnfluegge/agtx
license: Apache-2.0-root-license-with-Cargo-MIT-mismatch
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# agtx

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

agtx는 SQLite task board를 TUI로 보여 주고 dependency gate를 거쳐 task별 git worktree·tmux agent를 실행하며, 같은 상태 조작을 stdio MCP tool로 노출하는 terminal-native orchestration reference다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/fynnfluegge/agtx` |
| 기본 브랜치와 조사일 HEAD | `main` / `6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04` (2026-08-14) |
| 고정 버전 | `6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04` |
| pin과 최신 관찰 관계 | 조사일 default-branch HEAD와 같음. latest release 여부는 확인하지 않았고 fixed profile은 자동 갱신하지 않음 |
| 로컬 gitlink | [`multi-agent-tools/agtx`](../../multi-agent-tools/agtx/) |
| 유지보수 관찰 | GitHub metadata상 archived/disabled가 아니고 `pushed_at=2026-08-11T07:31:53Z`; 지원 SLA나 runtime 안정성 증거는 아님 |
| 출처 무결성 | `I2`: parent `.gitmodules`, `git ls-tree` mode `160000`, official fixed commit/tree를 대조 |
| license | root [`LICENSE`](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/LICENSE#L1-L30)는 Apache-2.0이고 GitHub SPDX metadata도 Apache-2.0이나, [`Cargo.toml`](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/Cargo.toml#L1-L9)은 `license = "MIT"`로 불일치. 재사용 전 maintainer 확인과 법무 검토 필요 |
| provenance limitation | 병렬 조사 worktree의 submodule 본문이 비어 local body를 읽지 못함. official GitHub fixed-SHA blob/tree와 metadata로만 `V2` 수집; build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| SQLite board | task, status, dependency reference와 transition request 저장 | MCP가 request를 enqueue하고 TUI가 side effect를 처리 | [schema와 queue](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/db/schema.rs#L134-L218) |
| Kanban/dependency view | task status와 DAG level·blocked 상태 투영 | dependency graph를 Kahn-style level로 정렬 | [dependency graph](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/tui/dep_graph.rs#L90-L199) |
| Worktree/tmux executor | task branch/worktree 생성과 agent pane 수명주기 | `.agtx/worktrees` + dedicated tmux window | [worktree create](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/git/worktree.rs#L5-L75), [tmux operations](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/tmux/operations.rs#L8-L59) |
| MCP router | board 조회·생성·이동·pane read/send | MCP stdio → SQLite queue/TUI → git·tmux side effect | [tools와 stdio serve](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L521-L549), [serve](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L1269-L1286) |

## 역할과 연동

- AgentRole: Planner, Scheduler, Worker Supervisor, Human Control Surface.
- Capability: `kanban-task-state`, `dependency-gate`, `task-worktree`, `tmux-session-routing`, `mcp-task-control`.
- Integration: TUI, CLI, MCP stdio, SQLite, git, tmux, agent CLI.
- SecurityOperationalRequirement: task ownership lease, generation fencing, dependency integrity, MCP caller authority, external-write approval, stale pane/session reconciliation이 별도 필요하다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `agtx-kanban-worktree-tmux` | architecture | task별 worktree와 tmux window를 Kanban lifecycle에 연결한다. | [README](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/README.md#L50-L69), [worktree](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/git/worktree.rs#L24-L75) | `I2` | `V2` | `W0` | partial pass(정적). 실제 agent/session/worktree 실행 없음 |
| `agtx-dependency-gate` | capability | Backlog의 forward transition은 referenced task가 Review/Done일 때만 허용한다. | [gate](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L690-L702), [predicate](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/db/schema.rs#L434-L446) | `I2` | `V2` | `W0` | partial. dependency ID가 없거나 DB read가 실패하면 `map_or(true)`여서 fail-open |
| `agtx-mcp-routing` | interface | stdio MCP가 task CRUD, transition queue, pane read/send를 project/global mode로 라우팅한다. | [parameter contract](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L16-L40), [move queue](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L658-L721), [pane send](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L921-L927) | `I2` | `V2` | `W0` | partial. stdio caller 인증·권한·approval은 이 경로에서 증명되지 않음 |
| `agtx-narrow-request-claim` | limitation | transition request에는 `claimed_by IS NULL` 조건부 update가 있으나 lease expiry·renewal·generation token이 없고 task ownership claim과도 다르다. | [claim](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/db/schema.rs#L558-L590), [age cleanup](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/db/schema.rs#L592-L600) | `I2` | `V2` | `W0` | confirmed scope limit. durable lease/generation/atomic task claim 보장 없음 |
| `agtx-license-mismatch` | limitation | root license/GitHub metadata의 Apache-2.0과 Rust manifest의 MIT 선언이 충돌한다. | [LICENSE](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/LICENSE#L1-L30), [Cargo manifest](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/Cargo.toml#L1-L9) | `I2` | `V2` | `W0` | confirmed metadata mismatch; license 결론은 보류 |
| `agtx-posix-runtime` | platform | 핵심 executor가 `tmux`, `sh`, `env -u`, `$SHELL`에 의존한다. | [tmux shell path](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/tmux/operations.rs#L61-L95), [worktree script](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/git/worktree.rs#L115-L127) | `I2` | `V2` | `W0` | native Windows 경로·실행 evidence 없음 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| TUI | terminal events + SQLite | human → board → task transition | human presence가 SCM 권한을 제한하지 않음 | [README shortcuts](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/README.md#L108-L130) |
| MCP | stdio, structured tool parameters/results | agent client → MCP server → queue | caller/process trust에 위임; 별도 actor/approval contract 없음 | [server info](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L1245-L1265) |
| tmux pane | CLI/key injection/pane capture | orchestrator/TUI → long-lived agent pane | injected text가 agent authority와 결합되므로 audit·allowlist 필요 | [tmux trait](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/tmux/operations.rs#L23-L58) |

## 운영·보안·trust boundary

- 보호 자산은 repository/worktree, agent CLI credential, MCP task mutation, tmux keystroke, merge/push 권한이다. worktree와 tmux 분리는 process/network/credential sandbox가 아니다.
- transition queue의 조건부 claim은 좁은 중복 소비 방지다. worker crash 뒤 안전한 회수, stale worker write 차단, task owner 세대 교체를 보장하지 않는다.
- dependency target 누락을 satisfied로 처리하므로 사내 gate는 unresolved/error를 `blocked/unknown`으로 두는 fail-closed predicate를 써야 한다.
- UI status와 agent pane의 “done”은 derived projection이며 commit identity, verifier, CI freshness, approval evidence와 분리한다.

## 플랫폼과 Windows

- `W0`: fixed source의 핵심 path가 tmux와 POSIX shell을 요구한다. WSL/remote Linux에서 호출 가능하다는 사실은 native Windows executor 증거가 아니다.
- Windows-first AX에서는 ConPTY + Job Object process tree, PowerShell/argv escaping, CRLF/long path, credential broker를 별도 adapter/executor로 구현해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | 지원 Claim | limitation |
|---|---|---|---|---|---|---|---|
| `agtx-origin-20260814` | `I2` | `6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04` | parent `.gitmodules` + `git ls-tree` + official GitHub commit/tree, exit 0 | Windows PowerShell 5.1; git 2.51.0.windows.1; gh 2.95.0 | pass | ToolVersion identity | local submodule body 비어 있음 |
| `agtx-static-20260814` | `V2/W0` | same | official fixed README/Rust source/license 정적 검토, exit 0 | same | partial pass | 위 Claims | build/runtime/E2E 아님 |
| `agtx-v3plus-none` | `V3~V6/W2~W3` | same | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 정적 결과를 실행 증거로 승격하지 않음 |

수집 실행 기록: `run_id=implement-deep-orchestration-profiles-20260814`, `profile_id=implement-deep@1`, role=`Documenter`, provider=`OpenAI`, model slug=`gpt-5.6-sol`, model version=`unknown`, requested/actual effort=`high/high`, base/head=`984cac0634b83d10af91d8e1814680816e67c53b`, started_at=`not-captured`, ended_at=`2026-08-14T23:54:03+09:00`, cost/latency=`unknown`, external write=`none`.

## 강점과 한계

- 강점: Kanban, dependency view, worktree/tmux session, MCP routing을 작은 local state model로 연결한다.
- 한계: task-level durable lease·generation fencing이 없고 dependency lookup error가 fail-open이다.
- 한계: license manifest가 root LICENSE와 충돌하며 native Windows path는 없다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | board state와 dependency graph를 같은 task identity에 연결하는 TUI/MCP projection | `agtx-kanban-worktree-tmux`, `agtx-mcp-routing` | `AX-N-CONTROL-VISIBILITY` |
| Adapt | transition queue를 durable outbox/inbox와 idempotency key로 변형 | `agtx-narrow-request-claim` | multi-process restart와 감사 보존 필요 |
| Avoid | missing dependency를 satisfied로 처리하거나 worktree/tmux를 sandbox로 간주 | `agtx-dependency-gate`, `agtx-posix-runtime` | fail-closed와 Windows-first 위반 |
| Build | atomic task claim + expiring lease + renewal + monotonic generation fencing + stale write rejection | `agtx-narrow-request-claim` | `AD-LEASE-FENCING` / `RM-CORE-SCHEDULER` |

회사 업종, 데이터 분류, 규정, 승인자, 망분리, SCM credential scope는 `unknown/decision-needed`이며 이 프로필에서 가정하지 않는다.

## 도입 판단

- 결정: 참고.
- 성격: 최종 vendor selection이 아니라 사내 AX control-plane/task-state 설계 재료.
- 적용 범위: Kanban/dependency/MCP UX reference와 fail-open/lease gap 비교.
- 재검토 조건: license 정정, native Windows adapter, `V3` build, concurrent claim·crash recovery `V5`.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|
| `agtx-v3-build` | core fixed version | `V3` | pinned Rust toolchain에서 build/test | exit 0와 dependency lock hash | logs, env, binary hash | network/dependency approval |
| `agtx-v5-race` | `agtx-narrow-request-claim` | `V5` | 두 TUI 소비자, crash-after-claim, stale retry | 중복 side effect 0; orphan 복구가 명시 contract와 일치 | DB trace, process/event log | isolated fixture |
| `agtx-w2-adapter` | `agtx-posix-runtime` | `W2` | Windows ConPTY adapter prototype | task lifecycle와 process-tree cleanup 관찰 | Windows build/runtime log | 별도 구현 결정 |

## 관계와 변경 이력

- `ToolVersion PROVIDES kanban-task-state/dependency-gate/mcp-task-control`.
- `Capability ADDRESSES AXNeed AX-N-CONTROL-VISIBILITY`.
- `ArchitectureDecision AD-LEASE-FENCING ADAPTS/AVOIDS agtx-narrow-request-claim`.
- 2026-08-14: `I2/V2/W0` fixed-SHA 프로필 작성. license mismatch, fail-open dependency, durable lease/generation 부재와 실행 미검증을 보존.
