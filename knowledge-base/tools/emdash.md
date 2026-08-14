---
id: tool-emdash
type: tool-profile
title: Emdash
status: observed
profile_schema_version: 2
tool_key: emdash
tool_version_id: tool-version:emdash@4366fcd589ae06014afa665bb900c93c1fcf9f54
tags: [knowledge-base, tool, desktop, worktree, runtime]
official_upstream: https://github.com/generalaction/emdash
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 286c8514186035e827f1f773dbd08679dd02c6d3
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 4366fcd589ae06014afa665bb900c93c1fcf9f54
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# Emdash

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

Emdash는 local/SSH workspace에서 worktree provisioning과 agent lifecycle을 desktop UI로 관리하는 multi-agent workspace runtime 참고 구현이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/generalaction/emdash` · `main` / `286c8514186035e827f1f773dbd08679dd02c6d3` (2026-08-15) |
| 고정 버전 / gitlink | `4366fcd589ae06014afa665bb900c93c1fcf9f54` · [`multi-agent-tools/emdash`](../../multi-agent-tools/emdash/) |
| pin 관계 | upstream이 pin 이후 이동; fixed ToolVersion은 갱신하지 않음 |
| license | [Apache-2.0 LICENSE](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/LICENSE.md#L1-L20) |
| provenance limitation | parent gitlink + official fixed-SHA docs/source 정적 검토; installers/build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Workspace runtime | local 또는 SSH host의 workspace/agent를 registry로 관리 | [README](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/README.md#L21-L45) |
| Provisioning saga | worktree 생성 단계를 순서화 | [create-worktree](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/create-worktree.ts#L35-L90) |
| Agent runtime | workspace 준비 후 agent spawnable state를 반환 | [runtime](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/runtime.ts#L685-L720) |
| Windows environment capture | Windows shell environment를 수집·정규화 | [windows-env](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/services/shell-env/node/windows-env.ts#L3-L42) |

## 역할과 연동

- AgentRole: Workspace Broker, Executor Supervisor, Human Control Surface.
- Capability: `staged-worktree-provisioning`, `local-ssh-runtime`, `agent-ready-state`, `desktop-workspace-ui`.
- Integration: Electron/Desktop, local process, SSH, git worktree, agent CLI.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `emdash-local-ssh` | architecture | local과 SSH workspace runtime을 같은 UI/control surface에서 다룬다. | [README](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/README.md#L21-L45) | `I2` | `V2` | `W1` | remote host trust/credential policy는 별도 |
| `emdash-provisioning-stages` | capability | worktree 생성과 설정을 단계화한다. | [create-worktree](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/create-worktree.ts#L35-L90) | `I2` | `V2` | `W1` | crash compensation/idempotency는 runtime 미검증 |
| `emdash-ready-state` | capability | provisioning 후 agent-spawnable runtime state를 반환한다. | [runtime](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/runtime.ts#L685-L720) | `I2` | `V2` | `W1` | 반환 상태는 health/readiness 실행 증거가 아님 |
| `emdash-windows-path` | platform | Windows environment capture 전용 source가 있다. | [windows-env](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/services/shell-env/node/windows-env.ts#L3-L42) | `I2` | `V2` | `W1` | W2/W3 runtime evidence 없음 |
| `emdash-credential-boundary` | security | agent/workspace process에 전달되는 credential environment는 command/host 경계가 필요하다. | [git credential env](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/primitives/git-credentials/api/env.ts#L32-L87) | `I2` | `V2` | `W1` | audience-scoped opaque handle이 아님 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Desktop/runtime registry | UI IPC → workspace runtime → process/SSH | UI state는 host authority를 제한하지 않음 | [README](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/README.md#L21-L45) |
| SSH/local executor | remote/local command channel | credential, host key, egress, workspace scope를 별도 정책화 | [runtime](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/runtime.ts#L685-L720) |

## 운영·보안·trust boundary

- local host와 SSH host는 서로 다른 trust domain이다. workspace readiness, credential audience, network egress, persistence를 실행 context별로 기록해야 한다.
- 단계화된 provisioning은 유용하지만 durable saga/compensation과 stale generation 차단은 별도 검증이 필요하다.

## 플랫폼과 Windows

- `W1 narrow`: Windows environment 전용 source와 installer 문서가 있으나 native agent process tree, SSH/local parity, long path/CRLF를 실행하지 않았다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `emdash-static-20260815` | `I2/V2/W1` | parent pin + official fixed source | partial pass | build/runtime/E2E 없음 |
| `emdash-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: local/remote workspace, staged provisioning, agent-ready state를 명시적 runtime layer로 분리한다.
- 한계: desktop/runtime 결합, credential inheritance, crash recovery와 readiness 의미가 사내 gate 수준으로 증명되지 않았다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | staged provisioning과 explicit ready point | `emdash-provisioning-stages`, `emdash-ready-state` | `AX-N-EXECUTOR-LIFECYCLE` |
| Adapt | local/SSH registry를 typed executor capability broker로 변형 | `emdash-local-ssh` | host별 policy와 fingerprint 필요 |
| Avoid | inherited credential와 UI ready를 권한·health 보장으로 간주 | `emdash-credential-boundary`, `emdash-ready-state` | fail-closed |
| Build | replayable saga + compensation + opaque credential handles | 위 Claims | `AD-EXECUTOR-CONTRACT` / `RM-SECRET-BROKER` |

## 도입 판단

- 결정: executor lifecycle reference. 최종 vendor 선택이 아니다.
- 재검토: Windows/local/SSH `V3~V5`, crash recovery, credential leak fixture.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `emdash-v3-build` | fixed version | `V3/W2` | Windows build/launch 성공, env fingerprint 보존 |
| `emdash-v5-saga` | provisioning | `V5` | 각 단계 crash 후 중복/잔여 자원 없이 복구 |
| `emdash-v5-secret` | credential | `V5` | 비대상 process/log에 secret 노출 0 |

## 관계와 변경 이력

- `Capability staged-worktree-provisioning ADDRESSES AXNeed AX-N-EXECUTOR-LIFECYCLE`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
