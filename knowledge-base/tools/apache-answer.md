---
id: tool-apache-answer
type: tool-profile
title: Apache Answer
status: observed
profile_schema_version: 3
tool_key: apache-answer
tool_version_id: tool-version:apache-answer@3b9f1370612e690a0b7f230f05e688930db4c6d3
tags:
  - knowledge-base
  - tool
  - knowledge-portal
official_upstream: https://github.com/apache/answer
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-21
upstream_default_branch: main
upstream_head_observed: 3b9f1370612e690a0b7f230f05e688930db4c6d3
upstream_checked_at: 2026-08-21
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P1
version_kind: commit
version_ref: 3b9f1370612e690a0b7f230f05e688930db4c6d3
parent_repo_head: 42f4f2d6a0b07bcb28cb782ac89ca6210f06abde
source_management: manifest-only
analysis_snapshot_date: 2026-08-21
---

# Apache Answer

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

사람이 축적·검토하는 Q&A 지식을 Web/API/MCP/AI chat으로 제공하고 search·vector search를 plugin으로 확장하는 self-hosted knowledge portal이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/apache/answer |
| 기본 브랜치와 조사일 HEAD | `main` / `3b9f1370612e690a0b7f230f05e688930db4c6d3` (2026-08-21) |
| 고정 버전 | `3b9f1370612e690a0b7f230f05e688930db4c6d3` |
| pin과 최신 관찰 관계 | 조사 시 default HEAD와 동일; repository `pushed_at`은 다른 ref 활동을 포함할 수 있어 fixed version과 분리 |
| 로컬 gitlink 또는 artifact | gitlink 없음; 임시 shallow clone으로 fixed source를 정적 검사하고 locator를 보존 |
| 조사일 | 2026-08-21 |
| 출처 무결성 | `I2`: GitHub branch API, `git ls-remote`, shallow clone HEAD가 동일 |
| 플랫폼 증거 | Windows `P0/unknown`; Linux `P1/partial`: Docker/Helm과 Go server path를 정적 확인. native/container runtime 미수행 |
| license | fixed [`LICENSE`](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/LICENSE#L1-L202) Apache-2.0, [`NOTICE`](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/NOTICE#L1-L7) 확인 |
| provenance limitation | README, Go module, plugin interfaces, MCP/auth, AI/tool loop, config를 정적으로 읽음. frontend/build/plugin/model/database/runtime 미실행 |
| source 관리 | `manifest-only`: knowledge portal 비교·설계 대상이며 GitHub source size 약 15.8 MB. 직접 connector/plugin 구현을 차용할 때 gitlink 전환 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Go/Gin application | Q&A domain, REST/Swagger, auth/permission, install/admin service | HTTP request → controller/service/repo → SQL/cache | [Go module](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/go.mod#L18-L55), [default config](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/configs/config.yaml#L18-L40) |
| Plugin registry | search, storage, auth, reviewer, agent, vector-search 등 extension 등록/호출 | compiled plugin init → typed stack → enabled plugin invocation | [registry](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/plugin.go#L55-L185) |
| MCP surface | questions/answers/comments/tags/users/semantic search를 tool로 노출 | streamable HTTP MCP → feature/auth middleware → read handlers | [router](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/router/mcp_router.go#L28-L48) |
| AI conversation | OpenAI-compatible streaming chat에 내부 MCP tools를 제공 | user conversation → model tool call → Answer handler → model response | [tool-enabled request](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L430-L449), [tool execution](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L620-L685) |
| Search/vector plugins | lexical external search와 semantic embedding/vector store 연결 | content sync/update/delete → plugin index; query → result IDs/metadata | [search interface](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/search.go#L103-L130), [vector interface](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/vector_search.go#L88-L124) |

## 역할과 연동

- AgentRole: Human Knowledge Author/Reviewer, Knowledge Retriever, AI Assistant; autonomous coding worker나 independent verifier는 아님.
- Capability: `human-curated-qa`, `knowledge-portal`, `content-permission`, `plugin-search`, `semantic-search`, `mcp-knowledge-read`, `ai-conversation`.
- Integration: Web UI, REST/Swagger, MCP streamable HTTP, OpenAI-compatible chat/embedding API, SQL, plugin interfaces, Docker/Helm.
- SecurityOperationalRequirement: Q&A ACL과 MCP/AI tool visibility 일치, plugin supply-chain isolation, model/embedding egress, prompt injection, tenant/retention/audit와 external auth 정책이 필요하다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | Go 1.25, UI build, SQLite/MySQL/PostgreSQL 중 DB, file cache/upload; optional search/vector/model plugins과 external services | [go.mod](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/go.mod#L18-L55), [default config](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/configs/config.yaml#L18-L40) |
| Supported protocols / surfaces | Web/REST, Swagger, MCP streamable HTTP, SSE-style AI chat streaming, plugin Go interfaces | [MCP router](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/router/mcp_router.go#L28-L48), [AI stream](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L475-L538) |
| Rate limits | fixed source에서 application-wide contract 확인 못함; model/search/plugin/provider 한도는 unknown | 2026-08-21 정적 조사 |
| Timeout / retry | HTTP/model/vector/plugin 공통 timeout·retry 계약은 unknown; request context와 provider client에 의존 | fixed source에서 중앙 policy를 확인하지 못함 |
| Fallback candidates | `cq`, `tencentdb-agent-memory` | Answer 장애 시 agent KU나 asset memory로 조회 가능하지만 human Q&A workflow·Web UX·content roles를 잃는다. schema/auth/data boundary가 달라 자동 전환 금지 |

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `answer-c1-human-qa-platform` | capability | Q&A content와 plugin extension을 중심으로 self-hosted knowledge portal을 구성한다. | [official site](https://answer.apache.org), 2026-08-21 | [README](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/README.md#L5-L37) | `I2` | `V1` | `windows:P0; linux:P1` | 제품/extension 문서 확인; workflow runtime 미검증 |
| `answer-c2-typed-plugin-seams` | architecture | core registry는 여러 typed plugin interface를 등록하며 search/vector 구현을 교체 가능하게 한다. | 없음 | [registry](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/plugin.go#L55-L185), [vector search](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/vector_search.go#L88-L124) | `I2` | `V2` | `windows:P0; linux:P1` | interface 정적 확인; plugin process isolation·ABI compatibility 미검증 |
| `answer-c3-mcp-read-surface` | interface | MCP server는 Q&A와 semantic search용 read tools를 streamable HTTP로 제공한다. | 없음 | [router](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/router/mcp_router.go#L28-L48), [semantic handler](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/mcp_controller.go#L364-L389) | `I2` | `V2` | `windows:P0; linux:P1` | tool registration/handler 확인; auth·content ACL parity와 transport runtime 미검증 |
| `answer-c4-ai-tool-loop` | architecture | AI chat은 OpenAI-compatible provider에 내부 MCP tool definitions를 주고 returned tool calls를 Answer handlers로 실행한다. | 없음 | [request](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L430-L449), [execution](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L620-L685) | `I2` | `V2` | `windows:P0; linux:P1` | loop 정적 확인; prompt injection, tool authorization, provider failure 미검증 |
| `answer-c5-vector-provider-boundary` | security | vector plugin이 indexing/storage를 소유하고 helper는 configured OpenAI-compatible endpoint로 content를 전송해 embedding을 생성할 수 있다. | 없음 | [interface](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/vector_search.go#L88-L124), [embedding helper](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/vector_search.go#L127-L179) | `I2` | `V2` | `windows:P0; linux:P1` | data egress path 확인; redaction/residency/provider policy 미검증 |
| `answer-c6-plugin-isolation-limit` | limitation | plugin은 in-process typed registry로 호출되며 interface 자체는 sandbox, per-plugin credential 또는 failure containment를 제공하지 않는다. | 없음 | [registration/call loop](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/plugin.go#L147-L180) | `I2` | `V2` | `windows:P0; linux:P1` | confirmed structural boundary; 실제 third-party plugin behavior 미검증 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| Web/REST | HTTP JSON/HTML, Swagger | browser/client ↔ Answer | session/admin/content permission에 의존 | [Swagger artifact](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/docs/swagger.yaml) |
| MCP | streamable HTTP | agent/MCP client → read handlers | site feature flag와 MCP auth middleware; content-level parity는 미검증 | [router](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/router/mcp_router.go#L28-L48), [middleware](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/base/middleware/mcp_auth.go) |
| AI provider | OpenAI-compatible HTTP streaming | Answer → configured model; tool calls → Answer internal handlers | provider credential와 prompt/content egress; user/tool authority 연결 검증 필요 | [AI request](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/internal/controller/ai_controller.go#L430-L449) |
| Plugin | in-process Go interface | compiled plugin ↔ core | process/DB/cache authority 공유 가능; enable flag는 sandbox 아님 | [plugin data/registry](https://github.com/apache/answer/blob/3b9f1370612e690a0b7f230f05e688930db4c6d3/plugin/plugin.go#L38-L75) |

## 운영·보안·trust boundary

- 보호 자산은 Q&A/attachment/user data, roles/permissions, DB/cache/upload, plugin code/config, MCP credential, model/embedding keys와 conversation records다.
- MCP와 AI tool path는 사람이 보는 Web permission projection과 별도 entry point다. 비공개·삭제·검토 중 content가 같은 정책으로 필터되는지 V5 fixture가 필요하다.
- plugin enable/disable과 typed interface는 code isolation이 아니다. 사내 배포는 signed inventory, dependency/SBOM, secret audience와 out-of-process adapter 여부를 결정해야 한다.
- model/embedding provider로 보내는 question/answer/comment 및 prompt에는 data classification, redaction, residency, retention과 cost gate가 필요하다.

## 플랫폼

- Windows `P0/unknown`: Go dependency에 Windows 관련 간접 경로가 있어도 제품의 native Windows workflow 근거로 승격하지 않았다.
- Linux `P1/partial`: Dockerfile, compose, Helm과 Linux container 배포 경로를 확인했지만 native host나 container runtime을 실행하지 않았다.
- DB driver별 migration/locking, filesystem upload cleanup, reverse proxy/TLS, plugin binary compatibility와 signal/upgrade를 실제 target 환경에서 검증해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `answer-v2-source-20260821` | `V2` | `3b9f1370612e690a0b7f230f05e688930db4c6d3` | GitHub metadata API, `git ls-remote`, `git clone --depth 1`, fixed source `rg/sed`; exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; Git 2.53.0 | origin, license, Q&A/plugin/MCP/AI/vector architecture와 trust boundary 확인 | 이 프로필 fixed-SHA locator | `answer-c1`~`answer-c6` | build/UI/DB/plugin/model/MCP/runtime/native OS 미실행 |
| `v3plus-none-answer` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | static Swagger/test/source를 runtime evidence로 승격하지 않음 |

## 강점과 한계

- 강점: human-reviewed Q&A, search/vector plugin seam, MCP와 AI assistant surface가 같은 content domain을 재사용한다(`answer-c1`~`answer-c4`).
- 확인된 한계: in-process plugin은 sandbox가 아니며(`answer-c6`), semantic/AI surface는 content를 external provider로 보낼 수 있다(`answer-c5`).
- 미확인·추론: multi-tenant isolation, private content leakage, moderation consistency, HA/backup/upgrade, plugin compatibility, search quality, model cost/rate limit과 Windows support는 unknown이다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | human Q&A workflow를 Web/REST/MCP retrieval로 재사용, typed search/vector seam | `answer-c1`~`answer-c3` | Knowledge portal과 connector contract |
| Adapt | AI tool loop를 per-user content policy와 model gateway에 연결 | `answer-c4`, `answer-c5` | `AX-D002`, `AX-D003`, `AX-D006`, `AX-D007` |
| Avoid | plugin enable flag를 sandbox로, MCP auth를 content authorization으로 간주 | `answer-c3`, `answer-c6` | least privilege와 fail-closed adapter isolation |
| Build | policy-filtered knowledge API, out-of-process plugin adapter, model/embedding egress receipt와 ACL parity tests | `answer-c3`~`answer-c6` | internal knowledge/policy/evidence layer |

## 도입 판단

- 결정: 참고
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: human-curated knowledge portal과 MCP/AI retrieval reference; production 배포·plugin 설치는 현재 범위 밖.
- 이유: `answer-c1`~`answer-c4`는 사람 지식과 agent retrieval 연결에 유용하지만 `answer-c5`, `answer-c6`의 provider/plugin 경계를 사내 정책으로 보강해야 한다.
- 재검토 조건: target DB/container V3, role/content/MCP V5 ACL matrix, plugin crash/secret isolation, prompt injection/model egress, backup/restore/upgrade와 license inventory.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `answer-test-build-deploy` | `answer-c1`, `answer-c2` | `V4/linux:P2` | pinned container, SQLite와 target production DB | reproducible build, migration, Q&A CRUD/search, restart/backup restore | build/deploy exit 0, data loss 0, digest/SBOM/schema 보존 | build log, image digest, DB diff, SBOM | dependency/container write 승인 |
| `answer-test-acl-egress` | `answer-c3`~`answer-c6` | `V5/linux:P2` | public/private/review/deleted content와 malicious plugin/model fixture | Web/REST/MCP/AI visibility matrix, prompt injection, provider canary, plugin crash/secret access | surface별 ACL 일치, forbidden provider/plugin disclosure 0, failure containment receipt 일치 | access matrix, HTTP/model trace, canary/crash report | security/privacy/model 비용 승인 |

## 관계

- `Tool HAS_VERSION tool-version:apache-answer@3b9f1370612e690a0b7f230f05e688930db4c6d3`
- `ToolVersion FITS_ROLE HumanKnowledgeAuthor/Reviewer/KnowledgeRetriever/AIAssistant`
- `ToolVersion PROVIDES human-curated-qa/mcp-knowledge-read/plugin-search/semantic-search`
- `ToolVersion SUPPORTS Web/REST/MCP/OpenAI-compatible/SQL/plugin`
- `Project EVALUATES ToolVersion` as human-curated knowledge portal reference

## 변경 이력

- 2026-08-21: official `main` HEAD를 manifest-only로 고정하고 `I2/V2`, Windows `P0`, Linux `P1` 정적 분석을 추가함.
