# 멀티 에이전트 도구 코드·GitHub 분석

기준일: 2026-08-14 (Asia/Seoul)

## 1. 분석 범위와 증거 경계

이 문서는 `multi-agent-tools/`에 shallow clone한 28개 분석 대상 저장소의 코드, 공식 문서, 테스트 구조와 GitHub 공개 메타데이터를 비교한다. 로컬 분석은 [클론 기준점](../multi-agent-tools/README.md#정확한-클론-기준점)에 기록된 SHA를 기준으로 했다. 대형 gh-aw는 blobless partial clone+sparse checkout을 사용하되 전체 Git tree로 파일 지표를 계산했다. 별도로 clone된 NTM은 LICENSE rider 확인 즉시 분석에서 제외했다.

- 확인함: 저장소 구조, 상태 모델, worktree/세션/메시징/스케줄링/복구/병합 코드, 라이선스, GitHub 활동·릴리스·이슈/PR 개수.
- 확인하지 않음: 모든 저장소의 의존성 설치, 전체 빌드, 실 에이전트 E2E, 실제 Windows 성능, 보안 침투 시험.
- 따라서 아래 평가는 설계·구현 성숙도 분석이지, 모든 기능이 현재 설치 환경에서 동작한다는 인증이 아니다.
- GitHub 수치는 변동 가능성이 있는 2026-08-14 스냅샷이다. `최근 30일 커밋`은 GitHub API 첫 100건 기준이므로 `100`은 `100건 이상`을 뜻한다.
- 코드/테스트 파일 개수는 확장자와 경로명 기반 휴리스틱이다. 테스트 파일 비율은 품질 점수가 아니라 검증 투자 규모를 가늠하는 보조 지표다.

## 2. 핵심 결론

현재 도구들은 크게 일곱 부류로 나뉜다.

1. **빠른 세션 관제형**: Orca, MulmoTerminal, Claude Squad, Agent Deck. 여러 에이전트를 띄우고 worktree·터미널·diff를 사람이 빠르게 관제하는 데 강하다.
2. **자동 오케스트레이션형**: agtx, Agetor, Overstory, Warren. 작업 상태, 의존성, 감시, 승인, 복구, 병합 또는 샌드박스를 자동화하는 데 강하다.
3. **의도·작업 그래프형**: sudocode, Beads, Taskplane. spec·issue·dependency·atomic claim·execution trajectory를 durable하게 관리한다.
4. **실행 substrate형**: E2B, E2B Infra, Vercel Sandbox, Container Use, Cloudflare Sandbox SDK. 에이전트와 control plane 아래에서 원격 MicroVM, hosted/local container의 command/PTY/filesystem/Git 수명주기를 제공한다.
5. **backend federation·protocol형**: OpenHands/Agent Canvas와 Software Agent SDK. 여러 local·remote·cloud Agent Server와 ACP agent를 한 control surface에서 선택하고 protocol·tool·runtime topology를 협상하며, 서버는 conversation/workspace lifecycle을 제공한다.
6. **상호운용·compatibility형**: Agent Client Protocol, acpx, AgentAPI. 정식 wire protocol과 session backend를 우선하고, 정식 protocol이 없는 CLI는 PTY heuristic bridge로 보완한다.
7. **event-triggered agent automation형**: GitHub Agentic Workflows. 자연어 source를 검증된 Actions manifest로 compile하고 read-only agent stage와 scoped write stage를 분리한다.

Buzz와 squad는 이 둘을 연결하는 **통신·작업 프로토콜 계층**에 가깝다. 신규 도구의 기회는 관제형의 짧은 시작 시간과 오케스트레이션형의 구조화된 완료 증명을 하나의 점진적 실행 모델로 통합하는 것이다.

## 3. 저장소별 분석

| 도구 | 코드에서 확인한 강점 | 한계 또는 신규 도구가 보완할 점 | 근거 |
|---|---|---|---|
| Orca | 구조화된 메시지, blocking ask/reply, task dispatch, `worker_done`, escalation, DAG, decision gate, federation까지 가장 넓은 오케스트레이션 표면을 제공한다. 네이티브 Windows와 worktree/터미널/UI 결합이 강하다. | 기능 표면과 상태 복구 경로가 매우 커 단순 작업의 조정 비용이 높아질 수 있다. task 상태가 `pending/ready/dispatched/completed/failed/blocked` 중심이므로 실제 실행·검증·병합 상태는 별도 증거와 함께 읽어야 한다. | [orchestration skill](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/skills/orchestration/SKILL.md#L23), [task status](https://github.com/stablyai/orca/blob/e7b85266f531f9a219dff59d8647f86585b4fc7e/src/main/runtime/orchestration/types.ts#L19), [공식 GitHub](https://github.com/stablyai/orca) |
| Buzz | 사람과 에이전트가 같은 identity/event 모델을 사용하며 메시지·반응·workflow·review approval·git event를 하나의 서명 이벤트 로그로 남긴다. 원격 협업과 감사 추적에 강하다. | 로컬 단일 머신의 초저지연 스케줄러로는 relay가 과하다. 실행 격리와 merge correctness는 별도 실행 계층이 담당해야 한다. | [signed event log](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/README.md#L29), [agent surface](https://github.com/block/buzz/blob/8abc2baf0b71844fc4ff7222aab5027c862b7d1f/README.md#L230), [공식 GitHub](https://github.com/block/buzz) |
| squad | daemon 없이 SQLite와 단발 CLI로 `queued → acked → completed` 작업 수명주기와 메시징을 제공한다. 표면이 작아 빠르고 조합하기 쉽다. | 실행기, worktree 기본 격리, 독립 검증, merge queue, 복구 watchdog이 핵심 범위 밖이다. `task complete`는 에이전트 자기보고이므로 검증 완료와 동일시할 수 없다. | [README](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/README.md#L16), [task states](https://github.com/mco-org/squad/blob/8146bcc1c38c439aedaf3ff44548c830654c8621/src/store.rs#L10), [공식 GitHub](https://github.com/mco-org/squad) |
| MulmoTerminal | 브라우저 그리드에서 여러 Claude/Codex 세션의 working/waiting/done 상태를 관찰하고 worktree, diff, push/PR, 포트·DB 이름 격리까지 지원한다. | 네이티브 Windows에서는 tmux 지속성이 없어 plain PTY fallback을 사용한다. 세션 관제는 강하지만 DAG·독립 검증·자동 병합 정책은 핵심이 아니다. | [README](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L5), [Windows fallback](https://github.com/receptron/mulmoterminal/blob/29787ace53e63f00950c7028f5d765eb035fedd5/README.md#L502), [공식 GitHub](https://github.com/receptron/mulmoterminal) |
| Claude Squad | 작은 Go TUI로 tmux 세션과 git worktree를 결합한다. 구현 표면이 작아 학습과 운영이 쉽다. | tmux 의존으로 Windows는 사실상 WSL 경로다. 상태·DAG·승인·복구·완료 증명 모델이 단순하다. AGPL-3.0이므로 소스 재사용 시 배포 형태와 라이선스 검토가 필요하다. | [README](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L3), [tmux/worktree](https://github.com/smtg-ai/claude-squad/blob/2dd388e9857233e07712c8c5b3e2bf3b471b39fa/README.md#L152), [공식 GitHub](https://github.com/smtg-ai/claude-squad) |
| Agent Deck | running/waiting/done 관제, 검색, session fork, worktree, 비용, fleet verify/recover와 conductor heartbeat를 하나의 TUI/Web UI에 결합한다. 테스트 파일 투자가 크다. | Windows는 WSL 지원이다. tmux 기반 세션 상태 탐지와 에이전트별 출력 형식 변화에 대한 호환성 비용이 있다. | [README](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L22), [worktrees](https://github.com/asheshgoplani/agent-deck/blob/4630080726ddf99885e1d3d190ffcd2e25d18683/README.md#L303), [공식 GitHub](https://github.com/asheshgoplani/agent-deck) |
| agtx | `backlog → planning → running → review → done`, 작업 의존성 차단, 단계별 서로 다른 에이전트, MCP 기반 coordinator, idle 감지와 conflict check가 간결하게 연결돼 있다. | 오케스트레이터가 experimental이며 tmux 중심이다. TUI가 transition side effect를 처리하므로 headless control plane과 실행기가 더 명확히 분리될 여지가 있다. | [lifecycle](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/db/models.rs#L7), [dependency gate](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/src/mcp/server.rs#L507), [orchestrator](https://github.com/fynnfluegge/agtx/blob/6f0d8dec975b4f62ff9a48ec52dbf8cdff92bb04/README.md#L629), [공식 GitHub](https://github.com/fynnfluegge/agtx) |
| Agetor | 작업별 pinned base/worktree, local SQLite event state, 승인·질문 카드, 재시작 시 session reattach/orphan 처리, 백그라운드 subagent 정착까지 실용적인 실패 복구를 구현했다. | macOS 우선의 초기 프로젝트이고 Windows/Linux 빌드는 미검증이다. 일부 Codex prompt 상태는 stdout 휴리스틱이며 에이전트 프로토콜 변화에 취약할 수 있다. | [README](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L7), [approvals](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/README.md#L255), [orphan recovery](https://github.com/alamops/agetor/blob/2a4f1a1f3eb8a88aae8bd9581592a5c109d87a85/src/bun/orchestrator.ts#L523), [공식 GitHub](https://github.com/alamops/agetor) |
| Overstory | typed SQLite mail, worktree, FIFO merge queue, 4-tier conflict resolution, 기계/AI/monitor 계층 watchdog을 모두 구현한 좋은 참조 아키텍처다. | 공식적으로 archived이며 신규 운영 기반으로 채택하면 안 된다. 설계 원칙만 가져오고 활성 후속인 Warren과 비교해야 한다. | [archive notice](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L9), [orchestration stack](https://github.com/jayminwest/overstory/blob/ff38f3f76f084abcc34f519bcaa69580f6e53cf1/README.md#L197), [공식 GitHub](https://github.com/jayminwest/overstory) |
| Warren | 짧은 수명의 sandbox run, HTTP/API/UI, steering/cancel, 수용 테스트, resource isolation, 관측성, PR 산출을 운영 인프라 수준으로 다룬다. | 현재 plan-run은 직렬 PR merge gate 중심이어서 로컬 개발의 저지연 병렬 작업에는 무겁다. Docker/Kubernetes와 보안 권한 구성이 필요하다. | [sandbox run](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L20), [runtime isolation](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L85), [serial plan-run](https://github.com/jayminwest/warren/blob/bb9a4f1ced640f220b062c1ddfb9ba778e990bfa/README.md#L91), [공식 GitHub](https://github.com/jayminwest/warren) |
| Emdash | foreground stage pipeline을 durable하게 기록하고 agent가 실행 가능한 시점에 먼저 반환한 뒤 setup/publish tail을 background에서 완료한다. local·SSH, PTY·ACP, Windows를 함께 다룬다. | 기능 표면이 큰 Electron monorepo다. provisioning 아이디어를 가져오되 persistence schema와 UI를 통째로 결합하지 않아야 한다. | [stage pipeline](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/create-worktree.ts#L35), [agent-spawnable return](https://github.com/generalaction/emdash/blob/4366fcd589ae06014afa665bb900c93c1fcf9f54/packages/core/src/runtimes/workspace-registry/node/runtime.ts#L685), [공식 GitHub](https://github.com/generalaction/emdash) |
| Gas Town | mailbox/handoff, Witness·Deacon watchdog, Beads/Dolt 상태, Bors식 batch/bisect Refinery merge queue까지 장기 운영 실패를 구체적으로 다룬다. | 역할 이름과 계층이 많고 tmux 기반 전체 운영은 Windows에서 WSL이 필요하다. 원칙은 채택하되 product taxonomy는 단순화해야 한다. | [roles](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L86), [merge queue](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md#L651), [공식 GitHub](https://github.com/gastownhall/gastown) |
| Taskplane | dependency DAG를 wave/lane으로 만들고 polyrepo task segment, persistent worker context, reviewer/merger, checkpoint와 transactional merge를 제공한다. | 특정 agent runtime과 planning convention에 결합된 부분이 있다. scheduler primitive만 공급자 중립 계약으로 추출하는 편이 적합하다. | [README](https://github.com/HenryLach/taskplane/blob/504ee6888239c511d69cd36479abf4ccfabe253f/README.md), [공식 GitHub](https://github.com/HenryLach/taskplane) |
| Agent Orchestrator | long-running Go daemon과 desktop UI, task/session/worktree, native Windows ConPTY, PR·CI·review 사실로부터 card 상태를 파생하는 구조가 강하다. | TUI와 structured chat 경로의 lifecycle 차이를 adapter capability로 명시해야 하며 ConPTY 자체를 sandbox로 오해하면 안 된다. | [Windows ConPTY](https://github.com/Untrivial-ai/agent-orchestrator/blob/12dbb8dd7d933764823cd06f36fb8eedbd0c1ac3/backend/internal/adapters/runtime/conpty/host_conpty_windows.go), [공식 GitHub](https://github.com/Untrivial-ai/agent-orchestrator) |
| sudocode | WHAT인 spec, HOW인 issue, 실제 trajectory인 execution을 Git의 Markdown+JSONL과 MCP로 연결하고 dependency graph를 실행한다. | 실제 process isolation, 독립 verifier, merge correctness는 다른 계층이 제공해야 한다. | [README](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/README.md), [공식 문서](https://docs.sudocode.ai/introduction) |
| Mux | local/worktree/SSH runtime, token·cost·compaction UX, workspace 밖 path guard, detached worktree patch dry-run과 benchmark adapter를 갖춘다. | AGPL-3.0이고 공개 배포의 Windows 공백이 있어 제품 코드를 직접 포함하기보다 clean-room 참고가 적합하다. | [README](https://github.com/coder/mux/blob/92e563e57a5778e197fc1ed48b6d24ea64d38d3f/README.md), [공식 GitHub](https://github.com/coder/mux) |
| Beads | blocker-aware ready queue와 atomic claim, Dolt 기반 동시 writer, message/thread, Git과 분리된 task graph 및 JSONL 교환을 제공한다. | embedded single-writer와 server 동시-writer mode를 배포 상황에 맞게 구분해야 한다. source branch와 task state의 동기화 정책도 별도 필요하다. | [README](https://github.com/gastownhall/beads/blob/d1e725d9f35ba307518551b4e61b3d504fb41ec5/README.md), [공식 GitHub](https://github.com/gastownhall/beads) |
| E2B | JS/Python SDK로 sandbox command·PTY·filesystem·Git, pause/resume, snapshot/fork와 network 수명주기를 제공한다. 같은 초기 상태의 1:N 실행에 적합하다. | cloud Linux substrate이며 비용·retention·network·secret 경계는 local executor와 다르다. provider outage와 lock-in도 고려해야 한다. | [SDK](https://github.com/e2b-dev/E2B/blob/f5d702a520de52ac0e5d4dda3ca0d5fca01d7993/packages/js-sdk/src/sandbox/), [persistence](https://e2b.dev/docs/sandbox/persistence), [공식 GitHub](https://github.com/e2b-dev/E2B) |
| E2B Infra | Firecracker VM, UFFD lazy memory, COW rootfs/NBD, cgroup·netns·nftables, best-of-K placement, envd readiness, control/data plane 분리를 실제 backend로 구현한다. | self-host는 Linux root 권한, Nomad/Terraform, Postgres/Redis/ClickHouse/object storage 운영이 필요해 MVP local kernel에는 과하다. | [architecture](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/docs/ARCHITECTURE.md), [self-host](https://github.com/e2b-dev/infra/blob/035b7eda0e5d5a007489535686df9a7f087c154c/self-host.md), [공식 GitHub](https://github.com/e2b-dev/infra) |
| OpenHands / Agent Canvas | frontend와 실행기를 분리하고 여러 backend의 identity·auth·health를 registry로 관리한다. `/server_info`에서 최소 버전, usable tool, agent 관점 runtime service topology를 받고 local은 typed SDK, cloud runtime은 server-side proxy로 접근한다. child conversation과 ACP profile도 같은 conversation contract에 연결한다. | host 직접 실행은 filesystem·network를 격리하지 않는다. backend health와 protocol compatibility는 별도이며, browser/host의 `localhost`를 sandbox topology로 추측하면 안 된다. | [architecture](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/docs/architecture.md), [compatibility probe](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/src/api/agent-server-compatibility.ts), [runtime topology](https://github.com/OpenHands/OpenHands/blob/4f465f3ccada5271a3bbe4a0148941b0c40d243b/scripts/runtime-services-info.mjs), [공식 GitHub](https://github.com/OpenHands/OpenHands) |
| OpenHands Software Agent SDK | SDK와 Agent Server를 분리하면서 local 또는 ephemeral workspace, REST/WebSocket conversation, conversation별 worktree, usable tool/capability 광고를 제공한다. `/alive`와 `/ready`를 분리하고 deferred init으로 warm process에 사용자별 workspace·auth·secret·webhook을 나중에 결합한다. | dormant process는 ready가 아니며 init 실패·재시도와 credential rotation을 별도 상태로 다뤄야 한다. host local 실행은 sandbox가 아니고 stress suite 일부는 POSIX 전용이다. | [README](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/README.md), [server info/readiness](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server/server_details_router.py), [deferred init](https://github.com/OpenHands/software-agent-sdk/blob/ceda00b478a41b64c2f259c096e08977ca7ea4dd/openhands-agent-server/openhands/agent_server/init_router.py), [공식 GitHub](https://github.com/OpenHands/software-agent-sdk) |
| Agent Client Protocol | editor와 coding agent가 JSON-RPC initialize에서 wire major와 양방향 capability를 합의하고 session, streaming update, permission, filesystem, terminal, cancellation을 표준화한다. schema artifact version과 wire version을 분리한다. | trusted editor-agent 상호작용 protocol이며 sandbox, durable task graph, verifier는 제공하지 않는다. omitted capability는 unsupported로 다뤄야 하고 draft v2를 stable v1처럼 사용하면 안 된다. | [architecture](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/get-started/architecture.mdx), [initialization](https://github.com/agentclientprotocol/agent-client-protocol/blob/25ce6f77d6a81b452e5579cf710e25c1c3922b4a/docs/protocol/v1/initialization.mdx), [공식 GitHub](https://github.com/agentclientprotocol/agent-client-protocol) |
| acpx | ACP agent를 cwd·agent command·name으로 scope한 persistent session과 queue-owner IPC로 감싼다. random generation lease, Windows named pipe, cooperative cancel, resume/load, raw NDJSON, permission mode와 structured compare/flow가 강하다. | pre-1.0이고 agent별 ACP capability가 다르다. resume/load 실패 뒤 새 session fallback은 governed run에서 context continuity 손실로 별도 표시해야 한다. | [sessions](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/docs/sessions.md), [output contract](https://github.com/openclaw/acpx/blob/5ef9b5849e137310a1c6f6e06d82ca606c2d8fb3/docs/output-formats.md), [공식 GitHub](https://github.com/openclaw/acpx) |
| AgentAPI | Claude, Codex, Gemini 등 여러 CLI의 PTY screen snapshot을 message/status로 변환해 HTTP/OpenAPI/SSE를 제공하고 experimental ACP transport도 갖춘다. protocol 없는 agent를 빠르게 통합하는 폭이 넓다. | screen diff, input-box, stability heuristic은 TUI 업데이트에 취약하다. `stable`은 idle 추정일 뿐 task completion이나 verification이 아니며 ACP mode의 persistence도 제한된다. | [README](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/README.md), [screen tracker](https://github.com/coder/agentapi/blob/9ff117e231822f670305254ef24f6389f75953f4/lib/screentracker/pty_conversation.go), [공식 GitHub](https://github.com/coder/agentapi) |
| Vercel Sandbox | persistent named Firecracker MicroVM과 그 안의 running session을 구분하고 stop 시 snapshot, get/resume·`onResume`, fork, custom OCI image, commands/files/ports를 SDK·CLI로 제공한다. network policy는 domain/subnet뿐 아니라 HTTP request matcher, header transform, forward proxy까지 표현한다. | hosted Linux substrate이며 SDK client가 Windows에서 동작해도 runtime 격리는 provider 경계다. 기본 egress와 image의 coding agent·passwordless sudo를 그대로 신뢰하지 말고 project policy, OIDC, snapshot secret scan을 강제해야 한다. | [README](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/README.md), [lifecycle](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/sandbox.ts), [network policy](https://github.com/vercel/sandbox/blob/2c2c942239fd9ef47bed0b9295389b702ce6c0ff/packages/vercel-sandbox/src/network-policy.ts), [공식 GitHub](https://github.com/vercel/sandbox) |
| GitHub Agentic Workflows | YAML frontmatter+Markdown source를 strict schema, expression/template-injection, permission, action-pin, firewall validation 뒤 `.lock.yml` Actions workflow로 compile한다. agent job은 최소 read 권한으로 artifact만 만들고 별도 threat detection과 scope별 safe-output job이 외부 write를 담당한다. | Public Preview이고 GitHub Actions runtime·GitHub forge에 결합된다. AI threat detection은 deterministic sanitizer/policy의 대체가 아니며 sandbox도 runner host, API proxy, MCP gateway 신뢰를 없애지 않는다. | [architecture](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/docs/src/content/docs/introduction/architecture.mdx), [compiler](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler.go), [safe-output job](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_job.go), [공식 GitHub](https://github.com/github/gh-aw) |
| Container Use | 환경별 branch/worktree와 Dagger container를 결합하고 setup-before-source cache, install-after-source, service binding, command/file 변경 export·commit, Git notes 상태·실행 로그를 MCP/CLI로 제공한다. 실패 command 뒤에도 container state를 보존해 재현·디버깅할 수 있다. | Dagger와 privileged nesting이 필요한 local container 경계다. 현재 source에는 secret reference 문자열을 project JSON과 Git notes state에 직렬화하고 `show/list`에서 값까지 출력하는 경로가 있어 문서의 masking 주장과 불일치한다. secret subsystem은 채택하면 안 된다. | [environment lifecycle](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/environment.go), [config serialization](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/config.go), [Git notes state](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/repository/git.go), [공식 GitHub](https://github.com/dagger/container-use) |
| Cloudflare Sandbox SDK | Worker→Durable Object→RPC WebSocket→container service를 primary control path로 두고 HTTP client는 compatibility path로 유지한다. command/file/process/session, streaming, sleep-after, R2 backup, tokenized preview를 제공하며 persisted runtime identity로 restart 뒤 stale stream·preview activation을 차단한다. | session은 cwd/env context이지 별도 격리 sandbox가 아니다. local 개발은 Docker, production isolation·capacity·retention은 Cloudflare platform 경계이며 preview는 custom wildcard domain과 restart 후 재활성화가 필요하다. | [architecture](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/.agents/skills/architecture/SKILL.md), [runtime identity](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/current-runtime-identity.ts), [sandbox lifecycle](https://github.com/cloudflare/sandbox-sdk/blob/2dd1476e32769656da97d5a8daf75e2f92b57e71/packages/sandbox/src/sandbox.ts), [공식 GitHub](https://github.com/cloudflare/sandbox-sdk) |

## 4. GitHub 활동 스냅샷

| 저장소 | Stars | Forks | 최근 30일 커밋 | 최신 릴리스 | 공개일 | Open issue | Open PR |
|---|---:|---:|---:|---|---|---:|---:|
| `stablyai/orca` | 44,752 | 3,122 | 100+ | `v1.4.180` | 2026-08-11 | 1,808 | 1,939 |
| `block/buzz` | 27,098 | 3,315 | 100+ | `desktop-v0.5.11` | 2026-08-12 | 1,109 | 1,422 |
| `mco-org/squad` | 628 | 62 | 0 | `v0.7.6` | 2026-04-05 | 9 | 1 |
| `receptron/mulmoterminal` | 141 | 19 | 100+ | `4.8.2` | 2026-08-13 | 53 | 1 |
| `smtg-ai/claude-squad` | 8,305 | 602 | 1 | `v1.0.19` | 2026-06-17 | 19 | 34 |
| `asheshgoplani/agent-deck` | 719 | 115 | 100+ | `v1.11.0` | 2026-08-01 | 44 | 34 |
| `fynnfluegge/agtx` | 1,236 | 109 | 7 | `v0.2.6` | 2026-06-28 | 10 | 6 |
| `alamops/agetor` | 45 | 5 | 64 | `v0.1.0` | 2026-08-11 | 1 | 3 |
| `jayminwest/overstory` | 1,326 | 209 | 0 | `v0.11.0` | 2026-05-02 | 16 | 8 |
| `jayminwest/warren` | 309 | 71 | 100+ | `v0.14.1` | 2026-08-11 | 11 | 0 |

### 4.1 추가 후보 GitHub 스냅샷

추가 후보는 같은 날 GitHub repository API에서 조회했다. `Open items`는 GitHub의 `open_issues_count`라 issue와 PR을 합친 값이다.

| 저장소 | Stars | Forks | Open items | 마지막 push(UTC) | 라이선스 |
|---|---:|---:|---:|---|---|
| `generalaction/emdash` | 5,402 | 558 | 204 | 2026-08-13 | Apache-2.0 |
| `gastownhall/gastown` | 17,601 | 1,618 | 363 | 2026-08-13 | MIT |
| `HenryLach/taskplane` | 210 | 15 | 19 | 2026-07-18 | MIT |
| `Untrivial-ai/agent-orchestrator` | 9,483 | 1,350 | 690 | 2026-08-13 | Apache-2.0 |
| `sudocode-ai/sudocode` | 290 | 26 | 11 | 2026-03-18 | Apache-2.0 |
| `coder/mux` | 1,966 | 129 | 261 | 2026-08-13 | AGPL-3.0 |
| `gastownhall/beads` | 26,285 | 1,771 | 610 | 2026-08-13 | MIT |
| `e2b-dev/E2B` | 13,383 | 988 | 40 | 2026-08-13 | Apache-2.0 |
| `e2b-dev/infra` | 1,321 | 382 | 153 | 2026-08-13 | Apache-2.0 |
| `OpenHands/OpenHands` | 83,928 | 10,864 | 485 | 2026-08-13 | MIT |
| `OpenHands/software-agent-sdk` | 984 | 417 | 346 | 2026-08-13 | MIT |
| `agentclientprotocol/agent-client-protocol` | 3,966 | 341 | 36 | 2026-08-13 | Apache-2.0 |
| `openclaw/acpx` | 3,126 | 320 | 19 | 2026-08-10 | MIT |
| `coder/agentapi` | 1,481 | 135 | 41 | 2026-05-27 | MIT |
| `vercel/sandbox` | 178 | 34 | 25 | 2026-08-13 | Apache-2.0 |
| `github/gh-aw` | 4,925 | 494 | 335 | 2026-08-13 | MIT |
| `dagger/container-use` | 4,004 | 202 | 57 | 2026-08-12 | Apache-2.0 |
| `cloudflare/sandbox-sdk` | 1,105 | 112 | 19 | 2026-08-13 | Apache-2.0 파일 (`NOASSERTION` API) |

해석 시 주의할 점:

- Stars는 사용자 관심도이지 안정성이나 적합성의 증명이 아니다.
- Orca/Buzz의 큰 issue/PR 수는 규모와 활동성을 동시에 반영한다. 숫자만으로 결함률을 비교할 수 없다.
- Agetor는 최근 활동은 높지만 `v0.1.0`의 초기 단계다.
- Overstory는 코드가 풍부해도 공식 archived 상태이므로 운영 후보가 아니라 설계 참조다.
- squad와 Claude Squad는 최근 변경량이 적지만 작은 표면과 안정화 단계일 가능성도 있으므로 단순히 열세로 보지 않는다.

## 5. 코드 규모와 검증 투자 휴리스틱

| 저장소 | 코드 파일 | 테스트 경로 파일 | 문서 파일 | 테스트 경로 비율 |
|---|---:|---:|---:|---:|
| Orca | 13,153 | 5,802 | 73 | 44.1% |
| Buzz | 2,868 | 843 | 96 | 29.4% |
| squad | 27 | 16 | 13 | 59.3% |
| MulmoTerminal | 1,426 | 707 | 625 | 49.6% |
| Claude Squad | 57 | 9 | 5 | 15.8% |
| Agent Deck | 1,651 | 1,169 | 77 | 70.8% |
| agtx | 40 | 8 | 19 | 20.0% |
| Agetor | 366 | 162 | 77 | 44.3% |
| Overstory | 337 | 137 | 24 | 40.7% |
| Warren | 1,032 | 446 | 35 | 43.2% |
| Emdash | 4,222 | 925 | 105 | 21.9% |
| Gas Town | 1,275 | 583 | 103 | 45.7% |
| Taskplane | 188 | 141 | 492 | 75.0% |
| Agent Orchestrator | 1,887 | 663 | 109 | 35.1% |
| sudocode | 874 | 414 | 35 | 47.4% |
| Mux | 2,424 | 916 | 80 | 37.8% |
| Beads | 2,846 | 1,559 | 359 | 54.8% |
| E2B | 704 | 381 | 12 | 54.1% |
| E2B Infra | 1,727 | 534 | 31 | 30.9% |
| OpenHands / Agent Canvas | 1,799 | 635 | 22 | 35.3% |
| OpenHands Software Agent SDK | 1,245 | 737 | 40 | 59.2% |
| Agent Client Protocol | 36 | 0 | 175 | 0.0% |
| acpx | 249 | 85 | 68 | 34.1% |
| AgentAPI | 69 | 11 | 7 | 15.9% |
| Vercel Sandbox | 214 | 50 | 30 | 23.4% |
| GitHub Agentic Workflows | 3,110 | 1,672 | 2,345 | 53.8% |
| Container Use | 82 | 27 | 20 | 32.9% |
| Cloudflare Sandbox SDK | 525 | 227 | 77 | 43.2% |

이 표는 생성물·fixture를 완전히 제거하지 않은 휴리스틱이다. `test/tests/spec/__tests__` 경로와 `*_test.*`, `*.test.*`, `*.spec.*` 이름을 테스트로 집계하며, inline Rust test나 문서 schema fixture는 누락될 수 있다. 신규 도구의 목표는 파일 수가 아니라 핵심 수명주기 전이에 대한 상태 기반 테스트, crash recovery 테스트, Windows 프로세스 테스트, merge correctness 테스트를 우선하는 것이다.

## 6. 교차 분석에서 도출된 설계 원칙

### 6.1 빠른 경로와 관리 경로를 분리해야 한다

단순 조사나 한 파일 수정까지 DAG·원격 relay·컨테이너를 강제하면 조정 오버헤드가 실제 작업보다 커진다. 반대로 여러 write task를 같은 checkout에 바로 실행하면 충돌과 상태 오판이 생긴다. 따라서 동일한 control plane 아래에 `Quick`, `Parallel`, `Governed` 세 실행 모드가 필요하다.

### 6.2 worktree는 파일만 격리한다

worktree는 포트, DB/schema, 캐시, 장치, emulator, 환경변수, secret을 격리하지 않는다. MulmoTerminal의 per-worktree port/slug 할당은 이 문제를 직접 다룬다. 신규 도구는 `ResourceLease`를 별도 일급 엔티티로 가져야 한다.

### 6.3 터미널 상태, 에이전트 상태, 작업 상태를 분리해야 한다

`PTY alive`, `agent waiting`, `run succeeded`, `task verified`, `branch merged`는 서로 다른 사실이다. Agetor가 terminal run 성공 뒤 background subagent가 남아 있으면 task를 `running`에 유지하는 구현은 이 분리의 중요성을 보여준다. 신규 도구는 한 개의 `status` 필드로 이를 압축하면 안 된다.

### 6.4 완료는 자기보고가 아니라 증거 패키지여야 한다

`task complete`, `worker_done`, 프로세스 exit code 0은 모두 필요한 신호지만 충분조건은 아니다. 변경 파일, commit, base SHA, 검증 명령/exit code, 테스트 결과, 미해결 위험을 포함하는 `CompletionEvidence`를 독립 verifier가 평가해야 `verified`로 승격할 수 있다.

### 6.5 polling보다 event-driven이 빠르고 정확하다

SQLite WAL 또는 append-only event log에 단조 증가 sequence를 두고 UI·scheduler·notifier가 구독하는 방식이 적합하다. 로컬은 embedded SQLite로 저지연을 확보하고, 원격 협업이 필요할 때만 Buzz형 relay adapter를 추가한다.

### 6.6 병렬화의 병목은 agent 수가 아니라 통합이다

무제한 fan-out은 더 많은 merge conflict, 환경 충돌, review backlog를 만든다. scheduler는 DAG critical path, 예상 write set, repository merge lane, CPU/RAM/API quota를 함께 고려해야 한다. 동일 저장소의 merge는 직렬화하되 독립 검증은 병렬화한다.

### 6.7 Windows는 fallback이 아니라 1급 플랫폼이어야 한다

tmux/Unix shell 전제를 제거하고 Windows에서는 ConPTY, Job Object 기반 process-tree 종료, PowerShell/cmd 인자 보존, long path, CRLF, junction/symlink 권한을 직접 시험해야 한다. WSL은 선택 가능한 executor이지 필수 control plane이 아니어야 한다.

### 6.8 workspace 준비는 재실행 가능한 staged saga여야 한다

`inspect → resolve_base → materialize → worktree_ready → setup_ready → published`를 개별 durable step으로 기록한다. agent는 `worktree_ready`부터 시작할 수 있지만 background setup/publish 실패는 사라지지 않아야 한다. 같은 idempotency key 재호출은 완료된 step을 반복하지 않고 중단 지점부터 재개한다.

### 6.9 shared workspace와 isolated workspace는 작업 결합도에 따라 선택해야 한다

독립 배포 가능한 feature는 별도 branch/worktree가 맞다. 반대로 구현·review·test repair가 같은 diff를 공유한다면 하나의 workspace에 여러 session을 두는 것이 context 전달과 merge 비용을 줄인다. planner는 `workspace_group`과 동시 write 정책을 명시해야 한다.

### 6.10 선언형 의도 그래프와 실행 그래프를 분리해야 한다

spec/issue의 WHAT·WHY·acceptance는 Git에 버전 관리하고, Run/Attempt/Session은 event store에 기록한다. chat transcript는 보조 evidence이지 장기 계획의 source of truth가 아니다.

### 6.11 ready 조회와 claim은 원자적이어야 한다

여러 worker가 blocker가 해제된 같은 task를 동시에 선택하지 않도록 eligibility 확인, lease 생성, attempt 연결을 하나의 transaction으로 수행한다. stale lease 회수도 별도 event와 fencing token을 가져야 한다.

### 6.12 UI 상태는 여러 사실의 projection이어야 한다

`working`, `review`, `merge_ready` 같은 카드는 terminal prompt 문자열만으로 결정하지 않는다. process/session, Git SHA, PR, CI, review, interaction, verifier event를 조합해 파생하고 각 상태에 reason과 evidence timestamp를 표시한다.

### 6.13 local과 cloud executor는 같은 계약, 다른 capability를 가져야 한다

create/ready/exec/observe/pause/resume/snapshot/terminate 계약은 같게 하되 isolation, network, secret, retention, cost capability는 provider별로 명시한다. 지원하지 않는 격리 요청을 fallback으로 낮추지 말고 거부한다.

### 6.14 snapshot은 준비 비용을 critical path에서 제거하는 도구다

lockfile/toolchain 기반 prepared image와 filesystem snapshot을 만들고 여러 task가 이를 fork하도록 한다. snapshot 출처, TTL, secret 포함 여부, base SHA와 invalidation key를 기록하지 않으면 빠른 대신 재현성과 보안이 무너진다.

### 6.15 ready는 authenticated tool endpoint까지 포함해야 한다

VM/process가 생겼다는 사실만으로 `executor_ready`를 발행하지 않는다. command/filesystem/PTY를 제공하는 in-guest endpoint가 인증 정보와 metadata를 받은 뒤 readiness probe를 통과해야 한다. preview service는 별도 `services_ready` event로 둔다.

### 6.16 control traffic과 sandbox data traffic을 분리해야 한다

task/event/policy API는 control plane으로, PTY·file transfer·preview port traffic은 sandbox data plane으로 보낸다. control plane은 routing catalog와 short-lived capability를 발급하되 대용량 데이터의 proxy 병목이 되지 않도록 한다.

### 6.17 placement는 가장 빈 node가 아니라 cache locality까지 고려해야 한다

ready node를 K개 표본 추출해 CPU/RAM commitment와 실제 사용량을 점수화하고, resume은 origin node/snapshot cache locality를 우선한다. startup time, cache hit, eviction, transfer bytes를 placement feedback으로 학습한다.

### 6.18 backend 연결과 실행 가능성은 다르다

HTTP 연결 성공만으로 backend를 runnable로 표시하지 않는다. protocol version, `usable_tools`, auth, runtime topology를 별도로 확인하고 `connected-but-incompatible`, `authenticated-but-capability-missing` 같은 이유를 보존한다. service URL은 backend가 agent 관점에서 광고해야 하며 host/browser가 추측하지 않는다.

### 6.19 warm process와 ready executor를 분리해야 한다

warm pool process는 binary와 tool을 미리 적재했더라도 사용자 workspace, session key, policy, secret binding을 받기 전에는 `dormant`다. liveness, initialization, authenticated readiness를 분리하고 init 실패는 안전하게 dormant generation으로 되돌아가야 한다. parent/child conversation도 같은 workspace ownership을 검증해야 한다.

### 6.20 structured protocol이 heuristic보다 우선해야 한다

ACP처럼 version, capability, permission, tool call, cancel, stop reason을 구조화한 adapter를 primary로 사용한다. AgentAPI식 PTY screen parsing은 정식 protocol이 없는 CLI의 fallback으로 유지하고 `adapter_confidence=heuristic`을 표시한다. idle/stable 화면을 completion이나 verification으로 승격하지 않는다.

### 6.21 protocol package version과 wire version을 분리해야 한다

SDK·schema artifact semver는 codegen이나 package API 호환성이고 실제 통신 호환성은 initialize에서 합의한 ACP `protocolVersion`과 capability다. 누락 capability는 unsupported이며, draft 기능은 explicit opt-in과 schema pin 없이 사용하지 않는다.

### 6.22 session identity와 live owner를 분리해야 한다

persistent logical session과 현재 adapter process/queue owner는 같은 것이 아니다. session은 provider id와 cwd scope로 보존하고, live owner는 IPC endpoint, heartbeat, PID probe, random generation lease로 증명한다. owner crash 뒤 reconnect가 새 session으로 fallback하면 context continuity가 끊겼다는 새 attempt evidence를 남긴다.

### 6.23 sandbox identity, running session, service readiness를 분리해야 한다

Vercel Sandbox의 persistent sandbox는 실행 session이 정지해도 snapshot으로 존재할 수 있고 resume 뒤 service는 `onResume`으로 다시 올라와야 한다. 따라서 `sandbox_exists`, `session_running`, `command_ready`, `services_ready`를 하나의 boolean으로 압축하지 않는다. snapshot/fork lineage, resume generation, restore hook 결과를 event로 남기고 각 child의 identity·secret·network lease를 새로 결합한다.

### 6.24 network policy의 범위와 default를 명시해야 한다

domain/subnet egress와 HTTP request matcher·header transform·forward proxy는 서로 다른 enforcement surface다. provider가 allow-all을 기본으로 하더라도 project policy는 deny/minimal allowlist를 기본으로 하고, setup·MCP·preview·proxy traffic 중 어느 경로가 적용 대상 밖인지 실행 전 contract와 evidence에 표시한다.

### 6.25 agent proposal과 외부 write 권한을 다른 stage에 둬야 한다

gh-aw는 agent에게 GitHub write token을 주지 않고 제안된 issue/comment/PR/patch를 artifact로 buffer한 뒤 별도 safe-output job이 구조·수량·파일 범위·secret 정책과 threat verdict를 확인해 최소 scope 권한으로 적용한다. 신규 도구도 외부 write를 agent process의 tool call로 즉시 수행하지 말고 immutable proposal과 policy decision을 거치는 scoped committer에 맡긴다.

### 6.26 자연어 automation도 compile 가능한 실행 manifest가 필요하다

사람이 관리하는 Markdown/spec와 실제로 실행되는 graph를 구분한다. compiler는 source hash, schema version, resolved action/container digest, engine, permissions, network/MCP policy, stage dependencies를 고정한 manifest를 만들고 동일 입력에서 deterministic해야 한다. deterministic CI는 그대로 유지하고 agentic workflow는 제안·분류·조사처럼 비결정성이 허용되는 보조 lane으로 둔다.

### 6.27 manifest update는 권한 drift review여야 한다

gh-aw의 strict/safe-update 경로는 기본 strict이며 기존 lock manifest를 Git `HEAD`에서 읽어 working-copy 조작이 approval baseline을 위조하지 못하게 한다. 새 manifest가 write scope, secret audience, network/MCP reachability, sandbox host access, unpinned dependency를 넓히면 일반 content diff와 분리된 privilege diff를 만들고 policy 또는 사람이 승인해야 한다.

### 6.28 branch, worktree, container는 하나의 실행 lineage로 묶어야 한다

Container Use는 환경별 branch/worktree와 Dagger container digest를 함께 유지하고 Git notes로 state를 commit에 연결한다. 신규 도구도 `base_sha → workspace_id/worktree → executor_id/container_digest → run_generation → output_commit` 계보를 하나의 Run에서 추적해야 한다. worktree는 source 충돌을, container는 dependency/process 충돌을 줄이지만 둘 중 어느 것도 secret·network·host 권한을 자동으로 증명하지 않는다.

### 6.29 cache 최적화와 검증 상태를 분리해야 한다

source mount 전 setup과 mount 후 install을 나누면 base dependency cache를 공유하면서 source별 설치는 정확히 다시 수행할 수 있다. 각 단계의 input digest, cache hit, exit code를 기록하고 실패 뒤 보존된 container는 `debuggable`일 뿐 `ready`나 `verified`로 승격하지 않는다.

### 6.30 secret reference도 durable state와 log에서 최소화해야 한다

opaque reference라 해도 vault 경로·환경변수 이름·파일 경로는 민감한 구조를 드러낼 수 있다. secret 원문이나 reference를 project JSON, Git notes, command line, stdout/stderr, snapshot에 저장하지 않고 credential gateway가 run 시점에 짧은 lease로 resolve해야 한다. UI와 API는 이름, audience, expiry, redaction token만 보여주며 source와 문서가 주장하는 masking contract는 leakage fixture로 검증한다.

### 6.31 runtime generation은 stale stream과 preview를 fencing해야 한다

Cloudflare Sandbox SDK는 현재 runtime identity를 Durable Object storage에 기록하고 preview activation과 진행 중 operation을 해당 identity에 scope한다. container restart 뒤 durable configuration이나 token이 남아도 이전 runtime의 stream, port activation, completion event는 새 generation에 적용하지 않는다. 신규 도구도 executor/session/process/service event마다 generation을 붙여 늦게 도착한 event를 거부해야 한다.

### 6.32 idle은 request 반환이 아니라 live resource가 없는 상태여야 한다

RPC 호출이 stream handle을 반환한 뒤에도 peer는 계속 출력할 수 있다. Cloudflare 구현은 connection의 live imports/exports를 관찰하며 sleep deadline을 갱신한다. scheduler도 API promise, terminal silence, process existence 하나로 idle을 결정하지 말고 active stream, background process, service, interaction, resource lease를 합성해야 한다.

## 7. 재사용·라이선스 판단

- MIT: Orca, squad, MulmoTerminal, Agent Deck, Agetor, Overstory, Warren, Gas Town, Taskplane, Beads, OpenHands/Agent Canvas, OpenHands Software Agent SDK, acpx, AgentAPI, GitHub Agentic Workflows.
- Apache-2.0: Buzz, agtx, Emdash, Agent Orchestrator, sudocode, E2B, E2B Infra, Agent Client Protocol, Vercel Sandbox, Container Use, Cloudflare Sandbox SDK의 LICENSE 파일. Cloudflare 저장소 API는 SPDX를 `NOASSERTION`으로 반환하므로 재사용 시 파일/notice를 기준으로 재확인한다.
- AGPL-3.0: Claude Squad, Mux.
- 분석 제외: NTM의 추가 rider는 OpenAI/Anthropic 및 그 관계자의 사용·분석을 금지하므로 어떤 설계 근거나 재사용 대상에도 포함하지 않는다.

아키텍처 아이디어와 공개 프로토콜 비교는 가능하지만 실제 코드를 복사할 때는 각 파일의 라이선스·notice·파생 저작물 의무를 검토해야 한다. 특히 Claude Squad의 코드를 신규 도구에 직접 포함하는 것은 배포 모델에 따라 AGPL 의무가 발생할 수 있으므로 기본 전략은 clean-room 재구현으로 둔다. Archived인 Overstory는 유지보수 위험 때문에 fork 기반 제품화보다 아이디어 참조가 적합하다.

## 8. 신규 도구에 채택할 조합

| 채택 요소 | 참고 구현 | 신규 도구에서의 형태 |
|---|---|---|
| worktree/터미널 관제 | Orca, MulmoTerminal, Agent Deck | 네이티브 desktop/web UI + headless CLI |
| 가벼운 로컬 메시징 | squad | embedded SQLite typed message/task queue |
| 원격 signed collaboration | Buzz | 선택적 relay adapter; 로컬 실행의 필수 의존성은 아님 |
| DAG와 단계별 agent routing | Orca, agtx | scheduler kernel의 기본 기능 |
| 승인·질문 표면 | Agetor | agent adapter의 structured interaction contract |
| crash recovery | Agetor, Agent Deck | persisted run/session identity + reconciliation loop |
| watchdog와 merge queue | Overstory | mechanical watchdog + repo별 FIFO/priority merge lane |
| sandbox와 운영 관측성 | Warren | Governed/Remote 모드 executor |
| Windows 네이티브 | Orca, MulmoTerminal 일부 | ConPTY/Job Object 기반 first-class executor |
| durable workspace provisioning | Emdash | foreground ready point + replayable background setup/publish saga |
| wave/lane/polyrepo planning | Taskplane | critical-path scheduler와 repository segment |
| spec/issue/execution graph | sudocode | Git versioned intent + event-store runtime projection |
| atomic ready/claim | Beads | transactional claim + lease fencing |
| derived mission-control state | Agent Orchestrator | session·Git·PR·CI·review evidence projection |
| batch/bisect merge | Gas Town | 검증 실패를 분리하는 repository integration lane |
| remote sandbox lifecycle | E2B | local executor와 동일 계약을 쓰는 첫 cloud adapter |
| VM snapshot/data plane/placement | E2B Infra | remote executor readiness·network·cache locality 기준 |
| cost·patch preflight UX | Mux | clean-room으로 비용 가시화와 detached dry-run 구현 |
| backend registry/capability negotiation | OpenHands / Agent Canvas | local·remote·cloud backend health, protocol floor, tool advertisement, agent-view service topology |
| warm Agent Server protocol | OpenHands Software Agent SDK | dormant/init/ready state, per-user runtime binding, conversation worktree와 parent-child ownership |
| structured agent protocol | Agent Client Protocol | wire major/capability negotiation, session/update/permission/cancel, client filesystem/terminal |
| persistent ACP session/queue | acpx | cwd-scoped session, queue-owner generation lease, cooperative cancel, raw NDJSON |
| protocol-less CLI fallback | AgentAPI | HTTP/SSE bridge와 PTY heuristic; low-confidence adapter로만 사용 |
| persistent remote sandbox | Vercel Sandbox | sandbox/session/service state 분리, stop/resume hook, snapshot/fork, L3-L7 network-policy conformance |
| compiled event-triggered automation | GitHub Agentic Workflows | Markdown intent→validated lock manifest, read-only agent artifact, threat/safe-output write stage 분리 |
| local container workspace | Container Use | branch/worktree+container lineage, setup/install cache boundary, Git-backed state idea; secret handling은 재사용하지 않고 fail-closed로 재설계 |
| edge container executor | Cloudflare Sandbox SDK | Durable Object control plane, runtime-generation fencing, session/process/stream separation, sleep/backup/preview lifecycle |

이 분석을 바탕으로 [빠른 멀티 에이전트 오케스트레이션 기획](./FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md)과 [신규 도구 요구사항](./AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md)을 정의한다.
