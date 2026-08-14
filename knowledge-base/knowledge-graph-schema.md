---
id: knowledge-graph-schema-v1
type: governance
title: 지식 베이스 작성 규칙과 최소 지식 그래프 스키마
status: active
schema_version: 1
tags:
  - knowledge-base
  - knowledge-graph
  - provenance
  - evidence
observed_at: 2026-08-14
source_parent_commit: 4e6731a1b274eba5a8451b97594aadcf570108ee
---

# 지식 베이스 작성 규칙과 최소 지식 그래프 스키마

[지식 베이스 홈](./index.md) · [33개 도구 카탈로그](./tools/catalog.md) · [플랫폼 청사진](./platform-blueprint.md) · [도구 프로필 템플릿](./templates/tool-profile.md)

## 원칙

1. `Tool`과 immutable `ToolVersion`을 분리한다. 새 upstream HEAD가 나타나도 이전 지식을 덮어쓰지 않는다.
2. 기능과 한계는 단순 속성이 아니라 검증 가능한 `Claim`으로 기록한다.
3. Claim마다 `SourceArtifact`와 가능한 경우 `Evidence`를 연결한다.
4. provenance와 검증 등급은 node뿐 아니라 edge에도 둔다. 같은 ToolVersion의 ACP, Windows, runtime 주장은 각각 다른 근거와 등급을 가질 수 있다.
5. 정적 코드 `V2`를 build/runtime/E2E `V3~V5`로 자동 승격하지 않는다.
6. 실패와 반증 evidence를 삭제하지 않고 `unknown`, `partial`, `fail`을 구분한다.
7. secret 원문, credential handle 내부값과 private endpoint는 지식 베이스에 저장하지 않는다.
8. 외부 서비스 가격·한도·상태는 TTL이 있는 관찰값으로 두고 코드·설계 사실과 분리한다.

## 최소 엔터티

| 엔터티 | 목적 | 필수 식별 정보 |
|---|---|---|
| Tool | 지속되는 제품·저장소·서비스 | `id`, 공식 upstream, license, maintenance status |
| ToolVersion | 조사한 immutable 버전 | parent Tool, `version_kind`, SHA/tag/digest/API revision, observed date |
| Capability | 정규화된 기능 | 예: task DAG, atomic claim, ConPTY, worktree, verifier, snapshot |
| AgentRole | 권한이 분리된 역할 | Planner, Scheduler, Worker, Verifier, Reviewer, Merger, Watchdog, Executor, Relay, Policy, Gateway, Spec/Memory |
| Integration | protocol·adapter·state interface | ACP, MCP, JSON-RPC, CLI, PTY, HTTP/SSE, WebSocket, GitHub, SQLite |
| SecurityOperationalRequirement | 보안·운영 조건 | isolation, secret audience/redaction, egress, retention, readiness, fencing, recovery, cost/SLO |
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
| `ToolVersion PROVIDES Capability` | 특정 버전의 기능 Claim이 있는 관계 |
| `ToolVersion SUPPORTS Integration` | protocol/adapter 지원 Claim |
| `ToolVersion FITS_ROLE AgentRole` | 역할에 적합하다는 판단 |
| `AgentRole REQUIRES Capability` | 역할 수행에 필요한 기능 |
| `Integration CONNECTS ToolVersion/Executor` | 연결 가능한 runtime 또는 executor |
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

각 edge에도 `claim_id`, `source_ids`, `evidence_ids`, `grade`, `confidence`, `observed_at`을 둘 수 있어야 한다.

## 공통 필드

모든 node와 edge는 가능한 범위에서 다음 필드를 가진다.

```yaml
id: tool-version-orca-e7b8526
type: ToolVersion
name: Orca e7b8526
status: observed
tags: [control-plane, windows-first]
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
  platform_scope: windows-source-paths
  environment_fingerprint: null
  confidence: medium
  limitations: dependencies not installed; build and runtime not executed
version:
  version_kind: commit
  version_ref: e7b85266f531f9a219dff59d8647f86585b4fc7e
  parent_repo_head: 4e6731a1b274eba5a8451b97594aadcf570108ee
```

Markdown frontmatter에는 자주 탐색하는 scalar와 tag만 두고, 상세 Claim/Evidence가 늘어나면 결정론적으로 생성하는 JSON/JSONL로 분리한다.

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

### Windows 증거 `W0~W3`

| 등급 | 의미 |
|---|---|
| `W0` | 문서 주장, 간접 지원 또는 미확인; Windows 전용 구현 근거 없음 |
| `W1` | Windows code/config/path를 고정 소스에서 정적으로 확인 |
| `W2` | 명시한 Windows 환경에서 실제 build/runtime를 수행하고 evidence 보존 |
| `W3` | Windows 회귀 suite가 반복 실행되며 process tree, CRLF, long path 등 실패 경계를 포함 |

Windows에서 remote API를 호출할 수 있다는 사실과 remote Linux sandbox 자체가 Windows runtime이라는 주장을 구분한다.

## Claim과 Evidence 예시

```text
tool_version:orca@e7b8526
  --PROVIDES {grade: V2, origin: I2, windows: W1}
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

- 도구 프로필은 [템플릿](./templates/tool-profile.md)의 frontmatter와 섹션 순서를 따른다.
- 내부 링크는 repository-relative Markdown link를 사용해 Obsidian과 GitHub 모두에서 연다.
- ToolVersion에는 full SHA/tag/digest와 조사일을 반드시 기록한다.
- Claim에는 source locator와 `V/I/W`를 기록하고 미실행 항목은 빈 evidence 또는 `unknown`으로 표시한다.
- 역사 자료를 삭제하거나 현재 상태로 덮어쓰지 않는다. 새 ToolVersion과 `SUPERSEDES`를 추가하고 이전 Claim은 `stale`로 표시한다.
- 생성 파일을 도입하면 Markdown → JSON 변환은 결정론적이어야 하며 생성 JSON은 수동 편집하지 않는다.

## 새 도구 또는 새 버전 추가 절차

1. **공식성 확인**: 제품 사이트, 조직, updater metadata 등으로 공식 upstream을 확인해 `I1`을 만든다.
2. **license gate**: root와 component license/NOTICE/rider를 읽는다. 사용·분석 제한이 있으면 clone·분석·게시를 중단하고 이유만 기록한다.
3. **immutable pin**: tag가 아니라 실제 commit SHA/image digest/API revision을 확보한다. submodule이면 gitlink·`.gitmodules`·checkout SHA 일치로 `I2`를 만든다.
4. **프로필 생성**: [도구 프로필 템플릿](./templates/tool-profile.md)을 복사해 Tool과 ToolVersion, 역할, Integration, Windows 상태, 도입 판단을 기록한다.
5. **Claim 분해**: “지원한다”를 기능·한계·platform·surface별 Claim으로 나누고 각 Claim에 공식 permalink나 repo-relative source locator를 붙인다.
6. **정적 검토**: 문서만이면 `V1`, 고정 source/config/test 확인까지 했으면 Claim별 `V2`로 기록한다. Windows 전용 code path가 있을 때만 `W1`을 준다.
7. **카탈로그 연결**: [도구 카탈로그](./tools/catalog.md)의 역할군과 도입 판단을 갱신하고 청사진의 선택·평가·보류 관계에 연결한다.
8. **검증 계획**: build는 `V3`, runtime은 `V4`, E2E/failure injection은 `V5`로 별도 RoadmapItem과 acceptance를 만든다. 실행하지 않은 단계는 pass로 기록하지 않는다.
9. **정적 gate**: 중복 ID, 깨진 상대 링크, SHA mismatch, license 누락, 출처 없는 Claim, artifact 없는 grade 승격, stale 조사일을 검사한다.
10. **리뷰와 commit**: diff를 검토하고 관련 파일만 명시적으로 stage한다. 자동 수집은 provenance를 추가할 수 있지만 등급 승격에는 artifact gate와 사람 리뷰가 필요하다.

## 단계적 확장

1. 현재: Markdown profile과 catalog를 사람이 리뷰한다.
2. 다음: JSON Schema v1로 Tool/ToolVersion/Claim/Evidence/Edge를 검사하고 `catalog.json`, `claims.jsonl`, `edges.jsonl`을 생성한다. Evidence는 append-only다.
3. CI: ID·link·SHA·license·grade gate와 Markdown/JSON drift를 차단한다.
4. 조회: SQLite 또는 DuckDB FTS와 coverage matrix로 미검증 항목을 관리한다.
5. 확장: 다중 hop 질의와 impact 분석이 필요할 때 property graph 또는 RDF/SHACL로 import한다. Markdown/JSON은 계속 source of truth다.

property graph와 RDF/SHACL 중 장기 표현은 아직 결정하지 않는다. 초기 공통 기반인 Markdown + JSON Schema + JSONL이 안정된 뒤 실제 질의 요구로 선택한다.
