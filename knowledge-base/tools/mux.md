---
id: tool-mux
type: tool-profile
title: Mux
status: observed
profile_schema_version: 2
tool_key: mux
tool_version_id: tool-version:mux@92e563e57a5778e197fc1ed48b6d24ea64d38d3f
tags: [knowledge-base, tool, multiplexer, acp, policy]
official_upstream: https://github.com/coder/mux
license: AGPL-3.0-only
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 8b32804322e7fa373f93127fc6d6654df1493b86
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 92e563e57a5778e197fc1ed48b6d24ea64d38d3f
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# Mux

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

Mux는 local/worktree/SSH compute에서 여러 coding agent를 Plan/Exec UX로 운용하고 ACP/MCP/CLI/HTTP/WebSocket 표면과 조직 정책을 결합하는 Electron multiplexer다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/coder/mux` · `main` / `8b32804322e7fa373f93127fc6d6654df1493b86` (2026-08-15) |
| 고정 버전 / gitlink | `92e563e57a5778e197fc1ed48b6d24ea64d38d3f` (`v0.28.3-nightly.1` 관찰) · [`multi-agent-tools/mux`](../../multi-agent-tools/mux/) |
| pin 관계 | upstream이 pin 이후 이동. tag 관찰과 default-branch current state는 fixed ToolVersion과 분리 |
| license | [AGPL-3.0 LICENSE](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/LICENSE#L1-L20); 코드 재사용 전 법무/네트워크 제공 의무 검토 필요 |
| provenance limitation | parent gitlink와 official fixed-SHA README/source tree 정적 검토. 일부 source locator는 directory-level이며 build/runtime/E2E 미실행 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Desktop/browser UI | parallel agent workspace, status, cost, Plan/Exec | [README](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md#L18-L36), [status/cost](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md#L57-L74) |
| Runtime broker | local worktree 또는 SSH compute 선택 | [runtime overview](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md#L18-L32) |
| Adapter/API layer | ACP stdio, MCP, CLI, HTTP/WebSocket | [fixed source tree](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src) |
| Admin policy | provider/model/runtime gate와 last-known-good startup policy | [fixed policy source tree](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src) |

## 역할과 연동

- AgentRole: Planner, Worker Supervisor, Runtime Broker, Policy Control Surface.
- Capability: `parallel-agent-workspace`, `runtime-selection`, `agent-status-cost`, `admin-capability-policy`, `acp-mcp-adapters`.
- Integration: Electron/browser, ACP stdio, MCP, CLI, HTTP/WebSocket, git worktree, SSH.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `mux-parallel-runtime` | architecture | local/worktree/SSH compute에서 parallel agent workspace를 제공한다. | [README](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md#L18-L36) | `I2` | `V2` | `W1` | 정적 pass; runtime parity 미검증 |
| `mux-derived-status-cost` | capability | sidebar status와 token/cost UI를 제공한다. | [README](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md#L57-L74) | `I2` | `V2` | `W1` | agent-reported/derived projection이며 billing·completion proof가 아님 |
| `mux-admin-policy` | security | provider/model/runtime allow gate와 fail-closed startup/last-known-good 정책 경로가 있다. | [fixed policy source](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src) | `I2` | `V2` | `W1` | directory-level locator; 실제 policy enforcement E2E 미검증 |
| `mux-plaintext-secrets` | limitation | fixed source가 `~/.mux/secrets.json` plaintext 저장·자동 주입 경로를 가진다. | [fixed source tree](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src) | `I2` | `V2` | `W1` | 사내 secret governance 패턴으로 채택 금지 |
| `mux-windows-static` | platform | Electron/Windows/WSL 판별과 packaging source가 있다. | [desktop source](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src/desktop/main.ts#L663-L711) | `I2` | `V2` | `W1` | native Windows agent runtime proof 없음 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| Agent adapter | ACP stdio / MCP / agent-specific loop | workspace → runtime/agent | adapter capability와 approval parity를 conformance로 확인해야 함 | [source tree](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src) |
| Control API | CLI + HTTP/WebSocket | human/automation → workspace | actor identity, remote exposure, external-write scope 별도 정책 필요 | [CLI source](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/src/cli/index.ts#L133-L149) |

## 운영·보안·trust boundary

- UI/policy registry, local host, SSH host, agent adapter, SCM committer는 서로 다른 authority domain이다.
- plaintext secret auto-injection은 audience·TTL·revocation·log redaction을 보장하지 않는다. 사내 플랫폼은 opaque handle과 run-scoped materialization을 사용해야 한다.

## 플랫폼과 Windows

- `W1 narrow`: Windows packaging/WSL detection source만 확인했다. native agent process tree, cancellation, SSH/local parity, sandbox는 W2/W3 미확인이다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `mux-static-20260815` | `I2/V2/W1` | parent pin + official fixed source | partial pass | 일부 locator directory-level; runtime 없음 |
| `mux-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | artifact 없음 |

## 강점과 한계

- 강점: runtime/provider/model policy, adapter surface, cost/status UX를 통합한다.
- 한계: AGPL 재사용 경계와 plaintext secret auto-injection, UI-derived 상태, Windows runtime 미검증이 있다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | fail-closed provider/model/runtime policy와 last-known-good | `mux-admin-policy` | `AX-N-POLICY-GOVERNANCE` |
| Adapt | status/cost UI를 evidence ledger 관찰값에 연결 | `mux-derived-status-cost` | 실제 cost/latency는 실행 record에서만 확정 |
| Avoid | plaintext file secret와 자동 전역 주입 | `mux-plaintext-secrets` | `AX-N-SECRET-GOVERNANCE` |
| Build | short-lived audience-scoped secret broker + policy receipt | 위 Claims | `AD-OPAQUE-CREDENTIAL` / `RM-SECRET-BROKER` |

## 도입 판단

- 결정: policy/UX clean-room 참고; AGPL 코드는 reference only. 최종 vendor 선택이 아니다.
- 재검토: 법무 검토, exact policy/secrets locator 보강, Windows runtime, policy bypass failure injection.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `mux-v3-build` | fixed version | `V3/W2` | Windows package build/launch |
| `mux-v5-policy` | admin policy | `V5` | invalid/stale policy에서 agent start 0; signed LKG audit |
| `mux-v5-secret` | secret flow | `V5` | non-audience process/log에 secret 노출 0 |

## 관계와 변경 이력

- `Capability admin-capability-policy ADDRESSES AXNeed AX-N-POLICY-GOVERNANCE`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
