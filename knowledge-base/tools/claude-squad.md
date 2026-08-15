---
id: tool-claude-squad
type: tool-profile
title: Claude Squad
status: observed
profile_schema_version: 2
tool_key: claude-squad
tool_version_id: tool-version:claude-squad@2dd388e9857233e07712c8c5b3e2bf3b471b39fa
tags: [knowledge-base, tool, orchestration, tui]
official_upstream: https://github.com/smtg-ai/claude-squad
license: AGPL-3.0-only
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 2dd388e9857233e07712c8c5b3e2bf3b471b39fa
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 2dd388e9857233e07712c8c5b3e2bf3b471b39fa
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# Claude Squad

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

Claude Squad는 여러 coding-agent CLI를 tmux session과 git worktree에 묶어 TUI에서 시작·일시정지·재개·checkout하는 작은 병렬 작업 관리자다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/smtg-ai/claude-squad` · `main` / `2dd388e9857233e07712c8c5b3e2bf3b471b39fa` (2026-08-15) |
| 고정 버전 / gitlink | `2dd388e9857233e07712c8c5b3e2bf3b471b39fa` · [`multi-agent-tools/claude-squad`](../../multi-agent-tools/claude-squad/) |
| pin 관계 | 조사일 HEAD와 같음 |
| license | [AGPL-3.0](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/LICENSE.md#L1-L20); 직접 결합·수정 배포 전 법무 검토/clean-room 경계 필요 |
| provenance limitation | parent gitlink와 official fixed-SHA README/source 정적 검토만 수행. build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| TUI session manager | 여러 agent session start/pause/resume/checkout | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L95-L105) |
| tmux runtime | long-lived CLI process/terminal state | [requirements](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L45-L51) |
| git worktrees | session별 filesystem branch 분리 | [architecture](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L148-L153) |

## 역할과 연동

- AgentRole: Worker Supervisor, Human Control Surface.
- Capability: `parallel-agent-session`, `pause-resume`, `task-worktree`, `tui-control`.
- Integration: TUI, tmux/PTY heuristic, git worktree, agent CLI.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `claude-squad-session-fleet` | capability | 여러 agent CLI session을 TUI에서 관리한다. | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L3-L12) | `I2` | `V2` | `W0` | 정적 pass; UI status는 execution proof가 아님 |
| `claude-squad-tmux-worktree` | architecture | tmux와 git worktree로 session process/files를 분리한다. | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L148-L153) | `I2` | `V2` | `W0` | process/network/credential sandbox가 아님 |
| `claude-squad-autoyes` | security | experimental autoyes는 agent prompt를 자동 승인한다. | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L63-L69) | `I2` | `V2` | `W0` | 사내 policy 기본값으로 부적합 |
| `claude-squad-posix` | platform | 핵심 runtime이 tmux를 요구한다. | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L45-L51) | `I2` | `V2` | `W0` | native Windows full workflow 근거 없음 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| TUI | keystroke → tmux session/agent CLI | terminal owner의 agent/SCM authority에 의존 | [controls](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L95-L105) |
| tmux | pane input/output heuristic | typed session/approval protocol 없음 | [architecture](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L148-L153) |

## 운영·보안·trust boundary

- 보호 자산은 repository, agent credentials, tmux input, branch/commit이다. worktree/tmux는 sandbox가 아니다.
- autoyes와 terminal heuristic은 approval provenance를 약화하므로 proposal→policy/human→committer 분리가 필요하다.

## 플랫폼과 Windows

- `W0`: tmux 의존 fixed source만 확인했다. Windows stub/WSL 가능성을 native Windows runtime 증거로 간주하지 않는다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `claude-squad-static-20260815` | `I2/V2/W0` | parent pin + official fixed source | partial pass | build/runtime/E2E 없음 |
| `claude-squad-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: 작고 이해하기 쉬운 session/worktree TUI로 병렬 작업을 가시화한다.
- 한계: tmux/PTY heuristic, autoyes, AGPL 결합 경계, native Windows 부재가 직접 채택을 제한한다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | 작은 session/worktree cockpit | `claude-squad-session-fleet` | `AX-N-CONTROL-VISIBILITY` |
| Adapt | pause/resume를 typed run state와 receipt로 변형 | `claude-squad-tmux-worktree` | 공통 contract와 Windows/Linux native executor 필요 |
| Avoid | autoyes와 terminal text를 승인·완료 증거로 사용 | `claude-squad-autoyes` | `AX-N-HUMAN-APPROVAL` |
| Build | 공통 executor contract, Windows ConPTY/Job Object 및 Linux PTY/process-group adapter, session identity, explicit approval event | 위 Claims | `AD-TYPED-ADAPTER` / `RM-NATIVE-EXECUTORS` |

회사 규정·데이터 분류·AGPL 사용 경계는 `unknown/decision-needed`다.

## 도입 판단

- 결정: clean-room UX 참고. 최종 도입 결론이 아니다.
- 재검토: 법무 경계, Windows native prototype, cancellation/process-tree/approval `V3~V5`.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `claude-squad-v3` | fixed version | `V3` | build/test 재현 |
| `claude-squad-v5-approval` | autoyes | `V5` | 위험 prompt 자동 승인 0 |
| `claude-squad-w2` | Windows adapter | `W2` | ConPTY session start/cancel/reap 관찰 |

## 관계와 변경 이력

- `Capability parallel-agent-session ADDRESSES AXNeed AX-N-CONTROL-VISIBILITY`.
- 2026-08-15: `I2/V2/W0` fixed-SHA profile 작성.
