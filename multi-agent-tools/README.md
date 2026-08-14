# Multi-agent coding tools survey

조사 기준일: 2026-08-14 (Asia/Seoul)

이 디렉터리는 Orca/Buzz와 두 도구에 인접한 **멀티 에이전트 코딩 운영 도구, 상호운용 protocol, CI automation 및 원격 sandbox 구현**을 비교하기 위한 소스 스냅샷이다. 조사 당시 license rider로 제외한 NTM을 뺀 33개를 분석했고, 공개 부모 저장소에는 이 33개만 submodule로 등록했다. 모두 shallow clone으로 확보했으며, 대형 `gh-aw`는 추가로 partial clone+sparse checkout을 사용했다. 의존성 설치·빌드·실행·사용자 설정 변경은 수행하지 않았다.

## 분석 산출물

- [33개 저장소 코드·GitHub 분석](../planning/REPOSITORY_GITHUB_ANALYSIS.md)
- [AI 코딩 에이전트 도구·서비스 landscape](../planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md)
- [빠른 멀티 에이전트 실행·오케스트레이션 기획](../planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md)
- [AI 에이전트 기반 개발 환경 요구사항](../planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md)

## 빠른 분류

| 도구 | 성격 | Codex | 격리/조정 방식 | Windows 관점 | 라이선스 | 판단 |
|---|---|---:|---|---|---|---|
| [Orca](./orca/) | 멀티 에이전트 ADE/데스크톱 관제 | 지원 | 에이전트별 git worktree, 터미널, diff/PR, 원격 워크스페이스 | 네이티브 Windows 지원 | MIT | 시각적 멀티 에이전트 운영의 기준 도구 |
| [Buzz](./buzz/) | 사람·에이전트 공동 작업/메시징 플랫폼 | 지원 | Nostr relay, 서명 이벤트 로그, 채널·워크플로·git 이벤트, ACP | Windows 데스크톱과 CLI 제공; 에이전트 shell은 Git Bash 필요 | Apache-2.0 | 에이전트 메시징·협업·감사 로그의 기준 도구 |
| [squad](./squad/) | 에이전트 간 메시징·작업 큐 | 지원 | SQLite 메시지/태스크, 역할 템플릿; 선택적 worktree | 네이티브 Windows 릴리스 안내 | MIT | Buzz와 가장 가까운 메시징 계층 |
| [MulmoTerminal](./mulmoterminal/) | 브라우저 기반 다중 세션 관제석 | 지원 | PTY/tmux, git worktree, diff/PR UI | 네이티브 실행 가능; tmux 지속성은 WSL 필요 | MIT | Orca와 가장 가까운 시각적 운영 도구 |
| [Claude Squad](./claude-squad/) | 터미널 다중 세션 관리자 | 지원 | tmux + git worktree | tmux 때문에 WSL 권장 | AGPL-3.0 | 작고 성숙한 TUI 기준점 |
| [Agent Deck](./agent-deck/) | 여러 프로젝트/에이전트 세션 관제 TUI | 지원 | tmux, worktree, 검색·비용·상태 추적 | 공식 지원은 WSL | MIT | 세션 관제 기능이 가장 풍부한 편 |
| [agtx](./agtx/) | 칸반 + 자율 오케스트레이터 | 지원 | 작업별 tmux/worktree, 단계별 에이전트 교체, MCP | Docker Desktop/WSL 경로가 현실적 | Apache-2.0 | 계획→구현→리뷰 역할 분업 연구용 |
| [Agetor](./agetor/) | 로컬 우선 칸반/데스크톱 제어면 | 지원 | 작업별 worktree, Claude tmux, Codex exec, SQLite | Windows 빌드는 구성됐지만 미검증 | MIT | UI/승인 흐름이 흥미롭지만 초기 단계 |
| [Warren](./warren/) | 자체 호스팅 샌드박스형 에이전트 제어면 | 제한적/구성 확인 필요 | Docker/Kubernetes 격리, API/UI, 실행별 ephemeral sandbox | Windows 로컬 앱보다는 Linux/Docker 서버용 | MIT | 팀/서버 규모 운영 아키텍처 참고용 |
| [Overstory](./overstory/) | 계층형 자율 에이전트 오케스트레이터 | 실험적 | worktree, SQLite mail, coordinator/watchdog/merge queue | Bun 중심; 운영 대상 아님 | MIT | 유지보수 종료. Warren의 역사적 전신으로만 보존 |
| [Emdash](./emdash/) | cross-platform agent desktop | 지원 | staged worktree provisioning, PTY/ACP, local/SSH | 네이티브 Windows 지원 | Apache-2.0 | 빠른 durable workspace 수명주기의 기준점 |
| [Gas Town](./gastown/) | 대규모 agent lifecycle/merge 운영 | 지원 | Beads/Dolt, mailbox/handoff, watchdog, Bors식 merge queue | 전체 기능은 tmux/WSL 중심 | MIT | 운영 원칙을 채택하되 역할 체계는 단순화 |
| [Taskplane](./taskplane/) | 계획 기반 multi-agent orchestrator | 지원 | DAG wave/lane, polyrepo segment, reviewer/merger, checkpoint | Windows cleanup fallback 존재 | MIT | 분해·critical path·검토 흐름의 기준점 |
| [Agent Orchestrator](./agent-orchestrator/) | daemon + desktop fleet control | 지원 | task/session/worktree, PR·CI·review projection | native ConPTY 구현 | Apache-2.0 | Windows runtime과 관제 상태 모델의 기준점 |
| [sudocode](./sudocode/) | spec/issue/execution graph | MCP 연동 | Git Markdown+JSONL, dependency, claim, worktree | 로컬 우선 | Apache-2.0 | 장기 의도와 실행 trajectory 모델에 채택 |
| [Mux](./mux/) | provider-neutral coding agent desktop | 지원 | local/worktree/SSH, patch dry-run, 비용·token UX | 공개 배포의 Windows 공백 | AGPL-3.0 | clean-room UX·검증 패턴 참고 |
| [Beads](./beads/) | dependency-aware task memory | agent 중립 | atomic ready/claim, Dolt, message/thread, JSONL | native Windows 안내 | MIT | ready queue와 atomic claim의 기준점 |
| [E2B](./e2b/) | cloud sandbox SDK | agent 중립 | command/PTY/files/Git, pause/resume, snapshot/fork | Windows control plane에서 API 사용 가능 | Apache-2.0 | 첫 remote executor 후보 |
| [E2B Infra](./e2b-infra/) | self-hostable sandbox infrastructure | agent 중립 | Firecracker VM, lazy snapshot, COW rootfs, netns/nftables, placement | Linux/Nomad/Terraform 운영; Windows에서는 원격 API로 사용 | Apache-2.0 | sandbox 보안·성능·ready semantics 기준점 |
| [OpenHands / Agent Canvas](./openhands/) | multi-backend agent control center | Codex·Claude·Gemini·OpenHands·ACP | backend registry, Agent Server compatibility/capability probe, runtime service topology 전달, local/cloud proxy | Windows 로컬 실행 안내와 Docker 배포 경로; host 직접 실행은 sandbox가 아님 | MIT | 공급자·실행기 중립 control surface와 capability negotiation 기준점 |
| [OpenHands Agent SDK](./openhands-agent-sdk/) | composable agent SDK + remote Agent Server | OpenHands·ACP·Codex credential binding | conversation/worktree, REST/WebSocket, usable tool advertisement, dormant warm-pool init, liveness/readiness 분리 | local host 또는 Docker/Kubernetes workspace; stress suite 일부는 POSIX 전용 | MIT | backend protocol과 warm executor lifecycle의 실제 구현 기준점 |
| [Agent Client Protocol](./agent-client-protocol/) | editor↔coding-agent wire protocol/schema | 공급자 중립 | JSON-RPC initialize/version/capability, session, permission, tool/diff/terminal stream, cancellation | platform-agnostic; 모든 path는 absolute wire path | Apache-2.0 | primary structured adapter protocol |
| [acpx](./acpx/) | headless stateful ACP client/backend | Codex·Claude·Gemini 등 ACP adapter | persistent session, queue owner/IPC, generation lease, cooperative cancel, raw NDJSON, compare/flow | Windows named pipe·path 변환 코드 포함 | MIT | ACP session/queue/persistence의 참고 구현 |
| [AgentAPI](./agentapi/) | coding CLI HTTP compatibility bridge | Codex 포함 다수 CLI | PTY screen diff 또는 experimental ACP, HTTP/SSE, OpenAPI, stable/running heuristic | Windows process path 존재; 이번 조사에서 빌드 미검증 | MIT | protocol 없는 CLI용 low-confidence fallback adapter |
| [Vercel Sandbox](./vercel-sandbox/) | hosted persistent MicroVM SDK/CLI | agent 중립 | Firecracker, named persistent sandbox/session, snapshot/resume/fork, L7 network policy, preview port | Windows에서 remote API 사용; runtime은 Linux MicroVM | Apache-2.0 | 두 번째 remote executor와 persistent sandbox 비교 기준점 |
| [GitHub Agentic Workflows](./gh-aw/) | Markdown→GitHub Actions agent workflow compiler | Copilot·Claude·Codex·Gemini 등 | compile-time validation, read-only agent job, sandbox/firewall, buffered safe outputs, threat-detection/write job 분리 | CLI 설치는 Windows 지원; 실제 workflow는 Actions runner에서 실행 | MIT | event/schedule 기반 Continuous AI와 privilege-separated external write 기준점 |
| [Container Use](./container-use/) | MCP/CLI 기반 local container workspace | MCP 호환 agent | 환경별 branch/worktree, Dagger container, Git notes 상태·실행 로그, setup/install cache 단계, service binding | Dagger container runtime이 필요하며 Windows native process 격리가 아님 | Apache-2.0 | local container executor와 재현 가능한 병렬 workspace의 기준점; 현재 secret 경계는 그대로 채택하지 않음 |
| [Cloudflare Sandbox SDK](./cloudflare-sandbox-sdk/) | hosted container SDK + runtime control plane | agent 중립, OpenAI Agents/Claude/OpenCode 예제 | Worker→Durable Object→RPC WebSocket→container service, session, runtime identity, sleep/backup, tokenized preview | local 개발은 Docker, 실제 격리·수명주기는 Cloudflare platform 경계 | Apache-2.0 파일(Forge API 미분류) | 세 번째 remote executor 후보와 runtime-generation fencing 기준점 |
| [DeepSeek Harness](./deepseek-harness/) | plugin-composed agent harness/runtime | Codex·Claude Code subagent | Cordis plugin tree, durable session/event, ACP, local/E2B sandbox provider | Windows ACL backend가 있으나 이번 조사에서 실행 미검증 | MIT; third-party notices 포함 | capability seam과 plugin lifecycle 기준점 |
| [Hermes Agent](./hermes-agent/) | self-improving personal agent runtime | ACP adapter | persistent memory·skills·cron·isolated subagent, multi-channel gateway, local/remote terminal backend | Windows 설치·backend 실행은 미검증 | MIT; optional skill별 별도 라이선스 존재 | 장기 상태와 채널 intake provenance 기준점 |
| [OpenClaw](./openclaw/) | single-operator assistant gateway/control plane | ACP core 포함 | gateway session/tool/event/channel, plugin·skill, companion node, host/sandbox 경계 | Windows 지원 범위는 정적 확인만 수행 | MIT; component notice 존재 | assistant gateway trust-domain 기준점 |
| [OpenAI Codex](./codex/) | local coding-agent runtime | 자체 runtime | CLI·TUI·app-server JSON-RPC, resume·approval, OS sandbox·network policy, MCP | Windows sandbox 구현이 있으나 build/E2E 미검증 | Apache-2.0 + NOTICE | surface별 capability profile 기준점 |
| [Cline](./cline/) | IDE/CLI coding agent | 자체 runtime | VS Code·JetBrains·headless CLI, hub/provider abstraction, MCP approval, checkpoint·subagent | Windows 실제 실행은 미검증 | Apache-2.0 | IDE/CLI/hub surface 분리 기준점 |

## Windows에서 먼저 볼 순서

1. `orca`: 현재 사용하는 시각적 worktree/에이전트 관제 기준을 소스에서 확인한다.
2. `buzz`: relay·서명 이벤트·에이전트 채널/워크플로 구조를 확인한다.
3. `squad`: 더 작은 표면으로 에이전트 메시징과 역할 분담을 비교한다.
4. `mulmoterminal`: Windows 네이티브 PTY 모드에서 여러 Codex/Claude 세션을 한 화면에 배치한다. 재시작 후 세션 지속성이 필요하면 WSL의 tmux를 사용한다.
5. `claude-squad` 또는 `agent-deck`: WSL에서 worktree 기반 터미널 운영 방식을 비교한다.
6. `agtx` 또는 `agetor`: 칸반·자동 위임·승인 흐름이 필요한 경우 검토한다.
7. `warren`: 로컬 데스크톱 도구가 아니라 자체 호스팅 에이전트 인프라가 필요할 때 검토한다.
8. `emdash`와 `agent-orchestrator`: Windows native runtime, durable provisioning, PR/CI 상태 projection을 비교한다.
9. `beads`, `taskplane`, `sudocode`: spec → DAG → atomic claim → execution evidence 모델을 비교한다.
10. `e2b`: local executor와 같은 task를 cloud sandbox에서 재현하는 adapter 실험에 사용한다.
11. `e2b-infra`: snapshot 복원, placement, readiness, network policy와 control/data plane 분리를 확인한다.
12. `openhands`: 여러 local/remote/cloud backend의 등록·health·호환성 검사와 agent 관점 runtime topology 전달을 확인한다.
13. `openhands-agent-sdk`: Agent Server의 `/server_info`, `/alive`, `/ready`, deferred init과 conversation/worktree 경계를 확인한다.
14. `agent-client-protocol`과 `acpx`: structured handshake, permission, session resume, queue ownership과 machine-readable stream을 확인한다.
15. `agentapi`: protocol 없는 legacy CLI를 PTY로 감싸는 경우의 효용과 heuristic status 한계를 확인한다.
16. `vercel-sandbox`: persistent sandbox와 running session, snapshot/fork, resume hook, network policy의 수명주기를 E2B와 비교한다.
17. `gh-aw`: Markdown source→immutable lock workflow compiler, read-only agent→threat detection→safe write job의 권한 분리와 GitHub Actions trigger를 확인한다.
18. `container-use`: branch/worktree와 Dagger container를 결합한 병렬 환경, Git notes 기반 상태·로그, cache 단계와 privileged nesting/secret 경계를 확인한다.
19. `cloudflare-sandbox-sdk`: Durable Object가 container lifecycle과 session을 조정하고 runtime identity로 stale stream/preview를 fencing하는 hosted executor 구조를 확인한다.
20. `codex`와 `cline`: CLI·TUI·app-server 또는 IDE·CLI·hub를 각각 별도 capability surface로 비교한다.
21. `deepseek-harness`: Cordis plugin tree, ACP와 local/E2B provider의 capability seam을 확인한다.
22. `hermes-agent`와 `openclaw`: coding workspace보다 넓은 channel·memory·credential trust domain을 확인한다.

## 정확한 클론 기준점

| 저장소 | 브랜치 | 클론 HEAD |
|---|---|---|
| `stablyai/orca` | `main` | `e7b85266f531f9a219dff59d8647f86585b4fc7e` |
| `block/buzz` | `main` | `8abc2baf0b71844fc4ff7222aab5027c862b7d1f` |
| `asheshgoplani/agent-deck` | `main` | `4630080726ddf99885e1d3d190ffcd2e25d18683` |
| `alamops/agetor` | `main` | `2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85` |
| `fynnfluegge/agtx` | `main` | `6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04` |
| `smtg-ai/claude-squad` | `main` | `2dd388e9857233e07712c8c5b3e2bf3b471b39fa` |
| `receptron/mulmoterminal` | `main` | `29787ace53e63f00950c7028f5d765eb035fedd5` |
| `jayminwest/overstory` | `main` | `ff38f3f76f084abcc34f519bcaa69580f6e53cf1` |
| `mco-org/squad` | `main` | `8146bcc1c38c439aedaf3ff44548c830654c8621` |
| `jayminwest/warren` | `main` | `bb9a4f1ced640f220b062c1ddfb9ba778e990bfa` |
| `generalaction/emdash` | `main` | `4366fcd589ae06014afa665bb900c93c1fcf9f54` |
| `gastownhall/gastown` | `main` | `649b832b7672bc7a2dbef26f5983aba6198b819b` |
| `HenryLach/taskplane` | `main` | `504ee6888239c511d69cd36479abf4ccfabe253f` |
| `Untrivial-ai/agent-orchestrator` | `main` | `12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3` |
| `sudocode-ai/sudocode` | `main` | `632de1910bc4e272f99db7a33dad8f22feb743d9` |
| `coder/mux` | `main` | `92e563e57a5778e197fc1ed48b6d24ea64d38d3f` |
| `gastownhall/beads` | `main` | `d1e725d9f35ba307518551b4e61b3d504fb41ec5` |
| `e2b-dev/E2B` | `main` | `f5d702a520de52ac0e5d4dda3ca0d5fca01d7993` |
| `e2b-dev/infra` | `main` | `035b7eda0e5d5a007489535686df9a7f087c154c` |
| `OpenHands/OpenHands` | `main` | `4f465f3ccada5271a3bbe4a0148941b0c40d243b` |
| `OpenHands/software-agent-sdk` | `main` | `ceda00b478a41b64c2f259c096e08977ca7ea4dd` |
| `agentclientprotocol/agent-client-protocol` | `main` | `25ce6f77d6a81b452e5579cf710e25c1c3922b4a` |
| `openclaw/acpx` | `main` | `5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3` |
| `coder/agentapi` | `main` | `9ff117e231822f670305254ef24f6389f75953f4` |
| `vercel/sandbox` | `main` | `2c2c942239fd9ef47bed0b9295389b702ce6c0ff` |
| `github/gh-aw` | `main` | `ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7` |
| `dagger/container-use` | `main` | `2e43e625e95216b719ec9338f4034fd3a0be2734` |
| `cloudflare/sandbox-sdk` | `main` | `2dd1476e32769656da97d5a8daf75e2f92b57e71` |
| `deepseek-ai/deepseek-harness` | `master` | `47f943859bef60e4160492346772ded9b24f765a` |
| `NousResearch/hermes-agent` | `main` | `1b1975781f372e4d7fe4f448eab86cea5441f2e7` |
| `openclaw/openclaw` | `main` | `f49eaf86399b91a1a7273ee2405bb298d64e9387` |
| `openai/codex` | `main` | `1c4f42863c1f84eb5175a1a0cfffe84641a63df3` |
| `cline/cline` | `main` | `3e0aac53a2f5f408a89a957d75430f6ec4084497` |

각 저장소는 독립된 Git 저장소다. 최신 이력 전체가 필요할 때만 해당 디렉터리에서 `git fetch --unshallow`을 실행한다.

## 조사했지만 클론하지 않은 항목

- **Vibe Kanban**: 기능적으로 강한 비교 대상이지만 공식 README가 현재 sunsetting 상태라고 명시하여 신규 평가 대상에서 제외했다.
- **CrewAI, AutoGen, LangGraph 계열**: 멀티 에이전트 애플리케이션을 만드는 개발 프레임워크다. 이번 범위인 “여러 코딩 에이전트 세션을 운영·격리·관제하는 도구”와 계층이 달라 제외했다.
- **상용 전용 도구**: 재현 가능한 공개 소스 클론이 없는 제품은 제외했다.
- **1Code**: 현재 공식 GitHub 저장소가 archived라 핵심 후보에서 제외했다.
- **Daytona**: GitHub API에서 라이선스가 명확히 식별되지 않아 서비스 비교군으로만 유지했다.

## 격리·분석 제외

- **NTM** (`multi-agent-tools/ntm`, local quarantine only): clone 뒤 LICENSE에 OpenAI/Anthropic 및 그 관계자의 사용·분석을 금지하는 추가 rider가 있음을 발견했다. 그 시점부터 코드 분석을 중단했으며 카탈로그·설계 근거·benchmark와 공개 저장소/submodule 목록에서 제외한다. 로컬 사본 삭제는 사용자의 명시적 승인 전까지 보류한다.

## 안전 메모

- 클론 완료는 소스 확보만 뜻한다. 설치 가능성, 빌드 성공, 실제 에이전트 실행 성공을 증명하지 않는다.
- 일부 도구는 에이전트를 현재 사용자 권한으로 실행하거나 Docker에 강한 권한을 요구한다. README와 실행 코드를 검토한 뒤 격리된 테스트 저장소에서 시작한다.
- `worktree remove`, 자동 merge, branch 삭제, PR 생성 기능은 실제 저장소에 적용하기 전에 복구 경계와 대상 경로를 확인한다.
