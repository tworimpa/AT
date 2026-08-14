---
id: tool-agent-deck
type: tool-profile
title: Agent Deck
status: observed
profile_schema_version: 2
tool_key: agent-deck
tool_version_id: tool-version:agent-deck@4630080726ddf99885e1d3d190ffcd2e25d18683
tags: [knowledge-base, tool, orchestration, tui]
official_upstream: https://github.com/asheshgoplani/agent-deck
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 4630080726ddf99885e1d3d190ffcd2e25d18683
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 4630080726ddf99885e1d3d190ffcd2e25d18683
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# Agent Deck

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

Agent Deck은 여러 coding-agent 세션을 TUI/Web에서 검색·관찰·fork하고 git worktree 수명주기와 연결하는 운영 UI 참고 구현이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/asheshgoplani/agent-deck` · `main` / `4630080726ddf99885e1d3d190ffcd2e25d18683` (2026-08-15) |
| 고정 버전 / gitlink | `4630080726ddf99885e1d3d190ffcd2e25d18683` · [`multi-agent-tools/agent-deck`](../../multi-agent-tools/agent-deck/) |
| pin 관계 | 조사일 default-branch HEAD와 같음. profile은 fixed SHA를 계속 가리킴 |
| license | [MIT LICENSE](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/LICENSE#L1-L21) |
| provenance limitation | parent `.gitmodules`와 mode `160000` gitlink, official fixed-SHA README/source를 대조했다. build/runtime/E2E는 실행하지 않았다 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Session dashboard | running/waiting/done 상태, 검색과 다중 세션 관찰 | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L22-L30) |
| Fork/archive | 대화·세션 metadata를 복제하거나 보존 | [fork semantics](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L471-L497) |
| Worktree lifecycle | 세션용 worktree 생성·finish·cleanup | [worktrees](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L303-L310) |

## 역할과 연동

- AgentRole: Human Control Surface, Session Supervisor.
- Capability: `session-observability`, `session-fork`, `worktree-lifecycle`, `archive-recovery`.
- Integration: TUI/Web, agent CLI/PTY, git worktree.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `agent-deck-fleet-ui` | capability | 여러 세션을 상태·검색 중심 UI로 투영한다. | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L22-L30) | `I2` | `V2` | `W0` | UI 상태는 derived projection이며 완료 증거가 아님 |
| `agent-deck-worktree` | architecture | 세션과 worktree create/finish/cleanup을 연결한다. | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L303-L310) | `I2` | `V2` | `W0` | worktree는 process/network/secret 격리가 아님 |
| `agent-deck-fork-policy` | security | fork 시 ignored files 포함은 선택이며 Web/API와 TUI 기본값이 다를 수 있다. | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L471-L493) | `I2` | `V2` | `W0` | secret 복제와 surface별 기본값 drift 위험 |
| `agent-deck-setup-fail-open` | limitation | worktree setup script 실패 후 경고하고 세션을 계속할 수 있다. | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L336-L368) | `I2` | `V2` | `W0` | readiness가 필수인 AX에서는 fail-closed gate 필요 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| TUI/Web | human → session manager → agent/worktree | UI 조작자가 가진 SCM·agent 권한을 자동 축소하지 않음 | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L22-L30) |
| Fork | session metadata/transcript + 선택적 ignored files | credential·local config 복제는 별도 승인 필요 | [fork](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L471-L493) |

## 운영·보안·trust boundary

- 보호 자산은 repository, ignored files/credentials, session transcript, SCM write 권한이다.
- worktree와 archive는 가시성·복구 패턴이지 sandbox나 verifier가 아니다. setup failure와 UI 상태는 별도 readiness/evidence gate로 차단해야 한다.

## 플랫폼과 Windows

- `W0`: fixed source에서 native Windows 전체 agent/worktree/PTY 경로를 입증하지 못했다. WSL 가능성은 native Windows 증거로 승격하지 않는다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `agent-deck-static-20260815` | `I2/V2/W0` | parent gitlink + official fixed source | partial pass | build/runtime/E2E 미실행 |
| `agent-deck-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | 실행 증거 없음 |

## 강점과 한계

- 강점: fleet visibility, 검색, fork/archive, worktree lifecycle을 한 운영 표면에 모은다.
- 한계: 상태 판정과 setup 성공, ignored-file 복제 정책이 강한 증거·보안 경계를 제공하지 않는다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | 세션 검색·상태·archive cockpit | `agent-deck-fleet-ui` | `AX-N-CONTROL-VISIBILITY` |
| Adapt | fork를 transcript/code/secret별 정책화 | `agent-deck-fork-policy` | 데이터 분류·승인 체계는 `unknown/decision-needed` |
| Avoid | UI done이나 worktree를 검증·격리 완료로 간주 | `agent-deck-worktree`, `agent-deck-setup-fail-open` | fail-closed evidence 원칙 |
| Build | event-derived status + readiness verifier + resource/credential lease | 위 Claims | `AD-EVIDENCE-SEPARATION` / `RM-CORE-CONTROL-PLANE` |

## 도입 판단

- 결정: UI/수명주기 패턴 참고. 최종 vendor selection이 아니라 AX 설계 재료다.
- 재검토: pinned build, Windows agent session, setup-failure, ignored-file fork를 `V3~V5/W2`로 검증.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `agent-deck-v3-build` | fixed version | `V3` | reproducible build와 dependency hash 보존 |
| `agent-deck-v5-fork` | fork/setup claims | `V5` | secret fixture 미복제, setup 실패 시 실행 차단, stale session 정리 |
| `agent-deck-w2` | Windows | `W2` | native Windows에서 process tree·worktree lifecycle 관찰 |

## 관계와 변경 이력

- `Capability session-observability ADDRESSES AXNeed AX-N-CONTROL-VISIBILITY`.
- 2026-08-15: `I2/V2/W0` fixed-SHA profile 작성.
