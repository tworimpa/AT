# AI 에이전트 기반 개발 환경 요구사항

제품명: **AIDE Fleet** (가칭)

문서 상태: Draft v0.2

기준일: 2026-08-14

상위 기획: [빠른 멀티 에이전트 실행·오케스트레이션](./FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md)

## 1. 제품 정의

AIDE Fleet은 여러 AI 코딩 에이전트를 로컬·WSL·원격·sandbox 환경에서 실행하고, task DAG, 격리된 workspace, 구조화된 상호작용, 독립 검증, review와 merge까지 관리하는 개발 control plane이다.

### 해결할 문제

- 여러 터미널에서 어떤 agent가 무엇을 하는지 알기 어렵다.
- terminal이 살아 있음, agent가 대기 중임, task가 완료됨이 혼동된다.
- 여러 worktree가 port, DB, cache, device를 공유해 실행 충돌이 난다.
- agent가 “완료”라고 말해도 현재 head에서 테스트가 실제 통과했는지 불분명하다.
- 프로세스·앱 재시작 후 run이 orphan되거나 같은 task가 중복 실행된다.
- Windows에서 tmux/Unix-only 경로 때문에 기능이 축소된다.
- 자동화가 강해질수록 secret, 외부 쓰기, destructive action, merge 위험이 커진다.

### 비목표

- 자체 foundation model 개발.
- 모든 agent CLI의 비공개 내부 상태를 역공학해 완벽히 통제.
- GitHub/GitLab/CI를 완전히 대체.
- production 배포 성공이나 물리 장치 동작을 소프트웨어 test만으로 자동 인정.
- MVP에서 완전 자율 무인 merge를 기본 활성화.

## 2. 사용자와 주요 시나리오

| 사용자 | 필요 |
|---|---|
| 개인 개발자 | 2~4개 agent를 빠르게 실행, 상태 확인, 질문 응답, 결과 비교 |
| Tech Lead | 기능을 DAG로 분해, 모델/역할 배정, review/merge gate 관리 |
| 플랫폼 엔지니어 | executor, policy, secret, quota, remote worker 운영 |
| 보안/감사 담당 | 누가 어떤 권한으로 어떤 명령·외부 쓰기를 했는지 추적 |
| CI/자동화 | API로 run을 만들고 evidence/상태를 machine-readable하게 소비 |

필수 사용자 여정:

1. 한 줄 명령으로 단일 agent task 실행.
2. 복합 요구를 2~5개 독립 task로 분해하고 병렬 실행.
3. 실행 중 agent 질문과 권한 요청에 UI에서 응답.
4. 앱 재시작 후 live session을 재연결하거나 orphan을 정확히 표시.
5. 변경별 테스트 evidence를 확인하고 review 후 merge.
6. Windows 로컬 agent와 WSL/SSH agent를 한 화면에서 관제.

## 3. 도메인 모델

### 3.1 엔티티

| 엔티티 | 필수 필드 |
|---|---|
| Project | `id`, repo URL/path, default branch, policy profile, platform config |
| Task | `id`, objective, scope, dependencies, risk, priority, acceptance, merge policy |
| Run | `id`, `task_id`, `attempt`, adapter, model, executor, workspace, status, budget |
| AgentSession | provider session id, process/session id, capability, last progress, state |
| Workspace | base SHA, branch, path, isolation type, owner run, cleanup policy |
| ResourceLease | type, value, owner, expiry, collision domain |
| Message | typed payload, sender/recipient, task/run/attempt, reply/dedupe key, sequence |
| Interaction | question/approval type, options, deadline, decision, decision maker |
| Evidence | source run, head/base SHA, command, exit code, artifact hash, limitations |
| Review | reviewer, scope, verdict, findings, evidence references |
| MergeOperation | target ref, expected base, source SHA, gate results, result ref |
| Event | monotonic sequence, entity, event type, payload schema version, timestamp |
| Spec | versioned intent, rationale, acceptance, source path/SHA, linked issue ids |
| IssueGraph | issue dependency, repository segment, wave/lane, ready/claim state |
| ExecutorProfile | provider, capability, isolation, image/snapshot, network, secret, retention |
| Snapshot | provider reference, source workspace/SHA, input hash, TTL, provenance, secret policy |
| Backend | stable id, kind, endpoint, auth mode, connection revision, protocol/tool capability, health |
| ChangeSet | fleet id, repository, transform/agent route, base/head SHA, CI, rollout, approval state |
| AdapterContract | provider, transport, confidence, wire/package version, capability snapshot, session semantics |
| RemoteSandbox | provider sandbox id, lifecycle generation, snapshot lineage, running session, command/service readiness, network policy |
| ExternalDelegation | source system, issue/incident id, human owner, delegated agent, external run id, stopping point, artifact/PR links |
| ExecutionManifest | source/compiler/schema hash, resolved adapter/action/image digests, stage DAG, permissions, network/MCP/secret policy, budget, expiry |
| LocalContainer | workspace/branch id, runtime, image/container digest, host mounts, privileged nesting, network mode, cache inputs, state/log references |

### 3.2 상태 분리

Task 상태:

```text
draft → queued → ready → running → verifying → review → merge_ready → merged
                   ↘ blocked       ↘ changes_requested
                   ↘ cancelled     ↘ failed
```

Run 상태:

```text
accepted → provisioning → starting → active → completion_reported
                                  ↘ waiting_input
                                  ↘ waiting_dependency
                                  ↘ stalled
                                  ↘ failed / cancelled / orphaned
```

AgentSession 상태:

```text
created → process_alive → ready → working ↔ waiting → exited/lost
```

Workspace 상태:

```text
requested → inspected → base_resolved → materialized → worktree_ready
                                                → dependencies_ready → services_ready
clean → dirty → preserved / cleanup_pending → removed
```

RemoteSandbox 상태:

```text
requested → sandbox_exists → session_starting → executor_ready → services_ready
                    ↘ stopped/snapshotted → resuming ────────────┘
                    ↘ terminated
```

LocalContainer 상태:

```text
requested → worktree_ready → base_cached → source_mounted → dependencies_ready → executor_ready
                                      ↘ command_failed → debuggable_failed
                                      ↘ stopped/preserved → resumed
                                      ↘ terminated
```

상위 상태를 하위 상태에서 무조건 추론하지 않는다. 예를 들어 `AgentSession.exited`와 `Run.completion_reported`가 있어도 verifier 전에는 `Task.merged` 또는 `Task.verified`가 될 수 없다.

## 4. 기능 요구사항

우선순위는 `MUST`, `SHOULD`, `COULD`로 표시한다.

### 4.1 Project와 repository discovery

- **FR-001 MUST**: 로컬 checkout, bare repository, remote Git URL을 project로 등록해야 한다.
- **FR-002 MUST**: default branch, current SHA, dirty status, remotes, submodule/LFS 존재를 read-only로 탐지해야 한다.
- **FR-003 MUST**: `AGENTS.md`, agent별 지침, package scripts, lockfile, CI workflow에서 실행 계약 후보를 추출해야 한다.
- **FR-004 MUST**: 사용자 변경이 있는 main checkout을 자동 reset/clean/checkout하지 않아야 한다.
- **FR-005 SHOULD**: monorepo package/workspace 경계를 탐지하고 task scope에 연결해야 한다.
- **FR-006 SHOULD**: 동일 remote의 clone/worktree를 하나의 project identity로 묶어야 한다.

인수 조건:

- dirty checkout 등록 시 파일이 변경되지 않는다.
- 동일 repo의 Windows 경로 대소문자·junction 차이로 project가 중복 등록되지 않는다.
- 발견된 모든 명령은 실행 전 사용자 또는 policy가 검토할 수 있다.

### 4.2 Task contract와 DAG

- **FR-010 MUST**: task는 objective, deliverable, scope, forbidden scope, dependency, acceptance criteria를 가져야 한다.
- **FR-011 MUST**: DAG cycle을 저장 전에 거부하고 cycle 경로를 반환해야 한다.
- **FR-012 MUST**: dependency가 `verified` 이상이 아닐 때 후속 write task 시작을 차단해야 한다. 정책으로 `review` 이상을 허용할 수 있다.
- **FR-013 MUST**: batch task 생성 시 index 또는 stable id로 dependency를 원자적으로 연결해야 한다.
- **FR-014 SHOULD**: 예상 write set과 resource need를 planner가 제안하고 사람이 수정할 수 있어야 한다.
- **FR-015 SHOULD**: critical path와 blocked reason을 UI/API에 제공해야 한다.
- **FR-016 COULD**: 과거 run 데이터를 이용해 예상 시간과 최적 model을 추천할 수 있다.

### 4.3 Scheduler와 concurrency

- **FR-020 MUST**: event-driven ready queue와 가중 semaphore를 제공해야 한다.
- **FR-021 MUST**: provider/account, CPU, RAM, disk, project, executor별 동시성 제한을 지원해야 한다.
- **FR-022 MUST**: 동일 workspace에 동시에 두 write run을 배치하지 않아야 한다.
- **FR-023 MUST**: 동일 repo의 destructive Git operation과 merge operation을 직렬화해야 한다.
- **FR-024 MUST**: task cancel이 queue, process, interaction, lease, workspace cleanup에 전파돼야 한다.
- **FR-025 SHOULD**: critical path, unblock count, startup cost, conflict risk를 반영한 priority scheduling을 제공해야 한다.
- **FR-026 SHOULD**: idle worker에 ready task를 할당하는 work stealing을 지원해야 한다.
- **FR-027 SHOULD**: speculative fan-out은 명시된 최대 후보 수·비용·취소 정책 안에서만 허용해야 한다.
- **FR-028 COULD**: provider rate-limit reset 시각을 반영해 task를 다른 account/model로 route할 수 있다.

인수 조건:

- 20개 task DAG에서 dependency가 충족되지 않은 task가 한 번도 시작되지 않는다.
- 동시 cancel/retry에도 동일 task의 active run은 policy가 허용한 개수를 넘지 않는다.
- scheduler 재시작 뒤 persistent ready/running 상태를 reconcile하고 중복 dispatch하지 않는다.

### 4.4 Agent adapter

- **FR-030 MUST**: adapter contract는 `detect`, `capabilities`, `launch`, `resume`, `send`, `interrupt`, `stop`, `observe`, `collectEvidence`를 제공해야 한다.
- **FR-031 MUST**: Codex와 Claude Code adapter를 MVP에 포함해야 한다.
- **FR-032 MUST**: agent binary/version/help를 실행 전 탐지하고 호환되지 않는 flag를 전달하지 않아야 한다.
- **FR-033 MUST**: structured output/API가 있으면 stdout heuristic보다 우선해야 한다.
- **FR-034 MUST**: heuristic 상태는 `confidence`와 `degraded_reason`을 노출해야 한다.
- **FR-035 MUST**: adapter가 provider session id와 resume 가능 여부를 영속화해야 한다.
- **FR-036 SHOULD**: Gemini CLI와 OpenCode adapter를 plugin으로 추가할 수 있어야 한다.
- **FR-037 SHOULD**: account/config home을 run별로 선택할 수 있고 credential 내용을 control plane DB에 복사하지 않아야 한다.
- **FR-038 COULD**: model capability/cost/latency 기반 자동 routing을 제공할 수 있다.

### 4.5 Executor와 플랫폼

- **FR-040 MUST**: Windows native ConPTY executor와 POSIX PTY executor를 제공해야 한다.
- **FR-041 MUST**: Windows process는 Job Object 또는 동등한 ownership으로 child tree를 대상 한정 종료해야 한다.
- **FR-042 MUST**: PowerShell, cmd, POSIX shell의 argv를 문자열 재조합 없이 가능한 한 배열로 보존해야 한다.
- **FR-043 MUST**: WSL executor를 선택 사항으로 제공하고 Windows control plane이 WSL 없이도 동작해야 한다.
- **FR-044 SHOULD**: SSH executor와 reconnect/keepalive를 제공해야 한다.
- **FR-045 SHOULD**: Docker sandbox executor를 제공해야 한다.
- **FR-046 COULD**: Kubernetes executor와 pod별 resource limit를 지원할 수 있다.
- **FR-047 MUST**: executor마다 working directory, environment handle, process/session id, liveness probe를 제공해야 한다.

### 4.6 Workspace와 resource isolation

- **FR-050 MUST**: write task는 기본적으로 고정 base SHA에서 task별 branch/worktree를 만들어야 한다.
- **FR-051 MUST**: worktree 생성이 실패하면 partial directory/registration을 감지하고 recoverable 상태로 남겨야 한다.
- **FR-052 MUST**: 기존 dirty worktree를 강제 제거하지 않아야 한다.
- **FR-053 MUST**: port, DB/schema slug, device/emulator, dev-server namespace를 `ResourceLease`로 할당해야 한다.
- **FR-054 MUST**: lease는 owner, collision domain, TTL, renew/release event를 가져야 한다.
- **FR-055 MUST**: `.env`/credential 파일은 기본 복사 대상이 아니며 policy-approved secret handle만 주입해야 한다.
- **FR-056 SHOULD**: lockfile hash 기반 setup cache와 warm workspace pool을 제공해야 한다.
- **FR-057 SHOULD**: worktree setup script는 timeout, 로그, exit code, idempotency key를 가져야 한다.
- **FR-058 COULD**: overlay filesystem 또는 prepared image로 대형 monorepo 준비 시간을 줄일 수 있다.

### 4.7 메시징과 interaction

- **FR-060 MUST**: typed message와 자유 텍스트 note를 모두 지원해야 한다.
- **FR-061 MUST**: message는 stable id, sequence, sender, recipient, task/run/attempt, reply target, dedupe key를 가져야 한다.
- **FR-062 MUST**: task assignment은 `dispatch → ack`를 요구하고 ack timeout을 노출해야 한다.
- **FR-063 MUST**: 질문은 blocking/non-blocking, 선택지, 기본값, deadline을 표현해야 한다.
- **FR-064 MUST**: approval은 요청 작업, 영향 범위, target, 위험, 만료, 결정자를 기록해야 한다.
- **FR-065 MUST**: 같은 dedupe key의 재전송은 side effect를 중복 발생시키지 않아야 한다.
- **FR-066 SHOULD**: local embedded transport와 optional remote signed relay transport를 동일 message interface로 제공해야 한다.
- **FR-067 SHOULD**: agent가 idle일 때만 non-urgent message를 inject해 현재 turn을 손상시키지 않아야 한다.

### 4.8 Lifecycle, watchdog, recovery

- **FR-070 MUST**: `accepted`, `executor_started`, `agent_ready`, `task_acknowledged`, `completion_reported`, `verification_passed`, `merged`를 별도 event로 기록해야 한다.
- **FR-071 MUST**: process liveness, output activity, semantic progress, task 상태를 독립적으로 관찰해야 한다.
- **FR-072 MUST**: silence timeout은 executor/task 유형별로 설정 가능해야 한다.
- **FR-073 MUST**: control plane 시작 시 running run/session/workspace/lease를 reconcile해야 한다.
- **FR-074 MUST**: live session이면 reattach, 없으면 `orphaned`, 판단 불가면 `unknown`으로 fail-closed 처리해야 한다.
- **FR-075 MUST**: retry는 새 attempt를 만들고 이전 event/evidence를 보존해야 한다.
- **FR-076 MUST**: 동일 completion/settlement event를 두 번 처리해도 상태가 손상되지 않아야 한다.
- **FR-077 SHOULD**: safe nudge 1회 후 escalation하는 계층형 watchdog을 제공해야 한다.
- **FR-078 SHOULD**: DB backup/checkpoint와 projection rebuild를 지원해야 한다.

### 4.9 Evidence와 verification

- **FR-080 MUST**: agent의 completion report와 verifier result를 분리해야 한다.
- **FR-081 MUST**: evidence는 base/head SHA, changed path, command argv, cwd, exit code, 시작/종료, artifact hash를 포함해야 한다.
- **FR-082 MUST**: 필수 verification은 agent worktree의 현재 head에서 독립 executor가 실행해야 한다.
- **FR-083 MUST**: command가 실행되지 않았거나 timeout이면 pass로 간주하지 않아야 한다.
- **FR-084 MUST**: software test, CI, deploy, external service, operator, physical device evidence를 다른 evidence class로 구분해야 한다.
- **FR-085 MUST**: `verified` 이후 head/base가 바뀌면 evidence를 stale로 표시해야 한다.
- **FR-086 SHOULD**: JUnit, coverage, SARIF, screenshot, benchmark artifact를 정규화해야 한다.
- **FR-087 SHOULD**: verifier가 flaky test 재시도 횟수와 최초 실패를 숨기지 않아야 한다.

### 4.10 Review와 merge

- **FR-090 MUST**: review 입력은 task contract, diff, evidence, unresolved limitation을 포함해야 한다.
- **FR-091 MUST**: reviewer agent는 기본 read-only/comment-only여야 한다.
- **FR-092 MUST**: merge 직전 remote target ref를 다시 읽고 expected base를 검증해야 한다.
- **FR-093 MUST**: stale base, conflict, required check 미완료 시 merge를 차단해야 한다.
- **FR-094 MUST**: 동일 repo의 merge operation을 serialized lane에서 수행해야 한다.
- **FR-095 MUST**: branch delete/worktree cleanup은 merge/ref 확인 후 별도 단계로 수행해야 한다.
- **FR-096 MUST**: MVP 자동 merge 기본값은 off여야 한다.
- **FR-097 SHOULD**: generated file/lockfile에 한해 policy-defined resolver를 제공할 수 있다.
- **FR-098 SHOULD**: GitHub/GitLab PR 생성, comment, check 상태 읽기를 connector로 제공해야 한다.

### 4.11 Policy, security, secrets

- **FR-100 MUST**: file path, command class, network, external write, secret, merge에 대한 policy를 project/org/run 수준에서 정의해야 한다.
- **FR-101 MUST**: destructive filesystem/Git action은 exact resolved target과 authorization을 기록해야 한다.
- **FR-102 MUST**: secret 값은 event, transcript index, UI, analytics에 저장하지 않아야 한다.
- **FR-103 MUST**: secret은 opaque handle로 전달하고 executor가 실행 시점에 최소 범위로 resolve해야 한다.
- **FR-104 MUST**: log redaction은 key name뿐 아니라 known value fingerprint도 적용해야 한다.
- **FR-105 MUST**: external mutation은 idempotency key 또는 mutation receipt를 가져야 한다.
- **FR-106 MUST**: remote message/event는 sender identity와 무결성을 검증할 수 있어야 한다.
- **FR-107 SHOULD**: sandbox profile은 read-only roots, writable roots, network allowlist, CPU/RAM/time budget을 정의해야 한다.
- **FR-108 SHOULD**: dependency/license/SBOM gate를 release 전에 실행해야 한다.

### 4.12 UI, CLI, API

- **FR-110 MUST**: Graph/Board, Fleet, Evidence/Review 화면을 제공해야 한다.
- **FR-111 MUST**: 모든 상태에 텍스트 reason과 마지막 evidence timestamp를 표시해야 한다.
- **FR-112 MUST**: 질문·승인·실패·merge-ready를 통합 interrupt inbox에 표시해야 한다.
- **FR-113 MUST**: CLI는 `--json`과 안정적인 exit code를 제공해야 한다.
- **FR-114 MUST**: API event stream은 sequence cursor로 resume할 수 있어야 한다.
- **FR-115 MUST**: UI action과 CLI/API action이 같은 domain command path를 사용해야 한다.
- **FR-116 MUST**: dangerous action은 preview/target 확인을 제공해야 한다.
- **FR-117 SHOULD**: diff inline comment를 agent에게 typed review message로 되돌릴 수 있어야 한다.
- **FR-118 SHOULD**: mobile/remote view는 read/steer/approve를 지원하되 secret 표시와 destructive bulk action을 제한해야 한다.

### 4.13 Plugin과 extension

- **FR-120 MUST**: agent adapter, executor, forge connector, notifier, verifier parser를 versioned plugin interface로 확장해야 한다.
- **FR-121 MUST**: plugin manifest에 capability, permission, platform, version compatibility를 선언해야 한다.
- **FR-122 MUST**: plugin이 요청하지 않은 filesystem/network/secret capability를 받지 않아야 한다.
- **FR-123 SHOULD**: MCP server를 통해 task/query/transition을 제공할 수 있어야 한다.
- **FR-124 SHOULD**: plugin crash가 control plane을 종료시키지 않도록 process boundary를 제공해야 한다.

### 4.14 Intent graph, wave/lane, workspace grouping

- **FR-130 MUST**: versioned Spec은 WHAT/WHY, acceptance criteria, source path/SHA와 연결된 Issue id를 가져야 한다.
- **FR-131 MUST**: Issue는 HOW, dependency, repository segment, expected write set, resource need를 표현해야 하며 Run과 분리돼야 한다.
- **FR-132 MUST**: planner는 dependency graph를 wave와 lane으로 계산하고 critical path와 lane 직렬화 이유를 노출해야 한다.
- **FR-133 MUST**: ready eligibility 확인, Attempt 생성, worker/workspace lease는 하나의 transaction으로 atomic claim되어야 한다.
- **FR-134 MUST**: claim은 fencing token을 가지며 만료된 token의 progress/completion mutation을 거부해야 한다.
- **FR-135 MUST**: task는 `isolated`, `shared`, `promote` workspace group 전략을 명시해야 한다.
- **FR-136 MUST**: shared workspace의 기본 write concurrency는 1이어야 하며 복수 writer는 path lease 또는 explicit turn ownership이 있어야 한다.
- **FR-137 SHOULD**: 동일 lane의 후속 task는 provider session/context를 재사용할 수 있으나 task별 contract와 evidence는 분리해야 한다.
- **FR-138 SHOULD**: exploration 결과를 target에 적용하기 전 detached verification workspace에서 patch/commit dry-run을 지원해야 한다.
- **FR-139 MUST**: Spec/Issue 변경과 Run event 사이 provenance link를 제공하되 chat transcript를 intent source of truth로 사용하지 않아야 한다.

### 4.15 Durable workspace provisioning

- **FR-140 MUST**: workspace provisioning을 `inspected`, `base_resolved`, `materialized`, `worktree_ready`, `dependencies_ready`, `services_ready`, `published`의 durable step으로 기록해야 한다.
- **FR-141 MUST**: 각 step은 input hash, idempotency key, started/succeeded/failed, output reference, stage error를 가져야 한다.
- **FR-142 MUST**: 동일 idempotency key의 재실행은 성공한 step을 반복하지 않고 마지막 성공 지점부터 재개해야 한다.
- **FR-143 MUST**: policy가 허용하면 `worktree_ready`에서 agent를 시작하고 dependency/service/publish step을 background에서 계속할 수 있어야 한다.
- **FR-144 MUST**: background step 실패를 성공으로 숨기지 않고 실행 중 agent와 state projector에 structured degradation event로 전달해야 한다.
- **FR-145 MUST**: partial worktree, Git registration, branch/ref, process, resource lease를 step별 compensation 또는 preserve 정책으로 처리해야 한다.
- **FR-146 SHOULD**: prepared image/snapshot/cache key는 base SHA, lockfile hash, toolchain, platform, policy profile을 포함해야 한다.
- **FR-147 SHOULD**: service readiness probe와 dependency install을 분리해 code-only agent가 불필요한 setup을 기다리지 않게 해야 한다.
- **FR-148 MUST**: provisioning의 각 step latency와 critical-path 포함 여부를 metric으로 제공해야 한다.

### 4.16 Local/cloud executor와 서비스 adapter

- **FR-150 MUST**: 모든 executor는 `detectCapabilities`, `create`, `waitReady`, `exec`, `stream`, `observe`, `terminate` 계약을 구현해야 한다.
- **FR-151 SHOULD**: 지원 가능한 executor는 `pause`, `resume`, `snapshot`, `fork`를 같은 optional capability로 구현해야 한다.
- **FR-152 MUST**: capability는 OS, isolation type, filesystem persistence, network policy, secret injection, retention, resource, timeout, cost dimension을 선언해야 한다.
- **FR-153 MUST**: 요청한 isolation/network/retention capability를 지원하지 않으면 약한 모드로 fallback하지 않고 실행 전 거부해야 한다.
- **FR-154 MUST**: ConPTY/POSIX PTY/SSH는 transport와 process boundary로 분류하며 security sandbox로 표시하지 않아야 한다.
- **FR-155 MUST**: remote executor 실행 전 image/snapshot, repository/base SHA, egress, secret handles, timeout, retention, 예상 비용을 preview해야 한다.
- **FR-156 MUST**: snapshot은 source workspace/SHA, provider, image, toolchain, 생성 actor/run, TTL, secret 포함 정책, content reference를 기록해야 한다.
- **FR-157 MUST**: snapshot이나 remote workspace 만료·삭제 뒤 stale reference를 사용하면 `not_found/expired`로 fail-closed해야 한다.
- **FR-158 SHOULD**: 첫 cloud adapter로 E2B를 제공하고 local ConPTY와 동일한 executor conformance suite를 실행해야 한다.
- **FR-159 SHOULD**: Runloop와 Modal 같은 추가 provider가 core schema 변경 없이 plugin으로 추가될 수 있어야 한다.
- **FR-160 MUST**: local/cloud 어느 쪽에서 실행해도 Task/Run/Attempt/Message/Evidence의 canonical schema는 동일해야 한다.
- **FR-161 MUST**: provider-native id, logs, cost, lifecycle event는 canonical entity에 provenance를 보존한 채 연결해야 한다.
- **FR-162 MUST**: service adapter의 API outage, quota, rate limit은 task failure와 구분된 executor availability 상태여야 한다.
- **FR-163 SHOULD**: child agent/session마다 token·time·provider cost budget을 두고 wait-all을 개별 polling이 아닌 aggregate event로 제공해야 한다.
- **FR-164 SHOULD**: planning/Q&A처럼 filesystem·command가 필요 없는 turn은 workspace를 만들지 않고 처리하며 첫 tool execution 직전에 compute를 lazy provision해야 한다.
- **FR-165 SHOULD**: self-hosted profile은 model/provider credential과 agent loop를 control plane에 두고 execution workspace에는 원본 model key를 주입하지 않는 구성을 지원해야 한다.
- **FR-166 MUST**: control plane이 workspace tool을 실행할 때 initiator의 RBAC와 workspace ownership을 그대로 적용하며 공유 service identity로 권한을 확장하지 않아야 한다.
- **FR-167 MUST**: `executor_started`, authenticated tool endpoint의 `executor_ready`, user service의 `services_ready`를 별도 event와 probe로 기록해야 한다.
- **FR-168 SHOULD**: remote placement는 ready node의 resource commitment/usage와 image/snapshot cache locality를 함께 점수화해야 한다.
- **FR-169 MUST**: PTY, file transfer, preview traffic은 task/event control API와 분리된 data-plane route와 scoped access token을 사용해야 한다.

### 4.17 Derived state와 service governance

- **FR-170 MUST**: Board/Fleet card 상태는 session, process, Git SHA, PR, CI, review, interaction, verifier event의 projection이어야 한다.
- **FR-171 MUST**: 각 projection은 source별 observed_at, freshness, reason과 evidence reference를 노출해야 한다.
- **FR-172 MUST**: 필요한 source가 stale 또는 unavailable이면 상태를 추측하지 않고 `unknown` 또는 `degraded`로 표시해야 한다.
- **FR-173 MUST**: plan approval, command permission, external write approval, review approval, merge approval을 서로 다른 interaction type으로 유지해야 한다.
- **FR-174 MUST**: network firewall의 적용 범위와 알려진 예외 경로(setup step, MCP, provider infrastructure)를 executor profile과 evidence에 기록할 수 있어야 한다.
- **FR-175 SHOULD**: GitHub/issue/chat/schedule/webhook trigger는 동일한 Intake contract와 initiator identity를 사용해야 한다.
- **FR-176 SHOULD**: agent-authored commit과 PR은 initiator, session, task, evidence bundle로 역추적할 수 있어야 한다.
- **FR-177 MUST**: orchestration mode를 `single`, `subagent`, `independent_fleet`, `communicating_team`으로 구분하고 각 mode의 message topology, workspace isolation, spawn 권한, budget을 선언해야 한다.
- **FR-178 MUST**: `communicating_team`은 direct peer message와 shared task list를 허용하되 expected write set을 분리하거나 explicit shared-writer lease를 요구해야 한다.
- **FR-179 SHOULD**: task completion 전 deterministic hook이 acceptance/evidence 부족을 이유로 transition을 거부하고 structured feedback을 worker에게 반환할 수 있어야 한다.
- **FR-180 MUST**: workload identity는 authoritative project/run/workspace identity와 audience로 파생하며 raw cloud credential을 sandbox image, event 또는 snapshot에 저장하지 않아야 한다.
- **FR-181 MUST**: sandbox fork는 parent의 workload identity token과 secret lease를 기본 상속하지 않고 새 policy evaluation을 요구해야 한다.
- **FR-182 SHOULD**: resume placement는 origin node와 snapshot cache를 우선하되 capacity·health가 부족하면 다른 node로 안전하게 이동해야 한다.
- **FR-183 SHOULD**: snapshot restore는 lazy memory/page와 COW filesystem의 fetched bytes, page fault, cache hit를 startup evidence에 기록할 수 있어야 한다.
- **FR-184 MUST**: running catalog, durable snapshot metadata, analytics/event, object artifact의 store 역할과 source-of-truth 경계를 문서화하고 reconciliation해야 한다.

### 4.18 Backend registry, capability negotiation, fleet routing

- **FR-185 MUST**: local, remote, cloud backend를 stable id, kind, host, auth mode, connection revision으로 등록·수정·비활성화할 수 있어야 한다.
- **FR-186 MUST**: transport health, protocol compatibility, authentication, advertised tool capability를 서로 다른 probe 결과와 timestamp로 저장해야 한다.
- **FR-187 MUST**: backend protocol version이 minimum floor보다 낮거나 해석되지 않으면 실행을 fail-closed하고 필요한 version과 실제 값을 표시해야 한다.
- **FR-188 MUST**: task가 요구하는 tool/lifecycle capability와 backend가 광고한 capability를 배치 전에 비교하고 부족하면 해당 backend에 dispatch하지 않아야 한다.
- **FR-189 MUST**: runtime service URL, API prefix, auth handle은 backend가 **agent 관점**에서 광고해야 하며 host/browser가 `localhost`나 port를 추측하지 않아야 한다.
- **FR-190 MUST**: provider·MCP·automation secret은 opaque lookup handle과 audience로 전달하고 backend가 spawn 시점에 해석해야 한다. browser storage, prompt, event, snapshot에는 원문을 저장하지 않아야 한다.
- **FR-191 MUST**: backend/credential 변경 시 connection revision으로 cache, health, conversation query를 무효화해 이전 connection의 상태가 새 connection에 섞이지 않게 해야 한다.
- **FR-192 SHOULD**: child conversation은 parent run/conversation id, 별도 budget, workspace policy, completion evidence를 가져야 하며 parent의 secret lease를 암묵 상속하지 않아야 한다.
- **FR-193 SHOULD**: multi-repository 작업은 deterministic transform 가능성을 먼저 판정하고 script executor와 coding-agent executor를 repository별로 혼합할 수 있어야 한다.
- **FR-194 SHOULD**: fleet rollout은 pilot repository, max concurrency, rollout window, pause/rollback, CI repair hook과 changeset별 human approval을 제공해야 한다.
- **FR-195 MUST**: warm executor는 `process_alive`, `dormant`, `initializing`, `executor_ready`를 분리하고 사용자 runtime binding 전에는 task를 받지 않아야 한다.
- **FR-196 MUST**: deferred init은 workspace, session auth, secret encryption key, webhook, concurrency policy를 하나의 generation에 원자적으로 연결해야 한다.
- **FR-197 MUST**: concurrent init은 하나만 허용하고 실패한 generation의 partial credential·workspace binding을 폐기한 뒤 retryable dormant 상태로 돌아가야 한다.
- **FR-198 MUST**: liveness endpoint와 authenticated readiness endpoint를 분리하고 scheduler는 readiness만 배치 근거로 사용해야 한다.
- **FR-199 MUST**: parent/child conversation link는 동일 project와 workspace identity에서만 허용하며 child는 별도 run budget, lease, evidence를 가져야 한다.

### 4.19 Structured agent protocol과 session ownership

- **FR-200 MUST**: adapter 선택 우선순위는 typed vendor protocol, stable ACP, structured JSON CLI, PTY heuristic 순이어야 하며 선택 이유를 Run에 기록해야 한다.
- **FR-201 MUST**: adapter는 `structured`, `hybrid`, `heuristic` confidence, implementation version, negotiated wire version, capability snapshot을 선언해야 한다.
- **FR-202 MUST**: ACP connection은 session 생성 전 initialize를 수행하고 합의되지 않은 protocol major 또는 누락된 capability를 unsupported로 처리해야 한다.
- **FR-203 MUST**: package/schema artifact version을 wire compatibility 근거로 사용하지 않고 negotiated protocol version과 capability만 사용해야 한다.
- **FR-204 MUST**: filesystem, terminal, MCP, rich prompt, session load/cancel 같은 양방향 call은 peer capability와 project policy를 모두 통과해야 한다.
- **FR-205 MUST**: prompt `stopReason`, tool-call status, terminal exit, task completion report, verification result를 서로 다른 event type으로 보존해야 한다.
- **FR-206 MUST**: PTY adapter의 prompt 표시, silence, screen `stable` 신호는 `agent_waiting`의 보조 evidence로만 사용하고 completion/verification transition을 직접 만들지 않아야 한다.
- **FR-207 MUST**: persistent logical session을 adapter process와 분리하고 `(adapter identity, canonical workspace id, optional name)`으로 scope해야 한다.
- **FR-208 MUST**: live session owner는 owner-only local IPC, random generation token, heartbeat, PID/process-tree probe, idle TTL을 가져야 한다.
- **FR-209 MUST**: 동일 session의 prompt는 단일 owner FIFO를 통해 직렬화하고 queue depth, enqueue receipt, start/completion sequence를 기록해야 한다.
- **FR-210 MUST**: cancel은 protocol-level cooperative cancel을 먼저 시도하고 deadline 뒤에만 해당 session의 scoped process tree를 종료해야 한다.
- **FR-211 MUST**: owner crash 뒤 provider session resume/load를 시도하고, 새 session fallback 시 새 attempt와 `context_continuity_lost` evidence를 남겨야 한다.
- **FR-212 MUST**: Governed mode는 resume/load 실패 뒤 새 session으로 자동 fallback하지 않고 사람 또는 policy gate 승인을 요구해야 한다.
- **FR-213 SHOULD**: raw structured stream을 sequence와 schema version 그대로 export하고 text rendering과 automation JSON output contract를 분리해야 한다.
- **FR-214 SHOULD**: 같은 prompt를 여러 adapter/model에 one-shot으로 실행해 latency, cost, permission denial, stop reason, verification 결과를 비교할 수 있어야 한다.

### 4.20 Persistent remote sandbox lifecycle

- **FR-215 MUST**: persistent sandbox identity, 현재 running session, authenticated command readiness, user service readiness를 별도 entity/state로 저장해야 한다.
- **FR-216 MUST**: `stop`, `pause`, `resume`, `get/reconnect`, `snapshot`, `fork`, `terminate`를 capability별로 구분하고 provider가 지원하지 않는 transition은 명시적 `unsupported`로 반환해야 한다.
- **FR-217 MUST**: resume은 새 lifecycle generation을 만들고 restore/`onResume` hook의 명령, exit code, service probe를 evidence로 남겨야 하며 hook 실패를 sandbox 소실이나 task 완료로 오인하지 않아야 한다.
- **FR-218 MUST**: snapshot/fork lineage를 source sandbox, source SHA, image, filesystem/environment hash와 연결하고 child에 parent의 workload identity, secret lease, temporary network exception을 암묵적으로 상속하지 않아야 한다.
- **FR-219 MUST**: network policy는 domain, subnet, port, protocol의 destination rule과 L7 HTTP request matcher, header transform, forward proxy를 구분해 capability와 effective policy로 표현해야 한다.
- **FR-220 MUST**: provider 기본 egress보다 project policy가 우선하며 unrestricted 또는 L7 credential injection은 별도 approval, audience, 만료와 audit event를 가져야 한다.
- **FR-221 MUST**: SDK/client handle을 durable workflow에 직렬화할 때 credential 값을 포함하지 않고 resume 시 OIDC/workload identity 또는 credential gateway를 통해 short-lived client를 재수화해야 한다.
- **FR-222 SHOULD**: E2B와 Vercel Sandbox adapter는 동일 base SHA/image task에서 create, ready, stop/resume, fork, cancel, retention, network deny/allow evidence를 같은 conformance schema로 출력해야 한다.

### 4.21 Issue·incident 기반 외부 위임

- **FR-223 MUST**: Linear/GitHub/GitLab issue의 사람 assignee와 delegated agent를 분리하고 agent delegation만으로 issue ownership이나 completion을 변경하지 않아야 한다.
- **FR-224 MUST**: external coding session/incident fix의 source id, initiator, external run id, repository/base SHA, requested stopping point, draft PR/change artifact를 `ExternalDelegation`과 local Run에 연결해야 한다.
- **FR-225 MUST**: Sentry형 incident flow는 `analysis`, `root_cause_proposed`, `change_proposed`, `change_applied`, `pr_opened`, `production_resolution_verified`를 분리하고 PR 생성만으로 incident 해결을 인정하지 않아야 한다.
- **FR-226 SHOULD**: workspace/team/project guidance의 precedence와 적용된 revision을 외부 session 시작 시 snapshot하고 Run evidence에 보존해야 한다.
- **FR-227 SHOULD**: 외부 서비스의 async run을 poll/webhook으로 수집할 때 delivery receipt, cursor/dedupe key, retry 횟수를 기록하고 동일 event를 idempotent하게 처리해야 한다.

### 4.22 Compiled agent automation과 privilege separation

- **FR-228 MUST**: natural-language/Markdown/spec automation source는 실행 전에 schema, trigger, expression, dependency pin, permission, network, MCP, secret audience를 검증한 immutable `ExecutionManifest`로 compile돼야 한다.
- **FR-229 MUST**: manifest는 source/base SHA, compiler/schema version, resolved action/container/adapter digest, stage DAG, effective permission/network policy, budget, expiration과 content hash를 포함해야 한다.
- **FR-230 MUST**: agent stage는 기본 read-only external credential과 scoped artifact output만 가지고 Git push, issue/PR mutation, deployment API를 직접 호출하지 않아야 한다.
- **FR-231 MUST**: 외부 write proposal은 typed artifact로 buffer하고 deterministic schema·수량·크기·allowed-path·secret-redaction·integrity 검사를 통과한 뒤에만 별도 committer stage로 전달해야 한다.
- **FR-232 MUST**: scoped committer는 operation별 최소 권한과 short-lived credential만 받고 manifest에 없는 mutation을 거부하며 external object id/ref/SHA와 receipt를 반환해야 한다.
- **FR-233 MUST**: optional AI threat detector는 agent와 committer 사이의 별도 unprivileged stage에서 실행하고 verdict, model/prompt version, limitations를 보존하되 deterministic policy를 대체하지 않아야 한다.
- **FR-234 SHOULD**: GitHub Actions/gh-aw connector는 source workflow SHA와 compiled lock SHA, trigger event, run id, agent artifact, threat verdict, safe-output result를 local Run/Evidence에 연결해야 한다.
- **FR-235 SHOULD**: deterministic build/test/release workflow와 agentic workflow를 별도 lane과 status로 표시하고 agentic 결과를 deterministic CI 성공으로 승격하지 않아야 한다.

### 4.23 AI reviewer service adapter

- **FR-236 MUST**: 외부 AI review는 provider, reviewed base/head SHA, full/incremental mode, capability/fallback mode, instruction·rule·code-graph revision과 provider review id를 기록해야 한다.
- **FR-237 MUST**: finding은 stable fingerprint, path/line, category, severity, confidence, evidence, suggestion, provider comment id와 lifecycle state를 가져야 한다.
- **FR-238 MUST**: review 뒤 head SHA 또는 영향 path가 바뀌면 해당 verdict/finding을 stale로 만들고 merge policy가 요구하면 새 head에서 re-review해야 한다.
- **FR-239 MUST**: AI review comment·label·suggested fix를 verifier result, deterministic check, human `APPROVED`/`CHANGES_REQUESTED`와 서로 다른 evidence type으로 저장해야 한다.
- **FR-240 MUST**: provider가 comment-only review만 지원하거나 runner 부재로 limited mode에 fallback하면 capability를 보존하고 required approval/check를 충족한 것으로 계산하지 않아야 한다.
- **FR-241 SHOULD**: 여러 reviewer의 중복 finding을 cluster하되 provider별 원본을 보존하고 모순을 표시하며 LLM 다수결로 finding을 자동 폐기하지 않아야 한다.
- **FR-242 SHOULD**: finding→fix Run→new commit→re-review 관계를 연결하고 dismissed/false-positive/accepted feedback에서 provider·category별 precision, noise, time-to-fix를 계산해야 한다.

### 4.24 Manifest safe update와 privilege drift

- **FR-243 MUST**: manifest update baseline은 trusted base ref/Git object 또는 signed registry의 committed manifest여야 하며 수정 가능한 working-copy manifest를 approval 근거로 사용하지 않아야 한다.
- **FR-244 MUST**: compiler는 이전·새 manifest의 repository write, external operation, secret audience, network/MCP reachability, sandbox host access, OIDC scope, dependency pin을 비교한 typed privilege diff를 생성해야 한다.
- **FR-245 MUST**: privilege 확대는 일반 compile 성공과 분리된 policy/human approval, approver identity, rationale, expiry를 요구하고 승인 전 dispatch되지 않아야 한다.
- **FR-246 SHOULD**: privilege 축소와 dependency digest-only refresh는 정책에 따라 자동 허용할 수 있지만 이전/새 hash와 결정 근거를 audit event로 남겨야 한다.

### 4.25 Local container executor와 secret boundary

- **FR-247 MUST**: local-container executor는 base SHA, branch, worktree path, runtime, image/container digest, lifecycle generation과 output commit을 하나의 `LocalContainer` lineage로 연결해야 한다.
- **FR-248 MUST**: executor profile은 runtime 종류, host bind/socket/device mount, root/uid, privileged nesting, network mode와 filesystem export 범위를 실행 전에 광고하고 project policy가 허용하지 않는 capability를 fail-closed해야 한다.
- **FR-249 SHOULD**: setup command는 source mount 전 cacheable stage, install command는 source mount 후 source-dependent stage로 분리하고 각 input digest, cache hit, command, exit code를 Evidence에 남겨야 한다.
- **FR-250 MUST**: non-zero command 뒤 container/workspace를 보존할 수 있지만 Run은 `debuggable_failed`로 표시하고 별도 verification 없이 `ready`, `completed`, `verified`로 승격하지 않아야 한다.
- **FR-251 MUST**: secret 원문과 vault/env/file reference를 repository config, Git commit/note, task/event store, command argument, stdout/stderr, snapshot 또는 serialized executor handle에 저장하지 않아야 한다.
- **FR-252 MUST**: credential gateway는 opaque handle을 실행 시점에 resolve해 audience·TTL·run identity가 제한된 lease로 주입하고 UI/API에는 secret name, audience, expiry와 redaction 상태만 노출해야 한다.
- **FR-253 MUST**: command log와 state propagation은 secret redaction을 적용하고 같은 commit에 대한 concurrent environment가 서로의 state note를 덮어쓰지 않도록 environment-specific commit 또는 equivalent namespaced key를 사용해야 한다.
- **FR-254 SHOULD**: container filesystem 변경을 worktree로 export할 때 absolute path와 `..` escape를 거부하고 allowed path 및 expected base를 검증한 뒤 commit hook 정책을 명시적으로 기록해야 한다.
- **FR-255 MUST**: remote executor의 sandbox/control identity, runtime generation, execution session, process/stream, service preview activation을 별도 식별자로 관리하고 모든 async event에 generation을 포함해야 한다.
- **FR-256 MUST**: runtime restart/replacement 뒤 이전 generation의 completion, stream chunk, process status와 preview activation을 거부하고 새 generation의 readiness·service activation을 다시 확인해야 한다.
- **FR-257 SHOULD**: executor idle/sleep eligibility는 active request뿐 아니라 live RPC/stream handle, background process, exposed service, pending interaction, resource lease를 포함해 계산해야 한다.
- **FR-258 SHOULD**: preview URL은 token authorization과 runtime-scoped activation을 분리하고 custom domain/DNS, token TTL, restart 재활성화, stale URL 거부 상태를 capability와 Evidence로 노출해야 한다.
- **FR-259 MUST**: session이 cwd/env만 분리하고 filesystem·process·network를 공유하는 provider에서는 서로 다른 tenant 또는 trust domain을 같은 sandbox에 배치하지 않아야 한다.
- **FR-260 MUST**: egress capability는 HTTP/HTTPS interception, non-HTTP port, DNS, direct IP, redirect와 proxy 경로별 enforcement coverage를 광고하고 partial coverage를 `deny_all`로 표현하지 않아야 한다.
- **FR-261 SHOULD**: untrusted sandbox의 외부 API access는 real credential 대신 audience·operation·TTL이 제한된 request token을 사용하고 trusted proxy가 검증·upstream credential injection·receipt를 담당해야 한다.
- **FR-262 MUST**: public service exposure는 auth mode, hostname stability, restart behavior, TTL/revocation을 기록하고 unauthenticated quick tunnel은 민감 workload와 Governed mode에서 기본 거부해야 한다.
- **FR-263 MUST**: executor는 persistence를 `ephemeral_reset`, `automatic_snapshot`, `explicit_backup_restore`, `persistent_volume`으로 선언하고 stable sandbox/control id만으로 filesystem·process·session continuity를 추론하지 않아야 한다.

## 5. 비기능 요구사항

### 5.1 성능

- **NFR-001**: local task create/ack p95 ≤ 250ms.
- **NFR-002**: warm Quick agent launch p95 ≤ 2초. 외부 agent 자체 초기화는 별도 측정한다.
- **NFR-003**: setup 제외 warm worktree materialization p95 ≤ 3초.
- **NFR-004**: event 발생부터 UI 반영 p95 ≤ 500ms.
- **NFR-005**: 8 agent 동시 실행 시 control plane 평균 CPU ≤ 5%, idle ≤ 1%.
- **NFR-006**: 100k event project의 board initial projection p95 ≤ 2초.

### 5.2 신뢰성

- **NFR-010**: 영속화가 확인되지 않은 mutation은 success receipt를 반환하지 않는다.
- **NFR-011**: event append와 projection checkpoint 사이 crash 후 재생 가능해야 한다.
- **NFR-012**: 동일 command/event 재처리는 idempotent해야 한다.
- **NFR-013**: control plane crash 후 10초 안에 reconciliation을 시작하고 결과를 표시해야 한다.
- **NFR-014**: verifier/merge evidence는 content hash로 tamper detection이 가능해야 한다.
- **NFR-015**: false-complete 비율 ≤ 0.5%를 GA gate로 둔다.

### 5.3 보안·개인정보

- **NFR-020**: 기본은 local-only bind이며 remote access는 명시적으로 활성화해야 한다.
- **NFR-021**: 모든 remote API는 인증·권한·TLS를 요구해야 한다.
- **NFR-022**: credential 값은 telemetry에 포함하지 않는다.
- **NFR-023**: audit event는 actor, action, target, decision, result, correlation id를 포함한다.
- **NFR-024**: telemetry는 opt-in이며 전송 전 payload preview와 redaction test를 제공한다.
- **NFR-025**: sandbox escape와 plugin privilege escalation을 release threat model에 포함한다.

### 5.4 호환성·이식성

- **NFR-030**: Windows 11 x64를 first-class CI/E2E 대상으로 지원해야 한다.
- **NFR-031**: Linux x64와 macOS arm64를 지원해야 한다.
- **NFR-032**: Windows long path, CRLF, Unicode path, space path, junction를 회귀 시험해야 한다.
- **NFR-033**: Git 2.36+를 기준으로 하되 capability detection으로 구버전 오류를 명확히 표시해야 한다.
- **NFR-034**: adapter compatibility를 agent CLI version matrix로 게시해야 한다.

### 5.5 유지보수성

- **NFR-040**: domain state machine과 executor/adapter를 package boundary로 분리해야 한다.
- **NFR-041**: event와 plugin protocol은 schema version과 migration 정책을 가져야 한다.
- **NFR-042**: lifecycle transition마다 unit/property test가 있어야 한다.
- **NFR-043**: crash, duplicate event, stale base, merge race, orphan process에 대한 integration test가 있어야 한다.
- **NFR-044**: 핵심 CLI/API contract는 golden/compatibility test를 가져야 한다.

### 5.6 Provisioning, cloud portability, governance

- **NFR-050**: local/cloud executor conformance suite는 lifecycle, cancel, timeout, log streaming, evidence, stale reference 동작을 동일하게 검증해야 한다.
- **NFR-051**: cached local `worktree_ready` p95는 3초 이하, remote warm snapshot `ready` p95는 provider별 SLO와 함께 측정해야 한다.
- **NFR-052**: `worktree_ready` 조기 반환이 background setup failure를 누락시키는 비율은 0이어야 한다.
- **NFR-053**: 20-task 경쟁 claim 시험에서 하나의 task/attempt에 유효한 fencing token은 정확히 하나여야 한다.
- **NFR-054**: event replay로 재생한 card projection은 같은 source snapshot에서 deterministic해야 한다.
- **NFR-055**: provider 교체 시 task/spec/evidence schema migration 없이 executor profile만 바꿀 수 있어야 한다.
- **NFR-056**: provider outage 중 local executor와 이미 실행 중인 다른 provider run은 계속 관찰·제어할 수 있어야 한다.
- **NFR-057**: 모든 remote artifact와 log는 project retention policy에 따라 만료·export·삭제 상태가 관찰 가능해야 한다.
- **NFR-058**: cost metric은 provider invoice 추정과 실제 청구의 오차를 측정하고 model/token/compute/storage/network 차원을 구분해야 한다.
- **NFR-060**: remote executor의 기본 egress는 deny 또는 project 최소 allowlist여야 하며 unrestricted는 명시 승인과 만료를 가져야 한다.
- **NFR-061**: snapshot 생성 전에 secret material과 credential cache를 탐지·제외하는 검증을 수행해야 한다.
- **NFR-062**: setup/MCP처럼 firewall 적용 밖일 수 있는 경로는 UI/API에서 숨기지 않아야 한다.
- **NFR-063**: cloud provider credential은 agent process에 원본으로 노출하지 않고 control plane 또는 credential gateway 경계에서 사용해야 한다.
- **NFR-064**: remote provider가 제공하는 isolation은 공급자의 공개 보안 문서와 검증된 설정 이상의 보장을 주장하지 않아야 한다.
- **NFR-065**: AGPL 또는 source-available 코드는 dependency/license gate 승인 없이는 product binary에 포함하지 않아야 한다.
- **NFR-066**: license rider로 분석이 제한된 repository는 index, benchmark, prompt context, generated design corpus에서 제외해야 한다.
- **NFR-067**: backend compatibility와 capability 결과는 동일 server-info fixture에서 deterministic해야 하며 protocol floor 회귀 시험을 가져야 한다.
- **NFR-068**: backend health polling은 반복 실패 후 circuit break하고 설정 변경 또는 명시적 retry 뒤에만 재개해 unavailable service를 과도하게 호출하지 않아야 한다.
- **NFR-069**: agent-view runtime topology는 local host, Docker, remote VM, cloud proxy fixture에서 연결 가능한 주소만 노출하는 contract test를 가져야 한다.
- **NFR-070**: mock full-stack E2E와 live provider E2E를 분리하고 live E2E는 opt-in이어야 하며 transcript, screenshot, video, artifact에 secret 원문이 0건이어야 한다.
- **NFR-071**: provider SDK/API upgrade 전에는 pinned protocol fixture와 최소·최대 지원 version matrix를 통과해야 한다.
- **NFR-072**: deterministic script와 coding-agent router는 task별 선택 이유, 예상 비용, 실제 비용, fallback 원인을 audit event로 남겨야 한다.
- **NFR-073**: 100개의 concurrent warm-pool init 요청에서 backend generation당 성공한 init은 최대 하나이며 실패 generation의 credential fingerprint가 후속 sandbox에서 0건이어야 한다.
- **NFR-074**: dormant warm executor는 liveness는 통과할 수 있으나 scheduler-ready probe는 항상 실패해야 하고 이 구분을 regression test로 고정해야 한다.
- **NFR-075**: ACP stable protocol fixture는 version mismatch, omitted capability, auth, permission deny, cancel, terminal truncation, reconnect/load를 OS별 conformance suite로 검증해야 한다.
- **NFR-076**: queue-owner generation이 교체된 뒤 stale owner의 prompt/complete mutation 수락 건수는 0이어야 한다.
- **NFR-077**: local IPC endpoint와 ownership metadata는 현재 사용자만 접근 가능해야 하며 Windows named pipe와 Unix socket 모두 권한 시험을 가져야 한다.
- **NFR-078**: raw structured JSON mode의 stdout에는 protocol message 외 텍스트가 0건이어야 하며 diagnostics는 별도 channel로 보내야 한다.
- **NFR-079**: PTY fallback은 지원 agent/version별 golden terminal fixture와 false-idle metric을 가져야 하고 fixture 없는 version은 `unverified`로 표시해야 한다.
- **NFR-080**: protocol draft capability는 project opt-in, exact schema pin, fallback plan 없이는 활성화하지 않아야 한다.
- **NFR-081**: 동일 remote sandbox의 stop/resume 100회 failure-injection 시험에서 lifecycle generation이 단조 증가하고 stale session event 수락 건수는 0이어야 한다.
- **NFR-082**: resume 완료 후 command readiness와 선언된 service readiness는 각각 provider별 SLO 안에 도달하거나 정확한 failed/degraded reason을 반환해야 한다.
- **NFR-083**: snapshot/fork 결과에서 parent credential fingerprint, session token, temporary egress exception의 무단 상속 건수는 0이어야 한다.
- **NFR-084**: network-policy conformance는 DNS/domain, IPv4/IPv6 subnet, port, redirect, HTTPS/L7 matcher, proxy 경로별 allow/deny와 enforcement coverage를 검증해야 한다.
- **NFR-085**: durable workflow와 SDK handle 직렬화 결과에 provider access token·refresh token·OIDC assertion 원문이 0건이어야 한다.
- **NFR-086**: external connector replay에서 동일 webhook/poll event를 10회 중복 전달해도 Run, ChangeSet, PR link는 하나만 생성돼야 한다.
- **NFR-087**: external service 기능·quota·가격·retention 정보는 확인일과 source URL을 포함하고 release/purchase decision 전 freshness gate를 통과해야 한다.
- **NFR-088**: 고정된 source, compiler, schema, registry snapshot을 100회 compile한 manifest hash는 100% 동일해야 한다.
- **NFR-089**: write permission, untrusted expression in shell, unpinned action/image, wildcard network/MCP rule mutation fixture는 strict compile에서 모두 fail-closed해야 한다.
- **NFR-090**: agent stage runtime과 artifact에서 committer credential 또는 repository write token의 검색 결과는 0건이어야 한다.
- **NFR-091**: proposal artifact 변조, secret 삽입, 허용 path 밖 patch, 최대 수량 초과는 committer 호출 전에 100% 차단되고 reason/evidence를 남겨야 한다.
- **NFR-092**: external committer는 동일 idempotency key 재처리 시 중복 issue/comment/PR/push를 만들지 않아야 한다.
- **NFR-093**: head SHA가 바뀐 뒤 이전 review verdict가 merge gate를 충족하는 건수는 0이어야 한다.
- **NFR-094**: seeded-defect benchmark는 reviewer별 category precision/recall, duplicate/noise, latency, cost, limited-mode 비율을 동일 schema로 산출해야 한다.
- **NFR-095**: instruction/rule/code-graph revision이 확인되지 않은 external review는 `provenance_incomplete`로 표시하고 required reviewer로 사용할 수 없어야 한다.
- **NFR-096**: review service outage나 timeout은 deterministic tests, human review, 이미 실행 중인 다른 reviewer를 중단시키지 않아야 한다.
- **NFR-097**: working-copy lock/manifest를 변조해도 trusted base 대비 privilege expansion 탐지율은 100%이고 무승인 dispatch는 0건이어야 한다.
- **NFR-098**: privilege diff는 동일 이전/새 manifest pair에서 deterministic하고 field omission을 privilege 축소로 잘못 해석하지 않아야 한다.
- **NFR-099**: secret 원문과 configured reference fingerprint를 repository JSON, Git objects/notes, event/log/UI/telemetry, snapshot, command history에서 검색한 결과는 0건이어야 한다.
- **NFR-100**: local-container conformance suite는 unprivileged, privileged-nesting, host-socket mount profile을 구분하고 정책 위반 profile의 dispatch 성공 건수는 0이어야 한다.
- **NFR-101**: 같은 base/cache input에서 20개 environment를 병렬 생성해도 branch/worktree/state key 충돌과 cross-environment state overwrite는 0건이어야 한다.
- **NFR-102**: setup cache hit가 source-dependent install을 잘못 생략하는 건수는 0이어야 하며 lockfile/source input 변경 시 해당 stage cache가 정확히 invalidate돼야 한다.
- **NFR-103**: 실패 command 뒤 보존된 container를 100회 resume해도 lifecycle generation은 단조 증가하고 stale session mutation 수락은 0건이어야 한다.
- **NFR-104**: filesystem export traversal, absolute path, symlink/junction escape fixture는 worktree 밖 파일 변경 전에 100% 거부돼야 한다.
- **NFR-105**: remote runtime을 100회 교체하는 failure-injection에서 이전 generation의 event·stream·preview request 수락 건수는 0이어야 한다.
- **NFR-106**: active stream 또는 background process가 있는 동안 sleep/scale-to-zero가 발생하는 건수는 0이어야 하며 종료 뒤 provider SLO 안에 idle 전환돼야 한다.
- **NFR-107**: preview token이 durable state에 남아 있어도 runtime activation이 없거나 generation이 다르면 접근 성공 건수는 0이어야 한다.
- **NFR-108**: 같은 sandbox의 session 간 filesystem/process/network 공유 fixture를 isolation으로 오분류하는 scheduler 배치 건수는 0이어야 한다.
- **NFR-109**: egress conformance는 HTTP, HTTPS, DNS, direct IP와 임의 non-HTTP port별 deny/allow를 측정하고 coverage 밖 traffic을 허용하면서 `deny_all`을 보고하는 건수는 0이어야 한다.
- **NFR-110**: credential-proxy 시험에서 sandbox filesystem/env/process/log의 real credential fingerprint는 0건이고 expired/wrong-audience request token의 upstream 성공은 0건이어야 한다.
- **NFR-111**: idle sleep 뒤 clean runtime을 반환하는 provider에서 pre-sleep filesystem/process/session이 보존됐다고 보고하는 건수는 0이어야 하며 explicit backup restore 없이는 continuity-required task를 자동 resume하지 않아야 한다.

## 6. CLI/API 최소 표면

```powershell
# Project와 task
aide project add E:\src\app --json
aide task create --file task.yaml --json
aide task plan <task-id> --json

# 실행과 관찰
aide run start <task-id> --mode parallel --json
aide run watch <run-id> --cursor <seq> --json
aide run send <run-id> --message-file answer.json --json
aide run cancel <run-id> --json

# 증거와 병합
aide evidence show <task-id> --json
aide verify <task-id> --json
aide review request <task-id> --agent codex --json
aide merge enqueue <task-id> --json

# 복구와 진단
aide doctor --platform --agents --git --executors --json
aide reconcile --dry-run --json
aide workspace list --orphaned --json
aide executor list --capabilities --json
aide executor check e2b --conformance --json
aide snapshot create <workspace-id> --policy secret-free --json
aide snapshot fork <snapshot-id> --count 4 --json
```

필수 API resource:

- `/projects`, `/tasks`, `/runs`, `/sessions`, `/workspaces`
- `/messages`, `/interactions`, `/evidence`, `/reviews`, `/merges`
- `/events?after=<seq>`, `/healthz`, `/readyz`, `/version`, `/metrics`
- `/specs`, `/issue-graphs`, `/executor-profiles`, `/snapshots`

mutation 응답은 최소한 `accepted`, `operation_id`, `dedupe_key`, `persisted_at`을 반환한다. 비동기 완료는 event stream으로 전달한다.

## 7. 관측성 요구사항

필수 metric:

- task/run 수와 상태별 gauge
- queue latency, provisioning latency, time-to-first-progress
- agent active/waiting/stalled 시간
- provider/model별 token, cost, retry, rate-limit
- worktree/setup/cache hit, resource lease 충돌
- verification pass/fail/flaky
- review changes-requested 비율
- merge queue wait, conflict, stale-base rerun
- orphan/recovery 결과
- human interrupt 수와 응답 시간

모든 log는 `request_id`, `operation_id`, `task_id`, `run_id`, `attempt_id` 중 관련 id를 포함해야 한다. transcript 원문과 운영 log는 보존 정책을 분리한다.

## 8. MVP 인수 시나리오

### AC-01 빠른 단일 실행

Windows에서 clean repo의 task를 생성하면 250ms 내 accepted receipt가 반환되고, Codex가 ConPTY에서 시작되며 `executor_started`, `agent_ready`, `task_acknowledged`가 순서대로 기록된다.

### AC-02 3-way 병렬 작업

서로 다른 path를 쓰는 task 3개를 만들면 별도 worktree/branch와 port lease를 얻어 동시에 실행된다. 한 task가 실패해도 다른 두 task의 process/worktree가 중단되지 않는다.

### AC-03 dependency gate

T3가 T1/T2에 의존할 때 T1/T2가 required evidence를 통과하기 전에는 T3 process가 생성되지 않는다. UI는 blocking task를 표시한다.

### AC-04 질문과 승인

agent 질문과 destructive command approval이 interrupt inbox에 나타난다. deny 시 command가 실행되지 않고 decision event가 기록된다. 같은 approval event 재전송은 두 번 실행되지 않는다.

### AC-05 crash recovery

3개 run 중 control plane을 강제 종료했다가 재시작하면 살아 있는 session은 reattach되고, 사라진 session은 orphaned가 되며, 동일 task가 자동으로 중복 실행되지 않는다.

### AC-06 false completion 방지

agent가 완료를 보고했지만 필수 test가 실패하면 task는 `verified`가 되지 않고 `changes_requested` 또는 `failed_verification`으로 이동한다.

### AC-07 stale base merge 차단

verification 후 target branch가 변경되면 기존 evidence가 stale로 표시되고 fresh-base integration test 전에는 merge가 실행되지 않는다.

### AC-08 Windows cleanup 안전

dirty worktree와 child process가 있는 run을 cancel하면 target process tree만 종료한다. dirty worktree는 보존되고 사용자에게 경로와 복구 상태를 표시하며 다른 repo/worktree/process는 건드리지 않는다.

### AC-09 secret redaction

secret handle로 주입된 값을 agent가 stdout/stderr에 출력해도 event/log/UI/telemetry에는 redacted form만 남는다. 원 값 검색 검사에서 0건이어야 한다.

### AC-10 external evidence 경계

CI가 green이어도 실제 deploy 확인이 없으면 task는 software verification만 통과한 것으로 표시되고 deployment/production acceptance는 pending으로 남는다.

### AC-11 atomic claim과 fencing

동시에 20개 worker가 같은 ready task를 claim하면 하나만 성공하고 나머지는 새 ready set을 받는다. 첫 lease가 만료된 뒤 새 fencing token이 발급되면 이전 worker의 늦은 completion mutation은 거부되고 audit event가 남는다.

### AC-12 staged provisioning 복구

dependency install 중 control plane을 종료한 뒤 재시작하면 이미 성공한 inspect/base/worktree step은 반복하지 않는다. 동일 workspace에서 setup을 재개하며 실패 stage와 partial artifact 처리 결과가 UI와 API에 보인다.

### AC-13 shared와 isolated workspace

독립 feature 3개는 별도 worktree/branch/PR lane에서 실행되고, 동일 feature의 implement-review-test 세션은 하나의 explicit shared workspace를 사용한다. shared workspace의 두 번째 writer는 lease 없이 시작할 수 없다.

### AC-14 local/cloud executor 동등성

같은 fixture task를 Windows ConPTY와 E2B에서 실행하면 canonical Task/Run/Attempt/Evidence JSON schema가 동일하다. VM isolation 또는 egress deny를 지원하지 않는 fake provider는 실행 전에 거부되며 silent fallback하지 않는다.

### AC-15 snapshot fan-out과 provenance

secret-free prepared snapshot 하나에서 네 sandbox를 fork해 병렬 실행한다. 각 run은 snapshot id, source base SHA, TTL, policy hash를 기록하며 만료 snapshot 재사용은 `expired`로 실패한다.

### AC-16 derived card state

terminal이 종료됐지만 PR check가 실행 중이면 card는 `done`이 아니라 `verifying`으로 표시된다. CI source가 stale이면 `unknown/degraded` reason을 표시하고 `merge_ready`를 추측하지 않는다.

### AC-17 firewall coverage preview

remote run 승인 전 egress allowlist와 setup/MCP 예외 경로를 보여준다. unrestricted egress를 선택하면 별도 승인과 만료가 필요하며 해당 결정이 audit event와 evidence bundle에 포함된다.

### AC-18 remote readiness와 data plane

VM process가 시작됐지만 authenticated command endpoint 초기화가 실패하면 `executor_started`만 기록되고 `executor_ready`가 되지 않는다. 정상 run의 PTY·file·preview 대용량 traffic은 event API를 통과하지 않으며 각각 scoped, expiring access token을 사용한다.

### AC-19 fork identity 비상속

workload identity와 secret lease가 있는 parent snapshot을 fork해도 child에는 해당 token/lease가 나타나지 않는다. child가 같은 audience가 필요하면 새 run identity와 policy로 별도 발급하고 parent credential fingerprint 검색 결과는 0건이어야 한다.

### AC-20 backend compatibility fail-closed

정상, minimum 미만, malformed version, tool 부족, stale API key인 fake backend 5개를 등록한다. 정상 backend만 runnable이고 나머지는 transport·compatibility·capability·auth 중 정확한 실패 축과 remediation을 표시한다.

### AC-21 agent-view service topology

host, Docker, remote VM fixture가 서로 다른 ingress와 automation URL을 광고한다. 새 conversation의 runtime context에는 각 agent가 실제 접근 가능한 URL과 opaque auth handle만 포함되고 browser URL, 잘못된 localhost, secret 원문은 없어야 한다.

### AC-22 deterministic/agent 혼합 fleet

10개 fixture repository의 동일 migration에서 7개는 deterministic script, 변형이 있는 3개는 coding agent로 라우팅한다. pilot 2개 검증 전에는 나머지 changeset을 게시하지 않고, CI failure 시 해당 repository만 repair하며 전체 비용과 선택 근거가 추적 가능해야 한다.

### AC-23 warm executor initialization

dormant Agent Server는 `/alive`가 성공해도 task를 받지 않는다. 동일 generation에 두 init 요청을 동시에 보내면 하나만 workspace·auth를 결합하고, 실패를 주입하면 partial binding 없이 dormant로 돌아간다. 성공한 새 generation의 authenticated command probe 뒤에만 `executor_ready`가 발행된다.

### AC-24 ACP capability conformance

ACP v1 fake agent가 terminal capability를 누락하면 terminal call을 보내지 않는다. incompatible major는 session 생성 전에 거부하고, permission deny와 cooperative cancel은 각각 별도 interaction/stop event로 보존한다. tool completed나 end_turn만으로 task가 verified가 되지 않는다.

### AC-25 queue owner fencing과 resume

같은 named session에 20개 prompt를 동시에 보내면 하나의 queue owner가 FIFO로 처리한다. owner를 중간에 종료하고 새 generation으로 resume한 뒤 이전 owner가 보내는 늦은 completion은 거부한다. provider load 실패 시 Parallel mode는 새 attempt와 continuity-loss를 표시하고 Governed mode는 승인 전 중단한다.

### AC-26 PTY fallback confidence

동일 agent를 ACP와 PTY bridge로 실행한다. ACP는 `structured`, PTY는 `heuristic`으로 표시되고, PTY 화면이 stable해져도 completion이나 verification 상태가 변하지 않는다. TUI fixture가 바뀌어 false idle이 발생하면 adapter는 degraded/unverified가 된다.

### AC-27 persistent sandbox resume와 fork

Vercel/E2B fake adapter에서 persistent sandbox를 stop한 뒤 resume한다. sandbox id는 유지되지만 lifecycle generation과 running session은 바뀌며, command probe와 `onResume` service probe가 각각 성공하기 전에는 `executor_ready`와 `services_ready`가 올라가지 않는다. snapshot을 4개 child로 fork했을 때 base SHA와 filesystem lineage는 같지만 identity·secret·temporary network lease는 모두 새 값이며 parent credential 검색 결과는 0건이어야 한다.

### AC-28 external delegation evidence boundary

사람 assignee가 있는 Linear issue를 coding agent에 위임하고 Sentry incident에서 analysis→draft PR 흐름을 재생한다. issue owner는 유지되고 external run id·guidance revision·base SHA·PR이 local Run에 연결된다. agent 종료와 draft PR 생성 뒤에도 verifier가 통과하지 않으면 task는 verified가 아니며, 배포 후 observability evidence가 없으면 incident는 `production_resolution_verified`가 되지 않는다.

### AC-29 compiled safe-output pipeline

같은 Markdown automation과 pinned registry를 두 번 compile하면 동일 manifest hash가 나온다. agent job은 read token만 가지고 PR proposal artifact를 만들며 직접 push/API write는 거부된다. artifact에 secret과 allowed path 밖 patch를 주입하면 deterministic gate가 committer 전에 차단한다. 정상 artifact는 threat/verifier gate 뒤 operation-specific credential을 받은 committer가 정확히 한 번 PR을 만들고 source SHA, manifest hash, proposal hash, external PR id를 하나의 evidence chain으로 반환한다.

### AC-30 reviewer freshness와 evidence class

seeded bug가 있는 PR을 두 reviewer adapter에 보내 finding을 수집한다. 첫 review 뒤 새 commit을 push하면 이전 verdict와 영향 finding은 즉시 stale가 되고 re-review 전 merge gate에 쓰이지 않는다. 한 provider가 comment-only/limited mode여도 human approval로 계산되지 않는다. 같은 bug의 중복 finding은 하나의 cluster로 보이지만 provider별 원본·confidence·rule revision은 유지되고, 수정 Run과 새 test/re-review evidence가 연결된 뒤에만 `fixed`가 된다.

### AC-31 manifest privilege drift

trusted base manifest는 read-only Git object에서 읽는다. working tree의 이전 lock을 낮은 권한으로 위조한 뒤 새 manifest에 repository write, wildcard egress, 새 secret audience, unpinned action을 추가해 compile한다. 네 항목 모두 privilege expansion으로 검출되고 approval 전 run은 시작되지 않는다. 승인에는 actor·rationale·expiry가 남으며, 같은 diff를 다시 계산하면 동일 hash가 나온다.

### AC-32 local container isolation과 secret leakage

같은 base SHA에서 20개 branch/worktree/container environment를 병렬 생성하고 setup cache를 공유한다. 각 environment의 state와 output commit은 다른 환경을 덮어쓰지 않으며 source/lockfile 변경은 install cache만 정확히 invalidate한다. privileged nesting과 host socket profile은 승인 없이는 시작되지 않는다. fake credential을 opaque handle로 주입해 command가 출력하도록 시도한 뒤 repository config·Git objects/notes·event/log/UI·snapshot을 검색하면 원문과 reference fingerprint가 0건이다. 실패 command의 container는 `debuggable_failed`로 resume할 수 있지만 verifier 전에는 완료 상태가 되지 않는다.

### AC-33 remote runtime generation과 sleep fencing

Cloudflare형 fake adapter에서 stream과 background service가 실행 중일 때 idle timeout을 넘겨도 runtime은 sleep하지 않는다. runtime을 강제 교체한 뒤 이전 generation의 늦은 completion·stream chunk·preview request는 모두 거부된다. durable preview token이 남아 있어도 새 runtime에서 service readiness와 activation을 다시 수행하기 전에는 preview가 열리지 않으며, 새 generation의 session/process/service id가 Evidence에 연결된다.

### AC-34 session trust, egress와 public exposure

같은 sandbox의 두 session에서 filesystem·process·localhost가 실제 공유됨을 fixture로 확인하고 서로 다른 tenant 배치를 거부한다. HTTP/HTTPS allowlist와 non-HTTP/DNS/direct-IP 경로를 각각 시험해 coverage가 정확히 표시된다. trusted proxy는 short-lived request token만 sandbox에 주고 real credential을 upstream 직전에 주입한다. unauthenticated quick tunnel은 Governed mode에서 거부되며 authenticated preview는 TTL 만료와 runtime restart 뒤 재활성화 전 접근이 모두 실패한다.

### AC-35 persistence semantics

동일 sandbox ID를 유지하는 Cloudflare형 `ephemeral_reset` adapter와 stop 시 snapshot되는 Vercel형 adapter를 같은 fixture로 실행한다. idle sleep 뒤 전자는 filesystem·process·session continuity가 `lost`이고 explicit backup restore 전 자동 resume되지 않으며, 후자는 새 runtime generation에서 snapshot lineage와 restore hook을 확인한 뒤 재개된다. 두 결과 모두 같은 canonical schema를 쓰되 persistence capability와 evidence가 정확히 다르다.

## 9. 출시 우선순위

### MVP MUST

- Local SQLite event kernel
- Windows/POSIX executor
- Codex/Claude adapter
- task DAG와 dependency gate
- task별 worktree + port/DB lease
- structured interaction
- evidence/verifier
- crash reconciliation
- CLI/API와 최소 board/fleet/evidence UI
- human-gated merge queue
- durable provisioning saga와 atomic claim
- isolated/shared workspace group과 derived state projection

### Beta SHOULD

- WSL/SSH/Docker executor
- GitHub/GitLab connector
- reviewer agent
- setup cache/warm workspace
- optional signed relay
- cost/rate-limit routing
- E2B remote executor와 local/cloud conformance suite
- Vercel Sandbox persistent executor와 stop/resume/fork/network-policy conformance
- Cloudflare Sandbox adapter와 runtime-generation/stream-aware sleep/preview activation conformance (첫 remote A/B go 이후)
- snapshot/fork warm pool, egress·retention preview
- Git-versioned spec/issue graph와 polyrepo wave/lane
- backend registry, protocol/tool capability negotiation, agent-view runtime topology
- deterministic script/coding-agent 혼합 fleet router
- ACP primary adapter, stateful queue owner와 confidence-aware PTY fallback
- Linear/Sentry 등 외부 issue·incident delegation connector와 evidence boundary
- compiled automation manifest와 read-only agent→safe-output committer 권한 분리
- multi-provider AI reviewer, finding freshness와 provenance-aware advisory evidence
- local-container executor, cache-stage conformance, privileged capability policy와 secret leakage gate

### 이후 COULD

- Kubernetes executor
- mobile steering
- speculative multi-model competition
- 학습 기반 duration/model prediction
- 조직 정책·SSO·다중 tenant

## 10. 추적성

| 요구 영역 | 참고한 구현 |
|---|---|
| 구조화된 orchestration/DAG/worker completion | Orca |
| signed event/audit/동일 identity model | Buzz |
| 작은 SQLite task/message kernel | squad |
| terminal grid, activity, port/DB lease | MulmoTerminal |
| 단순 tmux/worktree 세션 모델 | Claude Squad |
| fleet 상태, fork, recovery, 비용 | Agent Deck |
| phase별 agent routing, dependency gate, MCP | agtx |
| approval/question, pinned base, orphan recovery | Agetor |
| typed mail, watchdog, merge queue | Overstory |
| sandbox, API, resource isolation, operational evidence | Warren |
| staged workspace provisioning, local/SSH runtime | Emdash |
| wave/lane, polyrepo segment, reviewer/merger | Taskplane |
| native ConPTY와 derived card projection | Agent Orchestrator |
| spec/issue/execution provenance | sudocode |
| atomic ready/claim, Dolt task graph | Beads |
| watchdog, handoff, batch/bisect merge | Gas Town |
| patch dry-run, cost/token UX | Mux (clean-room reference) |
| cloud sandbox pause/resume/snapshot/fork | E2B |
| VM readiness, data plane, placement, workload identity | E2B Infra |
| backend registry, protocol/tool negotiation, runtime topology | OpenHands / Agent Canvas |
| dormant warm pool, liveness/readiness, conversation worktree | OpenHands Software Agent SDK |
| issue/MR/CI flow와 runner environment | GitLab Duo Agent Platform |
| multi-repo deterministic/agent routing과 rollout | Sourcegraph Agentic Batch Changes |
| wire version/capability/permission/session protocol | Agent Client Protocol |
| persistent ACP session, queue owner, raw structured output | acpx |
| protocol-less CLI HTTP/SSE bridge와 PTY heuristic | AgentAPI |
| persistent sandbox/session, resume hook, L3-L7 network policy | Vercel Sandbox |
| human-owned issue의 coding-session 위임 | Linear coding sessions |
| observability 기반 analysis→change→PR 단계 | Sentry Seer |
| Markdown→Actions compiler, read-only agent와 safe-output write stage | GitHub Agentic Workflows |
| branch/worktree+container lineage, cache stage, Git notes state와 실패 보존 | Container Use (secret subsystem 제외) |
| Durable Object control plane, runtime-generation fencing, stream-aware sleep, tokenized preview | Cloudflare Sandbox SDK |
| PR lifecycle reviewer와 comment-only approval boundary | GitHub Copilot code review |
| incremental multi-model/static review와 feedback learning | CodeRabbit |
| multi-agent review와 hierarchical compliance rule | Qodo Code Review |
| repository graph 기반 cross-file review와 fix handoff | Greptile |

구현 시에는 [라이선스 판단](./REPOSITORY_GITHUB_ANALYSIS.md#7-재사용라이선스-판단)에 따라 clean-room 재구현을 기본으로 하고, 직접 재사용하는 dependency/file은 SBOM과 notice에 기록한다.

## 11. 미결정 사항

1. Desktop shell과 kernel 언어 조합.
2. event log 단일 writer 모델과 remote federation 방식.
3. agent protocol이 없는 CLI의 heuristic 지원 수준과 SLA.
4. warm worktree pool의 disk 상한과 eviction 정책.
5. reviewer/merger agent가 사용할 별도 model/account 정책.
6. automatic merge를 허용할 risk score와 repository opt-in 형식.
7. 조직용 multi-tenant가 단일 local DB 이후의 별도 제품인지 같은 kernel 확장인지.

이 미결정 사항은 Phase 0 benchmark와 threat model 결과를 근거로 Architecture Decision Record로 확정한다.
