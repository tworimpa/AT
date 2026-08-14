---
id: tool-paseo
type: tool-profile
title: Paseo
status: observed
tags:
  - knowledge-base
  - tool
  - control-plane
  - multi-provider
  - windows
official_upstream: https://github.com/getpaseo/paseo
license: AGPL-3.0-reviewed-text
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: f0bd2c8483ff7961fdf6c0cd2070835741f6ac92
parent_repo_head: caaae4a47a127808eedac657c394b6a8fd9be460
---

# Paseo

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Paseo는 사용자가 이미 설치·인증한 여러 coding-agent CLI를 로컬 daemon이 실행·관제하고, desktop·mobile·web·CLI와 SDK에서 같은 agent/workspace 표면으로 다루게 하는 local-first control plane이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/getpaseo/paseo` |
| 기본 브랜치와 고정 버전 | `main` · `f0bd2c8483ff7961fdf6c0cd2070835741f6ac92` |
| 로컬 gitlink | [`multi-agent-tools/paseo`](../../multi-agent-tools/paseo/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | `I2`: 사용자 지정 공식 URL, GitHub 기본 브랜치 HEAD, shallow checkout, `.gitmodules` URL과 gitlink SHA 일치 확인 |
| 유지보수 관찰 | GitHub API에서 archived/disabled가 아니고 조사일에도 push가 관찰됨. 장기 안정성이나 support SLA의 증거는 아님 |
| license | root [`LICENSE`](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/LICENSE)는 third-party component의 원 라이선스를 보존하고 나머지를 AGPLv3로 둔다. 일부 package metadata는 `AGPL-3.0-or-later`이므로 파일별 재사용 전 재확인 필요 |

## 역할과 연동

- AgentRole: Gateway, Scheduler/Coordinator 보조, Executor supervisor, Relay, human control surface
- Capability: `multi-provider-agent-control`, `agent-lifecycle`, `workspace-worktree`, `agent-parentage`, `permission-response`, `scheduled-agent`, `cross-device-control`, `terminal-stream`
- Integration: WebSocket, TypeScript SDK, CLI, MCP, ACP provider adapter, provider-native adapters, optional E2EE relay
- SecurityOperationalRequirement: local process 권한·provider credential scope·network binding·relay trust anchor·worktree와 sandbox의 구분·AGPL 재사용 검토 필요

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `paseo-local-control-plane` | daemon이 agent process를 관리하고 desktop/mobile/web/CLI client가 WebSocket으로 관찰·제어한다. | [architecture](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/docs/architecture.md), [WebSocket transport](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/client/src/daemon-client-websocket-transport.ts) | `V2` | `W0` | pass(정적). 실제 daemon/client 연결은 미실행 |
| `paseo-provider-adapters` | native adapter와 generic ACP adapter로 여러 외부 agent CLI를 공통 lifecycle/capability 표면에 연결한다. | [provider docs](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/providers.md), [ACP client](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/server/src/server/agent/providers/acp-agent.ts#L788) | `V2` | `W0` | pass(정적). provider별 실제 capability와 CLI 버전 호환성은 미검증 |
| `paseo-orchestration-tools` | MCP/native tool catalog가 agent 생성·prompt·취소, workspace/worktree, terminal, schedule, permission 응답을 노출한다. | [MCP reference](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/mcp.md), [MCP adapter](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/server/src/server/agent/mcp-server.ts) | `V2` | `W0` | pass(정적). 독립 verifier나 merge correctness를 이 catalog만으로 보장하지 않음 |
| `paseo-worktree-boundary` | workspace는 local 또는 Git worktree가 될 수 있고 agent parentage와 workspace placement를 분리한다. | [worktree docs](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/worktrees.md), [MCP mental model](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/mcp.md) | `V2` | `W0` | pass(정적). worktree는 파일 상태 격리이며 OS 권한·credential·network sandbox가 아님 |
| `paseo-relay-crypto` | optional relay transport는 Curve25519 기반 shared key와 XSalsa20-Poly1305 authenticated encryption을 구현한다. | [crypto implementation](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/relay/src/crypto.ts#L1), [security model](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/security.md) | `V2` | `W0` | pass(구현 존재). 실제 relay E2E, key rotation, 공격·replay fixture는 이번 조사에서 미실행 |
| `paseo-windows-source` | Windows executable 탐색, `.cmd/.bat`·cmd.exe escaping, ConPTY launch path와 Electron 개발 경로가 구현돼 있다. | [Windows resolution](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/server/src/executable-resolution/windows.ts#L20), [ConPTY command resolution](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/server/src/terminal/terminal.ts#L235), [desktop scripts](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/packages/desktop/package.json#L17) | `V2` | `W1` | pass(정적). Windows build/runtime/E2E를 실행하지 않았으므로 `W2/W3` 아님 |
| `paseo-host-authority-limit` | agent CLI는 정상 사용자 subprocess로 실행되고 기존 provider credential을 사용하므로 Paseo 자체가 host sandbox나 credential broker를 제공한다고 볼 수 없다. | [provider model](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/providers.md), [security guidance](https://github.com/getpaseo/paseo/blob/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92/public-docs/security.md) | `V2` | `W0` | confirmed limitation. 민감 작업은 별도 OS/container/VM 정책과 scoped credentials 필요 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `paseo-origin-20260814` | GitHub repo API, `git ls-remote --symref`, shallow clone, gitlink 비교 | pass | `getpaseo/paseo@f0bd2c8483ff7961fdf6c0cd2070835741f6ac92` | origin과 ToolVersion |
| `paseo-static-20260814` | README/docs/config/source/test path 정적 검토 | partial pass | 위 fixed-SHA permalink | 모든 `V2` Claim |
| `paseo-v3plus-none` | install/build/runtime/agent E2E/Windows 실행을 수행하지 않음 | unknown | 없음 | `V3+`, `W2+` Claim 없음 |

## 강점과 한계

- 강점: multi-provider agent lifecycle, cross-device 관제, worktree-aware workspace, MCP/ACP/SDK/CLI 표면, permission과 schedule을 한 daemon 모델에 모은다.
- 강점: Windows 전용 executable/ConPTY/`.cmd` 처리와 테스트 경로가 있어 Windows-first 구현 비교에 유용하다.
- 한계: external coding agent 자체를 제공하지 않고 설치·인증된 CLI에 의존한다. adapter별 capability와 버전 호환성을 별도로 확인해야 한다.
- 한계: local agent는 사용자 권한과 기존 credential로 실행된다. worktree, PTY, E2EE relay는 각각 파일 분리, I/O, 전송 보호이며 process/credential sandbox가 아니다.
- 한계: AGPL 계열이므로 제품 코드 직접 통합보다 공개 protocol·상태 모델 비교와 clean-room 패턴 참조를 기본으로 둔다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: Windows local control plane과 cross-device agent supervision 비교, WebSocket/MCP/ACP surface 및 worktree/permission UX의 clean-room 참고
- 이유: `paseo-local-control-plane`, `paseo-provider-adapters`, `paseo-windows-source`는 현재 청사진과 직접 비교 가치가 크다. 다만 `paseo-host-authority-limit`, AGPL, `V3+` 미실행 때문에 핵심 runtime 의존 채택은 아직 이르다.
- 재검토 조건: 고정 ToolVersion을 갱신할 때 license/NOTICE 재검사, Windows `W2` build/runtime pilot, Codex·Claude lifecycle/permission/cancel E2E, worktree cleanup 실패 주입, relay security fixture

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE Gateway/ExecutorSupervisor/Relay`
- `ToolVersion PROVIDES multi-provider-agent-control/workspace-worktree/permission-response`
- `ToolVersion SUPPORTS WebSocket/SDK/CLI/MCP/ACP/E2EE-relay`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: 공식 `main` HEAD를 shallow fixed-SHA gitlink로 추가하고 문서·소스 정적 근거를 `I2 / V2 / W1`로 기록. build/runtime/E2E는 미수행으로 보존.
