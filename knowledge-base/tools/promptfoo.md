---
id: tool-promptfoo
type: tool-profile
title: Promptfoo
status: observed
profile_schema_version: 3
tool_key: promptfoo
tool_version_id: tool-version:promptfoo@ab84555c1b0ff74eca6b03abb7936ac9a0149242
tags:
  - knowledge-base
  - tool
  - evaluation
  - red-team
  - evidence
official_upstream: https://github.com/promptfoo/promptfoo
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: ab84555c1b0ff74eca6b03abb7936ac9a0149242
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P0
version_kind: commit
version_ref: ab84555c1b0ff74eca6b03abb7936ac9a0149242
parent_repo_head: 91d6d075d53185667e20996cc94ec7e10537d02c
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# Promptfoo

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

prompt·model·agent·RAG를 동일한 test/assertion 계약으로 비교하고, 공격 probe와 실행 trace를 결합해 품질 회귀와 보안 failure fixture를 만드는 평가·red-team runner다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/promptfoo/promptfoo |
| 기본 브랜치와 조사일 HEAD | `main` / `ab84555c1b0ff74eca6b03abb7936ac9a0149242` (2026-08-15) |
| 고정 버전 | `ab84555c1b0ff74eca6b03abb7936ac9a0149242` |
| pin과 최신 관찰 관계 | 조사 시점 default-branch HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; official GitHub metadata와 fixed-SHA file/tree API를 읽고 permalink를 보존 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: official `promptfoo/promptfoo` upstream의 default branch, full HEAD SHA, fixed tree와 license를 교차 확인 |
| 플랫폼 증거 | Windows `P0/unknown`, Linux `P0/unknown`: Node runtime 요구와 사용 예는 확인했지만 어느 OS에서도 native build/runtime를 실행하지 않았고 OS별 지원 계약을 검증하지 않음 |
| license | [fixed-SHA LICENSE](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/LICENSE#L1-L18): MIT; bundled dataset, provider SDK, optional component의 license inventory는 미검토 |
| provenance limitation | official fixed-SHA README, package manifest, evaluation/red-team/CI/telemetry 문서를 정적으로 읽음; clone, dependency install, build, eval, provider 호출, cloud service, Windows/Linux native 실행은 미수행 |
| source 관리 | `manifest-only`: 평가·설계 비교 대상이고 GitHub 보고 저장소 크기가 약 718397 KB로 크다. core adapter 채택 전에는 fixed-SHA source locator가 재현성과 clone cost에 더 적합 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Evaluation configuration | prompt, provider/target, test variable, assertion과 default test를 선언 | YAML/config → prompt×provider×test matrix → assertion score/pass/error | [configuration guide](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/configuration/guide.md#L20-L76) |
| Red-team generation | vulnerability plugin과 delivery strategy를 조합해 attack probe 생성 | purpose/policy + plugin + strategy → probe corpus | [red-team architecture](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L9-L17), [components](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L119-L134) |
| Target/provider interface | HTTP, model, browser, JavaScript/Python custom provider 등 대상 호출을 공통화 | probe/test → target call → response/error/metadata | [target interface](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L136-L146) |
| Evaluation/reporting | deterministic·model-graded assertion과 vulnerability detector로 결과 평가 | response + optional trace → result envelope, score, finding, report | [evaluation engine](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L148-L174) |
| Trace evidence | OpenTelemetry span을 trajectory로 정규화해 tool·guardrail·error 행동을 보강 | target spans → sanitized trajectory → grader/attack/investigation context | [trace-based testing](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/llm-agents.md#L297-L319) |

## 역할과 연동

- AgentRole: Evaluation Runner, Red-team Generator, Evidence Producer, CI Gate Advisor; production verifier나 deployment committer 자체는 아님.
- Capability: `declarative-agent-evaluation`, `adversarial-probe-generation`, `provider-comparison`, `trace-backed-grading`, `skill-version-evaluation`, `ci-quality-gate`.
- Integration: CLI, Node library/contracts, YAML/JSON/CSV test corpus, HTTP/model/browser/custom providers, OpenTelemetry trace, JSON/CSV/XML/HTML output, CI/CD.
- SecurityOperationalRequirement: `AX-D002` prompt/output/trace data classification, `AX-D004` target/provider/cloud egress, `AX-D005` credential audience, `AX-D006` model/provider 허용, `AX-D008` result/cache/trace retention, `AX-D010` 비용·quota가 결정되기 전 production 평가 runner 적합성은 unknown.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | npm/npx 경로는 Node.js `>=22.22.0`; provider에 따라 API key, network, browser, Docker 또는 custom JS/Python runtime 필요 | [README requirements](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/README.md#L25-L42), [package engines](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/package.json#L48-L50); dependency/runtime 조합 미실행 |
| Supported protocols / surfaces | CLI·Node library, YAML config, HTTP/model/browser/custom provider, OpenTelemetry, CI result formats | [package exports](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/package.json#L8-L25), [target interface](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L136-L146), [CI output](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/integrations/ci-cd.md#L83-L118) |
| Rate limits | core 고정값 `unknown`; 실제 limit은 선택 provider, target, cloud attack generation과 CI 환경에 의존 | [CI troubleshooting](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/integrations/ci-cd.md#L502-L510); 조사일 서비스별 quota 미조회, 자동 fallback 금지 |
| Timeout / retry | provider·strategy·CLI별 구성 가능성은 있으나 공통 fail-closed timeout/retry 계약은 이번 정적 조사에서 `unknown` | iterative attack은 최대 attempt까지 반복될 수 있음: [data flow](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L183-L203); 값·idempotency 미검증 |
| Fallback candidates | `skillspector`(skill artifact 정적 보안), custom deterministic test harness | SkillSpector로 전환하면 general eval·provider matrix·runtime trace/red-team capability가 손실된다. custom harness는 유지보수·evidence schema 비용이 생기므로 자동 전환하지 않음 |

fallback은 호환성·권한·안전성 보장이 아니라 검토 후보다. 전환으로 external write, credential audience, 데이터 경계, 비용 또는 검증 등급이 바뀌면 자동 선택하지 않고 새 capability/policy 협상과 필요한 승인을 거친다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `pf-c1-eval-contract` | architecture | YAML config는 provider/target, prompt, test case와 assertion을 분리해 조합 평가를 정의한다. | [official docs](https://www.promptfoo.dev/docs/configuration/guide/), 2026-08-15 | [configuration guide lines 20–76](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/configuration/guide.md#L20-L76) | `I2` | `V2` | `windows:P0; linux:P0` | 계약 문서 확인; parser·scoring runtime과 결정성 미검증 |
| `pf-c2-redteam-composition` | architecture | red-team은 plugin, strategy, probe, target, evaluation을 별도 확장점으로 구성한다. | [official docs](https://www.promptfoo.dev/docs/red-team/architecture/), 2026-08-15 | [architecture lines 9–17](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L9-L17), [component flow](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L166-L174) | `I2` | `V2` | `windows:P0; linux:P0` | 확장 구조 확인; detector recall/precision과 attack coverage 미검증 |
| `pf-c3-trace-evidence` | capability | OpenTelemetry trace를 trajectory로 정규화해 최종 응답과 실제 tool·guardrail·error 행동을 함께 grading/investigation에 제공한다. | [official agent guide](https://www.promptfoo.dev/docs/red-team/agents/), 2026-08-15 | [trace evidence lines 297–319](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/llm-agents.md#L297-L319) | `I2` | `V2` | `windows:P0; linux:P0` | 문서 계약만 확인; span 완전성·tamper resistance·secret redaction 미검증 |
| `pf-c4-skill-eval` | capability | agent skill 버전을 같은 fixture에서 비교하며 `skill-used`, task score, cost, latency 신호를 assertion으로 결합할 수 있다. | [official guide](https://www.promptfoo.dev/docs/guides/test-agent-skills/), 2026-08-15 | [comparison goal](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/guides/test-agent-skills.md#L11-L18), [assertions](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/guides/test-agent-skills.md#L138-L197) | `I2` | `V2` | `windows:P0; linux:P0` | guide 확인; skill-used 신호가 task quality나 causality를 독립 증명하지 않음 |
| `pf-c5-ci-provenance` | interface | eval/red-team run에 반복 가능한 tag로 CI run ID와 Git SHA를 붙이고 결과 envelope를 JSON으로 처리할 수 있다. | [official CI guide](https://www.promptfoo.dev/docs/integrations/ci-cd/), 2026-08-15 | [CI tags](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/integrations/ci-cd.md#L66-L80), [result envelope](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/integrations/ci-cd.md#L361-L405) | `I2` | `V2` | `windows:P0; linux:P0` | tag는 caller 입력이므로 commit 진위·artifact hash·independent verifier를 보장하지 않음 |
| `pf-c6-cloud-boundary` | security | 문서화된 red-team 흐름은 일부 공격 생성·후속 refinement·summary에 Promptfoo cloud service와 AI model 통신을 포함한다. | [official architecture](https://www.promptfoo.dev/docs/red-team/architecture/), 2026-08-15 | [data-flow lines 183–203](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L183-L203) | `I2` | `V2` | `windows:P0; linux:P0` | data residency, retention, tenant isolation, 비용과 offline 동등성은 unknown |
| `pf-c7-telemetry-egress` | limitation | CLI는 기본 usage telemetry와 npm update check를 수행하며 환경 변수로 각각 비활성화한다. | [official telemetry docs](https://www.promptfoo.dev/docs/configuration/telemetry/), 2026-08-15 | [telemetry lines 22–43](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/configuration/telemetry.md#L22-L43) | `I2` | `V2` | `windows:P0; linux:P0` | 망분리·privacy 환경은 deny-by-default wrapper와 실제 egress test 필요 |
| `pf-c8-executable-extension` | limitation | config는 JavaScript/Python variable·assertion·custom provider를 호출할 수 있어 config/data와 executable authority 경계가 겹칠 수 있다. | [official configuration docs](https://www.promptfoo.dev/docs/configuration/guide/), 2026-08-15 | [scripted variables](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/configuration/guide.md#L96-L138), [JavaScript assertion](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/configuration/guide.md#L52-L76) | `I2` | `V2` | `windows:P0; linux:P0` | untrusted fixture/config를 production credential 환경에서 실행하면 안 됨; sandbox enforcement 미검증 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| CLI | local process + YAML/JSON/CSV input, terminal/file output | operator/CI → one eval or red-team run → result ID/artifact | process environment의 provider credential·filesystem·network 권한을 상속 | [README quick start](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/README.md#L25-L45) |
| Node library/contracts | ESM/CJS package exports | application → evaluation library → result objects | embedding application의 identity와 secret scope; library가 독립 승인자가 아님 | [package exports](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/package.json#L8-L25) |
| Target/provider | HTTP/model/browser/custom JS·Python | probe/test → target session → response/metadata/error | target auth와 write-capable tool authority는 provider별; red-team prompt가 권한을 축소하지 않음 | [target types](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/architecture.md#L136-L146) |
| Trace | OpenTelemetry span/trajectory | instrumented target → collector/eval → grader/investigator | span producer 신뢰, attribute redaction, trace retention과 tamper evidence 필요 | [trace evidence](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/red-team/llm-agents.md#L297-L329) |
| CI output | JSON/CSV/XML/HTML + exit status | run → quality/security threshold → pipeline decision | tag/result 자체는 trusted commit·artifact·approval 증명이 아니며 CI identity binding 필요 | [CI outputs](https://github.com/promptfoo/promptfoo/blob/ab84555c1b0ff74eca6b03abb7936ac9a0149242/site/docs/integrations/ci-cd.md#L83-L118) |

## 운영·보안·trust boundary

- 보호 자산과 authority: prompt·system policy·test corpus·model output·trace/tool argument·target endpoint, provider/target credential, cache/result, browser/custom-script process 권한과 CI gate.
- local runner, custom executable config, model/provider, target system, Promptfoo cloud, telemetry/update endpoint, trace collector와 CI artifact store를 별도 trust domain으로 둔다. 외부 attack generation에 production prompt·trace·secret을 보내지 않도록 `AX-D002/D004/D006` 정책이 필요하다.
- `skill-used`, LLM grader, risk score, pass rate와 CI green은 derived evaluation signal이다. source SHA·environment·target revision·seed/config hash·raw trace·deterministic verifier가 없으면 production 완료나 안전 증거로 승격하지 않는다.
- telemetry opt-out과 output stripping은 배포별 설정이며 network deny, data deletion 또는 secret non-disclosure의 runtime proof가 아니다.

## 플랫폼

- Windows `P0/unknown`: Node runtime과 Codex/Claude provider 예시가 있어도 Windows native build/test artifact가 없으므로 지원을 추정하지 않는다.
- Linux `P0/unknown`: POSIX shell 예시는 문서 사용법일 뿐 Linux native runtime evidence가 아니며, 이번 조사에서 명시적 Linux support contract를 별도 확인하지 않았다.
- container, WSL, browser 또는 remote target 실행은 Windows/Linux host-native runner 증거로 바꾸지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `pf-v2-source-20260815` | `V2` | `ab84555c1b0ff74eca6b03abb7936ac9a0149242` | official GitHub repository/commit/tree/file API inspection; local `rg` duplicate search, exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; connector version unknown | official HEAD, MIT license, architecture/interface/security limitations과 KB 비중복성 확인 | 이 프로필의 official fixed-SHA URL | `pf-c1`~`pf-c8` | clone·dependency·build·runtime/provider/cloud 미실행; current web docs와 fixed SHA의 이후 drift 가능 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: declarative eval과 red-team composition(`pf-c1`, `pf-c2`), agent가 말한 결과와 실제 trajectory를 함께 보는 evidence loop(`pf-c3`), skill-version fixture(`pf-c4`)가 기존 orchestration 중심 KB의 evaluation/failure-injection 공백을 채운다.
- 확인된 한계: CI tag와 grader는 independent proof가 아니고(`pf-c4`, `pf-c5`), cloud·telemetry egress가 있으며(`pf-c6`, `pf-c7`), config 확장점이 executable authority를 가진다(`pf-c8`).
- 미확인·추론: assertion 결정성, red-team recall/false-positive, trace 완전성·tamper resistance, offline parity, cloud retention/tenant isolation, 비용, Windows/Linux native 동작은 unknown.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | provider/target × fixture × assertion의 versioned evaluation contract와 attack plugin/strategy 분리 | `pf-c1`, `pf-c2` | `RM-P3-false-complete-fixture`, `RM-P4-threat-fixtures` 입력 형식 |
| Adapt | trajectory와 CI tag를 source/config/target/environment hash가 있는 CompletionEvidence로 확장 | `pf-c3`, `pf-c5` | independent verifier, immutable artifact, redaction과 `AX-D008` retention 필요 |
| Avoid | LLM score·skill-used·pass rate만으로 안전/완료를 판정하거나 untrusted executable config를 credentialed runner에서 실행 | `pf-c4`, `pf-c8` | fail-closed evidence·sandbox·secret audience 원칙 |
| Build | provider-neutral eval adapter, deterministic failure corpus, trace receipt, budget/egress gate와 offline mode | `pf-c1`~`pf-c8` | `AD-PROP-006` verifier 분리, `RM-P3-verifier`, `RM-P4-threat-fixtures` |

## 도입 판단

- 결정: 파일럿
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: evaluation/failure-injection contract, skill/version comparison, trace-backed grader와 CI evidence envelope의 clean-room 참고; production target·provider 직접 연동은 미결정.
- 이유: `pf-c1`~`pf-c5`가 현재 KB의 evaluation plane 공백을 직접 채우지만 정적 `V2/P0`이고 `pf-c6`~`pf-c8`의 egress·executable authority 경계가 미검증이다.
- 재검토 조건: fixed-SHA dependency/license inventory, V3 offline build, Windows/Linux native P2, deterministic fixture repeatability, cloud/telemetry egress negative test, trace tamper/redaction과 cost ceiling 검증.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `pf-test-build-platforms` | `pf-c1`, `pf-c4`, `pf-c5` | `V3/windows:P2; V3/linux:P2` | 승인된 Windows/Linux native x86_64, 동일 Node/lockfile | fixed SHA install/build/unit + offline echo-provider eval | 두 OS에서 동일 fixture schema/result 의미와 exit 0 | environment, lock/SBOM, logs, result JSON hash | dependency network 승인, `AX-D011` |
| `pf-test-determinism` | `pf-c1`~`pf-c5` | `V4/linux:P2` | isolated local provider/agent fixture | fixed seed/input 반복, tool-call success/failure, false-complete, cancel/timeout | deterministic assertion은 동일; stochastic signal은 분리·분산 기록; missing trace fail-closed | config hash, raw/normalized trace, score distribution | synthetic data, no external model 우선 |
| `pf-test-egress-secret` | `pf-c6`~`pf-c8` | `V5/linux:P2` | deny-by-default network sandbox, canary secret | telemetry/update/cloud 차단, malicious JS/Python config, trace secret injection | 허용 endpoint 외 egress 0, secret exposure 0, executable config 격리/거부 | packet log, syscall/process trace, redacted report | security review, no production credential |
| `pf-test-trace-integrity` | `pf-c3`, `pf-c5` | `V5/linux:P2` | signed synthetic agent trace pipeline | dropped/reordered/forged span과 stale CI tag 주입 | incomplete/tampered evidence를 pass로 승격하지 않고 provenance mismatch 검출 | signed receipt, negative-test logs | evidence schema/identity 결정 필요 |

## 관계

- `Tool HAS_VERSION tool-version:promptfoo@ab84555c1b0ff74eca6b03abb7936ac9a0149242`
- `ToolVersion FITS_ROLE EvaluationRunner/RedTeamGenerator/EvidenceProducer`
- `ToolVersion PROVIDES declarative-agent-evaluation/adversarial-probe-generation/trace-backed-grading/skill-version-evaluation`
- `ToolVersion SUPPORTS CLI/Node/YAML/HTTP/OpenTelemetry/CI`
- `Project EVALUATES ToolVersion` as evaluation and failure-injection plane pilot reference

## 변경 이력

- 2026-08-15: official `main` HEAD를 manifest-only immutable pin으로 등록하고 fixed-SHA `I2/V2`, Windows `P0`, Linux `P0` 분석을 추가함.
