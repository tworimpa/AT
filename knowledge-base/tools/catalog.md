---
id: tool-catalog-2026-08-14
type: catalog
title: 34개 AI 에이전트 도구 역할 및 도입 판단
status: active
tags:
  - knowledge-base
  - tool-catalog
  - provenance
observed_at: 2026-08-14
source_parent_commit: caaae4a47a127808eedac657c394b6a8fd9be460
origin_integrity: I2
verification_ceiling: V2
---

# 34개 AI 에이전트 도구 역할 및 도입 판단

[지식 베이스 홈](../index.md) · [플랫폼 청사진](../platform-blueprint.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

이 문서는 기존 상세 분석을 다시 풀어 쓰는 보고서가 아니라 역할별 탐색 인덱스다. 기능·제약의 상세 근거는 [저장소 분석](../../planning/REPOSITORY_GITHUB_ANALYSIS.md)과 [소스 스냅샷 인덱스](../../multi-agent-tools/README.md)를 따른다. 기존 33개 SHA는 부모 저장소 `4e6731a1b274eba5a8451b97594aadcf570108ee`의 gitlink이며, Paseo는 2026-08-14에 확인한 fixed SHA를 새 gitlink로 추가했다. 공식 upstream URL은 `.gitmodules`에서 확인한다.

## 판단 기호

| 판단 | 의미 |
|---|---|
| 채택 | 표준·핵심 모델 또는 clean-room 설계 원칙으로 현재 청사진에 선택 |
| 파일럿 | 공통 conformance suite와 정량 gate로 실제 도입 여부를 시험 |
| 참고 | 구현을 직접 의존하지 않고 구조·UX·실패 패턴만 참고 |
| 보류 | 현재 Windows-first 우선순위 또는 성숙도·운영 경계상 도입하지 않음 |
| 역사 | 유지보수 종료 등으로 현재 제품 후보가 아닌 계보 근거로만 보존 |

등급은 축을 합치지 않고 `I2 / V2 / W0~W1`처럼 읽는다. 여기서 `V2`는 정적 분석 상한이며 모든 항목의 `V3+`는 미실행이다. `W0`은 Windows 관련 주장·간접 경로만 있는 상태, `W1`은 Windows 전용 코드나 설정 경로를 정적으로 확인한 상태다. 어느 쪽도 Windows 실행 성공을 뜻하지 않는다.

## 운영 UI와 로컬 관제

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [Orca](https://github.com/stablyai/orca) | [`e7b85266f531f9a219dff59d8647f86585b4fc7e`](./orca.md) | worktree·터미널·diff/PR을 묶는 멀티 에이전트 ADE | 채택: 시각 관제와 Windows 로컬 실행 기준 | `I2 / V2 / W1` |
| [MulmoTerminal](https://github.com/receptron/mulmoterminal) | [`29787ace53e63f00950c7028f5d765eb035fedd5`](./mulmoterminal.md) | 브라우저 기반 다중 PTY/tmux 세션 관제 | 파일럿: native PTY와 WSL 지속성 비교 | `I2 / V2 / W1` |
| [Claude Squad](https://github.com/smtg-ai/claude-squad) | [`2dd388e9857233e07712c8c5b3e2bf3b471b39fa`](./claude-squad.md) | tmux + worktree TUI | 참고: 작은 세션 관리자, AGPL 코드는 clean-room | `I2 / V2 / W0` |
| [Agent Deck](https://github.com/asheshgoplani/agent-deck) | [`4630080726ddf99885e1d3d190ffcd2e25d18683`](./agent-deck.md) | 다중 프로젝트 세션·비용·상태 TUI | 참고: 관제 UX와 crash recovery | `I2 / V2 / W0` |
| [Agetor](https://github.com/alamops/agetor) | [`2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85`](./agetor.md) | 로컬 칸반, 승인·질문·worktree 제어면 | 참고: structured interaction, 성숙도는 보류 | `I2 / V2 / W1` |
| [Emdash](https://github.com/generalaction/emdash) | [`4366fcd589ae06014afa665bb900c93c1fcf9f54`](./emdash.md) | cross-platform agent desktop와 staged provisioning | 채택: durable workspace 수명주기 패턴 | `I2 / V2 / W1` |
| [Mux](https://github.com/coder/mux) | [`92e563e57a5778e197fc1ed48b6d24ea64d38d3f`](./mux.md) | provider-neutral desktop, 비용·patch preflight | 참고: UX만 clean-room, AGPL 직접 통합 보류 | `I2 / V2 / W1` |
| [Paseo](https://github.com/getpaseo/paseo) | [`f0bd2c8483ff7961fdf6c0cd2070835741f6ac92`](./paseo.md) | local daemon 기반 multi-provider desktop/mobile/web/CLI control plane | 파일럿: Windows·cross-device 관제와 MCP/ACP/worktree UX; AGPL 직접 통합 보류 | `I2 / V2 / W1` |

## Scheduler, coordinator와 integration lane

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [agtx](https://github.com/fynnfluegge/agtx) | [`6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04`](./agtx.md) | 칸반 + 단계별 agent routing | 채택: 계획→구현→리뷰 DAG 패턴 | `I2 / V2 / W0` |
| [Gas Town](https://github.com/gastownhall/gastown) | [`649b832b7672bc7a2dbef26f5983aba6198b819b`](./gastown.md) | 대규모 lifecycle, handoff, batch/bisect merge | 채택: watchdog·integration lane 원칙 | `I2 / V2 / W0` |
| [Taskplane](https://github.com/HenryLach/taskplane) | [`504ee6888239c511d69cd36479abf4ccfabe253f`](./taskplane.md) | DAG wave/lane, polyrepo segment, reviewer/merger | 채택: critical-path scheduler 모델 | `I2 / V2 / W1` |
| [Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator) | [`12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3`](./agent-orchestrator.md) | daemon + desktop fleet, PR·CI·review projection | 파일럿: derived state와 native ConPTY | `I2 / V2 / W1` |
| [Warren](https://github.com/jayminwest/warren) | [`bb9a4f1ced640f220b062c1ddfb9ba778e990bfa`](./warren.md) | self-hosted sandbox fleet control plane | 참고: 서버 규모 운영·관측성 | `I2 / V2 / W0` |
| [Overstory](https://github.com/jayminwest/overstory) | [`ff38f3f76f084abcc34f519bcaa69580f6e53cf1`](./overstory.md) | 계층형 coordinator/watchdog/merge queue | 역사: 유지보수 종료, Warren의 전신 | `I2 / V2 / W0` |

## 협업, task memory와 intent graph

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [Buzz](https://github.com/block/buzz) | [`8abc2baf0b71844fc4ff7222aab5027c862b7d1f`](./buzz.md) | signed relay, 사람·에이전트 협업과 audit event | 파일럿: optional remote relay, 로컬 필수 의존성 아님 | `I2 / V2 / W1` |
| [squad](https://github.com/mco-org/squad) | [`8146bcc1c38c439aedaf3ff44548c830654c8621`](./squad.md) | embedded SQLite message/task queue | 채택: 가벼운 typed coordination 패턴 | `I2 / V2 / W0` |
| [Beads](https://github.com/gastownhall/beads) | [`d1e725d9f35ba307518551b4e61b3d504fb41ec5`](./beads.md) | dependency-aware task memory와 atomic claim | 채택: ready queue·lease fencing | `I2 / V2 / W0` |
| [sudocode](https://github.com/sudocode-ai/sudocode) | [`632de1910bc4e272f99db7a33dad8f22feb743d9`](./sudocode.md) | Git 기반 spec/issue/execution graph | 채택: intent graph와 run graph 분리 | `I2 / V2 / W0` |

## Protocol과 adapter

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [Agent Client Protocol](https://github.com/agentclientprotocol/agent-client-protocol) | [`25ce6f77d6a81b452e5579cf710e25c1c3922b4a`](./agent-client-protocol.md) | editor↔agent JSON-RPC capability/session 계약 | 채택: primary structured protocol | `I2 / V2 / W0` |
| [acpx](https://github.com/openclaw/acpx) | [`5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3`](./acpx.md) | stateful ACP client, queue owner와 generation lease | 파일럿: persistent session 참고 구현 | `I2 / V2 / W1` |
| [AgentAPI](https://github.com/coder/agentapi) | [`9ff117e231822f670305254ef24f6389f75953f4`](./agentapi.md) | protocol 없는 CLI의 HTTP/SSE·PTY bridge | 파일럿: low-confidence fallback 전용 | `I2 / V2 / W1` |

## Local·remote executor와 sandbox

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [E2B](https://github.com/e2b-dev/E2B) | [`f5d702a520de52ac0e5d4dda3ca0d5fca01d7993`](./e2b.md) | cloud sandbox command/PTY/files/snapshot SDK | 파일럿: 첫 remote executor | `I2 / V2 / W0` |
| [E2B Infra](https://github.com/e2b-dev/infra) | [`035b7eda0e5d5a007489535686df9a7f087c154c`](./e2b-infra.md) | Firecracker, snapshot, network와 placement | 참고: remote data-plane·readiness 기준 | `I2 / V2 / W0` |
| [Vercel Sandbox](https://github.com/vercel/sandbox) | [`2c2c942239fd9ef47bed0b9295389b702ce6c0ff`](./vercel-sandbox.md) | persistent MicroVM, resume/fork/preview/network policy | 파일럿: E2B와 동일 contract A/B | `I2 / V2 / W0` |
| [Container Use](https://github.com/dagger/container-use) | [`2e43e625e95216b719ec9338f4034fd3a0be2734`](./container-use.md) | branch/worktree + Dagger container lineage | 파일럿: local container; secret 경계는 재설계 | `I2 / V2 / W0` |
| [Cloudflare Sandbox SDK](https://github.com/cloudflare/sandbox-sdk) | [`2dd1476e32769656da97d5a8daf75e2f92b57e71`](./cloudflare-sandbox-sdk.md) | Durable Object 제어면과 hosted container runtime | 파일럿: 세 번째 remote adapter와 generation fencing | `I2 / V2 / W0` |

## Multi-backend platform, SDK와 harness

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [OpenHands / Agent Canvas](https://github.com/OpenHands/OpenHands) | [`4f465f3ccada5271a3bbe4a0148941b0c40d243b`](./openhands.md) | multi-backend registry와 capability-aware control surface | 채택: backend negotiation 패턴 | `I2 / V2 / W1` |
| [OpenHands Agent SDK](https://github.com/OpenHands/software-agent-sdk) | [`ceda00b478a41b64c2f259c096e08977ca7ea4dd`](./openhands-agent-sdk.md) | composable agent와 warm Agent Server | 파일럿: liveness/readiness·conversation ownership | `I2 / V2 / W1` |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | [`47f943859bef60e4160492346772ded9b24f765a`](./deepseek-harness.md) | plugin-composed runtime, ACP와 local/E2B provider | 참고: capability seam과 plugin lifecycle | `I2 / V2 / W1` |

## Automation과 권한 분리

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [GitHub Agentic Workflows](https://github.com/github/gh-aw) | [`ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7`](./gh-aw.md) | Markdown workflow compiler와 safe-output write stage | 파일럿: event automation과 external write 분리 | `I2 / V2 / W0` |

## Assistant gateway와 coding runtime

| 도구와 공식 출처 | 고정 ToolVersion / snapshot | 주 역할 | 판단 | 현재 등급 |
|---|---|---|---|---|
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [`1b1975781f372e4d7fe4f448eab86cea5441f2e7`](./hermes-agent.md) | memory·skills·cron·channel을 가진 personal runtime | 참고: 장기 상태와 intake provenance | `I2 / V2 / W0` |
| [OpenClaw](https://github.com/openclaw/openclaw) | [`f49eaf86399b91a1a7273ee2405bb298d64e9387`](./openclaw.md) | single-operator gateway, session/tool/channel control | 참고: assistant/coding trust-domain 경계 | `I2 / V2 / W1` |
| [OpenAI Codex](https://github.com/openai/codex) | [`1c4f42863c1f84eb5175a1a0cfffe84641a63df3`](./codex.md) | CLI·TUI·app-server coding-agent runtime | 채택: 첫 primary worker adapter | `I2 / V2 / W1` |
| [Cline](https://github.com/cline/cline) | [`3e0aac53a2f5f408a89a957d75430f6ec4084497`](./cline.md) | IDE·CLI·hub coding-agent surfaces | 참고: surface별 capability profile 비교 | `I2 / V2 / W1` |

## 우선 도입 묶음

1. **로컬 핵심**: Codex adapter, ACP contract, Windows ConPTY/Job Object, SQLite event kernel, task별 worktree와 resource lease.
2. **병렬화와 증거**: Beads식 atomic claim, Taskplane식 DAG/wave/lane, Agent Orchestrator식 derived state, 독립 Verifier와 merge lane.
3. **선택형 협업**: Buzz signed relay와 squad식 local queue를 서로 다른 trust boundary로 둔다.
4. **실행기 확장**: E2B와 Vercel을 먼저 동일 conformance suite로 비교하고, Container Use와 Cloudflare는 독립 pilot로 평가한다.
5. **확장 표면**: OpenHands의 capability negotiation, DeepSeek Harness의 plugin seam, Hermes/OpenClaw의 intake provenance를 핵심 runtime과 분리해 참고한다.

## 명시적 비채택·보류

- NTM은 license rider 때문에 분석·재사용·지식 그래프 seed에서 제외한다.
- Claude Squad와 Mux의 AGPL 코드는 제품에 직접 포함하지 않고 공개 아이디어만 clean-room으로 참고한다.
- Paseo의 AGPL 코드도 제품에 직접 포함하지 않고 [고정 ToolVersion 프로필](./paseo.md)의 protocol·상태 모델과 한계를 clean-room 비교한다.
- Overstory는 archived 계보 자료이며 현재 운영 후보가 아니다.
- PTY 화면 안정성이나 agent 자기보고는 completion 또는 verification으로 승격하지 않는다.
- 표의 모든 도입 판단은 설계 선택 또는 pilot 우선순위다. 구매, 배포, production acceptance를 의미하지 않는다.
