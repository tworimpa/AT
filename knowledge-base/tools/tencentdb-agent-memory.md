---
id: tool-tencentdb-agent-memory
type: tool-profile
title: TencentDB Agent Memory
status: observed
profile_schema_version: 3
tool_key: tencentdb-agent-memory
tool_version_id: tool-version:tencentdb-agent-memory@9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2
tags: [knowledge-base, tool, agent-memory, knowledge-plane]
official_upstream: https://github.com/TencentCloud/TencentDB-Agent-Memory
license: MIT
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: feat/server_team
upstream_head_observed: 9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P1
version_kind: commit
version_ref: 9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2
parent_repo_head: e0ebf2e5c2e3cefea119119228b9fc02ad83ac01
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# TencentDB Agent Memory

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

대화·작업·문서·코드를 계층형 Memory, Skill, Wiki, CodeGraph 자산으로 정제하고 팀·사용자·Agent 단위로 공유·장착하는 별도 memory/knowledge control plane이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/TencentCloud/TencentDB-Agent-Memory |
| 기본 브랜치와 조사일 HEAD | `feat/server_team` / `9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2` (2026-08-15) |
| 고정 버전 | `9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2` |
| pin과 최신 관찰 관계 | 조사 시점 HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; `/tmp` shallow clone으로 fixed SHA를 읽고 official permalink를 보존 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: Tencent Cloud verified GitHub 조직의 official upstream과 `git ls-remote --symref` HEAD를 확인하고 clone HEAD가 일치함 |
| 플랫폼 증거 | Windows `P0/unknown`; Linux `P1/partial` — Dockerfile·shell 배포 경로만 정적으로 확인, host-native runtime은 미실행 |
| license | [fixed-SHA LICENSE](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/LICENSE): MIT; 유래 component와 dependency license 전수 검토는 미수행 |
| provenance limitation | shallow clone의 문서·source/config/test를 정적으로 읽음; install/build/runtime, 실제 LLM·Redis·COS·TCVDB, Windows/Linux native 실행은 미수행 |
| source 관리 | `manifest-only`: 현재는 비교·설계 지식 대상이다. adapter/reference 구현을 직접 채택하기로 결정할 때 gitlink 전환을 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| MemoryCore | L0 conversation, L1 atom, L2 scenario, L3 profile과 Skill·팀·Agent·ACL metadata | HTTP gateway가 저장·검색·비동기 정제 파이프라인을 노출 | [MemoryCore README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryCore/README.md#architecture) |
| MemoryKnowledge | Wiki/CodeGraph content ingest, index, search와 tool discovery | `service_id`·`team_id`로 scope하고 async ingest 뒤 BM25/index를 생성 | [OpenAPI](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryKnowledge/openapi.yaml#L1-L16) |
| MemoryProxy | OpenAI/Anthropic 요청 앞에서 auth, memory injection, write-back, upstream forwarding | user key 검증 → session binding → 주입 → LLM → 비동기 추출·관측 | [Proxy request pipeline](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryProxy/README.md#request-pipeline) |
| MemoryPanel | 팀·Agent·asset·visibility·binding 관리 UI | 사람이 ownership/version/status/ACL과 Agent loadout을 관리 | [root README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/README.md#memory-hub-is-not-a-display-board--its-a-control-panel) |

## 역할과 연동

- AgentRole: Knowledge Curator, Memory Service, Policy/Metadata Manager; Agent executor나 scheduler는 아님.
- Capability: `layered-agent-memory`, `skill-asset-registry`, `wiki-codegraph-ingestion`, `memory-asset-binding`, `tenant-scoped-retrieval`, `prompt-context-injection`.
- Integration: HTTP v2/v3, OpenAI-compatible API, Anthropic Messages API, TypeScript/Python SDK, OpenClaw/Hermes adapter, `/v3/tools/list`·`/v3/tools/call`.
- SecurityOperationalRequirement: `AX-D002` data classification/retention, `AX-D003` RBAC/ownership, `AX-D004` egress, `AX-D005` secret broker, `AX-D008` deletion/audit가 결정되기 전 production 적합성은 unknown.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `tdam-c1-layered-memory` | architecture | MemoryCore는 L0 conversation, L1 atom, L2 scenario, L3 profile을 별도 계층으로 저장·검색한다. | [README](https://github.com/TencentCloud/TencentDB-Agent-Memory#technical-implementation), 2026-08-15 | [MemoryCore README lines 3–20](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryCore/README.md#L3-L20) | `I2` | `V2` | `windows:P0; linux:P1` | 구조·API 정적 확인; 정제 정확도와 durability 미검증 |
| `tdam-c2-asset-plane` | capability | Memory, Skill, Wiki, CodeGraph를 ownership/version/status/visibility/binding을 가진 팀 자산으로 다룬다. | [README](https://github.com/TencentCloud/TencentDB-Agent-Memory#memory-hub-is-not-a-display-board--its-a-control-panel), 2026-08-15 | [root README lines 305–316](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/README.md#L305-L316) | `I2` | `V2` | `windows:P0; linux:P1` | 데이터 모델·UI 주장 확인; ACL failure test 없음 |
| `tdam-c3-tenant-scope` | security | Knowledge API는 header의 `service_id`와 body의 `team_id`를 tenant/resource scope로 사용한다. | 없음 | [OpenAPI lines 10–16](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryKnowledge/openapi.yaml#L10-L16), [api helper](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryKnowledge/src/api-helpers.ts#L11-L67) | `I2` | `V2` | `windows:P0; linux:P1` | scope validation code 확인; cross-tenant runtime과 auth-disabled 경계 미검증 |
| `tdam-c4-proxy-auth-injection` | interface | Proxy는 user key를 Core에서 검증해 identity를 얻고 memory/skill/knowledge를 prompt 또는 tool로 제공한다. | [README](https://github.com/TencentCloud/TencentDB-Agent-Memory#technical-implementation), 2026-08-15 | [Proxy README lines 25–53](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryProxy/README.md#L25-L53) | `I2` | `V2` | `windows:P0; linux:P1` | secret 비노출·권한 enforcement runtime 미검증 |
| `tdam-c5-async-lifecycle` | limitation | Wiki ingest는 `pending`을 즉시 반환하며 delete는 in-flight job에 중단 신호 후 다음 checkpoint에서 정리한다. | 없음 | [OpenAPI lines 148–192](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryKnowledge/openapi.yaml#L148-L192) | `I2` | `V2` | `windows:P0; linux:P1` | 완료·삭제 증거와 generation fencing 미검증 |
| `tdam-c6-storage-degrade` | limitation | Proxy storage 초기화 실패 시 `cos → sqlite → fs → memory`로 자동 강등한다. | 없음 | [Proxy README lines 240–253](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryProxy/README.md#L240-L253) | `I2` | `V2` | `windows:P0; linux:P1` | health에 effective backend를 노출하지만 production에서 fail-open 위험 |
| `tdam-c7-retention` | limitation | local cleanup은 retentionDays 설정 때만 켜지고 Proxy `nottl` 상태는 영구 보존된다. | 없음 | [MemoryCore index](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryCore/index.ts#L326-L343), [Proxy README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryProxy/README.md#L244-L251) | `I2` | `V2` | `windows:P0; linux:P1` | end-to-end retention·backup/derived index 삭제 증거 unknown |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| MemoryCore Gateway | HTTP JSON v2/v3 | adapter/SDK → memory/meta/skill | service/user key와 team/user/agent identity | [MemoryCore API](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryCore/README.md#http-api) |
| Knowledge tools | HTTP JSON `/v3/tools/list`, `/v3/tools/call` | Agent가 discovery 후 Wiki/CodeGraph 조회 | `x-tdai-service-id` + team scope | [Knowledge README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryKnowledge/README.md#api-overview) |
| LLM Proxy | OpenAI Chat Completions, Anthropic Messages | client → auth/inject/forward → LLM → async write-back | user key, system-user bypass, admin shared secret | [Proxy endpoints](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2/MemoryProxy/README.md#main-http-endpoints) |

## 운영·보안·trust boundary

- 보호 자산과 authority: 원문 conversation, 추출 memory/persona, source document/code, membership·ACL·Agent binding, LLM/storage credential, prompt injection/write-back 권한.
- Core, Knowledge, Proxy, Panel과 upstream LLM/embedding, Redis/COS/SQLite/TCVDB를 별도 trust domain으로 본다. identity가 인증 principal에서 파생되는지, auth-disabled 경로가 scope를 우회하지 않는지 검증해야 한다.
- memory/skill은 장기적으로 행동을 바꾸므로 provenance, review, version, revoke, poisoning quarantine와 적용 snapshot이 필요하다. storage 자동 강등은 production에서 fail-closed policy로 대체해야 한다.
- README benchmark/privacy, UI status, upstream test는 정확도·격리·완료 증거가 아니다.

## 플랫폼

- Linux `P1/partial`: Linux container image와 shell 배포 경로만 확인했으며 build/runtime하지 않았다.
- Windows `P0/unknown`: portable Node/TypeScript라는 이유로 native 지원을 추정하지 않는다. Windows CI/native artifact를 확인하지 못했다.
- Docker/remote Linux 실행은 Windows native evidence로 승격하지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `tdam-v2-source-20260815` | `V2` | `9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2` | `git ls-remote --symref`; shallow clone; `rg`/source inspection, exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; git 2.53.0 | official pin, MIT license, architecture/interface/limitations 확인 | 이 프로필 fixed-SHA URL | `tdam-c1`~`tdam-c7` | dependency·build·runtime 미실행; WSL은 Windows native evidence가 아님 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: memory를 prompt blob이 아니라 계층·asset·binding·ACL·tool discovery가 있는 독립 plane으로 모델링한다(`tdam-c1`, `tdam-c2`, `tdam-c4`).
- 확인된 한계: async 취소/완료 fencing이 불명확하고(`tdam-c5`), storage 강등은 durability/security 경계를 낮출 수 있으며(`tdam-c6`), retention이 구성에 의존한다(`tdam-c7`).
- 미확인·추론: benchmark, extraction 품질, ACL bypass 저항, poisoning/revoke 전파, 완전 삭제, Windows native, multi-node consistency는 unknown.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | conversation → atom → scenario/profile 계층화와 asset metadata/binding 분리 | `tdam-c1`, `tdam-c2` | 반복 설명 감소와 provenance 있는 팀 지식 재사용 |
| Adapt | fixed binding + ACL + on-demand tool retrieval을 사내 RBAC/ABAC·data classification·approval에 연결 | `tdam-c2`, `tdam-c3`, `tdam-c4` | `AX-D002`, `AX-D003`, `AX-D005` 결정과 identity 검증 |
| Avoid | 더 약한 persistence로 자동 강등하거나 API status를 완료·삭제 증거로 간주 | `tdam-c5`, `tdam-c6`, `tdam-c7` | production은 fail-closed, generation fence, deletion receipt 필요 |
| Build | immutable source/revision, extraction provenance, review/revoke, poisoning quarantine, retention cascade를 가진 internal memory plane contract | `tdam-c1`~`tdam-c7` | `AD-PROP-011` 후보와 `RM-K2-memory-plane-evaluation` |

## 도입 판단

- 결정: 파일럿
- 성격: 사내 AX reference architecture용 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: memory/knowledge plane 계약과 asset governance 비교; 현재 제품 직접 통합은 결정하지 않음.
- 이유: 팀 memory 모델은 설계 영향이 크지만 정적 `V2`, Linux `P1`, Windows `P0`이고 storage/retention/ACL failure boundary가 미검증이다.
- 재검토 조건: 회사 data/retention/RBAC 결정, component license inventory, V3 build, V4 tenant/ACL runtime, V5 poisoning·revoke·delete·backend failure injection.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `tdam-test-build-linux` | `tdam-c1`~`c4` | `V3/linux:P2` | approved Linux x86_64 host | fixed SHA build + unit tests | reproducible build/test exit 0 | SBOM, logs, image digest | network·비용 승인 |
| `tdam-test-tenant-failure` | `tdam-c3`, `c4` | `V5/linux:P2` | isolated two-tenant fixture | ID 변조, revoked key, system-user/admin, prompt/tool ACL bypass | cross-tenant read/write deny와 audit | traces/audit log | synthetic data·security review |
| `tdam-test-lifecycle` | `tdam-c5`~`c7` | `V5/linux:P2` | SQLite와 production 후보 backend | ingest 중 delete, crash, outage, retention, cascade | stale write 차단, fail-closed, 파생물 삭제 receipt | DB diff/logs/receipt | `AX-D002`, `AX-D008` |
| `tdam-test-windows` | adoption-critical Claims | `V3/windows:P2` | 결정될 Windows native host | build/start/API smoke와 path/process/credential fixture | Linux contract와 동일 결과 | fingerprint/logs | `AX-D011` |

## 관계

- `Tool HAS_VERSION tool-version:tencentdb-agent-memory@9059e52d11b7e66c2a3b5eb6161e4b4b8603c8c2`
- `ToolVersion FITS_ROLE KnowledgeCurator/MemoryService/PolicyMetadataManager`
- `ToolVersion PROVIDES layered-agent-memory/skill-asset-registry/wiki-codegraph-ingestion/tenant-scoped-retrieval`
- `ToolVersion SUPPORTS HTTP/OpenAI-compatible/Anthropic-Messages/SDK`
- `Project EVALUATES ToolVersion` as memory/knowledge plane pilot reference

## 변경 이력

- 2026-08-15: official HEAD를 manifest-only immutable pin으로 등록하고 fixed-SHA `V2`, Windows `P0`, Linux `P1` 분석을 추가함.
