---
id: tool-cline
type: tool-profile
title: Cline
status: observed
tags:
  - knowledge-base
  - tool
  - coding-agent
  - multi-surface
  - acp
official_upstream: https://github.com/cline/cline
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 3e0aac53a2f5f408a89a957d75430f6ec4084497
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 3e0aac53a2f5f408a89a957d75430f6ec4084497
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Cline

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Cline은 shared agent core를 CLI, VS Code, JetBrains, SDK/Hub surface로 투영하고 ACP·MCP·approval·checkpoint·subagent 기능을 제공하는 multi-surface coding-agent comparator다.

## ToolVersion과 공식 최신 관찰

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/cline/cline` |
| 조사일 기본 브랜치 HEAD | `main` · `3e0aac53a2f5f408a89a957d75430f6ec4084497` |
| 고정 버전 | `3e0aac53a2f5f408a89a957d75430f6ec4084497` |
| pin과 최신 HEAD | 조사일 동일 |
| 로컬 gitlink | [`multi-agent-tools/cline`](../../multi-agent-tools/cline/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | `I2`: parent gitlink, official branch HEAD와 fixed tree가 일치 |
| 유지보수 관찰 | archived/disabled가 아니고 조사일 push 관찰. 각 surface release parity는 미확인 |
| license | fixed [`LICENSE`](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/LICENSE#L1-L20)의 Apache-2.0 text와 GitHub SPDX metadata 일치 |

## 기술 구조

| 구성 | 책임 | fixed-SHA 근거 |
|---|---|---|
| Shared agent core/SDK | CLI·Kanban·VS Code·JetBrains surface가 사용하는 agent engine과 extension hooks | [README SDK](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L110-L136) |
| CLI/TUI | terminal, headless mode, provider/model과 command surface | [README CLI](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L43-L49) |
| VS Code/JetBrains | editor diff·approval UX; JetBrains plugin source는 이 repo에 공개되지 않음 | [surface table](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L132-L136) |
| ACP adapter | session/capability와 tool approval을 ACP client에 투영 | [AcpAgent](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/acpAgent.ts#L106-L130), [permission bridge](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/permissions.ts#L33-L45) |
| MCP/checkpoint/subagent | MCP server 관리, workspace diff/restore, scoped subagent config | [MCP service](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/mcp.proto#L11-L23), [checkpoint service](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/checkpoints.proto#L11-L20), [agent config](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/src/core/task/tools/subagent/AgentConfigLoader.ts#L11-L30) |

## 역할과 연동

- AgentRole: Worker, IDE assistant, ACP agent, subagent coordinator
- Capability: `multi-surface-agent`, `tool-approval`, `checkpoint-diff-restore`, `mcp-management`, `subagent-config`, `provider-abstraction`
- Integration: CLI/TUI, VS Code host, JetBrains client, ACP, MCP, gRPC/protobuf host bridge, SDK/plugin hooks
- SecurityOperationalRequirement: surface capability negotiation, default-deny approval, MCP trust, checkpoint scope, provider credential isolation, external verifier

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `cline-multi-surface-core` | architecture | CLI, VS Code, JetBrains, SDK/Hub가 같은 agent core 계열을 서로 다른 surface로 노출한다. | [README](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L110-L136) | `I2` | `V2` | `W0` | partial pass. JetBrains plugin source는 공개되지 않음 |
| `cline-acp-agent` | interface | CLI가 ACP session/capability와 tool approval adapter를 구현한다. | [AcpAgent](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/acpAgent.ts#L106-L130), [permission translation](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/permissions.ts#L33-L45) | `I2` | `V2` | `W0` | pass(정적). ACP conformance runtime 미검증 |
| `cline-approval-fail-closed` | security | ACP permission은 allow once/always와 reject를 구분하고 unknown/failed request는 reject한다. | [options](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/permissions.ts#L15-L30), [response handling](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/permissions.ts#L69-L85), [request failure](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/permissions.ts#L115-L128) | `I2` | `V2` | `W0` | pass(정적). auto-approve 설정 시 경계가 완화됨 |
| `cline-checkpoint-surface` | capability | latest checkpoint 대비 multi-file diff, count, restore RPC surface가 있다. | [checkpoint proto](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/checkpoints.proto#L11-L27), [README UX](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L139-L140) | `I2` | `V2` | `W0` | pass(정적). rollback correctness와 untracked handling 미검증 |
| `cline-mcp-subagent` | capability | MCP server/tool 관리와 tool/model/skill이 명시된 subagent config가 있다. | [MCP service](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/mcp.proto#L11-L23), [subagent schema](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/src/core/task/tools/subagent/AgentConfigLoader.ts#L11-L30) | `I2` | `V2` | `W0` | pass(정적). recursive authority/resource bounds 미검증 |
| `cline-surface-parity-limit` | limitation | surface별 구현·공개 범위가 다르고 JetBrains source는 이 repository에 없다. | [surface table](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L132-L136) | `I2` | `V2` | `W0` | confirmed limitation; capability negotiation 필요 |

## Interface와 protocol

| 표면 | 계약 | 권한·상태 경계 | 근거 |
|---|---|---|---|
| CLI/TUI/headless | terminal agent surface | local shell/workspace와 provider credential | [README](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/README.md#L43-L49) |
| ACP | initialize, session, prompt, permission | client-mediated tool approval; auto-approve 별도 | [AcpAgent](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/cli/src/acp/acpAgent.ts#L106-L130) |
| MCP | server CRUD/auth/update stream/tool auto-approve | server별 credential·tool allow scope | [MCP proto](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/mcp.proto#L11-L23) |
| Host bridge | protobuf/gRPC services for editor host | surface별 capability 차이 | [checkpoint proto](https://github.com/cline/cline/blob/3e0aac53a2f5f408a89a957d75430f6ec4084497/apps/vscode/proto/cline/checkpoints.proto#L11-L27) |

## 운영·보안·trust boundary

- surface 이름이 같아도 CLI/VS Code/JetBrains/Hub의 tool, approval, checkpoint, provider capability가 동일하다고 가정하지 않는다.
- MCP server와 subagent는 별도 principal/resource budget으로 기록하고 recursive tool authority를 상속하지 않는다.
- auto-approve는 편의 설정이지 safety proof가 아니며 외부 write·merge는 `proposal → policy/verifier/human → committer` 단계로 분리한다.
- provider/MCP credential은 audience-scoped opaque handle로 surface에 전달하고 durable history/checkpoint에 원문을 저장하지 않는다.

## 플랫폼과 Windows

- 이번 fixed-source 범위에서 Windows 전용 implementation path를 평가하지 않았고 Windows build/runtime도 수행하지 않았다.
- VS Code/JetBrains/CLI가 Windows에서 설치 가능하다는 일반 제품 표면을 native process·shell·path correctness로 승격하지 않아 `W0`다.
- Windows shell quoting, process tree, CRLF/long path, checkpoint restore를 별도 `W2/W3`로 검증해야 한다.

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `cline-origin-20260814` | parent gitlink와 GitHub repo/branch/license metadata | pass | `cline/cline@3e0aac53a2f5f408a89a957d75430f6ec4084497` | origin과 ToolVersion |
| `cline-fixed-static-20260814` | fixed README, ACP, protobuf, subagent config 정적 검토 | partial pass | 위 fixed permalinks | 모든 `V2` Claims |
| `cline-v3plus-none` | build/runtime/ACP/MCP/editor/E2E/Windows 미실행 | unknown | 없음 | `V3+`, `W2+` 없음 |

병렬 조사 worktree submodule 본문은 비어 있어 로컬 본문을 읽지 않았다. parent `.gitmodules`+`git ls-tree`와 official GitHub fixed-SHA tree/metadata에서만 `I2/V2`를 수집했다.

## 강점과 한계

- 강점: `cline-multi-surface-core`는 동일 agent 기능을 여러 host에 투영할 때 capability negotiation 비교 기준이 된다.
- 강점: `cline-acp-agent`, `cline-approval-fail-closed`, `cline-checkpoint-surface`가 structured adapter·human approval·recovery UX 근거를 제공한다.
- 한계: `cline-surface-parity-limit` 때문에 surface 이름만으로 동일 capability나 release 상태를 추정할 수 없다.
- 한계: checkpoint는 recovery surface이지 Git merge correctness, sandbox, independent verification이 아니다.

## AX 설계 재료

| 구분 | 연결 Claim | 사내 AX 플랫폼에서의 사용 |
|---|---|---|
| Borrow | `cline-acp-agent`, `cline-approval-fail-closed` | ACP adapter와 explicit allow/reject UX |
| Adapt | `cline-multi-surface-core`, `cline-checkpoint-surface` | surface capability negotiation과 recoverable diff UX |
| Avoid | `cline-surface-parity-limit`, `cline-mcp-subagent` | surface parity 가정과 MCP/subagent 권한의 암묵 상속 |
| Build | `cline-approval-fail-closed`, `cline-surface-parity-limit` | per-surface conformance, scoped credential handle, independent verifier/committer |

회사별 IDE/CLI 허용 범위, repository 데이터 분류, provider/MCP 승인, auto-approve 정책, checkpoint retention은 `unknown/decision item`이다. 이 프로필은 Codex와 비교하는 AX 설계 재료이지 벤더 최종 선정이 아니다.

## 도입 판단

- 결정: 참고
- 적용 범위: primary Codex adapter와 비교할 multi-surface/ACP adapter, approval·checkpoint UX
- 이유: adapter 표면은 풍부하지만 surface parity, auto-approve, closed JetBrains source와 Windows runtime 공백이 있다.
- 재검토 조건: ACP conformance, CLI/VS Code capability diff, malicious MCP, checkpoint restore failure, Windows W2

## 다음 검증

| Item ID | 목표 Claim/등급 | 환경·시나리오 | 통과 기준 | 보존 artifact |
|---|---|---|---|---|
| `cline-v4-acp` | `cline-acp-agent` / `V4` | initialize/session/prompt/cancel/permission | protocol fixture와 상태 일치 | transcript, versions, exit codes |
| `cline-v5-permission` | `cline-approval-fail-closed` / `V5` | unknown response, disconnect, auto-approve drift, malicious MCP | 비승인 tool 실행 0 | decision/event logs |
| `cline-w2-surfaces` | Windows 상태 / `W2` | Windows CLI+VS Code shell/checkpoint | quoting, process cleanup, restore acceptance 통과 | environment, logs, workspace hashes |

## 관계와 변경 이력

- `ToolVersion FITS_ROLE Worker/IDEAssistant/ACPAgent`
- `ToolVersion PROVIDES multi-surface-agent/tool-approval/checkpoint`
- `ToolVersion SUPPORTS ACP/MCP/gRPC`
- `Project EVALUATES ToolVersion`
- 2026-08-14: official GitHub fixed-SHA 정적 프로필 작성. `I2 / V2 / W0`; runtime 미수행.
