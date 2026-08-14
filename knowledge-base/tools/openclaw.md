---
id: tool-openclaw
type: tool-profile
title: OpenClaw
status: observed
tags:
  - knowledge-base
  - tool
  - assistant-gateway
  - trust-boundary
  - windows
official_upstream: https://github.com/openclaw/openclaw
license: MIT-text-GitHub-NOASSERTION
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 530b33e4e37264c89ecd5abdd06279dd23d5c867
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: f49eaf86399b91a1a7273ee2405bb298d64e9387
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# OpenClaw

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

OpenClaw는 single operator의 model·tool·session·messaging channel·companion device를 한 local Gateway에 연결하는 personal assistant control plane이다.

## ToolVersion과 공식 최신 관찰

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/openclaw/openclaw` |
| 조사일 기본 브랜치 HEAD | `main` · `530b33e4e37264c89ecd5abdd06279dd23d5c867` |
| 고정 버전 | `f49eaf86399b91a1a7273ee2405bb298d64e9387` |
| pin과 최신 HEAD | 조사일 최신 HEAD가 pin보다 25 commits 앞섬. 아래 구현 주장은 pin에 고정 |
| 로컬 gitlink | [`multi-agent-tools/openclaw`](../../multi-agent-tools/openclaw/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | ToolVersion은 `I2`: parent gitlink와 공식 fixed tree를 대조 |
| 유지보수 관찰 | archived/disabled가 아니고 조사일 push 관찰. security/운영 SLA는 아님 |
| license | fixed [`LICENSE`](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/LICENSE#L1-L24)는 MIT text와 third-party notice를 가리키지만 GitHub API SPDX는 `NOASSERTION`. license 판단은 `I1`로 제한하고 component 재사용 전 재검토 |

## 기술 구조

| 구성 | 책임 | fixed-SHA 근거 |
|---|---|---|
| Gateway | session, tool, event, channel connection의 local control plane | [README architecture](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L54-L61) |
| Control surfaces | Control UI, CLI, TUI가 Gateway에 연결 | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L55-L59) |
| Channel adapters | WhatsApp/Telegram/Slack/Discord 등 inbound/outbound transport | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L57-L59) |
| Tools/skills/plugins/nodes | host·sandbox·companion device의 action surface | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L59-L67) |
| Policy layers | sandbox location, tool allow/deny, elevated exec를 독립 gate로 적용 | [policy model](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md#L10-L12) |

## 역할과 연동

- AgentRole: Gateway, Relay, Session owner, Tool router, Companion-node coordinator
- Capability: `multi-channel-assistant`, `session-control-plane`, `tool-policy`, `optional-sandbox`, `device-node`, `sender-pairing`
- Integration: CLI/TUI/Web UI, channel adapters, Gateway protocol, model providers, tools/skills/plugins, companion nodes
- SecurityOperationalRequirement: untrusted inbound treatment, sender pairing, gateway exposure control, sandbox/tool/elevated separation, credential audience, device action approval

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `openclaw-single-operator-gateway` | architecture | single operator를 위해 model·tool·channel·companion app을 한 Gateway에 연결한다. | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L17-L20), [architecture](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L54-L61) | `I2` | `V2` | `W0` | pass(정적). multi-tenant 안전성 주장이 아님 |
| `openclaw-channel-session-control` | capability | UI/CLI/TUI와 여러 channels가 Gateway의 session/tool/event surface를 공유한다. | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L55-L61) | `I2` | `V2` | `W0` | pass(정적). 실제 channel/device 연결 미실행 |
| `openclaw-untrusted-intake` | security | inbound message를 untrusted로 취급하고 unknown DM sender를 기본 pairing 대상으로 둔다. | [security note](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L63-L67) | `I2` | `V2` | `W0` | pass(정적). pairing bypass/federated identity 미검증 |
| `openclaw-policy-separation` | security | sandbox 실행 위치, tool allow/deny, elevated exec가 서로 다른 gate다. | [policy guide](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md#L10-L12), [deny semantics](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md#L56-L71) | `I2` | `V2` | `W0` | pass(정적). exec 허용은 내부 side effect를 읽기 전용으로 만들지 않음 |
| `openclaw-host-default-risk` | limitation | main session tool은 sandbox를 설정하지 않으면 host에서 실행된다. | [security warning](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L63-L67), [sandbox modes](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md#L32-L51) | `I2` | `V2` | `W0` | confirmed limitation. gateway를 coding executor sandbox로 간주 금지 |
| `openclaw-windows-source` | platform | Windows code page/registry/cmd.exe subprocess output 처리를 구현한다. | [Windows encoding](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/src/infra/windows-encoding.ts#L1-L28), [runtime resolver](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/src/infra/windows-encoding.ts#L86-L109) | `I2` | `V2` | `W1` | pass(정적). Windows gateway/runtime 미실행 |
| `openclaw-license-uncertain` | limitation | fixed LICENSE는 MIT text이나 official GitHub SPDX metadata가 NOASSERTION이다. | [LICENSE](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/LICENSE#L1-L24), [repository metadata](https://api.github.com/repos/openclaw/openclaw) | `I1` | `V1` | `W0` | license 재사용 판단 보류; component notices 확인 필요 |

## Interface와 protocol

| 표면 | 계약 | trust/permission 경계 | 근거 |
|---|---|---|---|
| Gateway | session/tool/event/channel control plane | single-operator identity와 exposure boundary | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L54-L67) |
| UI/CLI/TUI | Gateway client surfaces | client auth와 session routing | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L55-L59) |
| Channels/nodes | external sender와 device-local action | pairing, device authorization, recipient scope | [README](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/README.md#L57-L67) |
| Sandbox/tool/elevated | execution placement, callable tool, host escape | deny precedence와 exec-specific escalation | [policy guide](https://github.com/openclaw/openclaw/blob/f49eaf86399b91a1a7273ee2405bb298d64e9387/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md#L56-L71) |

## 운영·보안·trust boundary

- `openclaw-single-operator-gateway`는 assistant gateway이지 shared coding executor authority가 아니다.
- channel sender, gateway operator, model provider, plugin/tool, companion device, host process를 서로 다른 principal로 기록해야 한다.
- `openclaw-host-default-risk` 때문에 worktree나 tool deny만으로 host/credential isolation을 주장하면 안 된다.
- gateway→coding executor에는 audience·tool·repo·expiry가 붙은 opaque credential handle만 전달하고 원문 provider/channel credential을 공유하지 않는다.
- external write는 agent/gateway proposal을 policy·verifier·human이 검토한 뒤 별도 committer가 수행하도록 분리한다.

## 플랫폼과 Windows

- fixed source에 Windows console encoding, registry와 cmd.exe handling이 있어 `W1`이다.
- README installer의 Windows 표시는 문서 주장이고, 여기서 실제 Windows install/gateway/process tree는 검증하지 않았다.
- Windows companion/device와 host tool 실행은 각각 별도 `W2/W3` 시나리오가 필요하다.

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `openclaw-origin-20260814` | parent gitlink, GitHub repo/branch/compare metadata | pass | `openclaw/openclaw@f49eaf86399b91a1a7273ee2405bb298d64e9387` | origin과 ToolVersion |
| `openclaw-license-20260814` | fixed LICENSE와 GitHub SPDX metadata 대조 | partial | LICENSE=MIT text, API=`NOASSERTION` | `openclaw-license-uncertain` |
| `openclaw-fixed-static-20260814` | fixed README/policy/Windows source 검토 | partial pass | 위 fixed permalinks | `V2`, `W1` Claims |
| `openclaw-v3plus-none` | install/build/runtime/channel/device/E2E 미실행 | unknown | 없음 | `V3+`, `W2+` 없음 |

병렬 조사 worktree submodule 본문은 비어 있어 로컬 본문을 읽지 않았다. parent `.gitmodules`+`git ls-tree`, 공식 GitHub fixed-SHA tree/metadata에서만 근거를 수집했다.

## 강점과 한계

- 강점: `openclaw-channel-session-control`은 personal assistant의 channel·session·device control plane 비교에 유용하다.
- 강점: `openclaw-policy-separation`은 sandbox, tool availability, host elevation을 혼동하지 않는 운영 모델을 제공한다.
- 한계: `openclaw-host-default-risk`와 넓은 gateway trust domain 때문에 primary coding executor와 권한·credential을 분리해야 한다.
- 한계: `openclaw-license-uncertain`으로 직접 코드 재사용은 component license review 전 보류한다.

## AX 설계 재료

| 구분 | 연결 Claim | 사내 AX 플랫폼에서의 사용 |
|---|---|---|
| Borrow | `openclaw-untrusted-intake`, `openclaw-policy-separation` | inbound provenance와 sandbox/tool/elevated gate를 독립 정책으로 표현 |
| Adapt | `openclaw-channel-session-control`, `openclaw-windows-source` | channel/session 관제와 Windows 운영 기능을 capability-negotiated adapter로 축소 |
| Avoid | `openclaw-host-default-risk`, `openclaw-license-uncertain` | host-default tool 실행과 license 불명확 component의 직접 통합 |
| Build | `openclaw-single-operator-gateway`, `openclaw-host-default-risk` | gateway/executor trust split, opaque scoped credential broker, proposal→verifier/human→committer 체인 |

회사 업종, channel별 데이터 분류, device action 규정, gateway owner, elevated 승인자, retention과 credential audience는 `unknown/decision item`이다. 이 프로필은 사내 AX 설계 재료이며 벤더 선정이나 최종 운영 정책이 아니다.

## 도입 판단

- 결정: 참고
- 적용 범위: gateway trust split, inbound provenance, channel/device approval과 policy 설명 모델의 clean-room 참고
- 이유: control-plane 기능은 넓지만 host-default 실행과 license metadata 불일치가 직접 통합을 막는다.
- 재검토 조건: license/third-party audit, Windows W2, remote exposure/pairing bypass, sandbox bind/elevated escape, credential audience E2E

## 다음 검증

| Item ID | 목표 Claim/등급 | 환경·시나리오 | 통과 기준 | 보존 artifact |
|---|---|---|---|---|
| `openclaw-license-review` | `openclaw-license-uncertain` / `I2` | root/component manifest·notice 대조 | SPDX와 재사용 범위 확정 | reviewed inventory |
| `openclaw-w2-gateway` | `openclaw-windows-source` / `W2` | Windows gateway, channel, tool process | encoding·cancel·process tree 기준 통과 | logs, process snapshot |
| `openclaw-v5-boundary` | `openclaw-host-default-risk` / `V5` | malicious DM, denied tool, sandbox bind, elevated 요청 | 비승인 host/action/credential 접근 0 | redacted audit, failure matrix |

## 관계와 변경 이력

- `ToolVersion PROVIDES multi-channel-assistant/session-control-plane/tool-policy`
- `ToolVersion REQUIRES gateway-executor-trust-split/audience-scoped-credentials`
- `ToolVersion HAS_LICENSE_EVIDENCE I1`
- `Project EVALUATES ToolVersion`
- 2026-08-14: official GitHub fixed-SHA 정적 프로필 작성. origin `I2`, license `I1`, 기능 `V2`, Windows `W1`; runtime 미수행.
