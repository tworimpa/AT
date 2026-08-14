---
id: tool-agetor
type: tool-profile
title: Agetor
status: observed
profile_schema_version: 2
tool_key: agetor
tool_version_id: tool-version:agetor@2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85
tags: [knowledge-base, tool, orchestration, approvals]
official_upstream: https://github.com/alamops/agetor
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: f67a4da11b3a2d9371a32b66d873eb2ec88eecbb
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# Agetor

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

Agetor는 Kanban card를 pinned-base worktree의 agent child process로 실행하고 approval/question을 구조화된 UI와 localhost API로 중계하는 local control plane이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/alamops/agetor` · `main` / `f67a4da11b3a2d9371a32b66d873eb2ec88eecbb` (2026-08-15) |
| 고정 버전 / gitlink | `2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85` · [`multi-agent-tools/agetor`](../../multi-agent-tools/agetor/) |
| pin 관계 | upstream이 pin 이후 이동. 이 profile의 ToolVersion은 불변 |
| license | [MIT LICENSE](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/LICENSE#L1-L21) |
| provenance limitation | parent gitlink + official fixed-SHA 문서/코드 정적 검토. build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Local core/API | `127.0.0.1` JSON/SSE, per-launch bearer token, SQLite | [architecture](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L23-L53) |
| Worktree orchestrator | base SHA pin → task branch/worktree → teardown | [worktree lifecycle](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L243-L253) |
| Interaction bridge | approval/question을 run panel card로 중계 | [approvals](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L255-L267) |
| Daemon reconciliation | desktop/CLI가 공유 state와 daemon handoff 사용 | [CLI/core discovery](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L132-L163) |

## 역할과 연동

- AgentRole: Planner, Scheduler, Approval Broker, Worker Supervisor.
- Capability: `pinned-worktree-run`, `structured-approval`, `local-event-stream`, `orphan-reconciliation`.
- Integration: HTTP JSON/SSE, CLI, tmux/JSONL/stdout adapters, SQLite, git worktree.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `agetor-pinned-worktree` | architecture | task base SHA를 pin하고 별도 branch/worktree에서 실행한다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L17-L23) | `I2` | `V2` | `W1` | 정적 pass; isolation `none`도 허용 |
| `agetor-approval-bridge` | capability | Claude hook/transcript와 Codex stdout에서 approval/question을 구조화한다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L18-L20), [approval rules](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L255-L259) | `I2` | `V2` | `W1` | Codex path는 stdout heuristic; allow-always는 task scope에 지속 |
| `agetor-local-api-auth` | security | localhost API는 health 외 route에 per-launch token을 요구한다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L53-L53), [API](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L267-L289) | `I2` | `V2` | `W1` | local token은 child process/SCM 권한 축소나 sandbox가 아님 |
| `agetor-destructive-teardown` | limitation | delete는 forced worktree removal, branch deletion, rm fallback을 사용한다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L243-L253) | `I2` | `V2` | `W1` | generation/ownership fencing 없이 재사용하면 위험 |
| `agetor-windows-configured` | platform | Windows build가 구성됐지만 공식 문서가 미시험이라고 명시한다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L67-L72) | `I2` | `V2` | `W1` | W1은 build path/doc 정적 근거만; W2/W3 아님 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Core API | localhost HTTP JSON/SSE + bearer | caller 인증과 process/SCM authority는 별개 | [API](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L267-L289) |
| Approval bridge | hook/JSONL/tmux/stdout → UI answer | parser가 잘못 판단할 수 있어 fail-closed confirmation 필요 | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L18-L20) |

## 운영·보안·trust boundary

- agent는 사용자 shell/credential 권한으로 실행한다. localhost token과 worktree는 secret/network/process sandbox가 아니다.
- `allow always`, isolation `none`, forced teardown은 회사별 데이터 분류·승인·retention 결정 전 기본 허용하면 안 된다.

## 플랫폼과 Windows

- `W1 narrow`: Windows build configuration/문서 경로만 확인했다. native child-process cancellation, path/CRLF, daemon handoff, worktree cleanup을 실행하지 않았다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `agetor-static-20260815` | `I2/V2/W1` | parent gitlink + fixed README/source | partial pass | build/runtime/E2E 미실행 |
| `agetor-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | 실행 artifact 없음 |

## 강점과 한계

- 강점: pinned base, structured approvals, durable local history와 daemon reconciliation을 한 control plane으로 연결한다.
- 한계: heuristic prompt detection, optional isolation, persistent allow rule, destructive cleanup은 강한 policy/fencing이 필요하다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | pinned base와 approval card/event stream | `agetor-pinned-worktree`, `agetor-approval-bridge` | `AX-N-REPRODUCIBILITY`, `AX-N-HUMAN-APPROVAL` |
| Adapt | localhost core를 actor-scoped API와 durable audit로 변형 | `agetor-local-api-auth` | 승인자·credential audience는 `unknown/decision-needed` |
| Avoid | stdout heuristic 자동승인, isolation none, unfenced forced delete | `agetor-approval-bridge`, `agetor-destructive-teardown` | fail-closed와 복구 가능성 |
| Build | typed adapter + lease/generation + fenced cleanup + approval expiry | 위 Claims | `AD-LEASE-FENCING` / `RM-POLICY-BROKER` |

## 도입 판단

- 결정: control-plane 패턴 참고. 최종 vendor selection이 아니다.
- 재검토: pinned Windows build, cancellation/cleanup failure injection, token/approval policy E2E.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `agetor-v3-build` | fixed version | `V3/W2` | Windows build·launch·worktree lifecycle exit 0 |
| `agetor-v5-approval` | approval bridge | `V5` | malformed/stale prompt가 auto-allow되지 않음 |
| `agetor-v5-cleanup` | teardown | `V5/W3` | stale generation이 새 worktree/branch를 삭제하지 않음 |

## 관계와 변경 이력

- `Capability structured-approval ADDRESSES AXNeed AX-N-HUMAN-APPROVAL`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
