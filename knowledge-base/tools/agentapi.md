---
id: tool-agentapi
type: tool-profile
title: AgentAPI
status: observed
tags:
  - knowledge-base
  - tool
  - http
  - sse
  - pty
  - windows
official_upstream: https://github.com/coder/agentapi
license: MIT
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 9ff117e231822f670305254ef24f6389f75953f4
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# AgentAPI

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md) · [ACP](./agent-client-protocol.md)

## 한 줄 역할

AgentAPI는 구조화 protocol이나 SDK가 없는 interactive coding-agent CLI를 PTY screen 관찰로 감싸 HTTP/OpenAPI와 SSE message/status event로 노출하는 fallback bridge다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/coder/agentapi` |
| 기본 브랜치와 고정 버전 | `main` · `9ff117e231822f670305254ef24f6389f75953f4` |
| 로컬 gitlink | [`multi-agent-tools/agentapi`](../../multi-agent-tools/agentapi/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 현재 upstream 관찰 | GitHub `main` HEAD가 고정 버전과 같은 `9ff117e231822f670305254ef24f6389f75953f4`였다. archived/disabled가 아니며 마지막 push 관찰은 2026-05-27 UTC다. 장기 maintenance 보장은 아니다. |
| 출처 무결성 | `I2`: parent [`.gitmodules`](../../.gitmodules) URL과 `git ls-tree` gitlink SHA, official fixed-SHA GitHub tree/blob를 대조했다. |
| license | fixed SHA root [`LICENSE`](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/LICENSE#L1-L7)의 MIT grant와 GitHub metadata가 일치한다. |

## 기술 구조

- Go HTTP server가 message/status/history/event endpoint와 generated OpenAPI를 제공한다.
- SSE emitter가 message, status, screen, agent-error event를 fan-out하며 bounded channel이 가득 차면 subscriber를 끊는다.
- PTY conversation이 일정 간격 screen snapshot을 만들고 polling·diff·stability heuristic으로 prompt 처리 시작·종료와 message 경계를 추정한다.
- build-tagged Windows process/signal 파일이 PID liveness와 Ctrl+C shutdown 차이를 처리한다.

## 역할과 연동

- AgentRole: Legacy CLI adapter, PTY bridge, HTTP gateway
- Capability: `agent-http-control`, `conversation-history`, `sse-events`, `pty-screen-tracking`, `status-heuristic`, `openapi`
- Integration: HTTP/JSON, OpenAPI, SSE, PTY/TUI, local web chat
- SecurityOperationalRequirement: loopback binding, allowed-host/origin 최소화, 별도 authentication/TLS, agent credential와 process authority 격리, heuristic result에 confidence/freshness 표시

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `agentapi-http-sse` | `/messages`, `/message`, `/status`, `/events` HTTP surface와 SSE event stream을 제공한다. | [README endpoints](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/README.md#L78-L87), [server transport](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/httpapi/server.go#L23-L57) | `V2` | `W0` | pass(정적). live HTTP/SSE 연결은 미실행 |
| `agentapi-event-backpressure` | message/status/screen/error event를 bounded subscriber channel로 보내며 소비자가 drain하지 않으면 연결을 해제한다. | [event types](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/httpapi/events.go#L17-L36), [fan-out policy](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/httpapi/events.go#L140-L160) | `V2` | `W0` | pass(정적). reconnect cursor·lossless replay 계약은 확인되지 않음 |
| `agentapi-pty-heuristic` | PTY screen polling/diff와 stability window로 conversation 상태·message를 추정한다. | [PTY model](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/screentracker/pty_conversation.go#L20-L38), [snapshot/stability state](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/screentracker/pty_conversation.go#L94-L167) | `V2` | `W0` | pass(구현 존재). typed protocol보다 낮은 신뢰도의 heuristic fallback |
| `agentapi-tui-drift-risk` | TUI 구조 변화 시 extra element 제거 logic이 갱신되어야 하고 terminal artifact가 message에 섞일 수 있다고 문서가 경고한다. | [README limitation](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/README.md#L180-L192) | `V1` | `W0` | confirmed limitation. vendor TUI regression corpus 필요 |
| `agentapi-network-boundary` | allowed host와 CORS origin을 설정하지만 wildcard도 허용한다. 이 검사는 application authentication이나 TLS의 증거가 아니다. | [allowed hosts](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/README.md#L89-L110), [allowed origins](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/README.md#L113-L120), [host parser](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/httpapi/server.go#L118-L167) | `V2` | `W0` | confirmed limitation. 비-loopback 공개에는 별도 authn/authz/reverse proxy 필요 |
| `agentapi-windows-process-source` | Windows build-tagged source가 PID liveness를 best-effort로 낮추고 `os.Interrupt` shutdown handler를 둔다. | [Windows liveness](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/cmd/server/process_windows.go#L1-L10), [Windows signal handler](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/cmd/server/signals_windows.go#L1-L24) | `V2` | `W1` | pass(정적). 실제 Windows PTY/process tree 종료는 미실행 |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `agentapi-origin-20260814` | parent `.gitmodules` + `git ls-tree`, official GitHub metadata와 fixed commit 비교 | pass | `coder/agentapi@9ff117e231822f670305254ef24f6389f75953f4` | origin과 ToolVersion |
| `agentapi-static-20260814` | official fixed-SHA README/Go source/OpenAPI 관련 path 정적 검토 | partial pass | 위 fixed-SHA permalink | `V1/V2`, `W1` Claim |
| `agentapi-local-body-v3plus-none` | 조사 worktree submodule 본문이 비어 로컬 본문을 읽지 못했고 build/runtime/HTTP·SSE/agent E2E/Windows 실행을 수행하지 않음 | unknown | 없음 | `V3+`, `W2+` Claim 없음 |

## 강점과 한계

- 강점: protocol 없는 CLI를 작은 HTTP/SSE surface로 감싸 비교적 빠르게 통합할 수 있고 OpenAPI가 client 생성을 돕는다.
- 강점: PTY output, message history와 status를 한 adapter에 모으며 Windows-specific process/signal 차이를 source에 드러낸다.
- 한계: screen stability와 formatter는 vendor TUI output에 결합된다. `stable`은 agent correctness, tool completion, commit 또는 merge 증거가 아니다.
- 한계: allowed-host/CORS는 인증이 아니다. agent를 원격에 노출할 때 local CLI credential과 filesystem authority가 HTTP caller에게 확장될 수 있다.
- 한계: Windows liveness가 항상 false인 best-effort 경로이므로 stale PID와 process cleanup을 별도로 검증해야 한다.

## AX 설계 재료

- `Borrow`: `agentapi-http-sse`의 작은 HTTP/OpenAPI surface와 event fan-out을 protocol 없는 legacy CLI adapter의 외곽 계약으로 차용한다.
- `Adapt`: `agentapi-event-backpressure`, `agentapi-pty-heuristic`에 cursor, reconnect, loss 표시, confidence와 observed-at를 추가해 derived status임을 소비자에게 노출한다.
- `Avoid`: PTY `stable`을 task completion으로 사용하거나 wildcard host/origin을 authentication으로 간주하지 않는다(`agentapi-tui-drift-risk`, `agentapi-network-boundary`).
- `Build`: `agentapi-network-boundary`, `agentapi-tui-drift-risk`, `agentapi-windows-process-source`에 대응하는 격리된 executor, authenticated loopback proxy, vendor별 TUI golden/failure corpus, Windows process-tree cleanup fixture와 typed API/ACP로 승격 가능한 adapter selector를 구축한다.
- `unknown / decision item`: 회사가 허용할 legacy agent, HTTP 호출자 trust domain, prompt/output 데이터 분류, remote 노출 여부, 자동화 승인 범위는 확인되지 않았다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정이나 최종 구현 답이 아니라, 사내 AX adapter 우선순위 최하단의 PTY heuristic fallback(`typed API → ACP → JSON CLI → PTY heuristic`)과 legacy agent comparator를 설계하기 위한 재료
- 이유: `agentapi-http-sse`는 통합 비용을 낮추지만 `agentapi-pty-heuristic`, `agentapi-tui-drift-risk` 때문에 핵심 orchestration truth source로 채택하지 않는다.
- 재검토 조건: Go build `V3`, loopback HTTP/SSE `V4`, TUI golden corpus·event loss·cancel·restart `V5`, Windows ConPTY/process-tree/liveness `W2/W3`, authentication front door 설계

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE LegacyAdapter/HTTPGateway`
- `ToolVersion PROVIDES agent-http-control/sse-events/pty-screen-tracking`
- `ToolVersion SUPPORTS HTTP/OpenAPI/SSE/PTY`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: parent gitlink와 official fixed-SHA tree/blob를 대조해 `I2 / V2 / W1` 프로필 작성. local submodule body와 build/runtime/E2E는 미검증으로 보존.
