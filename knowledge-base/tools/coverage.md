---
id: tool-profile-coverage-2026-08-14
type: coverage-matrix
title: 34개 ToolVersion 프로필 커버리지
status: active
tags:
  - knowledge-base
  - tool-profile
  - coverage
  - provenance
observed_at: 2026-08-14
last_reviewed: 2026-08-15
source_parent_commit: 984cac0634b83d10af91d8e1814680816e67c53b
verification_ceiling: V2
---

# 34개 ToolVersion 프로필 커버리지

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 템플릿](../templates/tool-profile.md) · [스키마와 acceptance gate](../knowledge-graph-schema.md#상세-프로필-acceptance-gate)

이 표는 34개 catalog/gitlink가 상세 ToolVersion 프로필과 필수 섹션으로 연결됐는지를 추적한다. `coverage`는 문서 구조의 완성도이고 `I/V/W`는 Claim의 증거 ceiling이다. 프로필이 `10/10`이어도 build/runtime/E2E가 실행됐다는 뜻이 아니며, `I2/V2`여도 문서 섹션이 완성됐다는 뜻이 아니다.

## 판정 기준과 현재 합계

- 고정 집합: 부모 `984cac0634b83d10af91d8e1814680816e67c53b`의 `.gitmodules` 34개 path와 mode `160000` gitlink 34개.
- provenance: 각 행의 `.gitmodules` official upstream, gitlink full SHA와 official upstream fixed-SHA `tree` URL. submodule 본문이 비어 있을 수 있어 부모 repository의 submodule 내부 deep link는 근거로 사용하지 않는다.
- 필수 섹션 10개: ToolVersion, 기술 구조, Claims, Interface/protocol, 운영·보안 trust boundary, 플랫폼/Windows, Evidence, AX 설계 재료, 도입 판단, 다음 검증.
- 작성됨 34개: 그중 `10/10 covered` 23개, 현재 템플릿 기준 `partial` 11개. 파일 존재만으로 covered로 세지 않았다.
- missing/in-progress 0개. 새 9개도 `V2` 정적 근거까지만 작성했으며 실행 검증 완료를 뜻하지 않는다.
- 공통 실행 경계: build/runtime/E2E 미실행, `V3+` 0건, `W2/W3` 0건. `W1`은 좁은 Windows 정적 근거다.

## Coverage matrix

| # | ToolVersion · official fixed source | 프로필 상태 | 필수 섹션 | provenance | I | V | W | 다음 검증 | coverage |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | [acpx `5ef9b58`](https://github.com/openclaw/acpx/tree/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3) | [작성됨](./acpx.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | session queue·owner/generation을 build/runtime에서 검증 | partial |
| 2 | [Agent Client Protocol `25ce6f7`](https://github.com/agentclientprotocol/agent-client-protocol/tree/25ce6f77d6a81b452e5579cf710e25c1c3922b4a) | [작성됨](./agent-client-protocol.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | protocol conformance, cancel·permission interoperability | partial |
| 3 | [Agent Deck `4630080`](https://github.com/asheshgoplani/agent-deck/tree/4630080726ddf99885e1d3d190ffcd2e25d18683) | [작성됨](./agent-deck.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W0` | Windows session/recovery·fork secret fixture | covered |
| 4 | [Agent Orchestrator `12dbb8d`](https://github.com/Untrivial-ai/agent-orchestrator/tree/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3) | [작성됨](./agent-orchestrator.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | Windows daemon·desktop projection runtime | partial |
| 5 | [AgentAPI `9ff117e`](https://github.com/coder/agentapi/tree/9ff117e231822f670305254ef24f6389f75953f4) | [작성됨](./agentapi.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | HTTP/SSE·PTY lifecycle, cancel과 false-complete fixture | partial |
| 6 | [Agetor `2a4f1a1`](https://github.com/alamops/agetor/tree/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85) | [작성됨](./agetor.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | Windows approval/cancel·fenced cleanup fixture | covered |
| 7 | [agtx `6f0d8de`](https://github.com/fynnfluegge/agtx/tree/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04) | [작성됨](./agtx.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W0` | durable lease/generation/atomic claim absence와 runtime gate 검증 | covered |
| 8 | [Beads `d1e725d`](https://github.com/gastownhall/beads/tree/d1e725d9f35ba307518551b4e61b3d504fb41ec5) | [작성됨](./beads.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | concurrent claim atomicity와 Windows runtime 검증 | covered |
| 9 | [Buzz `8abc2ba`](https://github.com/block/buzz/tree/8abc2baf0b71844fc4ff7222aab5027c862b7d1f) | [작성됨](./buzz.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | Windows relay lifecycle, identity/replay/revoke 검증 | covered |
| 10 | [Claude Squad `2dd388e`](https://github.com/smtg-ai/claude-squad/tree/2dd388e9857233e07712c8c5b3e2bf3b471b39fa) | [작성됨](./claude-squad.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W0` | AGPL clean-room·Windows adapter·approval fixture | covered |
| 11 | [Cline `3e0aac5`](https://github.com/cline/cline/tree/3e0aac53a2f5f408a89a957d75430f6ec4084497) | [작성됨](./cline.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W0` | Windows IDE/CLI surface별 adapter conformance | covered |
| 12 | [Cloudflare Sandbox SDK `2dd1476`](https://github.com/cloudflare/sandbox-sdk/tree/2dd1476e32769656da97d5a8daf75e2f92b57e71) | [작성됨](./cloudflare-sandbox-sdk.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | runtime generation·preview fencing과 egress fixture | partial |
| 13 | [Codex `1c4f428`](https://github.com/openai/codex/tree/1c4f42863c1f84eb5175a1a0cfffe84641a63df3) | [작성됨](./codex.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | Windows app-server/ConPTY adapter `V3/W2` | covered |
| 14 | [Container Use `2e43e62`](https://github.com/dagger/container-use/tree/2e43e625e95216b719ec9338f4034fd3a0be2734) | [작성됨](./container-use.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | container isolation, cache·secret leakage fixture | partial |
| 15 | [DeepSeek Harness `47f9438`](https://github.com/deepseek-ai/deepseek-harness/tree/47f943859bef60e4160492346772ded9b24f765a) | [작성됨](./deepseek-harness.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` negative/narrow | ACP conformance·Windows confinement fixture | covered |
| 16 | [E2B `f5d702a`](https://github.com/e2b-dev/E2B/tree/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993) | [작성됨](./e2b.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | remote create/resume/fork/cancel conformance | partial |
| 17 | [E2B Infra `035b7ed`](https://github.com/e2b-dev/infra/tree/035b7eda0e5d5a007489535686df9a7f087c154c) | [작성됨](./e2b-infra.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | snapshot·network·placement/readiness 통제 runtime | partial |
| 18 | [Emdash `4366fcd`](https://github.com/generalaction/emdash/tree/4366fcd589ae06014afa665bb900c93c1fcf9f54) | [작성됨](./emdash.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | Windows/local/SSH lifecycle·secret fixture | covered |
| 19 | [Gas Town `649b832`](https://github.com/gastownhall/gastown/tree/649b832b7672bc7a2dbef26f5983aba6198b819b) | [작성됨](./gastown.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W0` | WSL workflow와 native Windows 지원 분리, runtime 검증 | covered |
| 20 | [GitHub Agentic Workflows `ef14fab`](https://github.com/github/gh-aw/tree/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7) | [작성됨](./gh-aw.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` CLI only | Actions compile/safe-output, approve bypass·non-HTTP/DNS threat fixture | covered |
| 21 | [Hermes Agent `1b19757`](https://github.com/NousResearch/hermes-agent/tree/1b1975781f372e4d7fe4f448eab86cea5441f2e7) | [작성됨](./hermes-agent.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | gateway memory/channel/secret trust-boundary runtime | covered |
| 22 | [MulmoTerminal `29787ac`](https://github.com/receptron/mulmoterminal/tree/29787ace53e63f00950c7028f5d765eb035fedd5) | [작성됨](./mulmoterminal.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | Windows PTY exit/process/resource lease fixture | covered |
| 23 | [Mux `92e563e`](https://github.com/coder/mux/tree/92e563e57a5778e197fc1ed48b6d24ea64d38d3f) | [작성됨](./mux.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | AGPL clean-room·policy bypass·secret fixture | covered |
| 24 | [OpenClaw `f49eaf8`](https://github.com/openclaw/openclaw/tree/f49eaf86399b91a1a7273ee2405bb298d64e9387) | [작성됨](./openclaw.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | Windows gateway session/tool/channel authority runtime | covered |
| 25 | [OpenHands `4f465f3`](https://github.com/OpenHands/OpenHands/tree/4f465f3ccada5271a3bbe4a0148941b0c40d243b) | [작성됨](./openhands.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | backend capability·secret/config concurrency fixture | covered |
| 26 | [OpenHands Agent SDK `ceda00b`](https://github.com/OpenHands/software-agent-sdk/tree/ceda00b478a41b64c2f259c096e08977ca7ea4dd) | [작성됨](./openhands-agent-sdk.md) | `10/10` | parent pin + official fixed source | `I2` | `V2` | `W1` narrow | lease/recovery·auth/secret/egress fixture | covered |
| 27 | [Orca `e7b8526`](https://github.com/stablyai/orca/tree/e7b85266f531f9a219dff59d8647f86585b4fc7e) | [작성됨](./orca.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | native Windows worktree/process/adapter workflow 검증 | partial |
| 28 | [Overstory `ff38f3f`](https://github.com/jayminwest/overstory/tree/ff38f3f76f084abcc34f519bcaa69580f6e53cf1) | [작성됨](./overstory.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W0` | archived 상태 고정, WSL2 code와 native Windows 분리 | covered |
| 29 | [Paseo `f0bd2c8`](https://github.com/getpaseo/paseo/tree/f0bd2c8483ff7961fdf6c0cd2070835741f6ac92) | [작성됨](./paseo.md) | `4/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | BAAB·trust/interface 섹션 보강 후 Windows daemon/UI runtime | partial |
| 30 | [squad `8146bcc`](https://github.com/mco-org/squad/tree/8146bcc1c38c439aedaf3ff44548c830654c8621) | [작성됨](./squad.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | Windows CI/process와 queue runtime 검증; CRLF는 unknown 유지 | covered |
| 31 | [sudocode `632de19`](https://github.com/sudocode-ai/sudocode/tree/632de1910bc4e272f99db7a33dad8f22feb743d9) | [작성됨](./sudocode.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | v0.2.0 pin 관계, CRLF·Windows runtime 검증 | covered |
| 32 | [Taskplane `504ee68`](https://github.com/HenryLach/taskplane/tree/504ee6888239c511d69cd36479abf4ccfabe253f) | [작성됨](./taskplane.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W1` narrow | actual Windows scheduler lifecycle와 collision fixture | covered |
| 33 | [Vercel Sandbox `2c2c942`](https://github.com/vercel/sandbox/tree/2c2c942239fd9ef47bed0b9295389b702ce6c0ff) | [작성됨](./vercel-sandbox.md) | `6/10` | parent pin + official tree | `I2` | `V2` | `W0` | remote create/resume/fork/network policy conformance | partial |
| 34 | [Warren `bb9a4f1`](https://github.com/jayminwest/warren/tree/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa) | [작성됨](./warren.md) | `10/10` | parent pin + official tree | `I2` | `V2` | `W0` | sandbox fleet isolation·recovery runtime 검증 | covered |

## Known gaps and interpretation

- `covered`는 필수 섹션이 존재한다는 뜻일 뿐 Claim 품질이나 실행 적합성의 최종 승인도 아니다. fixed locator, license와 Claim별 근거는 별도 정적 gate에서 계속 검사한다.
- `partial`은 profile 파일이 있으나 현재 template acceptance의 섹션이 빠졌다는 뜻이다. 기존 분석을 삭제하거나 섹션이 있다고 추정하지 않는다.
- `missing`은 상세 profile gap이다. catalog와 `I2` pin이 있다는 사실을 프로필 완성으로 세지 않는다.
- agtx는 Kanban/dependency routing을 보여도 durable lease/generation/atomic claim 근거가 없다. Beads의 atomic-ish identity도 실제 concurrent atomicity 검증 전에는 보장으로 쓰지 않는다.
- gh-aw의 safety는 read-only/proposal/write 분리를 참고하되 warning/lock 우회와 HTTP/HTTPS proxy 범위를 넘어선 egress 보장을 가정하지 않는다.
- Overstory는 archived/EOL reference이며 advanced baseline으로 선택하지 않는다. 다른 도구의 active 관찰도 fixed ToolVersion이 latest release라는 뜻이 아니다.
