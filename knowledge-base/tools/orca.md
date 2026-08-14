---
id: tool-orca
type: tool-profile
title: Orca
status: observed
tags:
  - knowledge-base
  - tool
  - desktop
  - worktree
  - terminal
  - control-plane
official_upstream: https://github.com/stablyai/orca
license: MIT
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: e7b85266f531f9a219dff59d8647f86585b4fc7e
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Orca

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Orca는 여러 coding-agent CLI를 각 Git worktree와 terminal에 배치하고 desktop·mobile·CLI에서 작업, diff, PR과 사람 개입 지점을 한 화면으로 관제하는 human-visible agent development environment다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/stablyai/orca` |
| 기본 브랜치와 고정 버전 | `main` · `e7b85266f531f9a219dff59d8647f86585b4fc7e` |
| 로컬 gitlink | [`multi-agent-tools/orca`](../../multi-agent-tools/orca/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 현재 upstream 관찰 | GitHub `main`은 조사 시 `cb42b60849d81ff58976200baa6b89dc5df99fb7`로 고정 버전보다 앞서 있었다. archived/disabled가 아니고 같은 날 push가 관찰됐다. |
| 출처 무결성 | `I2`: parent [`.gitmodules`](../../.gitmodules) URL과 `git ls-tree` gitlink SHA를 확인하고 official fixed-SHA GitHub tree/blob를 대조했다. |
| package 관찰 | fixed SHA [`package.json`](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/package.json#L1-L11)은 `1.4.178-rc.2`와 Electron main/CLI entry를 기록한다. release 안정성 보장은 아니다. |
| license | fixed SHA root [`LICENSE`](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/LICENSE#L1-L13)의 MIT text와 GitHub metadata가 일치한다. |

## 기술 구조

- Electron desktop main/renderer와 CLI가 local runtime RPC를 통해 worktree, terminal, agent session, browser, source-control surface를 공유한다.
- worktree command surface가 create/list/show/remove, parent lineage, startup agent/prompt와 CLI provenance를 명시적으로 전달한다.
- terminal surface가 create/read/send/wait/split/stop 등을 structured RPC로 노출하며 interactive TUI는 renderer-backed terminal path를 선택할 수 있다.
- desktop/mobile의 task·terminal·diff·PR 표시는 여러 underlying state를 사람이 읽기 좋게 projection한다. 이 UI는 관제 surface이지 독립 verifier가 아니다.

## 역할과 연동

- AgentRole: Human control surface, Worktree/Terminal fleet supervisor, Relay, Review workspace
- Capability: `parallel-worktree`, `terminal-fleet`, `agent-lineage`, `diff-annotation`, `mobile-supervision`, `cli-control`, `human-attention-routing`
- Integration: Electron desktop, local runtime RPC, CLI JSON/text, PTY terminal, Git/GitHub/Linear, SSH, mobile companion
- SecurityOperationalRequirement: worktree와 OS sandbox 구분, terminal process/credential authority, destructive remove approval, UI freshness/provenance, remote/mobile transport trust

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `orca-worktree-fleet` | 여러 agent를 별도 Git worktree에서 병렬 실행·비교하는 desktop workflow를 제공한다. | [README role](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L18-L21), [parallel worktrees](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L49-L57), [CLI create contract](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/worktree.ts#L198-L257) | `V2` | `W0` | pass(정적). agent parallel E2E와 merge correctness는 미검증 |
| `orca-terminal-control` | terminal list/read/send/wait/create/stop을 structured runtime call로 노출하고 unsatisfied wait를 nonzero exit로 표시한다. | [terminal handlers](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/terminal.ts#L54-L114), [terminal create](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/terminal.ts#L129-L149) | `V2` | `W0` | pass(정적). terminal output가 task completion proof는 아님 |
| `orca-human-review-surface` | diff annotation, PR/issues, terminal과 mobile follow-up을 같은 작업 표면에 모은다. | [GitHub/Linear](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L91-L100), [diff annotation](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L119-L127), [mobile companion](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L35-L43) | `V2` | `W0` | pass(정적 구조+문서). 실제 notification, PR write, mobile auth는 미검증 |
| `orca-ui-derived-not-proof` | 화면의 agent 상태, diff, PR과 terminal은 underlying source를 읽기 쉽게 투영한 것으로, UI 표시 자체가 commit/CI/review/merge 또는 agent correctness의 독립 evidence가 아니다. | [feature surfaces](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L29-L158), [CLI terminal result surface](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/terminal.ts#L54-L114) | `V2` | `W0` | design limitation. source SHA, CI provider, review API와 verifier evidence를 별도 보존해야 함 |
| `orca-worktree-not-sandbox` | worktree는 branch/file-state 분리이며 terminal agent의 process, network, credential 권한을 제한하는 security sandbox로 볼 수 없다. | [worktree create fields](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/worktree.ts#L198-L257), [terminal command launch](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/terminal.ts#L129-L149) | `V2` | `W0` | confirmed limitation. separate executor sandbox와 scoped secrets 필요 |
| `orca-destructive-remove-boundary` | `worktree rm --force`는 PTY stop proof까지 waive할 수 있으므로 automation에서 destructive approval boundary가 필요하다. | [remove handler](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/cli/handlers/worktree.ts#L279-L289) | `V2` | `W0` | pass(정적). cleanup failure injection 미실행 |
| `orca-windows-claim-only` | README와 build scripts가 Windows distribution을 언급하지만 이번 조사에서는 Windows implementation/runtime을 검증하지 않았다. | [platform badge/install](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L5-L12), [Windows download](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/README.md#L210-L216) | `V1` | `W0` | 문서 주장만 인정. `W1/W2/W3`로 승격하지 않음 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `orca-origin-20260814` | parent `.gitmodules` + `git ls-tree`, official GitHub metadata와 fixed commit 비교 | pass | `stablyai/orca@e7b85266f531f9a219dff59d8647f86585b4fc7e` | origin과 ToolVersion |
| `orca-static-20260814` | official fixed-SHA README/package/CLI source 정적 검토 | partial pass | 위 fixed-SHA permalink | `V1/V2` Claim |
| `orca-local-body-v3plus-none` | 조사 worktree submodule 본문이 비어 로컬 본문을 읽지 못했고 install/build/desktop/runtime/agent E2E/Windows 실행을 수행하지 않음 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

## 강점과 한계

- 강점: worktree, terminal, diff/PR과 사람 attention을 한 fleet UI/CLI에 연결해 다중 agent 운영을 사람이 추적하기 쉽다.
- 강점: CLI가 worktree lineage, terminal wait와 JSON-friendly RPC를 제공해 외부 coordinator가 UI와 같은 surface를 사용할 수 있다.
- 한계: human-visible projection은 source-of-truth event나 verifier proof가 아니다. stale terminal/status와 provider API freshness를 분리해야 한다.
- 한계: worktree는 isolation처럼 보이지만 credential/network/process sandbox가 아니다. `--force` cleanup은 승인과 복구 경계가 필요하다.
- 한계: Windows 배포 주장은 있으나 이번 증거는 `W0`이며 실제 Windows build/runtime을 의미하지 않는다.

## AX 설계 재료

- `Borrow`: `orca-worktree-fleet`, `orca-terminal-control`, `orca-human-review-surface`의 worktree/terminal lineage와 사람이 이해할 수 있는 attention surface를 차용한다.
- `Adapt`: 모든 UI card와 terminal wait에 source SHA, event cursor, observed-at, confidence, verifier evidence를 붙여 `orca-ui-derived-not-proof` 경계를 화면에서도 보존한다.
- `Avoid`: worktree를 security sandbox로, terminal output·green UI를 task/commit/CI/merge proof로, `--force` cleanup을 무승인 자동화로 사용하지 않는다(`orca-worktree-not-sandbox`, `orca-destructive-remove-boundary`).
- `Build`: `orca-ui-derived-not-proof`, `orca-worktree-not-sandbox`, `orca-destructive-remove-boundary`에 대응하는 run/session truth kernel, evidence store, policy/verifier/human approval gate, scoped executor·secret broker와 cleanup reconciliation을 구축한다.
- `unknown / decision item`: 회사의 remote/mobile 허용 범위, worktree retention, destructive action 승인자, repository/credential 분류와 UI에 표시 가능한 데이터는 확인되지 않았다.

## 도입 판단

- 결정: 채택
- 적용 범위: 벤더 선정이나 최종 구현 답이 아니라, 사내 AX의 human-visible worktree/terminal fleet surface, CLI control과 attention routing UX를 설계하기 위한 재료. execution truth는 별도 kernel/verifier에 둔다.
- 이유: `orca-worktree-fleet`, `orca-terminal-control`, `orca-human-review-surface`는 운영자 관제에 강하다. `orca-ui-derived-not-proof`, `orca-worktree-not-sandbox`를 architecture boundary로 유지한다.
- 재검토 조건: current upstream pin 갱신, desktop/CLI build `V3`, agent/worktree/terminal lifecycle `V4`, stale projection·remove failure·PR drift E2E `V5`, Windows build/ConPTY/process cleanup `W2/W3`

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE HumanControlSurface/WorktreeSupervisor/ReviewWorkspace`
- `ToolVersion PROVIDES parallel-worktree/terminal-fleet/diff-annotation/human-attention-routing`
- `ToolVersion SUPPORTS Electron/CLI/runtime-RPC/PTY/GitHub/SSH/mobile`
- `Project SELECTS ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA tree/blob를 대조해 `I2 / V2 / W0` 프로필 작성. UI projection을 proof와 분리하고 local body/build/runtime/E2E 미검증을 보존.
