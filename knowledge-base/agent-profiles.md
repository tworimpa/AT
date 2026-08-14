---
id: agent-execution-profiles-v1
type: profile-catalog
title: 에이전트 실행 프로파일
status: active
profile_schema_version: 1
tags:
  - knowledge-base
  - agent-profile
  - execution-policy
  - evidence
observed_at: 2026-08-14
source_parent_commit: 55227696af0ba94b934187876c6db6669dd2b574
---

# 에이전트 실행 프로파일

[지식 베이스 홈](./index.md) · [공통 운영 규칙](../AGENTS.md) · [지식 그래프 스키마](./knowledge-graph-schema.md)

## 경계

루트 `AGENTS.md`는 모든 작업에 적용되는 공통 규칙이고, 이 문서의 Profile은 한 실행의 **모델 등급, effort, 권한, 예산, 증거 기대치와 escalation 정책을 묶은 실행 정책**이다. Profile은 Planner·Worker·Verifier 같은 역할이 아니다. 한 역할이 작업 위험에 따라 여러 Profile을 쓸 수 있고, 하나의 Profile도 여러 역할에 적용할 수 있다.

Profile은 모델 성능·가격·한도를 보증하지 않는다. 실행 결과에는 선택 정책뿐 아니라 실제 provider/model/version, effort, environment fingerprint, cost/latency 관찰을 남겨 이후 비교 가능한 Evidence로 만든다.

## 모델 해석 계약

| 필드 | 규칙 |
|---|---|
| `model_tier` | `fast`, `balanced`, `deep`, `strict` 같은 공급자 중립 요구 등급 |
| `model_slug` | dispatcher가 해당 실행 환경에서 지원 목록을 확인한 뒤 고정하는 실제 slug. 확인 전에는 `unresolved` |
| `effort` | `low`, `medium`, `high`, `xhigh` 중 실행기가 지원하는 값. 실제 값과 요청값을 모두 기록 |
| 조건부 예시 | Codex 실행기가 현재 `gpt-5.6-terra`와 `gpt-5.6-sol`을 명시적으로 광고하는 환경에서만 `fast/balanced → gpt-5.6-terra`, `deep/strict → gpt-5.6-sol` 후보로 해석할 수 있다. 다른 환경에는 이 slug를 이식하지 않고 그 실행기가 광고한 동급 후보를 사용한다. 이는 효능·가격 주장이 아니라 environment-scoped resolver 예시다. |

요청 등급을 지원하지 않으면 동일 권한 안의 가장 가까운 지원 모델을 선택하고 제한을 기록할 수 있다. 더 넓은 권한, 비용 또는 외부 동작이 생기는 대체는 사람 승인 없이는 진행하지 않는다.

## 공통 실행 기록

```yaml
run_id: <stable-id>
profile_id: <profile-id>
profile_revision: 1
agent_role: <planner|worker|verifier|reviewer|researcher|other>
model:
  provider: <provider-or-unknown>
  requested_tier: <fast|balanced|deep|strict>
  slug: <actual-slug-or-unknown>
  version: <actual-version-or-unknown>
effort:
  requested: <low|medium|high|xhigh>
  actual: <value-or-unknown>
scope:
  base_sha: <sha-or-null>
  head_sha: <sha-or-null>
environment_fingerprint: <os/runtime/toolchain/container-image-or-unknown>
budget:
  timebox_minutes: <number-or-null>
  retry_limit: <number>
observations:
  latency_ms: <observed-or-unknown>
  cost: <observed-value-and-unit-or-unknown>
evidence_ids: []
limitations: []
```

시간과 token/cost는 hard fact가 아니라 작업 계약의 budget과 실행 후 관찰을 분리한다. provider가 비용이나 latency를 제공하지 않으면 `unknown`으로 보존한다.

## 프로파일 카탈로그

| Profile ID | model tier | effort | 적용 역할 예 | 주 용도 | 기본 권한 | 기본 timebox / retry | 요구 증거 |
|---|---|---|---|---|---|---|---|
| `research-fast` | fast | low | Researcher, Triager | upstream 식별, 문서·metadata 조사, 빠른 triage | read-only, network read | 20분 / 1회 | 출처 URL·관찰 시각; fixed SHA를 읽었을 때만 `V2` |
| `planner-balanced` | balanced | medium | Planner, Coordinator | 범위·DAG·acceptance·risk 계획 | read-only; 요청된 planning 문서만 write | 45분 / 1회 | 가정·의존성·승인 gate·검증 계획 |
| `implement-deep` | deep | high, 필요 시 xhigh | Worker, Documenter | 코드·문서 구현과 로컬 검증 | workspace write/test; 외부 write 금지 | 120분 / 2회 | diff, 명령/exit, artifact, base/head; 실행한 단계까지만 `V3+` |
| `verify-strict` | strict | high 또는 xhigh | Verifier, Tester | 독립 검증, failure boundary, release gate | read-only + test execution | 90분 / 1회 | 재현 명령, 환경, pass/fail/unknown, 반증과 stale 여부 |
| `review-fast` | fast 또는 balanced | low 또는 medium | Reviewer, Security Reviewer | exact-SHA diff/PR 정적 review | read-only; approve/merge 금지 | 30분 / 1회 | base/head, finding locator, severity/confidence, 미검토 범위 |

timebox는 기본값이며 사용자 계약이나 runtime 한도가 우선한다. 시간이 끝났다는 이유만으로 성공으로 처리하지 않고 안전한 중간 상태와 남은 작업을 보고한다.

## `research-fast`

- 작업: 공식 upstream 확인, default branch/HEAD/license/maintenance metadata, README·문서 요약, 중복 후보 triage.
- 권한: repository와 공식 웹 source 읽기만 허용한다. clone/submodule·문서 변경·외부 write는 별도 작업 계약이 있어야 한다.
- 증거: 변동 정보에 `observed_at`을 붙이고 공식 source를 우선한다. README 주장은 `V1`, fixed SHA source를 직접 읽은 claim만 `V2`다.
- 승인·escalation: 라이선스 rider, 공식 출처 불명, 인증 필요, source 간 충돌, runtime 확인 필요 시 중단하고 `planner-balanced` 또는 사람 결정으로 올린다.

## `planner-balanced`

- 작업: 목표/비범위, task DAG, role·resource lease, acceptance, evidence class, rollback과 approval gate 정의.
- 권한: 기본 read-only다. 사용자가 planning 문서 작성을 요청한 경우 그 파일만 수정하며 실행·배포·외부 write는 하지 않는다.
- 증거: 각 결정에 source/assumption과 검증 방법을 연결한다. 모델 효능·비용·기간은 관찰 없이는 가정으로 표시한다.
- 승인·escalation: 요구 충돌, scope가 다른 구현 선택, production/secret/외부 시스템 결정은 사람에게 올린다. 구현이 승인되면 새 `implement-deep` run으로 분리한다.

## `implement-deep`

- 작업: 승인된 범위의 코드·문서 변경, deterministic 검사, 관련 build/test, 명시된 commit 생성.
- 권한: workspace 파일 변경과 로컬 명령 실행은 허용한다. push, merge, deploy, production, 외부 메시지, secret/권한 변경, destructive 데이터 작업은 명시 승인 없이는 금지한다.
- 증거: 변경 path, base/head, 명령 argv/cwd/exit, test artifact를 보존한다. 정적 검사만 했으면 `V2`, build를 실행·보존했으면 해당 claim만 `V3`다.
- 승인·escalation: 두 번의 좁은 재시도 뒤 같은 blocker, base drift, 권한 확대, destructive migration, 실제 service/device가 필요하면 중단한다. 더 높은 effort는 새 attempt로 기록한다.

## `verify-strict`

- 작업: 구현자와 분리된 acceptance 재검증, negative/failure case, provenance·SHA·artifact·stale evidence 검사.
- 권한: source를 수정하지 않고 test/build/inspection만 수행한다. fix가 필요하면 finding과 재현을 반환하고 별도 implementation run을 만든다.
- 증거: `pass`, `fail`, `partial`, `unknown`을 모두 보존한다. CI, deploy, external service, operator, physical device 증거를 서로 바꾸어 쓰지 않는다.
- 승인·escalation: flaky/비결정 결과는 같은 입력으로 한 번만 재현하고 두 결과를 모두 남긴다. production·외부 서비스·비용 발생 검증은 승인과 별도 environment fingerprint가 필요하다.

## `review-fast`

- 작업: exact base/head의 diff·PR을 정적으로 읽고 correctness/security/maintainability finding을 우선순위화한다.
- 권한: comment 초안까지 read-only다. GitHub approve/request-changes/comment 제출, code fix, merge는 별도 승인 없이는 수행하지 않는다.
- 증거: finding마다 path/line, category, severity, confidence, 영향과 수정 방향을 남긴다. 정적 review는 `V2` 상한이며 CI나 runtime 성공으로 승격하지 않는다.
- 승인·escalation: 대형 diff, architecture 결정, 보안 경계, 재현이 필요한 finding은 `verify-strict`; 수정은 `implement-deep`으로 넘긴다.

## Profile 선택과 승격

1. task contract에서 위험, 변경 여부, 외부 동작, 필요한 최고 증거 등급을 확인한다.
2. 가장 낮은 권한과 충분한 모델 등급의 Profile을 선택한다.
3. 실행기가 실제 model/effort를 해석한 결과를 run record에 고정한다.
4. 범위·권한·evidence class가 바뀌면 같은 run을 암묵 확장하지 않고 새 attempt/profile로 승격한다.
5. 완료 보고에는 profile, 실제 model/effort, 사용 budget, 증거와 미수행 항목을 포함한다.

## 검증해야 할 미래 가설

- 어느 model tier/effort가 어떤 작업에서 더 정확하거나 빠른지 현재 카탈로그는 주장하지 않는다.
- profile별 성공률, latency, cost는 동일 fixture와 environment fingerprint를 가진 반복 run에서 관찰한 뒤에만 비교한다.
- 가격, quota, 지원 모델과 context 한도는 provider별 TTL이 있는 외부 사실이며 실행 전에 다시 확인한다.
