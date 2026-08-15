---
id: tool-entire-cli
type: tool-profile
title: Entire CLI
status: observed
profile_schema_version: 3
tool_key: entire-cli
tool_version_id: tool-version:entire-cli@7ddf2fc26c1ba521309ca2b5cf356d1e54228afb
tags: [knowledge-base, tool, execution-provenance, checkpoint, git, transcript]
official_upstream: https://github.com/entireio/cli
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 7ddf2fc26c1ba521309ca2b5cf356d1e54228afb
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P1
  linux: P1
version_kind: commit
version_ref: 7ddf2fc26c1ba521309ca2b5cf356d1e54228afb
parent_repo_head: 91d6d075d53185667e20996cc94ec7e10537d02c
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# Entire CLI

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

coding-agent hook에서 session·prompt·transcript·file change를 수집해 code commit과 연결된 Git-backed checkpoint로 보존하고 explain·resume·attribution에 사용하는 개발 실행 provenance CLI다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/entireio/cli |
| 기본 브랜치와 조사일 HEAD | `main` / `7ddf2fc26c1ba521309ca2b5cf356d1e54228afb` (2026-08-15) |
| 고정 버전 | `7ddf2fc26c1ba521309ca2b5cf356d1e54228afb` |
| pin과 최신 관찰 관계 | 조사 시점 default-branch HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; official upstream fixed-SHA tree·blob을 원격 정적 검사하고 이 manifest-only 프로필에 locator를 보존 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: Entire 공식 조직 저장소와 `git ls-remote --symref`의 `main` HEAD를 대조하고 fixed-SHA docs/source를 직접 읽음 |
| 플랫폼 증거 | Windows `P1/partial`, Linux `P1/partial` — fixed source tree에 OS별 hook/process 경로가 있지만 어느 native OS에서도 build/runtime하지 않음 |
| license | [fixed-SHA MIT LICENSE](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/LICENSE#L1-L20); bundled/plugin/dependency license 전수 검토는 미수행 |
| provenance limitation | clone·install 없이 official fixed-SHA README, architecture/security docs와 선택 source path를 정적으로 읽음. agent hook, Git checkpoint, remote sync, redaction, resume, Windows/Linux native runtime은 미실행 |
| source 관리 | `manifest-only`: 현재는 evidence-layer 비교·설계 대상. checkpoint/evidence prototype에서 구현을 직접 차용하거나 conformance fixture를 유지할 때 gitlink 전환 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Agent/Git hooks | supported coding agent lifecycle과 Git commit/push event를 수집 | agent session → local session state/shadow checkpoint → commit condensation/pre-push sync | [README hook flow lines 137–181](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L137-L181), [managed Git hooks](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/cmd/entire/cli/strategy/hooks.go#L18-L41) |
| Session/checkpoint model | active session, ephemeral full snapshot과 persistent metadata record를 분리 | `.git/entire-sessions` + shadow branch → persistent git branch/ref | [model lines 145–172](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L145-L172) |
| Persistent checkpoint store | transcript·prompt·metadata·content hash를 checkpoint ID 아래 보존 | commit trailer/ID → Git tree → `entire/checkpoints/v1` 또는 per-checkpoint ref | [checkpoint layout lines 274–324](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L274-L324) |
| Git refs backend | checkpoint마다 독립 ref/history와 queued fast-forward sync 제공 | local write → `refs/entire/checkpoints/<shard>/<id>` → push/fetch/recovery | [backend overview lines 7–20](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L7-L20), [write/push lines 66–112](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L66-L112) |
| Redaction/privacy path | stored transcript·metadata를 sanitize/redact하고 선택적 OPF로 pre-push 재작성 | raw agent transcript → sanitize → built-in redaction → optional OPF → Git objects/remote | [sanitization lines 193–225](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L193-L225), [privacy lines 17–28](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/security-and-privacy.md#L17-L28) |
| Attribution/signing projections | hook timing과 diff로 agent/human line 비율을 추정하고 checkpoint commit 서명을 시도 | session/checkpoint snapshots → informational trailer; configured signer → signed or unsigned checkpoint | [attribution lines 53–70](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/attribution.md#L53-L70), [signing lines 1–40](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/checkpoint-signing.md#L1-L40) |

## 역할과 연동

- AgentRole: Execution Recorder, Developer Workflow Adapter, Evidence/Audit Projection; independent verifier나 merge authorizer 자체는 아님.
- Capability: `agent-session-capture`, `git-backed-checkpoint-provenance`, `commit-session-linkage`, `checkpoint-resume`, `transcript-redaction`, `informational-line-attribution`.
- Integration: native CLI, Git hooks/branches/refs/object store, agent-specific hooks for Codex·Claude Code·Gemini CLI·Cursor 등, optional Git remote/checkpoint repository와 summary/privacy provider.
- SecurityOperationalRequirement: transcript·prompt·tool-output data classification, repository/ref ACL, retention/legal hold/deletion, redaction failure policy, checkpoint integrity, verifier separation과 external push approval가 필요하다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | Entire native CLI, Git repository와 installed/authenticated supported agent. remote checkpoint sync·login·AI summary·OPF는 각각 network, token/keyring, provider 또는 external executable이 추가로 필요 | [README prerequisites and enable flow](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L41-L43), [hook setup lines 137–181](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L137-L181), [token handling lines 230–262](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L230-L262) |
| Supported protocols / surfaces | CLI, agent hooks, Git hooks, Git object/branch/ref storage, Git push/fetch; optional checkpoint remote | [hook locations](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L446-L461), [checkpoint remote lines 463–505](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L463-L505), [ref backend](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L7-L20) |
| Rate limits | local checkpoint path에 고정 request rate limit 없음; Git hosting, login/control plane, model summary와 OPF provider/service 한도는 unknown | fixed source에서 공통 서비스 rate-limit 계약을 확인하지 못함; 2026-08-15 |
| Timeout / retry | optional OPF `timeout_seconds` 기본 30초; checkpoint-ref batch push 실패 시 per-ref recovery, conflict면 queued 상태 유지. agent hook·Git command의 공통 timeout은 unknown | [OPF config lines 108–159](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/security-and-privacy.md#L108-L159), [push recovery lines 98–119](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L98-L119) |
| Fallback candidates | none/unknown | 기존 AX KB에는 같은 session→commit Git checkpoint implementation 대체재를 평가하지 않음. 자체 evidence store로 전환하면 resume/transcript/Git linkage를 잃을 수 있으므로 별도 architecture decision과 migration·retention 승인이 필요 |

fallback은 호환성·권한·안전성 보장이 아니라 검토 후보다. 전환으로 external write, credential audience, 데이터 경계, 비용 또는 검증 등급이 바뀌면 자동 선택하지 않고 새 capability/policy 협상과 필요한 승인을 거친다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `entire-c1-session-checkpoint-model` | architecture | active session, ephemeral full-state checkpoint와 persistent metadata checkpoint를 서로 다른 Git-local state로 관리한다. | [official README](https://github.com/entireio/cli#sessions), 2026-08-15 | [model lines 145–191](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L145-L191) | `I2` | `V2` | `windows:P1; linux:P1` | 구조 정적 확인; concurrent session·crash/reconcile runtime 미검증 |
| `entire-c2-git-backed-provenance` | capability | persistent checkpoint는 transcript·prompt·metadata·content hash를 code commit과 연결하고 Git branch 또는 checkpoint별 ref에 보존한다. | [official README](https://github.com/entireio/cli#checkpoints), 2026-08-15 | [layout lines 274–324](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L274-L324), [ref model lines 7–20](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L7-L20) | `I2` | `V2` | `windows:P1; linux:P1` | implementation/document contract 확인; integrity, remote durability, exact attribution proof는 미검증 |
| `entire-c3-ref-sync-recovery` | interface | refs backend는 checkpoint별 history를 fast-forward-only로 push하고 divergence 때 remote를 보존한 replay를 시도하며 conflict는 queue에 남긴다. | 없음 | [write/push lines 66–112](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L66-L112) | `I2` | `V2` | `windows:P1; linux:P1` | fail-safe intent 정적 확인; network loss·multi-writer failure injection 미실행 |
| `entire-c4-transcript-privacy-boundary` | security | transcript·metadata는 redaction되지만 repository 접근자는 full interaction을 읽을 수 있고 shadow code snapshot은 raw blob이므로 수동 push하면 secret이 노출될 수 있다. | [official README security section](https://github.com/entireio/cli#security--privacy), 2026-08-15 | [security lines 1–28](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/security-and-privacy.md#L1-L28) | `I2` | `V2` | `windows:P1; linux:P1` | confirmed trust boundary; secret/PII detector recall과 deletion cascade 미검증 |
| `entire-c5-optional-opf-fail-closed` | security | OPF를 enable한 push에서는 missing binary·timeout·failure가 push를 중단하지만 env override로 한 번 건너뛸 수 있고 local Git에는 더 약하게 redacted object가 일정 기간 남는다. | 없음 | [OPF behavior lines 132–175](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/security-and-privacy.md#L132-L175), [persistence lines 200–210](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/security-and-privacy.md#L200-L210) | `I2` | `V2` | `windows:P1; linux:P1` | scoped fail-closed path와 bypass/retention limitation 확인; OPF 실행·정확도 미검증 |
| `entire-c6-attribution-informational` | limitation | agent/human attribution은 hook timing과 line diff의 휴리스틱 추정이며 정확한 authorship 또는 security evidence가 아니다. | 없음 | [attribution lines 53–70](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/attribution.md#L53-L70), [trade-offs lines 198–206](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/attribution.md#L198-L206) | `I2` | `V2` | `windows:P1; linux:P1` | confirmed limitation; independent verifier/identity proof로 사용 금지 |
| `entire-c7-signing-best-effort` | limitation | checkpoint signing은 signer가 실패하면 unsigned commit을 만들고 계속 진행한다. | 없음 | [signing lines 1–40](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/checkpoint-signing.md#L1-L40) | `I2` | `V2` | `windows:P1; linux:P1` | confirmed fail-open integrity boundary; mandatory signed evidence 요구를 충족하지 않음 |
| `entire-c8-platform-static-only` | platform | repository에는 Windows와 Unix용 command/cancel 구현 경로가 분리돼 있지만 full workflow의 양쪽 native runtime 근거는 이번 조사에 없다. | 없음 | [Windows hook test](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/cmd/entire/cli/agent/hook_command_exec_windows_test.go), [Windows cancel](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/cmd/entire/cli/checkpoint/remote/command_cancel_windows.go), [Unix cancel](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/cmd/entire/cli/checkpoint/remote/command_cancel_unix.go) | `I2` | `V2` | `windows:P1; linux:P1` | narrow static path만 확인; build/runtime/agent hook/remote sync `P2` 없음 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| Agent hooks | agent-specific JSON/config/plugin hooks | agent lifecycle → session state, transcript and checkpoint events | hook installer와 local user가 agent/repository 권한을 공유; agent event는 verifier proof가 아님 | [hook configuration](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L446-L461) |
| Git hooks | shell hook delegation for prepare/commit/post-commit/post-rewrite/pre-push | working tree commit/push → checkpoint condensation/link/sync | repository hook write와 push authority에 의존; pre-push privacy path에는 explicit bypass가 존재 | [hook source lines 177–242](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/cmd/entire/cli/strategy/hooks.go#L177-L242) |
| Checkpoint tree | Git tree/commit plus JSON/JSONL/text/blob | session/checkpoint ID → persistent transcript·metadata; explain/resume readers가 조회 | repository/ref read ACL이 transcript 열람 권한; code branch ACL과 자동 분리되지 않음 | [checkpoint layout](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/sessions-and-checkpoints.md#L274-L324) |
| Checkpoint refs | Git refs and push/fetch | local checkpoint history → selected remote; on-demand fetch/read | Git credential와 remote ACL에 의존; fast-forward policy는 signature·review를 대체하지 않음 | [ref backend lines 66–119](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/docs/architecture/ref-checkpoint-backend.md#L66-L119) |
| CLI projections | CLI status/explain/resume/blame/why | operator query → checkpoint read/projection | attribution과 summary는 derived/informational; source commit·verifier receipt와 분리 | [README command surfaces lines 296–325](https://github.com/entireio/cli/blob/7ddf2fc26c1ba521309ca2b5cf356d1e54228afb/README.md#L296-L325) |

## 운영·보안·trust boundary

- 보호 자산과 authority: source/worktree snapshots, prompts, full transcripts, tool/MCP data, checkpoint metadata/refs, Git credentials, optional provider/token/keyring와 signing key다.
- code branch와 checkpoint refs를 분리해도 같은 repository ACL을 쓰면 transcript 독자가 넓어질 수 있다. public repo에서는 transcript가 공개되므로 dedicated private checkpoint remote와 회사 data classification 결정이 필요하다(`entire-c4`).
- redaction은 safety net이다. raw agent transcript, raw shadow code snapshot, unreachable Git object/reflog와 remote retention을 각각 별도 data lifecycle로 다뤄야 한다(`entire-c4`, `entire-c5`).
- fast-forward-only refs는 concurrent overwrite 위험을 줄이지만 immutable append-only audit, mandatory signature, independent verification이나 legal hold를 자동 제공하지 않는다(`entire-c3`, `entire-c7`).
- checkpoint link는 “어떤 session이 어떤 commit 주변에서 기록됐는가”의 provenance다. 실행 성공·test 통과·agent 정직성·line authorship의 proof로 승격하지 않는다(`entire-c6`).
- UI/CLI summary, attribution trailer, checkpoint 존재와 agent 자기보고는 derived projection이며 required receipt와 verifier evidence가 없으면 AX completion은 `unverified`다.

## 플랫폼

- Windows `P1/partial`: Windows hook command test와 cancel implementation path를 fixed SHA에서 확인했지만 native build, Codex/Git hook, keyring, checkpoint push를 실행하지 않았다.
- Linux `P1/partial`: Unix cancel path와 portable Go/Git workflow source를 확인했지만 Linux native build/runtime를 실행하지 않았다. 조사 host가 WSL2라는 사실은 Linux host-native `P2` 또는 Windows native evidence가 아니다.
- Windows path quoting, executable extension, Credential Manager와 process cancellation; Linux permission, signal, keyring과 filesystem semantics를 공통 conformance fixture로 분리해야 한다.
- remote Git server는 control client OS와 별도 trust domain이며, Windows/Linux client static path가 remote durability·privacy를 증명하지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `entire-v2-source-20260815` | `V2` | `7ddf2fc26c1ba521309ca2b5cf356d1e54228afb` | `git ls-remote --symref`, official fixed-SHA tree, README/docs/source 원격 정적 inspection, 최종 exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; git 2.53.0 | official pin, MIT license, checkpoint/ref/redaction/attribution/signing/platform boundary 확인 | 이 프로필의 official fixed-SHA locator | `entire-c1`~`entire-c8` | install/build/runtime/E2E 미실행; 최초 sandbox DNS attempt exit 128 뒤 승인된 read-only network로 재시도 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | upstream test/source 존재를 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: `entire-c1`~`entire-c3`가 현재 AX architecture에 계약만 있고 runtime reference가 없는 session→checkpoint→commit/ref provenance와 resume 가능한 Git-backed record 패턴을 제공한다.
- 확인된 한계: transcript가 고감도 Git data가 되고(`entire-c4`, `entire-c5`), attribution과 signing은 security/verification gate가 아니다(`entire-c6`, `entire-c7`).
- 미확인·추론: hook event loss, crash consistency, checkpoint tamper detection, cross-worktree/multi-device conflict, secret/PII detection recall, remote deletion/legal hold, Windows/Linux parity, long-term Git object cost는 unknown이다.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | session/checkpoint identity, code commit linkage, checkpoint별 Git ref/history와 queued non-force sync | `entire-c1`~`entire-c3` | Evidence layer의 실행 provenance와 `RM-P3-verifier` 입력 artifact |
| Adapt | transcript sanitize/redact pipeline과 checkpoint remote를 사내 data classification·private evidence store·retention policy에 연결 | `entire-c4`, `entire-c5` | `AX-D002`, `AX-D005`, `AX-D007`, `AX-D008` 결정 필요 |
| Avoid | attribution percentage, checkpoint 존재, best-effort signature 또는 agent transcript를 completion·authorship·verification proof로 사용 | `entire-c6`, `entire-c7` | `AD-PROP-006` independent verifier와 fail-closed evidence 원칙 유지 |
| Build | mandatory signed/hashed evidence envelope, verifier identity, base/head/environment/exit/artifact contract, tamper/retention/deletion receipt와 OS별 hook conformance | `entire-c1`~`entire-c8` | internal Evidence/verifier lane과 `RM-P3-false-complete-fixture` |

## 도입 판단

- 결정: 참고
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: Git-backed execution provenance와 developer checkpoint UX의 reference implementation 비교; 현재 hook 설치나 production transcript 저장은 결정하지 않음.
- 이유: `entire-c1`~`entire-c3`은 기존 KB의 추상 Evidence contract에 비중복 구현 재료를 제공한다. 그러나 `entire-c4`~`entire-c7` 때문에 사내 evidence store·verifier·privacy gate를 대체하지 않는다.
- 재검토 조건: 회사 transcript 분류·retention·repository ACL 결정, component license/SBOM, Windows/Linux build `V3/P2`, agent hook/runtime `V4`, event loss·concurrent refs·redaction·tamper·delete `V5`.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `entire-test-build-native` | `entire-c1`, `entire-c8` | `V3/windows:P2; linux:P2` | 결정된 Windows와 Linux native x86_64 host | fixed SHA reproducible build/unit test와 CLI help/smoke | 양쪽 OS build/test exit 0, binary digest·dependency inventory 보존 | build logs, SBOM, binary hash, environment fingerprint | dependency/network 승인 |
| `entire-test-checkpoint-lifecycle` | `entire-c1`~`entire-c3` | `V5/windows:P2; linux:P2` | isolated Git repo·bare remote와 synthetic agent fixture | concurrent sessions, commit/amend/rebase, crash, failed/non-FF push, second-device fetch/resume | stale/lost linkage 없음, force push 없음, retry/queue 상태와 recovery receipt 일치 | Git graph/refs dump, event log, checkpoint tree hash | synthetic remote와 filesystem write 승인 |
| `entire-test-privacy` | `entire-c4`, `entire-c5` | `V5/windows:P2; linux:P2` | private isolated repo와 secret/PII canary corpus | transcript/tool output/raw source secret, OPF missing/timeout/bypass, cleanup/gc/delete | policy상 forbidden remote disclosure 0, failure는 정의대로 차단, local/remote 잔존 위치와 삭제 receipt 확인 | canary report, object/reflog scan, push trace | security/privacy review, OPF dependency·비용 승인 |
| `entire-test-verifier-separation` | `entire-c6`, `entire-c7` | `V5/windows:P2; linux:P2` | worker와 independent verifier identity가 분리된 fixture | forged transcript, wrong attribution, missing signer, green agent claim/failed test | checkpoint projection만으로 completion 불가, verifier receipt와 mandatory integrity gate 없으면 `unverified` | signed evidence envelope, negative test log | AX verifier/policy contract 결정 |

## 관계

- `Tool HAS_VERSION tool-version:entire-cli@7ddf2fc26c1ba521309ca2b5cf356d1e54228afb`
- `ToolVersion FITS_ROLE ExecutionRecorder/DeveloperWorkflowAdapter/EvidenceProjection`
- `ToolVersion PROVIDES agent-session-capture/git-backed-checkpoint-provenance/checkpoint-resume/transcript-redaction`
- `ToolVersion SUPPORTS CLI/Git-hooks/Git-branches/Git-refs/agent-hooks`
- `Project EVALUATES ToolVersion` as execution provenance and checkpoint reference implementation

## 변경 이력

- 2026-08-15: official `main` HEAD를 manifest-only immutable pin으로 등록하고 fixed-SHA `I2/V2`, Windows `P1`, Linux `P1` 정적 프로필을 작성함. install/build/runtime/E2E와 외부 write는 미수행.
