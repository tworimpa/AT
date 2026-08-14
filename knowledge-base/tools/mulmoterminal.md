---
id: tool-mulmoterminal
type: tool-profile
title: MulmoTerminal
status: observed
profile_schema_version: 2
tool_key: mulmoterminal
tool_version_id: tool-version:mulmoterminal@29787ace53e63f00950c7028f5d765eb035fedd5
tags: [knowledge-base, tool, terminal, pty, worktree]
official_upstream: https://github.com/receptron/mulmoterminal
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 096d53e452b6df821bfd44b326a6575134545f88
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 29787ace53e63f00950c7028f5d765eb035fedd5
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# MulmoTerminal

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

MulmoTerminal은 browser UI에서 실제 PTY/tmux agent sessions, git worktrees, diff/PR 흐름과 port 환경을 다루는 terminal cockpit 참고 구현이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/receptron/mulmoterminal` · `main` / `096d53e452b6df821bfd44b326a6575134545f88` (2026-08-15) |
| 고정 버전 / gitlink | `29787ace53e63f00950c7028f5d765eb035fedd5` · [`multi-agent-tools/mulmoterminal`](../../multi-agent-tools/mulmoterminal/) |
| pin 관계 | upstream이 pin 이후 이동; profile pin은 불변 |
| license | [MIT LICENSE](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/LICENSE#L1-L21) |
| provenance limitation | parent gitlink + official fixed-SHA README 정적 근거 중심. build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Browser cockpit | session 상태, terminal, worktree/diff/PR UI | [features](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L50-L72) |
| PTY/WebSocket | browser ↔ server ↔ node-pty terminal stream | [architecture](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L343-L356) |
| tmux/worktree | persistent session과 branch filesystem 분리 | [persistence/platform](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L481-L504) |
| worktreeEnv | worktree별 ports/slug 환경 부여 | [resource environment](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L746-L810) |

## 역할과 연동

- AgentRole: Terminal Supervisor, Human Control Surface, Workspace Broker.
- Capability: `web-pty`, `persistent-session`, `worktree-diff-pr`, `workspace-resource-env`.
- Integration: WebSocket, node-pty, tmux, git worktree, agent CLI.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `mulmo-web-pty` | interface | browser와 real PTY를 WebSocket/server로 연결한다. | [README](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L8-L13), [architecture](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L343-L356) | `I2` | `V2` | `W1` | terminal text는 typed lifecycle receipt가 아님 |
| `mulmo-worktree-resources` | capability | worktree별 환경/port를 구성하지만 worktree 자체는 port를 격리하지 않는다. | [worktreeEnv](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L746-L810) | `I2` | `V2` | `W1` | collision 방지는 allocation/lease로 별도 구현 필요 |
| `mulmo-exit-gap` | limitation | one-shot command 외 agent cell은 명령 종료/exit code를 명시적으로 표시하지 않는다. | [README](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L637-L650) | `I2` | `V2` | `W1` | false-complete 위험; verifier receipt 필요 |
| `mulmo-windows-fallback` | platform | native Windows에서는 tmux persistence 없이 plain PTY fallback을 사용한다. | [requirements](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L223-L230), [fallback](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L481-L504) | `I2` | `V2` | `W1` | Windows 지속 session/recovery 근거 없음 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Terminal | WebSocket + PTY bytes | browser actor → server process → shell/agent | authentication, command policy, transcript retention 별도 결정 | [architecture](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L343-L356) |
| Git/PR UI | UI → worktree/git/remote | external write는 explicit verifier/human/committer gate 필요 | [features](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L50-L72) |

## 운영·보안·trust boundary

- PTY는 agent adapter fallback일 뿐 actor identity, approval, exit receipt를 제공하지 않는다.
- worktree는 files만 분리하며 port, process, credential, network를 격리하지 않는다. port assignment에는 lease/expiry/fencing이 필요하다.

## 플랫폼과 Windows

- `W1 narrow`: Windows plain PTY fallback이 문서화됐지만 persistence/cancel/process-tree/exit semantics는 미검증이다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `mulmo-static-20260815` | `I2/V2/W1` | parent pin + official fixed README | partial pass | build/runtime/E2E 없음 |
| `mulmo-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: terminal, worktree, diff/PR, resource hints를 하나의 human-visible cockpit에 결합한다.
- 한계: PTY heuristic, exit-code 공백, Windows persistence 부재, port 비격리가 있다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | session/worktree/resource cockpit | `mulmo-web-pty`, `mulmo-worktree-resources` | `AX-N-CONTROL-VISIBILITY` |
| Adapt | PTY를 typed adapter 아래 fallback으로 제한 | `mulmo-exit-gap` | adapter priority: typed API→ACP→JSON CLI→PTY |
| Avoid | terminal 색/텍스트나 worktree를 완료·격리 증거로 사용 | `mulmo-exit-gap`, `mulmo-worktree-resources` | fail-closed |
| Build | ConPTY/Job Object + structured exit receipt + ResourceLease | 위 Claims | `AD-TYPED-ADAPTER` / `RM-WINDOWS-EXECUTOR` |

## 도입 판단

- 결정: cockpit/resource UX 참고. 최종 vendor 선택이 아니다.
- 재검토: Windows PTY lifecycle, WebSocket auth, port collision, external write `V3~V5/W2~W3`.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `mulmo-v3-build` | fixed version | `V3/W2` | Windows build/launch |
| `mulmo-v5-exit` | exit gap | `V5/W3` | cancel/crash/child-tree에서 정확한 terminal receipt |
| `mulmo-v5-port` | resource env | `V5` | concurrent allocation collision 0, stale lease 회수 |

## 관계와 변경 이력

- `Capability web-pty ADDRESSES AXNeed AX-N-CONTROL-VISIBILITY`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
