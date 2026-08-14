---
id: ax-platform-context-2026-08-14
type: project-context
title: 사내 AX 맞춤형 에이전트 플랫폼 지속 컨텍스트
status: active
tags:
  - knowledge-base
  - ax-platform
  - handoff
  - governance
observed_at: 2026-08-14
last_reviewed: 2026-08-15
source_parent_commit: 984cac0634b83d10af91d8e1814680816e67c53b
verification_ceiling: V2
---

# 사내 AX 맞춤형 에이전트 플랫폼 지속 컨텍스트

[지식 베이스 홈](./index.md) · [사내 AX reference architecture](./internal-ax-reference-architecture.md) · [34개 ToolVersion 커버리지](./tools/coverage.md) · [스키마와 소스 운영 규칙](./knowledge-graph-schema.md) · [플랫폼 청사진](./platform-blueprint.md)

이 문서는 다음 세션과 에이전트가 작업 전에 읽는 짧은 지속 컨텍스트다. 상세 Claim과 source of truth를 대체하지 않으며, 서로 충돌하면 fixed-SHA ToolVersion 프로필과 연결된 SourceArtifact/Evidence 및 최신 승인 Decision Log를 우선한다.

## Goal

목표는 34개 중 하나를 골라 도입하거나 벤더 순위를 만드는 것이 아니다. 사내 AX 도입에 맞는 맞춤형 에이전트 플랫폼을 설계하기 위해 각 도구의 장점·한계·실패 경계를 고정 버전에서 분석하고, 재사용 가능한 지식을 축적하는 것이다.

각 ToolVersion 프로필은 다음 네 가지 설계 재료를 분리한다.

- `Borrow`: 계약·상태 모델·UX 등 직접 참고할 패턴
- `Adapt`: Windows, 사내 권한, 망분리, 감사 요구에 맞게 변형할 패턴
- `Avoid`: fail-open, 모호한 완료 판정, license·운영 위험 등 가져오지 않을 패턴
- `Build`: 우리 control plane·executor·adapter·evidence·policy·knowledge layer에서 직접 구현할 capability

도구별 “채택/파일럿/참고/보류/역사” 표시는 설계 탐색 우선순위일 뿐 구매, 배포 또는 production 적합성의 최종 답이 아니다.

## Baseline and provenance

- 조사 집합: 부모 저장소에 등록된 34개 official-upstream fixed-SHA gitlink.
- 요청 기준점: `984cac0634b83d10af91d8e1814680816e67c53b`.
- 조사 환경 한계: 병렬 조사 worktree에서 submodule 본문이 비어 있을 수 있어 부모 `.gitmodules`와 `git ls-tree`로 URL·gitlink SHA를 확인하고, 공식 upstream의 fixed-SHA `tree`/`blob` 및 metadata URL로 정적 근거를 수집했다.
- provenance 제한: 부모 GitHub 저장소의 submodule 내부 deep link는 official source 근거가 아니며 checkout 상태에 따라 열리지 않는다. 프로필 Claim은 official upstream fixed-SHA URL을 사용한다.
- 정적 ceiling: 공통 출처 무결성은 `I2`, 기능 근거는 최대 `V2`, Windows는 Claim별 `W0` 또는 좁은 정적 경로 `W1`이다.
- 미수행: 의존성 설치, 전체 build(`V3`), 통제 runtime(`V4`), E2E/failure injection(`V5`), 운영 검증(`V6`), 실제 Windows 실행(`W2`)과 회귀 suite(`W3`).

`I2`, `V2`, `W1`은 서로 다른 축이다. fixed SHA가 정확해도 기능 동작을 증명하지 않고, Windows code/CI/process/CRLF 경로가 보여도 native Windows workflow가 실행됐다는 뜻이 아니다.

## Core decisions in force

1. **Windows-first, not Windows-assumed**: local control plane과 executor 계약은 Windows를 첫 기준으로 설계한다. 실제 지원은 `W2/W3` evidence 전까지 완료로 표현하지 않는다.
2. **Claim/Evidence separation**: 문서·정적 코드의 Claim, 실행 Evidence와 분석자의 판단을 분리한다. agent 자기보고나 UI 상태는 verification pass가 아니다.
3. **Independent evidence axes**: `I0~I2`, `V0~V6`, `W0~W3`을 합산 점수로 만들지 않는다.
4. **Fail-closed state and authority**: atomic claim, lease/generation fencing, cancellation, completion, verification, approval과 external write를 서로 다른 상태·권한으로 둔다. 구현이 없거나 우회 가능하면 보장으로 쓰지 않는다.
5. **Profiles are immutable-version analyses**: `Tool`, 고정 `ToolVersion`, 시점성 `CurrentUpstreamObservation`, 분석 `AnalysisSnapshot`을 분리한다. fixed version은 latest release와 동의어가 아니다.
6. **Design-material policy**: 모든 상세 프로필에 `Borrow/Adapt/Avoid/Build`와 다음 검증을 둔다. license와 upstream activity도 고정 버전 정보와 현재 관찰을 섞지 않는다.

## Hybrid source policy for future targets

현재 34개 submodule을 일괄 폐기하거나 자동 재분류하지 않는다. 다음 정책은 미래 신규 대상 등록에 적용한다.

| 대상 성격 | 기본 보존 방식 | 필요한 기록 |
|---|---|---|
| adapter, reference implementation 또는 핵심 설계에 직접 영향을 주는 도구 | official upstream + fixed SHA gitlink submodule | upstream 공식성, gitlink SHA, license, expected design impact, clone cost, fixed-SHA source URLs |
| 비교·시장·문서 조사 도구 | versioned manifest + source URLs + Claims/Evidence | immutable version/ref, URL, checksum 또는 commit identity, license/activity observation, analysis snapshot |
| manifest-only이나 코드 확인이 필요한 경우 | 임시 shallow clone 또는 remote fixed-SHA inspection | 명령/방법, inspected SHA, 보존 artifact, 한계; 영구 submodule 전환 여부는 별도 결정 |

신규 등록 때 `official upstream`, `license`, `activity`, `expected design impact`, `clone cost`를 평가해 `submodule`과 `manifest-only`를 선택한다. submodule 작업트리가 비어 있으면 부모 `.gitmodules` + `git ls-tree`로 pin을 확인하고 official upstream fixed-SHA URL을 SourceArtifact로 쓴다.

## Current state

- 34개 고정 ToolVersion이 catalog와 gitlink에 등록돼 있다.
- 상세 ToolVersion 프로필은 34/34 작성됐으며 [커버리지 매트릭스](./tools/coverage.md)는 현재 템플릿 기준 `covered` 23개와 legacy/부분 구조 `partial` 11개를 구분한다. `missing`과 `in-progress`는 0개다.
- [사내 AX reference architecture](./internal-ax-reference-architecture.md)는 control plane, executor, adapter, evidence, policy, knowledge ingestion layer와 최소 코어/확장 옵션을 제안 상태로 정리한다.
- 지식 그래프는 `Capability → AXNeed → ArchitectureDecision/RoadmapItem`과 각 edge의 source/evidence를 보존하도록 확장했다.
- 현재 산출물은 문서·fixed-SHA 정적 통합 `V2`다. build/runtime/E2E는 수행하지 않았다.
- 이 통합 변경은 2026-08-15에 commit·push 승인을 받았다. 실제 반영 여부와 SHA는 Git history와 완료 보고에서 확인하며, 문서 자체가 배포 성공을 증명하지 않는다.

## Do not assume

- 회사의 업종, 데이터 분류, 규제, 승인 체계, 조직 경계, 망분리 수준 또는 허용 cloud/model provider를 가정하지 않는다.
- catalog의 도입 판단을 벤더 선정, 구매 승인, 보안 승인 또는 production acceptance로 읽지 않는다.
- tool README의 “safe”, “sandbox”, “atomic”, “Windows support” 문구를 failure test 없는 보장으로 승격하지 않는다.
- CI에 Windows job이나 process/CRLF 코드가 있다는 이유로 `W2/W3`를 부여하지 않는다.
- HTTP/HTTPS proxy가 non-HTTP 또는 DNS egress까지 차단한다고 가정하지 않는다.
- warning/lock이 우회 flag, 관리자 승인 또는 alternate write path를 막는다고 가정하지 않는다.
- current upstream observation을 고정 ToolVersion의 속성으로 소급 적용하지 않는다.
- 비어 있는 submodule 디렉터리를 “소스가 없음” 또는 “조사가 끝남”으로 해석하지 않는다.

## Decision-needed company conditions

아래는 설계 입력이며 아직 답이 없다. 답을 얻기 전에는 placeholder와 decision log로 유지한다.

| Decision ID | 필요한 회사 입력 | 상태 | 결정 시 영향 |
|---|---|---|---|
| `AX-D001` | 업종과 적용 규제·계약 의무 | decision-needed | data residency, audit, model/provider gate |
| `AX-D002` | 데이터 분류 체계와 source/prompt/output별 처리 규칙 | decision-needed | executor placement, retention, redaction, egress |
| `AX-D003` | 조직·프로젝트·repository 권한 모델과 승인자 | decision-needed | RBAC/ABAC, separation of duties, merge/write gate |
| `AX-D004` | 인터넷, 사내망, 망분리 구간과 허용 protocol/DNS 정책 | decision-needed | adapter/executor topology, proxy와 deny policy |
| `AX-D005` | secret 발급·회전·audience·break-glass 정책 | decision-needed | broker, short-lived token, audit, incident response |
| `AX-D006` | 허용 model/provider, prompt/data 사용 조건과 지역 | decision-needed | model gateway, routing, fallback, legal review |
| `AX-D007` | SCM·CI·ticket·문서·메신저 시스템과 write 승인 방식 | decision-needed | connector 범위, safe output, external action gate |
| `AX-D008` | 로그·transcript·artifact 보존 기간과 열람/삭제 정책 | decision-needed | evidence store, privacy, legal hold, cost |
| `AX-D009` | 가용성·복구·지원 시간·RTO/RPO/SLO | decision-needed | control plane HA, reconciliation, backup, on-call |
| `AX-D010` | 예산, chargeback/showback, concurrency와 quota | decision-needed | scheduler budget, provider selection, cost controls |
| `AX-D011` | pilot 대상 업무, 사용자군과 성공/중단 기준 | decision-needed | roadmap order, evaluation suite, rollout gates |
| `AX-D012` | 내부 개발·운영 owner와 보안/법무/감사 의사결정체 | decision-needed | ownership, exception process, production approval |

승인된 결정은 날짜·owner·근거·대안·만료/재검토 조건과 함께 별도 Decision Log로 승격한다. 미응답은 암묵적 기본값이 아니다.

## Next safe steps

1. 34행 [커버리지 매트릭스](./tools/coverage.md)의 legacy/부분 구조 11개를 현재 template에 맞추되 evidence 등급과 문서 완성도를 섞지 않는다.
2. 각 프로필의 Claim이 official upstream fixed-SHA URL, license와 명시적 한계를 갖는지 정적 검사한다.
3. `Borrow/Adapt/Avoid/Build`를 정규 Capability와 AX Need에 매핑하고 중복·충돌을 architecture decision 후보로 묶는다.
4. `AX-D001~D012`를 사내 owner와 검토해 assumptions가 아닌 승인된 decision으로 바꾼다.
5. 승인 뒤 Windows local kernel pilot부터 `V3/W2` evidence 계획을 실행한다. runtime, external service, 비용 발생, credential 사용과 write는 별도 권한·profile을 요구한다.
6. 새 조사 대상은 하이브리드 소스 등록 평가를 먼저 수행한다. 현재 34개의 저장 방식을 자동 변경하지 않는다.

## Provenance note

Last reviewed `2026-08-15`. 이 컨텍스트는 부모 저장소의 34개 `.gitmodules`/gitlink, 34개 fixed-SHA ToolVersion 정적 프로필, 지식 베이스 schema/catalog와 통합 결과를 요약한다. 실행하지 않은 검증은 완료로 기록하지 않았으며, upstream의 현재 상태는 관찰일 이후 달라질 수 있다.
