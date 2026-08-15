---
id: knowledge-graph-schema-v2
type: governance
supersedes: knowledge-graph-schema-v1
title: 지식 베이스 작성 규칙과 최소 지식 그래프 스키마
status: active
schema_version: 2
tags:
  - knowledge-base
  - knowledge-graph
  - provenance
  - evidence
  - cross-platform
observed_at: 2026-08-14
source_parent_commit: 55227696af0ba94b934187876c6db6669dd2b574
---

# 지식 베이스 작성 규칙과 최소 지식 그래프 스키마

[지식 베이스 홈](./index.md) · [AX 플랫폼 지속 컨텍스트](./ax-platform-context.md) · [사내 AX reference architecture](./internal-ax-reference-architecture.md) · [34개 도구 카탈로그](./tools/catalog.md) · [프로필 커버리지](./tools/coverage.md) · [에이전트 실행 프로파일](./agent-profiles.md) · [플랫폼 청사진](./platform-blueprint.md) · [도구 프로필 템플릿](./templates/tool-profile.md)

## 원칙

1. `Tool`과 immutable `ToolVersion`을 분리한다. 새 upstream HEAD가 나타나도 이전 지식을 덮어쓰지 않는다.
2. 기능과 한계는 단순 속성이 아니라 검증 가능한 `Claim`으로 기록한다.
3. Claim마다 `SourceArtifact`와 가능한 경우 `Evidence`를 연결한다.
4. provenance와 검증 등급은 node뿐 아니라 edge에도 둔다. 같은 ToolVersion의 ACP, Windows, Linux, runtime 주장은 각각 다른 근거와 등급을 가질 수 있다.
5. 정적 코드 `V2`를 build/runtime/E2E `V3~V5`로 자동 승격하지 않는다.
6. 실패와 반증 evidence를 삭제하지 않고 `unknown`, `partial`, `fail`을 구분한다.
7. secret 원문, credential handle 내부값과 private endpoint는 지식 베이스에 저장하지 않는다.
8. 외부 서비스 가격·한도·상태는 TTL이 있는 관찰값으로 두고 코드·설계 사실과 분리한다.
9. `Profile`은 모델·effort·권한·예산·evidence/escalation을 묶는 실행 정책이며 `AgentRole`과 분리한다.
10. 고정 `ToolVersion`, 시점이 있는 `CurrentUpstreamObservation`, 분석자의 `AnalysisSnapshot`을 분리한다. 최신 관찰이 과거 고정 버전의 Claim을 바꾸지 않는다.
11. Markdown의 `status`는 문서 유형별 lifecycle을 나타낸다. 실행 기록의 역사 상태와 현재 규칙·설계 상태를 같은 enum으로 오인하지 않는다.

## 최소 엔터티

| 엔터티 | 목적 | 필수 식별 정보 |
|---|---|---|
| Tool | 지속되는 제품·저장소·서비스 | `id`, 공식 upstream, license, maintenance status |
| ToolVersion | 조사한 immutable 버전 | parent Tool, `version_kind`, SHA/tag/digest/API revision, observed date |
| CurrentUpstreamObservation | upstream의 시점성 상태 | observed date, default branch/head 또는 release, activity/archive 상태, source URL, TTL |
| AnalysisSnapshot | 특정 시점의 해석 묶음 | analysis date, 대상 ToolVersion, scope, author/reviewer, evidence ceiling |
| Capability | 정규화된 기능 | 예: task DAG, atomic claim, ConPTY, worktree, verifier, snapshot |
| AXNeed | 사내 업무·통제·운영 요구 | stable need ID, 이해관계자, desired outcome, 제약, 상태(`known|unknown|decision-needed`) |
| ArchitectureDecision | 근거가 연결된 설계 선택 | decision ID, 후보, 상태(`proposed|accepted|rejected|deferred`), 결정권자·조건 |
| AgentRole | 권한이 분리된 역할 | Planner, Scheduler, Worker, Verifier, Reviewer, Merger, Watchdog, Executor, Relay, Policy, Gateway, Spec/Memory |
| Profile | 역할과 독립된 실행 정책 | stable profile ID/revision, model tier, effort, permission, budget, evidence와 escalation policy |
| ExecutionRun | Profile이 해석된 실제 실행 | run ID, role, profile ID/revision, 실제 model/version·effort, environment fingerprint, cost/latency observation |
| Integration | protocol·adapter·state interface | ACP, MCP, JSON-RPC, CLI, PTY, HTTP/SSE, WebSocket, GitHub, SQLite |
| SecurityOperationalRequirement | 보안·운영 조건 | isolation, secret audience/redaction, egress, retention, readiness, fencing, recovery, cost/SLO |
| PlatformCapabilityProfile | OS/host/guest별 실행 capability와 검증 상태 | platform, edition/distribution, version, architecture, shell/service manager, host/guest scope, `P0~P3`, result |
| Claim | 참·거짓·부분 여부를 검증할 문장 | subject, predicate, object/value, scope, status |
| SourceArtifact | Claim의 출처 | repo-relative path 또는 upstream permalink, line/anchor, artifact kind, license |
| Evidence | 실제 검증 결과 | method, result, artifact locator, environment fingerprint, limitations |
| Project | 제품·실험·benchmark | 목적, 상태, 선택·평가 범위 |
| RoadmapItem | 구현·검증 단위 | phase, priority, acceptance, dependency, owner status |

## 핵심 관계

| 관계 | 의미 |
|---|---|
| `Tool HAS_VERSION ToolVersion` | 지속 ID와 고정 버전 연결 |
| `ToolVersion SUPERSEDES ToolVersion` | 이전 조사 기록을 보존한 버전 계보 |
| `CurrentUpstreamObservation OBSERVES Tool` | 현재 upstream 상태와 지속 Tool 연결 |
| `AnalysisSnapshot ANALYZES ToolVersion` | 분석 시점과 immutable 대상 연결 |
| `ToolVersion PROVIDES Capability` | 특정 버전의 기능 Claim이 있는 관계 |
| `Capability ADDRESSES AXNeed` | 도구에서 관찰한 capability가 사내 AX 요구를 어떻게 지원하는지 연결 |
| `AXNeed DRIVES ArchitectureDecision` | 확인된 또는 미결 요구가 설계 선택을 유발 |
| `ArchitectureDecision SELECTS/ADAPTS/AVOIDS Capability` | Borrow·Adapt·Avoid 판단과 조건·근거 보존 |
| `ArchitectureDecision CREATES RoadmapItem` | Build 결정과 구현·검증 작업 연결 |
| `ToolVersion SUPPORTS Integration` | protocol/adapter 지원 Claim |
| `ToolVersion FITS_ROLE AgentRole` | 역할에 적합하다는 판단 |
| `AgentRole REQUIRES Capability` | 역할 수행에 필요한 기능 |
| `AgentRole MAY_USE Profile` | 역할과 실행 정책을 동일시하지 않는 허용 관계 |
| `Profile CONFIGURES ExecutionRun` | 선택 정책과 실제 실행 해석 연결 |
| `ExecutionRun PRODUCES Evidence` | 실제 model/effort/environment와 검증 artifact 연결 |
| `Integration CONNECTS ToolVersion/Executor` | 연결 가능한 runtime 또는 executor |
| `ToolVersion/Executor HAS_PLATFORM_PROFILE PlatformCapabilityProfile` | Windows/Linux native와 WSL/container/remote guest의 capability·증거 범위 연결 |
| `ToolVersion SATISFIES/REQUIRES/VIOLATES Requirement` | 보안·운영 조건에 대한 상태 |
| `Claim ABOUT node/edge` | 검증 대상 지정 |
| `Claim DERIVED_FROM SourceArtifact` | 주장 출처 연결 |
| `Evidence SUPPORTS/REFUTES Claim` | 성공·실패 증거 연결 |
| `Capability VERIFIED_BY Evidence` | 기능 검증 결과 연결 |
| `Project SELECTS/EVALUATES/REJECTS ToolVersion` | 도입 판단과 시점 보존 |
| `RoadmapItem IMPLEMENTS Capability` | 로드맵과 기능 연결 |
| `RoadmapItem DEPENDS_ON RoadmapItem` | 선후 관계 |
| `RoadmapItem MITIGATES Requirement` | 위험 완화 목적 |
| `RoadmapItem VALIDATED_BY Evidence` | exit gate의 실제 증거 |

`Borrow`, `Adapt`, `Avoid`, `Build`는 vendor 순위를 뜻하지 않는다. ToolVersion의 Claim을 AXNeed와 ArchitectureDecision/RoadmapItem에 연결하는 설계 관계다. 각 관계에는 `source_ids`, `claim_id`, `grade`, `conditions`, `unknowns`, `observed_at`을 두고, 회사 업종·데이터 분류·규정·승인 체계가 미제공이면 `unknown`을 사실처럼 채우지 않는다.

각 edge에도 `claim_id`, `source_ids`, `evidence_ids`, `grade`, `confidence`, `observed_at`을 둘 수 있어야 한다.

## 공통 필드

모든 node와 edge는 가능한 범위에서 다음 필드를 가진다.

```yaml
id: tool-version-orca-e7b8526
type: ToolVersion
name: Orca e7b8526
status: observed
tags: [control-plane, cross-platform]
valid_from: null
valid_to: null
observed_at: 2026-08-14
updated_at: 2026-08-14
provenance:
  source_ids: [source-gitmodules, source-orca-readme]
  locator: multi-agent-tools/orca@e7b85266f531f9a219dff59d8647f86585b4fc7e
  collector: human-reviewed-static-analysis
  method: static-code
  captured_at: 2026-08-14
verification:
  grade: V2
  result: partial
  platform_scope:
    windows:
      grade: P1
      host_or_guest: host
      result: partial
    linux:
      grade: P0
      host_or_guest: host
      result: unknown
  environment_fingerprint: null
  confidence: medium
  limitations: dependencies not installed; build and runtime not executed
version:
  version_kind: commit
  version_ref: e7b85266f531f9a219dff59d8647f86585b4fc7e
  parent_repo_head: 4e6731a1b274eba5a8451b97594aadcf570108ee
```

Markdown frontmatter에는 자주 탐색하는 scalar와 tag만 두고, 상세 Claim/Evidence가 늘어나면 결정론적으로 생성하는 JSON/JSONL로 분리한다.

## 문서 lifecycle과 authority

`status`는 대문자/소문자 변형이나 별도 `state` 필드를 병행하지 않고 아래 kebab-case 값으로 기록한다. 같은 값이라도 `type`과 함께 해석한다.

| 문서 유형 | 허용 lifecycle | authority와 사용 규칙 |
|---|---|---|
| `index`, `project-context`, `profile-catalog`, `governance`, `catalog`, `coverage-matrix` | `active`, `superseded`, `deprecated` | `active`만 현재 탐색·작성 규칙으로 사용한다. |
| `reference-architecture`, `project-blueprint` | `proposed`, `accepted`, `superseded`, `deprecated` | proposal과 승인된 결정을 구분하며 최신 accepted Decision이 우선한다. |
| `ArchitectureDecision` | `proposed`, `accepted`, `rejected`, `deferred`, `superseded`, `deprecated` | `superseded`면 `superseded_by`로 대체 결정을 연결한다. |
| `tool-profile` | `observed`, `superseded`, `deprecated` | `observed`는 고정 ToolVersion 분석이며 current upstream 또는 runtime 성공을 뜻하지 않는다. |
| `execution-record` | `historical-snapshot` | 기록된 run의 명령·환경·결과에만 authoritative하며 현재 정책·아키텍처 규칙이 아니다. |

`superseded`에는 `superseded_by`를 필수로 둔다. 역사 문서는 삭제하거나 현재형으로 고치지 않고 새 문서와 관계를 추가한다. 현재 규칙과 과거 실행 기록이 충돌하면 active governance, 최신 accepted Decision, fixed ToolVersion의 Claim/Evidence 순위를 먼저 적용하고 실행 기록은 당시 관찰의 증거로만 사용한다.

## 서로 독립적인 증거 축

### 기능 검증 `V0~V6`

| 등급 | 의미 | 필요한 최소 근거 |
|---|---|---|
| `V0` | 미확인 | 출처나 재현 가능한 관찰이 없음 |
| `V1` | 문서 확인 | 공식 문서·README·서비스 설명의 Claim |
| `V2` | 고정 SHA 정적 확인 | immutable source/config/test를 읽고 Claim과 locator를 연결 |
| `V3` | build 확인 | 고정 버전, 명시 환경과 명령에서 build 결과·로그 보존 |
| `V4` | 통제 runtime 확인 | 고정 입력과 환경에서 실제 프로세스/API 동작을 관찰 |
| `V5` | E2E 또는 failure injection | 실제 연결 흐름, 취소·재시작·오류·보안 gate까지 검증 |
| `V6` | 운영 확인 | 기간·SLO·배포 범위가 명시된 production 관찰 |

상위 등급은 이전 결과를 지우지 않는다. Claim마다 가장 높은 유효 evidence와 실패/제약을 함께 보여준다. build 성공만으로 runtime을, E2E 성공만으로 장기 운영을 추정하지 않는다.

### 출처 무결성 `I0~I2`

| 등급 | 의미 |
|---|---|
| `I0` | upstream 공식성·버전 무결성을 확인하지 않음 |
| `I1` | 공식 upstream 또는 공식 배포 출처를 확인 |
| `I2` | 공식 출처와 immutable SHA/tag/digest를 고정하고 gitlink/checksum 등으로 무결성을 확인 |

`I2`는 “무엇을 읽었는지”를 확정할 뿐 기능이 작동함을 증명하지 않는다.

### 플랫폼별 증거 `P0~P3`

| 등급 | 의미 |
|---|---|
| `P0` | 해당 플랫폼 지원이 문서 주장·간접 경로이거나 미확인; 플랫폼별 immutable 구현 근거와 실행 artifact가 없음 |
| `P1` | 해당 플랫폼의 전용 또는 명시적으로 portable한 code/config/test path를 고정 소스에서 정적으로 확인 |
| `P2` | 명시한 OS/edition·distribution/version/architecture 환경에서 build 또는 runtime을 실제 수행하고 명령·결과·artifact를 보존 |
| `P3` | 해당 플랫폼 회귀 suite가 반복 실행되며 process tree/signal, path·case·symlink, newline·permission 등 플랫폼 failure boundary를 포함 |

`P0~P3`은 `windows`, `linux` 등 플랫폼마다 별도로 기록하고 `pass|fail|partial|unknown` 결과를 함께 둔다. `P2`가 build인지 runtime인지는 기능 축 `V3/V4`가 구분하며, 플랫폼 등급만으로 기능 등급을 추정하지 않는다. host OS, guest OS와 control client도 분리해 WSL·container·remote Linux를 Windows native 또는 Linux host-native 증거로 바꾸어 쓰지 않는다.

기존 ToolVersion 프로필의 `W0~W3`은 조사 당시 Windows 전용 evidence axis로 보존한다. 의미는 각각 `platform=windows`의 `P0~P3`에 대응하지만, 이관 시 원본 값과 변환 시점을 기록하며 기존 분석을 일괄 덮어쓰지 않는다. Linux에는 legacy 값을 복제하지 않고 새로운 source 또는 실행 artifact로 판정한다.

## Claim과 Evidence 예시

```text
tool_version:orca@e7b8526
  --PROVIDES {grade: V2, origin: I2, platforms: {windows: P0, linux: P0}}
  --> capability:structured-orchestration

tool_version:agentapi@9ff117e
  --SUPPORTS {grade: V2, confidence: low, limitations: [pty-heuristic]}
  --> integration:pty-screen

roadmap:phase1-local-kernel
  --IMPLEMENTS--> capability:windows-conpty

evidence:e2b-pilot-001
  --SUPPORTS {grade: V4, result: pass}
  --> claim:e2b-resume-contract
```

마지막 예시는 향후 실제 실행 뒤에만 생성할 수 있다. 현재 저장소에는 해당 `V4` evidence가 없다.

## Markdown source of truth

초기에는 사람이 리뷰 가능한 Markdown을 source of truth로 사용한다.

source-of-truth 우선순위는 다음과 같다.

1. `.gitmodules` URL, parent index의 mode `160000` gitlink와 official fixed-SHA permalink가 immutable identity와 정적 근거다.
2. `knowledge-base/tools/<tool_key>.md`가 해당 ToolVersion의 현재 합성 프로필이다.
3. `tools/catalog.md`와 coverage matrix는 프로필을 찾아가는 파생 인덱스다.
4. `planning/REPOSITORY_GITHUB_ANALYSIS.md` 같은 기존 분석은 역사적 secondary snapshot이다. underlying fixed locator를 다시 연결하지 않으면 그 문구만으로 `V2`를 부여하지 않는다.

조사일의 공식 default branch HEAD, maintenance 상태와 서비스 문서는 시변 `V1` 관찰이다. 분석한 fixed SHA와 별도 필드로 기록하며 upstream이 이동해도 기존 ToolVersion을 덮어쓰지 않는다. 조사 작업 트리에서 submodule 본문을 읽지 못하고 official GitHub fixed-SHA tree/API만 사용했다면 그 수집 경로와 local build/runtime 미수행을 `provenance limitation`에 명시한다.

- 도구 프로필은 [템플릿](./templates/tool-profile.md)의 frontmatter와 섹션 순서를 따른다.
- 내부 링크는 repository-relative Markdown link를 사용해 Obsidian과 GitHub 모두에서 연다.
- ToolVersion에는 full SHA/tag/digest와 조사일을 반드시 기록한다.
- Claim에는 source locator와 `I/V`, OS별 `P`를 기록하고 미실행 항목은 빈 evidence 또는 `unknown`으로 표시한다. `V2` Claim은 40자리 SHA를 포함한 파일 permalink와 가능한 가장 좁은 line/heading anchor가 필요하다.
- 역사 자료를 삭제하거나 현재 상태로 덮어쓰지 않는다. 새 ToolVersion과 `SUPERSEDES`를 추가하고 이전 Claim은 `stale`로 표시한다.
- 생성 파일을 도입하면 Markdown → JSON 변환은 결정론적이어야 하며 생성 JSON은 수동 편집하지 않는다.

### 도구 선택·fallback 제약

신규 또는 구조를 갱신하는 ToolVersion 프로필은 템플릿의 `실행 선택 제약` 표에 다음 항목을 기록한다.

- runtime과 prerequisite: OS/host·guest, runtime/version, 설치·credential·network·service 의존성
- supported protocol/surface: CLI, REST, WebSocket, MCP 등과 실제로 확인한 고정 버전 범위
- rate limit과 timeout: fixed source 설정인지 시변 외부 서비스 관찰인지 구분하고, 시변 값에는 source·관찰 시각·TTL을 둔다.
- fallback candidate: 전환 조건, 잃는 capability·evidence·security property, 추가 승인·credential·비용 조건

fallback은 후보 관계일 뿐 자동 실행 권한이 아니다. 대체가 external write, credential audience, 데이터 경계, 비용, 검증 등급을 바꾸면 새 capability/policy 협상과 필요한 사람 승인을 거쳐야 한다. `unknown` 한도나 미검증 대체재를 안전한 기본값으로 해석하지 않는다.

## 새 도구 또는 새 버전 추가 절차

1. **공식성 확인**: 제품 사이트, 조직, updater metadata 등으로 공식 upstream을 확인해 `I1`을 만든다.
2. **license gate**: root와 component license/NOTICE/rider를 읽는다. 사용·분석 제한이 있으면 clone·분석·게시를 중단하고 이유만 기록한다.
3. **소스 보존 방식 결정**: official upstream, license/activity, 예상 설계 영향, clone 크기·비용을 기록한다. adapter·reference implementation·핵심 설계에 직접 영향을 주면 official upstream + fixed SHA gitlink submodule을 기본으로 하고, 비교·시장·문서 조사면 versioned manifest + source URL + Claim/Evidence를 기본으로 한다. 필요할 때만 shallow clone 또는 remote fixed-SHA inspection을 수행한다.
4. **immutable pin**: tag가 아니라 실제 commit SHA/image digest/API revision을 확보한다. submodule이면 gitlink·`.gitmodules`·checkout SHA 일치로 `I2`를 만든다. manifest-only면 공식 immutable URL과 checksum/commit API 등 재현 가능한 pin을 남기고 충족한 범위에서만 `I2`를 부여한다.
5. **프로필 생성**: [도구 프로필 템플릿](./templates/tool-profile.md)을 복사해 Tool과 ToolVersion, 역할, Integration, Windows/Linux 플랫폼 상태, `Borrow/Adapt/Avoid/Build`를 기록한다.
6. **Claim 분해**: “지원한다”를 기능·한계·platform·surface별 Claim으로 나누고 각 Claim에 공식 permalink나 repo-relative source locator를 붙인다.
7. **정적 검토**: 문서만이면 `V1`, 고정 source/config/test 확인까지 했으면 Claim별 `V2`로 기록한다. 플랫폼별 전용 또는 명시적으로 portable한 fixed-SHA path가 있을 때만 해당 OS에 `P1`을 주고 다른 OS로 복제하지 않는다.
8. **카탈로그 연결**: [도구 카탈로그](./tools/catalog.md)의 역할군과 도입 판단을 갱신하고 청사진의 선택·평가·보류 관계에 연결한다.
9. **검증 계획**: build는 `V3`, runtime은 `V4`, E2E/failure injection은 `V5`로 별도 RoadmapItem과 acceptance를 만든다. 실행하지 않은 단계는 pass로 기록하지 않는다.
10. **정적 gate**: 중복 ID, 깨진 상대 링크, SHA mismatch, license 누락, 출처 없는 Claim, artifact 없는 grade 승격, stale 조사일을 검사한다.
11. **리뷰와 commit**: diff를 검토하고 관련 파일만 명시적으로 stage한다. 자동 수집은 provenance를 추가할 수 있지만 등급 승격에는 artifact gate와 사람 리뷰가 필요하다.
12. **저장소 정적 gate**: `python3 scripts/validate_knowledge_base.py`로 frontmatter, lifecycle status, 중복 ID와 상대 링크를 검사하고 명령·exit를 execution record에 남긴다.

### 하이브리드 소스 운영 경계

- 위 정책은 미래 신규 대상의 등록 원칙이다. 현재 34개 fixed-SHA submodule을 자동 제거하거나 재분류하지 않는다.
- submodule 작업트리가 비어 있어도 부모 `.gitmodules`와 `git ls-tree <parent>:multi-agent-tools`로 URL과 gitlink SHA를 확인할 수 있다. 본문 Claim은 official upstream의 fixed-SHA `tree`/`blob` URL로 연결한다.
- 부모 GitHub 저장소의 submodule 내부 경로 deep link는 소스 근거로 사용하지 않는다. checkout 상태에 따라 열리지 않으며 official upstream provenance도 흐린다.
- `ToolVersion`, `CurrentUpstreamObservation`, `AnalysisSnapshot`은 각각 갱신한다. “현재 active/archived”, “fixed version”, “분석 당시 판단”을 한 필드로 합치지 않는다.

## 단계적 확장

1. 현재: Markdown profile과 catalog를 사람이 리뷰한다.
2. 다음: JSON Schema v1로 Tool/ToolVersion/Claim/Evidence/Edge를 검사하고 `catalog.json`, `claims.jsonl`, `edges.jsonl`을 생성한다. Evidence는 append-only다.
3. CI: ID·link·SHA·license·grade gate와 Markdown/JSON drift를 차단한다.
4. 조회: SQLite 또는 DuckDB FTS와 coverage matrix로 미검증 항목을 관리한다.
5. 확장: 다중 hop 질의와 impact 분석이 필요할 때 property graph 또는 RDF/SHACL로 import한다. Markdown/JSON은 계속 source of truth다.

property graph와 RDF/SHACL 중 장기 표현은 아직 결정하지 않는다. 초기 공통 기반인 Markdown + JSON Schema + JSONL이 안정된 뒤 실제 질의 요구로 선택한다.

## 상세 프로필 acceptance gate

1. `.gitmodules` path, mode `160000` gitlink, catalog `tool_key`, profile `tool_key`가 34개 일대일이고 URL·full SHA가 일치한다.
2. 목적, 공식 최신 관찰, license/NOTICE, 기술 구조, Claim, interface/protocol, trust boundary, 플랫폼, 강점·한계, 도입 판단과 다음 검증 섹션이 비어 있지 않다.
3. capability, interface, trust/security, platform, limitation Claim이 각각 근거를 가지며 각 Claim의 `I/V/W`를 독립 판정한다.
4. 실행 명령·exit, environment fingerprint와 보존 artifact가 모두 없으면 `V3+` 또는 플랫폼별 `P2+`로 승격하지 않는다. upstream CI, test 파일 존재, UI 상태와 agent 자기보고도 같은 제한을 받는다.
5. 도입 판단은 Claim ID, license/trust/platform blocker와 재검토 gate를 참조한다.
6. 미검증 adoption-critical Claim마다 목표 등급, 환경, 시나리오, pass 기준, artifact와 승인 조건이 있는 다음 검증 항목을 둔다.
7. 중복 ID, 깨진 상대 링크, moving-branch `V2` URL, catalog/profile 역링크, frontmatter enum/date와 SHA drift를 정적 검사한다.
8. cross-platform profile은 최소한 `windows`와 `linux` 각각의 `P` grade, result, host/guest scope와 limitation을 가진다. `P1+`에는 OS별 source가, `P2+`에는 environment fingerprint와 실행 artifact가 있어야 하며 한 OS의 값을 다른 OS로 복제하지 않는다.
9. 신규 또는 구조를 갱신한 프로필은 runtime/prerequisite, protocol, rate-limit/timeout의 source·시점, fallback의 capability loss와 승인 조건을 기록한다. 값이 없거나 확인하지 못했으면 추정하지 않고 `unknown`으로 둔다.
