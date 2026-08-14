---
id: tool-hermes-agent
type: tool-profile
title: Hermes Agent
status: observed
tags:
  - knowledge-base
  - tool
  - personal-agent
  - gateway
  - windows
official_upstream: https://github.com/NousResearch/hermes-agent
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: c896c09c42910c584c4c7d2325b58c14713ea42c
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 1b1975781f372e4d7fe4f448eab86cea5441f2e7
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Hermes Agent

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Hermes Agent는 CLI/TUI와 여러 메시징 채널을 한 gateway에 연결하고, memory·skills·cron·subagent·terminal backend를 결합하는 장기 상태 personal-agent runtime이다.

## ToolVersion과 공식 최신 관찰

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/NousResearch/hermes-agent` |
| 조사일 기본 브랜치 HEAD | `main` · `c896c09c42910c584c4c7d2325b58c14713ea42c` |
| 고정 버전 | `1b1975781f372e4d7fe4f448eab86cea5441f2e7` |
| pin과 최신 HEAD | 조사일 최신 HEAD가 pin보다 4 commits 앞섬. 아래 주장은 pin 범위 |
| 로컬 gitlink | [`multi-agent-tools/hermes-agent`](../../multi-agent-tools/hermes-agent/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | `I2`: parent gitlink와 공식 GitHub fixed tree 일치 |
| 유지보수 관찰 | archived/disabled가 아니고 조사일 push 관찰. unattended automation의 운영 신뢰성 증거는 아님 |
| license | fixed [`LICENSE`](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/LICENSE#L1-L20)의 MIT text와 GitHub metadata 일치 |

## 기술 구조

| 구성 | 책임 | fixed-SHA 근거 |
|---|---|---|
| Agent loop/TUI | model 호출, tool dispatch, streaming terminal interaction | [README capability overview](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L23-L30) |
| GatewayRunner | configured channel adapter, authorization, session lifecycle을 한 process에서 관제 | [GatewayRunner](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/run.py#L6269-L6272) |
| Pairing/AuthZ | unknown DM sender를 one-time code와 operator approval로 등록 | [pairing contract](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/pairing.py#L1-L18) |
| Memory/skills | 장기 사용자·세션 지식과 procedural skill을 agent context에 연결 | [README](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L24-L29) |
| Cron scheduler | due job을 gateway background tick에서 실행하고 결과를 channel에 전달 | [scheduler contract](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/cron/scheduler.py#L1-L7) |
| Terminal backends | local/container/SSH/hosted sandbox로 command 실행 surface 제공 | [backend overview](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4f448eab86cea5441f2e7/README.md#L28-L30) |

## 역할과 연동

- AgentRole: Gateway, Relay, Scheduler, Personal Assistant, Executor frontend
- Capability: `multi-channel-intake`, `persistent-memory`, `scheduled-automation`, `subagent-delegation`, `multi-backend-terminal`, `dm-pairing`
- Integration: CLI/TUI, Telegram/Discord/Slack/WhatsApp/Signal/Email, MCP, ACP adapter, local/Docker/SSH/hosted sandbox backends
- SecurityOperationalRequirement: sender authorization, channel provenance, command approval, memory/skill integrity, scoped provider/tool credentials, unattended cron budget

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `hermes-multi-channel-gateway` | capability | 한 gateway process가 CLI와 여러 messaging platform의 대화를 연결한다. | [README](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L24-L29), [entry points](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L145-L150), [runner](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/run.py#L6269-L6272) | `I2` | `V2` | `W0` | pass(정적). 실제 channel 연결 미실행 |
| `hermes-memory-skill-loop` | capability | memory·session search·skill creation을 장기 agent context에 포함한다. | [README](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L24-L29) | `I2` | `V2` | `W0` | partial(정적). 품질·retention·poisoning 방어 미검증 |
| `hermes-cron-automation` | capability | gateway가 주기적으로 due cron job을 실행하는 scheduler를 포함한다. | [README](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L26-L29), [scheduler](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/cron/scheduler.py#L1-L7) | `I2` | `V2` | `W0` | pass(정적). unattended cost/failure recovery 미검증 |
| `hermes-pairing-boundary` | security | unknown sender에게 code를 발급하고 owner CLI approval로 authorize하는 pairing store가 있다. | [pairing design](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/pairing.py#L1-L18), [store](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/pairing.py#L405-L412) | `I2` | `V2` | `W0` | pass(정적). channel identity takeover·replay E2E 미검증 |
| `hermes-windows-service-path` | platform | Scheduled Task/Startup fallback와 Windows subprocess hiding/encoding 경로가 구현돼 있다. | [Windows backend](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/hermes_cli/gateway_windows.py#L1-L25), [schtasks spawn](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/hermes_cli/gateway_windows.py#L158-L175) | `I2` | `V2` | `W1` | pass(정적). Windows build/runtime 미실행 |
| `hermes-wide-trust-domain` | limitation | channel·memory·cron·skills·terminal이 한 personal gateway에 모여 coding worker보다 넓은 identity/credential/retention 경계를 가진다. | [feature aggregation](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L23-L30), [gateway runner](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/gateway/run.py#L6269-L6272) | `I2` | `V2` | `W0` | confirmed architectural limitation; code executor trust domain과 분리 필요 |

## Interface와 protocol

| 표면 | 계약 | trust/permission 경계 | 근거 |
|---|---|---|---|
| CLI/TUI | interactive conversation와 streaming tool output | local operator session | [README](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L23-L25) |
| Messaging gateway | platform message ↔ agent session | pairing/allowlist와 channel identity | [entry points](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/README.md#L145-L150) |
| MCP/ACP | external tools와 agent adapter | server/tool별 credential·approval 별도 | [integration index](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4f448eab86cea5441f2e7/README.md#L173-L179) |
| Cron | persisted schedule → agent/script → platform delivery | unattended authority·cost·recipient scope | [scheduler](https://github.com/NousResearch/hermes-agent/blob/1b1975781f372e4d7fe4f448eab86cea5441f2e7/cron/scheduler.py#L1-L7) |

## 운영·보안·trust boundary

- inbound channel text는 coding instruction이 아니라 provenance가 붙은 untrusted intake event로 취급해야 한다.
- pairing은 sender authorization의 한 층일 뿐 tool/terminal 권한, target repository, external write 승인을 뜻하지 않는다.
- memory와 skill은 다음 세션 prompt를 바꾸는 durable input이므로 poisoning·retention·삭제·source attribution 정책이 필요하다.
- cron은 사람이 없는 상태에서 channel과 tool을 호출할 수 있으므로 별도 budget, expiry, delivery audience와 kill switch가 필요하다.
- 플랫폼 통합에서는 gateway와 coding executor를 별도 trust domain으로 두고, provider/tool credential은 audience-scoped opaque handle로 전달하며 gateway가 원문을 보유·상속하지 않게 한다.

## 플랫폼과 Windows

- fixed source에 Windows 전용 gateway service, `schtasks`, console hiding·encoding 경로가 있어 `W1`이다.
- README의 native Windows 주장은 정적 문서 근거이며 실제 동작을 뜻하지 않는다.
- Windows 11 gateway, channel, cron, terminal backend를 실행하지 않아 `W2/W3`가 아니다.

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `hermes-origin-20260814` | parent gitlink와 GitHub repo/branch/compare/license metadata | pass | `NousResearch/hermes-agent@1b1975781f372e4d7fe4f448eab86cea5441f2e7` | origin과 ToolVersion |
| `hermes-fixed-static-20260814` | fixed README, gateway/pairing/cron/Windows source 정적 검토 | partial pass | 위 fixed-SHA permalink | `V2`, `W1` Claims |
| `hermes-v3plus-none` | install/build/runtime/channel/E2E 미실행 | unknown | 없음 | `V3+`, `W2+` 없음 |

병렬 조사 worktree의 submodule 본문은 비어 있어 로컬 본문을 읽지 않았다. parent `.gitmodules`+`git ls-tree`와 공식 GitHub fixed-SHA tree/metadata만으로 `I2/V2`를 수집했다.

## 강점과 한계

- 강점: `hermes-multi-channel-gateway`, `hermes-memory-skill-loop`, `hermes-cron-automation`이 장기 personal agent의 intake·memory·automation을 한 surface에 모은다.
- 강점: `hermes-pairing-boundary`와 Windows service source가 sender authorization과 native 운영 비교 근거를 준다.
- 한계: `hermes-wide-trust-domain` 때문에 일반 coding worker credential을 그대로 상속시키면 blast radius가 커진다.
- 한계: 지속 memory, self-created skill, unattended cron의 품질·비용·복구는 정적 구현 존재만으로 검증되지 않는다.

## AX 설계 재료

| 구분 | 연결 Claim | 사내 AX 플랫폼에서의 사용 |
|---|---|---|
| Borrow | `hermes-multi-channel-gateway`, `hermes-pairing-boundary` | channel provenance와 sender authorization을 명시한 intake adapter |
| Adapt | `hermes-memory-skill-loop`, `hermes-cron-automation` | retention·expiry·budget·owner가 있는 memory/automation service로 분리 |
| Avoid | `hermes-wide-trust-domain` | gateway가 coding workspace와 provider/tool credential을 암묵 상속하는 구조 |
| Build | `hermes-wide-trust-domain`, `hermes-pairing-boundary` | gateway/executor trust split, audience-scoped opaque credential handle, policy·human approval bridge |

회사 업종, message·memory의 데이터 분류, 규정상 retention, 허용 channel, cron 비용 한도, sender pairing 뒤의 승인 체계는 `unknown/decision item`이다. 이 판단은 벤더 선정이 아니라 AX 설계 재료다.

## 도입 판단

- 결정: 참고
- 적용 범위: channel intake provenance, memory/cron lifecycle, Windows gateway 운영 패턴 비교
- 이유: personal gateway 기능은 유용하지만 `hermes-wide-trust-domain`을 primary code executor와 분리해야 한다.
- 재검토 조건: opaque scoped credential broker, Windows W2, malicious DM/pairing replay, poisoned memory/skill, cron budget·cancel E2E

## 다음 검증

| Item ID | 목표 Claim/등급 | 환경·시나리오 | 통과 기준 | 보존 artifact |
|---|---|---|---|---|
| `hermes-w2-gateway` | `hermes-windows-service-path` / `W2` | Windows 11 install/start/status/stop | process tree 회수, 재시작 후 상태 일치 | commands, event/log, process snapshot |
| `hermes-v5-intake` | `hermes-pairing-boundary` / `V5` | unknown sender, expired/replayed code, revoked sender | unauthorized tool invocation 0 | channel events, auth decisions, redacted audit |
| `hermes-v5-scope` | `hermes-wide-trust-domain` / `V5` | gateway→executor opaque handle 전달 | 비대상 tool/repo/channel에서 resolve 0 | broker decision log, failure injection |

## 관계와 변경 이력

- `ToolVersion PROVIDES multi-channel-intake/persistent-memory/scheduled-automation`
- `ToolVersion SUPPORTS CLI/MCP/ACP/messaging-channels`
- `ToolVersion REQUIRES gateway-executor-trust-split/audience-scoped-credentials`
- `Project EVALUATES ToolVersion`
- 2026-08-14: official GitHub fixed-SHA 정적 프로필 작성. `I2 / V2 / W1`; runtime 미수행.
