# AI 코딩 에이전트 도구·서비스 조사

조사 기준일: 2026-08-14 (Asia/Seoul)

범위: 로컬 멀티 에이전트 도구, 호스팅형 코딩 에이전트, 원격 sandbox/devbox 서비스

## 1. 결론

AI 코딩 개발 환경을 빠르게 개선하려면 하나의 거대한 에이전트를 새로 만드는 것보다 다음 네 계층을 조합하는 편이 효과적이다.

1. **의도 계층**: spec, issue, acceptance criteria와 dependency graph를 버전 관리한다.
2. **control plane**: ready queue, atomic claim, concurrency budget, 질문·승인, watchdog, evidence projection, merge lane을 담당한다.
3. **agent adapter**: Codex, Claude, Gemini, Cursor 등 공급자별 launch/resume/steer/evidence 차이를 흡수한다.
4. **executor**: Windows native ConPTY/Job Object와 Linux native PTY/process group·cgroup, 로컬 worktree, WSL/SSH와 E2B/Runloop/Modal 같은 원격 sandbox를 공통 수명주기 계약 아래 플랫폼별 capability profile로 제공한다.

가장 중요한 제품 차별점은 agent 수가 아니라 **낮은 시작 지연**, **충돌 없는 병렬성**, **거짓 완료를 막는 증거**, **Windows와 Linux native 1급 지원**, **로컬과 클라우드 사이의 이동성**이다.

권장 조합은 다음과 같다.

- **MVP core**: cross-platform event kernel + 공통 executor contract + Windows native ConPTY/Job Object 및 Linux native PTY/process-group executor + ACP primary adapter + PTY fallback. Orca/Agent Orchestrator의 관제, Emdash의 staged provisioning, Beads/Taskplane의 claim·DAG, gh-aw의 proposal/write 권한 분리를 결합한다. Container Use의 branch/worktree+container 패턴은 host-native executor와 구분되는 선택형 local-container provider로 흡수한다.
- **Remote A/B pilot**: E2B와 Vercel Sandbox만 먼저 같은 conformance suite로 비교한다. self-host E2B Infra, Runloop, Modal, Cloudflare는 workload가 확인된 뒤 확장한다.
- **Workflow connector pilot**: GitHub Actions/gh-aw를 scheduled/issue-triggered automation에 쓰고 Linear와 Sentry는 task/incident source connector로만 둔다. 외부 서비스의 상태를 kernel source of truth로 만들지 않는다.
- **Review pilot**: Copilot Review와 CodeRabbit/Qodo/Greptile 중 하나를 비교하되 advisory evidence로만 수집한다. deterministic test, independent verifier, human approval을 대체하지 않는다.

## 2. 증거 경계

- 조사 당시 NTM을 제외한 34개 저장소를 분석하고 공개 부모 저장소의 submodule로 등록했다.
- 기존 10개 저장소에 Emdash, Gas Town, Taskplane, Agent Orchestrator, sudocode, Mux, Beads, E2B SDK, E2B Infra, OpenHands/Agent Canvas, OpenHands Software Agent SDK, Agent Client Protocol, acpx, AgentAPI, Vercel Sandbox, GitHub Agentic Workflows, Container Use, Cloudflare Sandbox SDK를 추가했다.
- 모든 분석 대상은 `--depth 1` shallow clone이며 checkout은 clean 상태다.
- 신규 5개는 DeepSeek Harness(plugin-composed harness), Hermes Agent·OpenClaw(personal assistant runtime/gateway), OpenAI Codex·Cline(coding-agent runtime) 계층에 둔다. 근거는 고정 SHA의 source와 문서이며 install, build, Windows 실행, remote provider, 실 agent E2E는 수행하지 않았다.
- Paseo는 multi-provider local control plane 계층에 추가했다. daemon·WebSocket·SDK/CLI/MCP, ACP/native provider adapter, worktree workspace, optional E2EE relay와 Windows source path를 고정 SHA에서 확인했지만 build/runtime/E2E는 수행하지 않았다.
- 의존성 설치, 전체 빌드, 실제 에이전트 실행, E2E, 서비스 가입이나 유료 기능 검증은 하지 않았다.
- GitHub 수치와 서비스 기능은 조사일의 공개 정보 스냅샷이다. 요금, 한도, 지원 플랫폼은 별도 구매 결정 전에 다시 확인해야 한다.
- `ntm`은 clone 후 LICENSE의 추가 rider가 OpenAI/Anthropic 및 그 관계자의 사용·분석을 금지함을 발견했다. 즉시 분석에서 제외했으며 삭제는 명시적 승인 전까지 보류한다.

## 3. 추가 클론한 구현체

| 프로젝트 | 중심 역할 | 소스에서 확인한 핵심 | Windows/배포 관점 | 라이선스 | 판단 |
|---|---|---|---|---|---|
| [Emdash](../multi-agent-tools/emdash/) | cross-platform agent desktop | stage-tagged worktree 생성, 빠른 durable half와 background tail, local/SSH runtime, PTY/ACP | 네이티브 Windows와 SSH를 함께 지원 | Apache-2.0 | workspace provisioning saga의 가장 좋은 참고 구현 |
| [Gas Town](../multi-agent-tools/gastown/) | 대규모 agent town/merge 운영 | mailbox·handoff, Witness 복구, Deacon patrol, Bors식 Refinery merge queue, Beads/Dolt 상태 | 전체 기능은 tmux/WSL 중심 | MIT | 운영 원칙은 강력하지만 역할 체계는 그대로 복제하지 않음 |
| [Taskplane](../multi-agent-tools/taskplane/) | 계획 기반 multi-agent orchestrator | DAG를 wave/lane으로 실행, polyrepo segment, worker/reviewer/merger, checkpoint commit | Windows cleanup fallback과 테스트 존재 | MIT | critical path와 동일 context review 설계에 채택 |
| [Agent Orchestrator](../multi-agent-tools/agent-orchestrator/) | daemon + desktop fleet control | session/worktree, PR·CI·review 사실에서 card 상태 파생, native ConPTY backend | Windows ConPTY 구현이 명확함 | Apache-2.0 | Windows runtime과 mission-control projection 기준점 |
| [sudocode](../multi-agent-tools/sudocode/) | spec/issue/execution graph | WHAT인 spec과 HOW인 issue, execution trajectory를 Markdown+JSONL·MCP로 연결 | 로컬 우선, Git 친화적 | Apache-2.0 | 대화가 아닌 버전 관리된 의도 그래프에 채택 |
| [Mux](../multi-agent-tools/mux/) | provider-neutral coding agent desktop | local/worktree/SSH runtime, cost·token·compaction UX, patch dry-run, workspace path 제한 | 현재 공개 배포는 Windows 공백이 있음 | AGPL-3.0 | UX·검증 패턴 참고; 제품 코드 직접 재사용은 보류 |
| [Beads](../multi-agent-tools/beads/) | dependency-aware task memory | blocker-aware ready queue, atomic `ready --claim`, Dolt 동시성, 메시지/thread, JSONL 교환 | native Windows 안내 존재 | MIT | task graph와 atomic claim의 기준 구현 |
| [E2B](../multi-agent-tools/e2b/) | 원격 secure sandbox SDK | commands·PTY·filesystem·Git, pause/resume, snapshot/fork, network config, JS/Python SDK | control plane은 Windows에서도 API 사용 가능; runtime은 cloud Linux | Apache-2.0 | 첫 remote executor 후보 |
| [E2B Infra](../multi-agent-tools/e2b-infra/) | self-hostable sandbox control/data plane | Firecracker, UFFD lazy memory, COW rootfs, per-sandbox netns/nftables, best-of-K placement, envd readiness | GCP 지원, AWS beta; Linux root 권한·Nomad/Terraform 운영 필요 | Apache-2.0 | remote executor 보안·성능·배치의 구현 기준점 |
| [OpenHands / Agent Canvas](../multi-agent-tools/openhands/) | multi-backend agent control center | local·remote·cloud backend registry, `/server_info` 버전·도구·runtime service probe, ACP agent, local/cloud runtime adapter | host 직접 실행은 사용자 filesystem·network 권한을 가지므로 Docker/VM 또는 엄격한 host scope가 필요 | MIT | 공급자 중립 UI와 backend capability negotiation의 기준점 |
| [OpenHands Software Agent SDK](../multi-agent-tools/openhands-agent-sdk/) | composable SDK + remote Agent Server | local/ephemeral workspace, REST/WebSocket conversation, per-conversation worktree, usable tools/capabilities, dormant→ready warm-pool init | Kubernetes/Docker에 적합하나 host local은 사용자 권한; 일부 stress test는 POSIX 전용 | MIT | backend protocol, credential binding, warm executor lifecycle의 실제 구현 기준점 |
| [Agent Client Protocol](../multi-agent-tools/agent-client-protocol/) | editor↔coding-agent interoperability protocol | stable v1 JSON-RPC wire version/capability negotiation, session/prompt/update/cancel, permission, client filesystem/terminal, schema artifacts | trusted editor-agent 모델이며 sandbox나 scheduler 자체는 제공하지 않음 | Apache-2.0 | structured adapter의 primary protocol |
| [acpx](../multi-agent-tools/acpx/) | headless stateful ACP client/backend | cwd·agent·name scope, persistent session, queue owner IPC/generation lease, cooperative cancel, raw NDJSON, permission policy, flow/compare | pre-1.0이라 CLI/runtime 호환성이 변할 수 있음 | MIT | session continuity와 prompt queue의 참고 구현 |
| [AgentAPI](../multi-agent-tools/agentapi/) | coding CLI HTTP compatibility bridge | 다수 CLI를 PTY screen diff로 HTTP/SSE화하고 experimental ACP도 제공 | TUI 변화와 screen heuristic에 취약; `stable`은 검증 완료가 아님 | MIT | 정식 protocol이 없는 CLI의 low-confidence fallback |
| [Vercel Sandbox](../multi-agent-tools/vercel-sandbox/) | hosted persistent MicroVM SDK/CLI | named sandbox와 running session 분리, stop 시 snapshot, get/resume·`onResume`, fork, OCI image, port preview, domain/subnet 및 L7 network policy | Windows는 remote API client 경로이고 runtime은 Linux MicroVM; 기본 image의 coding agent·passwordless sudo와 기본 egress를 project policy로 축소해야 함 | Apache-2.0 | E2B와 비교할 두 번째 remote executor 및 persistent lifecycle 기준점 |
| [GitHub Agentic Workflows](../multi-agent-tools/gh-aw/) | Markdown→GitHub Actions agent workflow compiler | YAML frontmatter+Markdown을 `.lock.yml`로 compile, strict schema/expression/action-pin validation, read-only agent job, AWF sandbox/firewall, buffered safe-output와 별도 write job | CLI는 Windows에서도 설치 가능하지만 실행 substrate는 Actions runner; 대형 repo는 partial+sparse clone으로 핵심 compiler/docs만 checkout | MIT | event/schedule 기반 Continuous AI와 최소권한 stage compiler 기준점 |
| [Container Use](../multi-agent-tools/container-use/) | MCP/CLI local container workspace | 환경별 branch/worktree, Dagger container, setup-before-source cache, service binding, 실행 결과 export·commit, Git notes 상태·명령 로그 | Dagger runtime과 privileged nesting을 사용하며 native Windows/ConPTY executor가 아님. config와 state에 secret reference 문자열이 남고 현재 CLI가 이를 그대로 출력하므로 secret 정책은 재설계 필요 | Apache-2.0 | 재현 가능한 local-container executor의 유력 기준점이지만 secret subsystem은 clean-room 재설계 |
| [Cloudflare Sandbox SDK](../multi-agent-tools/cloudflare-sandbox-sdk/) | hosted container SDK/control plane | Worker→Durable Object→capnweb RPC WebSocket→container service의 3계층, command/file/process/session, runtime identity, sleep-after, R2 backup, runtime-scoped preview activation | local dev는 Docker가 필요하고 실제 isolation·capacity·retention은 Cloudflare platform 계약이다. session은 cwd/env context이지 별도 VM이 아니며 preview token은 durable해도 restart 뒤 재활성화가 필요 | Apache-2.0 파일(Forge API는 `NOASSERTION`) | remote executor generation fencing, control/data-plane, service readiness의 강한 기준점 |
| [Paseo](../multi-agent-tools/paseo/) | multi-provider local agent control plane | daemon, WebSocket/SDK/CLI/MCP, native·ACP provider adapter, worktree workspace, permission/schedule, optional E2EE relay | Windows executable·ConPTY·`.cmd` 경로는 정적 확인했지만 host subprocess는 sandbox가 아니며 실제 Windows 실행은 미검증 | AGPL-3.0 계열(파일별 확인) | cross-device 관제와 provider-neutral UX를 pilot하고 protocol/state pattern만 clean-room 참고 |

### 3.1 코드 구조에서 얻은 구체적 교훈

- Emdash의 `createWorktree` 경로는 inspect부터 worktree 생성까지 foreground stage로 기록하고, agent가 시작 가능한 시점 이후 artifact clone·push 같은 작업을 durable background tail로 넘긴다. 신규 도구도 `worktree_ready`를 조기 반환하되 setup/publish 결과를 잃지 않는 staged saga로 구현해야 한다.
- Taskplane은 DAG를 단순 ready 목록으로 보지 않고 wave와 lane, polyrepo segment로 계획한다. scheduler는 critical path와 repository별 segment를 모두 알아야 한다.
- Agent Orchestrator는 terminal 문자열 하나가 아니라 session, PR, CI, review의 사실로 카드 상태를 계산한다. UI 상태는 이벤트의 projection이어야 하며 사용자가 직접 임의 변경하는 단일 status 필드가 아니어야 한다.
- sudocode는 spec, issue, execution을 분리한다. 장기 의도와 acceptance는 chat transcript가 아니라 Git에 남는 선언형 그래프로 관리해야 한다.
- Beads의 atomic claim은 여러 worker가 같은 task를 동시에 가져가는 경쟁을 막는다. `ready` 조회와 `claim`은 하나의 트랜잭션이어야 한다.
- Mux의 detached worktree dry-run은 patch 적용 전에 충돌을 싸게 탐지하는 패턴이다. agent 산출물을 실제 작업 branch에 반영하기 전 검증 workspace를 사용할 수 있다.
- E2B의 pause/resume는 하나의 sandbox를 보존하는 1:1 수명주기이고 snapshot은 같은 초기 상태에서 여러 sandbox를 만드는 1:N fan-out이다. warm pool과 speculative 실행에는 snapshot/fork가 더 적합하다.
- E2B Infra는 sandbox 생성을 cold boot가 아니라 pre-booted Firecracker snapshot 복원으로 처리하고, memory page와 rootfs block을 lazy/COW로 가져온다. warm 시작 SLO는 단순 process spawn이 아니라 snapshot locality와 page/block fetch까지 측정해야 한다.
- E2B Infra의 API는 node를 고른 뒤 VM의 envd `/init`가 성공할 때까지 기다린다. `executor_ready`는 VM process 존재가 아니라 authenticated tool endpoint의 readiness probe 통과여야 한다.
- control plane은 placement·auth·quota·catalog를 담당하고 sandbox traffic은 data plane으로 직접 흐른다. 대용량 PTY/file/preview traffic을 orchestration event API로 우회시키지 않아야 한다.
- workload identity는 raw credential을 VM에 전달하는 대신 identity definition만 전달하고 runtime에서 권위 있는 team/sandbox/execution id로 파생한다. fork는 identity를 자동 상속하지 않는 것이 안전한 기본값이다.
- ConPTY나 PTY는 입출력 transport이지 보안 경계가 아니다. 로컬 executor는 사용자 권한으로 동작하며 격리가 필요하면 container/VM sandbox로 승격해야 한다.
- Agent Canvas는 frontend를 실행기와 분리하고 여러 local·remote·cloud backend를 registry로 관리한다. control surface는 특정 sandbox provider를 하드코딩하지 말고 backend identity, auth mode, connection revision, health를 일급 상태로 가져야 한다.
- Agent Server의 `/server_info`는 최소 호환 버전, `usable_tools`, `runtime_services`를 제공한다. 연결 성공만으로 실행 가능하다고 판단하지 말고 protocol version과 capability를 협상하고, 지원하지 않는 도구는 UI와 scheduler에서 비활성화해야 한다.
- runtime service URL은 browser 또는 host 관점이 아니라 **agent가 실행되는 sandbox 관점**에서 backend가 광고하고 system context에 주입해야 한다. `localhost`나 고정 port를 추측하는 방식은 local·Docker·remote topology가 바뀌면 실패한다.
- 저장된 secret은 이름과 opaque lookup handle만 conversation 생성 payload에 보내고 agent server가 spawn 시점에 해석하는 경계가 적합하다. browser storage나 snapshot에 provider credential 원문을 두지 않아야 한다.
- OpenHands Agent Server는 `/alive`와 `/ready`를 분리하고, warm pool에서는 process를 `dormant`로 미리 띄운 뒤 `POST /api/init`에서 사용자별 workspace·session key·secret key·webhook·concurrency를 결합한다. warm capacity는 준비 비용을 줄이되 dormant process를 runnable로 오인하지 않는 명시적 state machine이 필요하다.
- deferred init은 concurrent call을 lock으로 직렬화하고 실패 시 `dormant`로 되돌아가 재시도한다. 이 전이는 idempotency와 generation token을 추가한 provisioning saga로 흡수하는 것이 좋다.
- Agent Server는 conversation별 worktree를 만들고 parent/child conversation은 같은 workspace에만 연결한다. sub-agent 계보와 workspace ownership을 함께 검증하면 부모가 다른 repository의 child를 잘못 소유하는 것을 막을 수 있다.
- ACP는 package/schema artifact version과 wire `protocolVersion`을 분리한다. adapter compatibility는 package semver를 추정하지 말고 initialize에서 합의한 major wire version과 누락 시 unsupported인 capability snapshot을 기준으로 해야 한다.
- ACP의 terminal/file method는 client가 실행 권한을 소유하는 역방향 요청이다. agent가 protocol을 지원한다는 사실만으로 filesystem/terminal을 허용하지 말고 client capability와 project policy를 교차시켜야 한다.
- `session/prompt` 응답의 `stopReason=end_turn`, tool-call `completed`, terminal exit code, task verification은 서로 다른 층이다. structured protocol을 사용해도 완료 evidence gate는 별도로 유지한다.
- acpx는 session을 `(agentCommand, absoluteCwd, optional name)`으로 scope하고 live ACP connection을 queue-owner lease가 소유한다. named pipe/Unix socket, random generation, heartbeat/process probe를 조합해 같은 session의 concurrent adapter spawn을 막는 패턴이 유용하다.
- crash 뒤 provider session resume/load가 실패했을 때 acpx는 새 session fallback을 허용하지만, 신규 도구의 governed mode에서는 context continuity 손실을 숨기지 말고 새 attempt와 명시적 approval을 요구해야 한다.
- AgentAPI는 protocol이 없는 agent를 폭넓게 지원하는 좋은 완충층이지만 screen stability와 input-box 탐지에 의존한다. adapter마다 `structured`, `hybrid`, `heuristic` confidence를 표시하고 heuristic 신호로 verification/merge 상태를 올리지 않아야 한다.
- Vercel Sandbox는 영속 `Sandbox` identity와 그 안에서 실제로 실행 중인 `Session`을 분리한다. `stop()` 뒤 자동 snapshot이 생기고 이후 `get()`/resume 시 `onResume` hook으로 service를 복원하므로, control plane도 `workspace_exists`, `executor_running`, `services_ready`를 각각 추적해야 한다.
- snapshot/fork는 filesystem과 환경을 복제하더라도 run identity, secret lease, network exception을 자동 상속하는 근거가 아니다. child마다 새 policy binding과 credential audience를 발급하고 snapshot 직전 secret scan을 통과시켜야 한다.
- domain/subnet allow·deny와 HTTP request matcher/header transform/forward proxy는 네트워크 정책의 서로 다른 층이다. 제품 UI는 L3/L4 destination 정책과 L7 request rewrite·proxy를 분리해 보여주고, provider 기본값보다 project의 deny-by-default 정책을 우선해야 한다.
- SDK client가 Workflow 객체 등에 직렬화된 뒤 복원될 수 있어도 access token을 객체 상태에 함께 넣어서는 안 된다. 재수화 시 workload identity나 OIDC로 짧은 수명의 client를 다시 얻는 credential gateway가 필요하다.
- gh-aw는 자연어 workflow source를 직접 실행하지 않고 compiler가 schema, GitHub expression, action pin, template injection, strict permission/network policy를 검증한 `.lock.yml`을 만든다. 신규 도구의 policy도 실행 시점의 문자열 검사보다 **compile/plan 시점의 immutable execution manifest**로 내려야 한다.
- gh-aw의 agent job은 외부 state에 직접 write하지 않고 산출물을 artifact로 buffer한다. 별도 threat-detection job과 scope별 권한을 가진 safe-output job이 통과한 것만 GitHub에 반영한다. AIDE Fleet의 외부 쓰기도 `agent proposal → deterministic validation → policy/optional AI detection → scoped committer`로 분리해야 한다.
- sandbox/firewall, MCP gateway, API proxy, safe-output은 서로 다른 trust layer다. container가 있다고 secret·MCP key·runner host가 안전해지는 것은 아니며 compiler가 생성한 stage graph와 credential distribution을 evidence로 보존해야 한다.
- gh-aw는 strict mode를 기본값으로 두고 기존 lock manifest를 working copy가 아니라 Git `HEAD`에서 읽어 privilege 변경의 기준선으로 사용한다. 신규 도구도 새 manifest가 permission, secret audience, network, MCP, external write, unpinned dependency를 넓히면 일반 재compile이 아니라 명시적 policy approval을 요구해야 한다.
- Container Use는 환경마다 고유 branch와 worktree를 만들고, 빈 초기 commit으로 같은 부모 commit의 state note 덮어쓰기를 피한다. worktree의 파일 격리와 container의 dependency/process 격리를 함께 쓰되 branch, worktree, container digest, run generation을 하나의 lineage로 연결해야 한다.
- setup command는 source mount 전에 실행해 image/cache 재사용을 높이고 install command는 source mount 뒤 실행한다. 이 두 단계의 input digest와 cache hit를 분리하면 빠른 시작과 소스 의존 설치의 정확성을 함께 측정할 수 있다.
- command exit가 0이 아니어도 마지막 container state를 보존하는 설계는 디버깅에는 유용하지만 성공으로 승격할 근거는 아니다. command·exit code·stdout/stderr는 실행 evidence이며 독립 verifier 결과와 별도로 저장해야 한다.
- Container Use의 현재 구현은 `Secrets` 문자열을 project JSON과 Git notes state에 포함하고 `config show/list`에서 값까지 출력한다. 문서의 dynamic resolution/masking 주장과 소스 구현이 일치하지 않으므로 신규 도구는 opaque secret reference만 저장하고 resolve는 credential gateway 안에서 수행하며 terminal, event, note, snapshot에는 이름과 redaction token만 남겨야 한다.
- Dagger container는 유용한 실행 경계지만 `ExperimentalPrivilegedNesting`을 켠 run/service 경로가 있다. `container=true`를 강한 보안 등급으로 간주하지 말고 runtime, host mount, privileged nesting, network, secret audience를 manifest capability로 명시해야 한다.
- Cloudflare Sandbox SDK는 Worker와 container 사이의 primary control path를 Durable Object→RPC WebSocket→container-side service로 두고 HTTP route client는 compatibility path로 유지한다. 신규 executor adapter도 domain API와 wire transport를 분리해 transport 교체가 Task/Run 계약을 바꾸지 않게 해야 한다.
- Durable Object storage에 현재 runtime identity를 보존하고 stream·preview activation을 해당 generation에 scope한다. container가 재시작되면 durable preview token 자체는 남아도 activation은 stale이므로 다시 `exposePort`해야 한다. 이 패턴은 stale session/stream/preview event fencing에 직접 채택할 수 있다.
- 단일 RPC promise가 반환돼도 peer가 반환한 stream은 계속 busy일 수 있어 SDK가 RPC import/export table을 관찰하며 sleep deadline을 갱신한다. remote executor의 idle 판단도 API call 반환이나 terminal silence가 아니라 live stream/process/resource lease를 포함해야 한다.
- session은 cwd·env를 나누는 execution context이며 sandbox/container와 동일한 isolation 단위가 아니다. `sandbox_id`, `runtime_generation`, `session_id`, `process_id`, `service_preview_activation`을 각각 추적해야 한다.
- Cloudflare의 platform 문서는 sandbox별 VM isolation을 제공한다고 명시하지만 같은 sandbox의 모든 session은 filesystem·process·network를 공유한다. multi-tenant 또는 서로 신뢰하지 않는 agent는 session이 아니라 sandbox를 분리해야 한다.
- Paseo는 여러 provider의 native adapter와 generic ACP adapter를 같은 daemon/client 표면에 투영한다. control plane은 provider별 mode·permission·session capability를 공통 최소값으로 평탄화하지 말고 실행 시 snapshot해야 한다.
- Paseo의 worktree workspace와 optional E2EE relay는 각각 파일 상태 분리와 전송 보호다. agent process는 기존 사용자 credential을 가진 host subprocess이므로 별도 executor/sandbox와 credential policy를 유지해야 한다.
- outbound handler/allowlist는 강력하지만 programmable interception 범위는 HTTP/HTTPS다. public internet을 켜 둔 상태의 비-HTTP traffic을 같은 정책이 막는다고 가정하지 말고 `enableInternet=false`를 기본으로 한 뒤 protocol별 enforcement coverage를 Evidence에 남겨야 한다.
- credential은 sandbox env/file로 직접 주기보다 trusted Worker proxy가 short-lived JWT를 검증한 뒤 upstream 요청에 실제 credential을 붙이는 구조가 낫다. 이는 AIDE Fleet의 scoped committer/credential gateway를 data-plane API 호출에도 확장한 패턴이다.
- custom-domain preview와 quick tunnel은 다른 노출 방식이다. quick tunnel은 별도 access token이 없고 restart 때 URL이 바뀌므로 민감한 service에는 사용하지 않으며 preview/tunnel마다 authentication, hostname stability, TTL, restart semantics를 capability로 광고해야 한다.
- 같은 Cloudflare sandbox ID/Durable Object를 다시 얻어도 10분 기본 idle sleep 뒤 새 container는 clean filesystem으로 시작한다. Vercel의 stop→automatic snapshot과 의미가 다르므로 executor는 `ephemeral_reset`, `automatic_snapshot`, `explicit_backup_restore`, `persistent_volume`을 별도 persistence capability로 선언해야 한다.

## 4. 호스팅형 도구·서비스

| 서비스 | 실행 위치와 병렬 모델 | 강점 | 주의점 | AIDE Fleet에 반영할 요소 |
|---|---|---|---|---|
| [Conductor](https://www.conductor.build/docs/concepts/parallel-agents) | Mac 로컬, Git worktree workspace | 독립 배포 작업은 별도 workspace, 구현·review·test처럼 결합된 일은 동일 workspace에 여러 agent 배치 | workspace는 파일 상태를 격리하지만 OS 권한은 격리하지 않음 | `workspace_group`을 명시하고 shared/isolated를 planner가 선택 |
| [Claude Code agent view/teams](https://code.claude.com/docs/en/agents) | local background session, subagent, experimental team, worktree session | shared task list·direct inter-agent message·file-lock claim·completion hook·plan approval; 독립 task는 agent view/worktree | team은 teammate를 worktree로 자동 격리하지 않고 token 사용량이 크게 늘며 resume/shutdown 제약이 있음 | 단순 subagent, independent fleet, communicating team을 별도 orchestration mode로 제공 |
| [Codex cloud](https://developers.openai.com/codex/cloud) | 격리된 cloud environment에 여러 task 병렬 위임 | 웹·GitHub·Linear·Slack 진입점, 재현 가능한 environment, diff/follow-up/PR 흐름 | cloud/local 간 capability와 secret 정책 차이를 명시해야 함 | 동일 Task/Run 계약 위에 cloud adapter 제공 |
| [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents) | task별 ephemeral environment | GitHub 안에서 session 관리, test/lint, signed commit과 session-log 추적성 | [firewall은 Bash가 시작한 process에만 적용되고 MCP/setup step은 제외](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-firewall) | commit→session→evidence provenance와 firewall coverage 표시 |
| [GitHub Agentic Workflows](https://github.github.com/gh-aw/) | Markdown workflow를 Actions의 sandboxed agent job과 후속 write job으로 compile | issue/PR/schedule trigger, multi-engine, read-only default, safe outputs, threat detection, credit budget·OpenTelemetry | Public Preview이며 비결정적 reasoning을 deterministic CI/CD 대체재로 사용하면 안 됨 | local kernel을 대체하지 않고 event-triggered external executor/connector로 통합; source hash와 compiled lock hash를 Run에 고정 |
| [Cursor Background Agents](https://docs.cursor.com/background-agent) | isolated Ubuntu VM, 별도 branch | 비동기 실행, follow-up/takeover, snapshot 기반 환경 설정 | internet access와 terminal auto-run으로 prompt injection·exfiltration 위험 | remote run은 egress/auto-run/retention을 사용자에게 노출 |
| [Devin Managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities) | child session마다 isolated VM | coordinator가 분해·감시·충돌 해결·결과 취합, child별 비용 한도, wait-all API | 강한 vendor 종속과 비용 관리 필요 | child budget, wait-all event, coordinator는 제안자이고 scheduler는 기계적 source of truth |
| [Jules](https://jules.google/docs/tasks-repos) | task마다 독립 short-lived VM | 동시에 여러 task, plan approval, task별 log/environment/code 분리 | GitHub 중심이며 서비스 quota가 변할 수 있음 | plan approval과 task별 immutable environment record |
| [Factory Droids](https://docs.factory.ai/reference/cli-reference) | local·CI·remote 배포 선택 | spec mode, worktree, structured output, 단계별 autonomy, event-driven automation | 높은 autonomy는 격리 sandbox에서만 안전 | `read_only/low/medium/high` capability profile과 trigger automation |
| [GitHub Agent HQ](https://github.com/features/copilot/agents) | GitHub의 agent session 관제 | 여러 agent와 PR workflow를 한 화면에서 추적 | 구현 세부와 지원 agent가 계속 변함 | 공급자 중립 mission-control UX 참고 |
| [Coder Agents](https://coder.com/docs/ai-coder/agents) | self-hosted control plane + 필요할 때 provision하는 workspace | agent loop와 model key를 control plane에 두고 workspace에는 AI key/software가 없어도 됨; sub-agent와 template routing | Beta이며 Coder 운영·template 설계가 필요 | agent reasoning과 tool execution을 분리하고 compute-lazy provisioning 채택 |
| [GitLab Duo Agent Platform](https://docs.gitlab.com/user/duo_agent_platform/) | GitLab.com·Self-Managed·Dedicated의 flow/session, CI runner 또는 IDE local | Developer·Review·CI fix·Security flow와 custom/external agent를 GitLab issue/MR/CI 권한 체계에 연결 | hosted와 self-managed의 edition·version·credit·runner 제약이 다름 | forge의 issue→session→draft MR→review evidence를 connector로 수용하고 control plane은 대체하지 않음 |
| [JetBrains AI agents](https://www.jetbrains.com/help/ai-assistant/agents.html) | IDE 안에서 Junie·Claude·Codex·Copilot·ACP agent 선택 | 기존 IDE project model, `AGENTS.md`, skills, MCP를 여러 agent에 공통 제공 | agent별 autonomy mode와 instruction/ignore 지원 차이가 큼 | backend capability matrix와 project instruction precedence를 명시적으로 노출 |
| [Sourcegraph Agentic Batch Changes](https://sourcegraph.com/docs/agentic-batch-changes) | 다수 repository를 isolated executor에서 병렬 변경하고 changeset으로 게시 | code graph로 범위를 정하고 deterministic script와 Codex/Claude coding-agent step을 작업 특성에 따라 라우팅, CI hook·rollout window·RBAC | fleet migration용 beta이며 단일 repo interactive loop 대체재가 아님 | multi-repo 작업에서 deterministic transform 우선, 판단이 필요한 부분만 agent에 위임하는 cost-aware router |
| [Linear coding sessions](https://linear.app/docs/coding-sessions) | issue에서 Claude Code·Codex session을 위임하고 draft PR까지 추적 | 사람 assignee를 ownership source로 유지한 채 agent에 실행을 위임하고 diff·PR·session history를 issue context에 연결 | issue 상태와 agent run 상태를 같은 값으로 취급하면 ownership·완료가 왜곡됨 | `human_owner`, `delegated_agent`, `run`, `draft_pr`를 별도 관계로 보존하고 workspace/team guidance precedence를 snapshot |
| [Sentry Seer](https://docs.sentry.io/product/ai-in-sentry/seer) | production observability를 바탕으로 root cause 분석부터 code change·PR까지 비동기 실행 | error trace·logs·profile·code context에서 actionability를 판정하고 multi-repo fix를 단계별 `stopping_point`까지 수행 | 자동 제안이나 PR 생성은 배포·운영 해결 증거가 아니며 production data·repository access 경계가 큼 | incident→analysis→proposal→change→PR을 별도 stage로 모델링하고 async run id와 observability provenance를 evidence에 연결 |
| [GitHub Copilot code review](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/code-review) | draft/open/new-push PR에 수동 또는 자동 review, agentic runner로 추가 context 수집 | repository/path instruction, skills·MCP, suggested fix, 새 push 재검토 | review는 항상 `COMMENT`이며 required approval이나 merge block이 아니고, runner가 없으면 제한된 mode로 fallback할 수 있음 | review head SHA, capability/mode, instruction revision을 고정하고 comment를 approval/verification과 분리 |
| [CodeRabbit](https://docs.coderabbit.ai/guides/code-review-overview) | PR open/commit마다 multi-model·static analysis 기반 incremental review | severity/type, security·summary·one-click fix, team learning과 multi-repo/MCP/issue context, CLI/IDE feedback | context source와 learned rule이 늘수록 provenance·privacy·stale guidance 관리가 필요 | reviewer finding을 stable fingerprint와 head SHA로 수집하고 accepted/rejected/false-positive feedback을 quality metric으로 환류 |
| [Qodo Code Review](https://docs.qodo.ai/code-review) | multi-agent PR review와 조직 rule/compliance 적용 | codebase·PR history·명시 요구에서 rule system을 구성하고 global/group/repo hierarchy로 compliance 적용 | AI rule 판단과 label 자체는 deterministic branch protection이나 human approval이 아님 | policy revision·scope·finding confidence를 기록하고 deterministic rule/check와 AI finding을 별도 evidence class로 유지 |
| [Greptile](https://www.greptile.com/docs/introduction) | repository-wide graph context로 PR 자동 review 후 agent별 fix handoff | function/class/dependency graph 기반 cross-file 영향 분석, finding을 Codex·Claude·Cursor·Devin 등에 전달 | 외부 code indexing과 vendor context graph의 freshness·retention·권한을 평가해야 함 | code-graph revision과 reviewed head SHA를 연결하고 finding→fix Run→re-review의 폐루프를 추적 |

서비스 조사에서 얻은 공통 원칙은 다음과 같다.

1. 별도 PR로 배포 가능한 단위는 별도 workspace, 같은 branch의 구현·review·test는 shared workspace가 더 빠르다.
2. 원격 agent는 항상 branch, session log, environment definition, initiator, 비용, network policy와 연결돼야 한다.
3. plan 승인, command 권한, merge 승인과 같은 서로 다른 gate를 하나의 “승인” 상태로 뭉치지 않는다.
4. cloud firewall의 존재를 완전한 데이터 유출 방지로 표현하지 않는다. 실제 적용 범위와 우회 가능성을 evidence에 남긴다.
5. agent loop가 반드시 code workspace 안에 있을 필요는 없다. Coder처럼 model 호출과 policy는 control plane에 두고 파일·명령 tool만 workspace connection으로 실행하면 credential·egress 경계가 단순해진다.
6. 계획·질문처럼 compute가 필요 없는 turn은 즉시 처리하고, 실제 read/write/command 시점에만 workspace를 provision하는 compute-lazy 경로가 시작 지연과 비용을 줄인다.
7. coordinator에게만 보고하는 subagent와 worker끼리 직접 협의하는 team은 비용·상태·복구 계약이 다르다. 직접 통신은 상호 도전이 필요한 research/review에만 쓰고, 독립 구현은 worktree fleet가 단순하고 안전하다.
8. agent가 task를 `completed`로 바꾸기 전 hook/verifier가 거부할 수 있어야 한다. claim의 file lock만으로는 process crash 뒤 stale ownership을 다루기 어려우므로 persistent fencing token을 추가한다.
9. 모든 작업을 LLM agent에 맡기지 않는다. Sourcegraph처럼 기계적으로 표현 가능한 변경은 deterministic script로 실행하고, repository별 변형과 판단이 필요한 step만 coding agent로 라우팅하면 비용과 변동성을 줄일 수 있다.
10. IDE·forge·desktop·cloud control surface는 같은 agent라도 서로 다른 capability와 policy를 제공한다. 실행 전에 backend가 실제 지원하는 worktree, sub-agent, skill, MCP, network, secret, review 기능을 협상하고 snapshot으로 보존해야 한다.
11. AI reviewer의 comment, suggested fix, compliance label은 독립 verification이나 사람 approval이 아니다. reviewed head SHA가 바뀌면 stale로 표시하고 재검토해야 하며, finding→수정→re-review→resolved/false-positive를 stable fingerprint로 추적해야 한다.
12. learned rule, repository graph, MCP, issue history처럼 review context가 풍부할수록 결과 provenance가 중요하다. 어떤 policy/context revision으로 판단했는지 없으면 재현도·감사도 할 수 없다.

## 5. Sandbox·devbox 서비스

| 서비스 | 수명주기·성능 기능 | 보안·운영 기능 | 적합한 사용 |
|---|---|---|---|
| [E2B](https://e2b.dev/docs/sandbox/persistence) | create/connect/pause/resume/kill, memory+filesystem snapshot, fork | workload identity, network 설정, SDK·self-host 경로 | interactive remote agent, snapshot fan-out |
| [Runloop Devboxes](https://docs.runloop.ai/docs/devboxes/overview) | 수초 내 VM, stateful/stateless, snapshot/suspend/resume, blueprint | egress Network Policy, credential을 숨기는 Agent Gateway/MCP Hub | enterprise repo build/test, 장기 세션 |
| [Modal Sandboxes](https://modal.com/docs/guide/sandboxes) | secure container, filesystem/directory/memory snapshot, 최대 실행 시간 정책 | resource 제한, log·snapshot retention 문서화 | burst test, 대규모 동일 초기 상태 실험 |
| [Daytona](https://www.daytona.io/docs/en/guides/) | on-demand sandbox API와 lifecycle | 서비스형 secure runtime | 후보 비교군; clone은 라이선스 식별 전 보류 |
| [Vercel Sandbox](https://vercel.com/docs/sandbox) | persistent named MicroVM, stop→snapshot, get/resume, fork, session·snapshot 목록 | OIDC 권장, custom OCI image, domain/subnet 및 L7 request policy, port preview | remote coding agent, long-lived workspace, preview와 network-policy 실험 |
| [Cloudflare Sandbox](https://developers.cloudflare.com/sandbox/) | container commands·files·background process·service·preview, Durable Object별 격리와 coordination | RPC/HTTP bridge, session, tokenized preview, runtime-generation fencing, R2 backup; 공식 SDK source도 clone 분석 | edge-triggered short/medium task와 웹 서비스 preview; Paid plan·platform capacity/retention/egress와 custom-domain 요구를 pilot 전에 확인 |

### 5.1 공통 remote executor 계약

```yaml
executor_profile:
  provider: local-conpty | ssh | e2b | runloop | modal | vercel | cloudflare
  isolation: user_process | container | vm
  image_or_snapshot: immutable-reference
  repository: url + base_sha
  resources: cpu + memory + disk + timeout
  network: deny | allowlist | unrestricted
  secrets: opaque-handles
  retention: logs + workspace + snapshots
  lifecycle: create + ready + exec + observe + stop + resume + snapshot + fork + terminate
```

provider가 지원하지 않는 capability는 조용히 무시하지 않고 `unsupported`로 반환해야 한다. 예를 들어 local ConPTY에 `isolation: vm`을 요청하면 실행을 거부해야 한다.

## 6. 기능 커버리지와 시장 공백

| 능력 | 공개 도구에서 강한 사례 | 서비스에서 강한 사례 | 남은 공백 |
|---|---|---|---|
| 빠른 workspace 시작 | Emdash, Mux | E2B, Runloop, Modal snapshot | Windows local과 cloud를 같은 지표로 비교하는 control plane |
| task graph/claim | Beads, Taskplane, Gas Town | Devin managed sessions | spec→issue→run→evidence의 end-to-end provenance |
| native Windows | Orca, Agent Orchestrator, Emdash | 대다수 cloud는 Linux | ConPTY+Job Object와 cloud VM의 동일 lifecycle API |
| 협업·audit | Buzz, Gas Town | GitHub signed commit/session log | agent message, Git evidence, external/physical evidence의 명시적 분리 |
| merge correctness | Gas Town, Taskplane, Overstory | GitHub PR checks | 최신 base 재검증과 batch/bisect를 공급자 중립으로 구현 |
| 권한·격리 | Warren, Mux path guard | GitHub firewall, Runloop policy, Factory autonomy | firewall coverage, secret boundary, retention을 실행 전 preview |
| 비용·관측 | Agent Deck, Mux | Devin budget, Factory analytics | task critical path와 비용을 함께 최적화하는 scheduler |
| self-hosted governance | Warren | Coder Agents | agent loop·model gateway와 execution workspace의 분리, user identity/RBAC 전파 |
| fast isolated VM | E2B Infra | E2B Cloud | snapshot locality, best-of-K placement, readiness, data-plane routing을 함께 최적화 |
| local container workspace | Container Use | Docker/Dagger ecosystem | branch/worktree/container lineage와 cache는 강하지만 privileged host capability·secret reference·log redaction의 검증된 경계가 부족 |
| backend federation | OpenHands / Agent Canvas | GitHub Agent HQ, JetBrains ACP | local·remote·cloud backend의 protocol/capability/health를 하나의 registry에서 정규화 |
| fleet-wide change | Taskplane polyrepo | Sourcegraph, GitLab flows | deterministic transform과 coding-agent 판단을 혼합한 repository별 rollout·rollback |
| agent interoperability | ACP, acpx | JetBrains ACP, OpenHands ACP | wire version·capability·permission·session continuity를 공급자 중립 adapter contract로 연결 |
| legacy CLI bridge | AgentAPI | 해당 없음 | PTY heuristic의 confidence와 degradation을 숨기지 않는 fallback tier |
| persistent sandbox lifecycle | E2B, Vercel Sandbox SDK | Vercel Sandbox | sandbox identity, running session, service readiness, snapshot lineage를 별도 상태로 추적 |
| runtime-generation fencing | Cloudflare Sandbox SDK | Cloudflare Sandbox | restart 전 stream/process/preview event 차단과 live resource-aware sleep 판단 |
| issue·incident delegation | 해당 없음 | Linear coding sessions, Sentry Seer | 사람 ownership, agent delegation, production evidence, PR 산출물의 경계를 유지 |
| event-triggered Continuous AI | gh-aw | GitHub Actions | natural-language source와 compiled execution manifest, agent read stage와 scoped write stage의 provenance |
| independent AI review | 해당 없음 | Copilot Review, CodeRabbit, Qodo, Greptile | review head SHA·mode·policy/context revision·finding lifecycle을 보존하고 approval/test와 분리 |

따라서 신규 도구는 기존 제품과 똑같은 “agent tab manager”보다 다음 조합에 집중해야 한다.

- Windows/Linux native local kernel과 cloud sandbox adapter
- spec/issue/run/evidence를 잇는 durable graph
- 단계형 provisioning과 snapshot 기반 빠른 fan-out
- atomic claim, waves/lanes, resource lease, merge lane
- PR/CI/review/command 결과로 파생되는 mission-control 상태
- capability·network·secret·retention을 사전에 보여주는 실행 계약
- backend version·tool·runtime topology를 협상하는 registry와 compatibility gate
- deterministic script와 coding agent를 함께 선택하는 multi-repo router
- ACP primary adapter와 PTY fallback을 구분하는 confidence-aware adapter stack

## 7. Build / integrate / buy 판단

| 영역 | 결정 | 이유 |
|---|---|---|
| task/event/policy kernel | Build | 제품의 정확성·이식성·Windows 지원을 결정하는 핵심 차별점 |
| desktop fleet UI | Build, 기존 패턴 참고 | card 상태와 evidence projection이 신규 kernel과 밀접함 |
| agent CLI | Integrate | Codex/Claude/Gemini 등의 기존 agent를 adapter로 사용 |
| local PTY/worktree | Build 또는 검증된 library 채택 | low-latency 경로이며 Windows Job Object 제어 필요 |
| local container workspace | Build adapter, Container Use 패턴 검증 | Dagger/Docker를 선택형 executor로 연결하되 privileged nesting·host mount는 capability gate, secret subsystem은 clean-room 구현 |
| cloud compute | 먼저 Buy/Integrate | E2B 또는 Runloop로 빠르게 검증하고 사용량이 커지면 self-host 검토 |
| persistent remote workspace | Evaluate Vercel Sandbox | session 재개·snapshot/fork·preview가 강하며 E2B와 lifecycle/cost/security를 동일 conformance suite로 비교 |
| enterprise self-host | Evaluate Coder/Warren | regulated 환경에서 model key와 workspace egress를 분리하고 기존 RBAC/template을 활용 |
| forge/issue/chat | Integrate | GitHub/GitLab/Linear/Slack을 대체하지 않음 |
| multi-backend control surface | Build, OpenHands 패턴 참고 | local·remote·cloud를 같은 UX로 다루되 protocol과 capability 차이를 숨기지 않아야 함 |
| agent protocol/session backend | Integrate ACP, evaluate acpx | 표준 wire contract는 직접 발명하지 않고 session/queue 구현은 conformance와 안정성을 검토해 채택 |
| legacy CLI compatibility | Integrate or isolate AgentAPI pattern | protocol 없는 agent 지원은 유용하지만 heuristic 상태를 core truth로 승격하지 않음 |
| fleet migration | Integrate/Evaluate Sourcegraph·GitLab | 수백 repo scope/search/rollout은 별도 전문 서비스가 강하며 로컬 kernel의 핵심 범위를 넘음 |
| scheduled/event repository automation | Integrate gh-aw | GitHub Actions를 쓰는 팀에 compiler-generated guarded workflow를 제공하되 deterministic CI와 별도 lane으로 운영 |
| merge policy | Build | fresh-base verification과 조직별 gate는 control plane 책임 |

라이선스 기본 방침은 MIT/Apache-2.0 구현을 우선 비교하고, AGPL-3.0인 Mux·Claude Squad는 clean-room 아키텍처 참고로만 사용하는 것이다. NTM은 rider 때문에 어떤 분석·재사용 대상에도 포함하지 않는다.

## 8. 권장 검증 순서

1. Emdash식 staged provisioning으로 local Windows `worktree_ready` p95를 측정한다.
2. Beads식 atomic claim과 Taskplane식 wave/lane으로 20-task synthetic DAG를 실행한다.
3. 동일 task를 local ConPTY와 E2B executor에서 실행해 Task/Run/Evidence가 동일하게 보이는지 확인한다.
4. E2B snapshot 또는 Runloop blueprint로 4-way fan-out cold/warm 시작 시간과 비용을 측정한다.
5. GitHub PR/CI/review 사실을 주입해 Agent Orchestrator식 card projection의 오탐을 시험한다.
6. shared workspace의 implement-review-test와 isolated workspace의 독립 feature 3개를 비교한다.
7. firewall 예외, unrestricted egress, secret handle, retention 만료를 threat model과 UI preview로 검증한다.
8. fresh-base merge, batch failure bisect, crash/restart, duplicate event, Windows orphan process를 failure injection으로 시험한다.
9. 서로 다른 Agent Server version과 `usable_tools`를 광고하는 fake backend를 등록해 compatibility fail-closed와 UI capability 숨김을 시험한다.
10. 동일한 10-repository migration을 deterministic script 우선 경로와 agent-only 경로로 실행해 비용, 성공률, CI repair 횟수를 비교한다.
11. ACP stable v1 fixture로 version mismatch, omitted capability, permission deny, session cancel, terminal truncation, reconnect/load를 conformance test한다.
12. 같은 agent를 ACP와 AgentAPI PTY bridge로 실행해 time-to-first-progress, message fidelity, false idle, cancel 성공률을 비교하고 PTY 결과를 low-confidence로 표시한다.
13. E2B와 Vercel Sandbox에서 동일 image/base SHA를 실행해 create·resume·fork p50/p95, service restore, snapshot secret scan, network-policy deny/allow 증거를 비교한다.
14. Linear issue delegation과 Sentry incident fix를 mock connector로 재생해 human ownership, external run id, draft PR, verifier와 production-resolution evidence가 섞이지 않는지 확인한다.
15. 동일 Markdown workflow를 두 번 compile해 lock hash가 deterministic한지 확인하고, write permission·untrusted expression·unpinned action mutation이 compile-time에 거부되는지 시험한다. agent artifact를 변조해 threat/safe-output gate가 실제 write를 차단하는지도 별도 fixture로 검증한다.
16. 같은 seeded-defect PR을 Copilot Review, CodeRabbit, Qodo, Greptile 중 2개 이상에 보내 detection precision/recall, 중복·모순 finding, head 변경 후 stale 처리, re-review latency를 비교한다. 결과는 advisory evidence로만 저장하고 deterministic test/human gate를 유지한다.
17. Container Use형 fixture에서 20개 branch/worktree/container를 병렬 생성해 cache hit와 state collision을 측정한다. privileged nesting·host socket은 무승인 차단하고 fake secret의 원문과 reference fingerprint가 config·Git notes·명령 로그·snapshot 어디에도 남지 않는지 검사한다.
18. 첫 remote A/B가 통과하면 Cloudflare adapter fixture에서 runtime을 교체해 이전 stream·process·preview event가 fencing되는지, active stream/background service 중 sleep하지 않는지, restart 뒤 preview 재활성화가 필요한지 검증한다.

### 8.1 5개 독립 pilot의 go/no-go gate

| Pilot | 2주 범위 | Go 기준 | No-go/보류 기준 |
|---|---|---|---|
| Local orchestration | Windows 11에서 Codex/Claude, 20-task DAG, 4 concurrent worktree | warm start p95 ≤ 3초, duplicate claim 0, false-complete < 2%, orphan 회수 ≥ 80% | ConPTY/process-tree cleanup 불안정, coordinator overhead가 makespan 절감보다 큼 |
| Remote executor | 동일 task/image를 E2B와 Vercel에서 create/resume/fork | contract 결과 동일, secret inheritance 0, deny/allow evidence 완전, provider별 비용·p95 측정 가능 | capability silent downgrade, retention/egress 증거 불충분, local 대비 이점 없음 |
| Event automation | gh-aw로 issue triage·docs proposal 각 1개, safe-output mock write | source→manifest deterministic, agent write credential 0, tampered proposal 100% 차단 | deterministic CI와 상태 혼동, safe-output provenance 또는 idempotency 부족 |
| Reviewer | seeded defect 30개를 두 service와 static/test baseline으로 비교 | head freshness 100%, precision/recall·noise·cost 측정, finding→fix loop 추적 | stale verdict가 merge gate 통과, provenance 없는 rule/context, human review 시간 절감 없음 |
| Local container | 20개 environment, setup/install cache, failure resume, secret leakage fixture | state collision 0, cache invalidation 정확, 무승인 privileged 실행 0, secret/reference fingerprint 0 | container를 VM으로 과장, Git state overwrite, config/log/snapshot leakage, Windows host runtime 불안정 |

각 pilot은 별도 feature flag, credential audience, retention policy와 예산을 가진다. 하나가 실패해도 local kernel·다른 provider·deterministic CI가 계속 동작해야 한다.

## 9. 조사에서 제외하거나 보류한 후보

- [1Code](https://github.com/21st-dev/1code): GitHub에서 archived 상태라 핵심 기준점에서 제외했다.
- Superset: source-available 라이선스와 기존 desktop orchestrator 중복 때문에 서비스 비교군으로만 보류했다.
- Daytona: GitHub API에서 라이선스가 명확히 식별되지 않아 clone하지 않았다.
- NTM: 위 rider 때문에 격리·제외했다.

## 10. 관련 문서

- [저장소 코드·GitHub 분석](./REPOSITORY_GITHUB_ANALYSIS.md)
- [빠른 멀티 에이전트 실행·오케스트레이션 기획](./FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md)
- [AI 에이전트 기반 개발 환경 요구사항](./AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md)
- [클론 카탈로그](../multi-agent-tools/README.md)
