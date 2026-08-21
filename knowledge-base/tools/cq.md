---
id: tool-cq
type: tool-profile
title: Mozilla AI cq
status: observed
profile_schema_version: 3
tool_key: cq
tool_version_id: tool-version:cq@4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd
tags:
  - knowledge-base
  - tool
  - agent-knowledge
official_upstream: https://github.com/mozilla-ai/cq
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-21
upstream_default_branch: main
upstream_head_observed: 4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd
upstream_checked_at: 2026-08-21
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P1
  linux: P1
version_kind: commit
version_ref: 4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd
parent_repo_head: 42f4f2d6a0b07bcb28cb782ac89ca6210f06abde
source_management: manifest-only
analysis_snapshot_date: 2026-08-21
---

# Mozilla AI cq

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

에이전트가 작업 전 지식을 조회하고 작업 중 발견을 구조화해 제안·확인·반박하도록 만드는 local-first MCP 지식 공유 계층이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/mozilla-ai/cq |
| 기본 브랜치와 조사일 HEAD | `main` / `4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd` (2026-08-21) |
| 고정 버전 | `4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd` |
| pin과 최신 관찰 관계 | 조사 시 default HEAD와 동일; fixed profile은 자동 갱신하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; 임시 shallow clone으로 official fixed SHA를 정적 검사하고 locator를 이 프로필에 보존 |
| 조사일 | 2026-08-21 |
| 출처 무결성 | `I2`: GitHub branch API, `git ls-remote`, shallow clone HEAD가 동일 |
| 플랫폼 증거 | Windows `P1/partial`: Scoop·Windows config path가 명시됨. Linux `P1/partial`: XDG path와 portable Go 경로 확인. 양쪽 native 실행은 미수행 |
| license | fixed [`LICENSE`](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/LICENSE#L1-L202)의 Apache-2.0 text와 GitHub SPDX metadata 일치 |
| provenance limitation | README, architecture, schema, Go client와 skill prompt를 정적으로 읽음. install/build/MCP/server/remote service/native OS 실행은 미수행 |
| source 관리 | `manifest-only`: 현재 knowledge-plane 비교·설계 대상이며 약 2.8 MB GitHub source size. 직접 adapter 또는 schema 구현을 차용할 때 gitlink 전환 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Agent skill/plugin | query-before-retry와 propose/confirm/flag 행동 지침 | agent context → MCP tool call; 지침 준수는 policy enforcement가 아님 | [skill protocol](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/sdk/go/prompts/SKILL.md#L17-L110) |
| Local MCP/Go client | 다섯 MCP tool, local SQLite, optional remote merge/drain | stdio MCP → local store; configured remote에는 HTTP | [README tools and boundaries](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L63-L123), [client operations](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/sdk/go/client.go#L88-L191) |
| Knowledge-unit schema | insight/context/evidence/provenance의 wire contract | propose payload → validated KU → query/confirm/flag lifecycle | [schema](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/schema/knowledge_unit.json#L1-L180) |
| Remote API/store | shared namespace, auth, review와 retrieval | local client → REST API → shared DB/hosted service | [remote options](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L73-L108) |

## 역할과 연동

- AgentRole: Knowledge Consumer, Knowledge Proposer, Human Reviewer; independent verifier 자체는 아님.
- Capability: `query-before-retry`, `structured-knowledge-unit`, `local-knowledge-store`, `knowledge-confirm-flag`, `optional-remote-sharing`.
- Integration: MCP over stdio, CLI, Go/Python SDK, SQLite, HTTP REST, hosted 또는 self-hosted remote.
- SecurityOperationalRequirement: tenant/RBAC, source provenance, prompt-injection/PII scan, publish approval, revocation·retention, stale/poisoned knowledge 격리와 독립 검증이 필요하다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | Go CLI/MCP와 local SQLite; remote는 API URL·API key 및 hosted service 또는 FastAPI container/database | [runtime boundaries](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L114-L123) |
| Supported protocols / surfaces | CLI, MCP stdio, Go/Python SDK, remote HTTP REST | [published components](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L125-L137) |
| Rate limits | local path는 명시적 rate limit 없음; hosted `cq.exchange` 한도는 unknown | fixed source에서 hosted quota 계약을 확인하지 못함; 2026-08-21 |
| Timeout / retry | CLI operation timeout 기본 30초; 공통 retry/backoff 계약은 unknown | [CLI environment](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/cli/README.md#L77-L91), [bounded context](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/sdk/go/client.go#L521-L531) |
| Fallback candidates | `tencentdb-agent-memory`, `apache-answer` | cq 장애 시 문서형 Q&A 또는 asset memory로 조회를 대체할 수 있으나 KU confidence/confirm/flag와 local-first workflow를 잃는다. credential·data boundary가 달라 자동 전환 금지 |

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `cq-c1-local-first-mcp` | architecture | agent process, local MCP/SQLite, optional remote API가 분리돼 local-only와 shared mode를 제공한다. | [official docs](https://docs.mozilla.ai/cq), 2026-08-21 | [README lines 114–123](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L114-L123) | `I2` | `V2` | `windows:P1; linux:P1` | 구조 정적 확인; process isolation·DB durability 미검증 |
| `cq-c2-query-feedback-loop` | capability | query/propose/confirm/flag/status가 조회→제안→사회적 feedback loop를 구성한다. | [official README](https://github.com/mozilla-ai/cq), 2026-08-21 | [tools lines 63–70](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L63-L70) | `I2` | `V2` | `windows:P1; linux:P1` | interface 확인; knowledge 정확도·중복 방지 효과 미검증 |
| `cq-c3-confidence-not-verification` | limitation | confidence는 confirm/flag 기반 사회적 신호이며 freshness나 정확성 보장이 아니다. | 없음 | [skill guidance lines 34 and 100–104](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/sdk/go/prompts/SKILL.md#L34-L104) | `I2` | `V2` | `windows:P1; linux:P1` | 확인된 limitation; verifier evidence로 사용 금지 |
| `cq-c4-publish-gate-conflict` | security | architecture 문서는 human review 후 remote graduation을 설명하지만 configured remote의 skill 지침은 `propose`가 shared store에 즉시 publish된다고 명시한다. | 없음 | [review model](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/docs/architecture.md#L86-L95), [immediate publish warning](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/sdk/go/prompts/SKILL.md#L197-L205) | `I2` | `V2` | `windows:P1; linux:P1` | 문서/실행 지침의 authority boundary 차이 확인; 실제 server state transition 미실행 |
| `cq-c5-long-lived-agent-key` | security | remote data plane은 환경변수의 long-lived agent API key를 사용할 수 있다. | 없음 | [credential contract](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/cli/README.md#L77-L88), [key semantics](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/cli/README.md#L123-L130) | `I2` | `V2` | `windows:P1; linux:P1` | secret materialization 경계 확인; audience·rotation·leak fixture 미검증 |
| `cq-c6-development-status` | limitation | upstream은 0.x이며 breaking change를 예상하라고 명시한다. | [official README](https://github.com/mozilla-ai/cq), 2026-08-21 | [status](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L1-L4) | `I2` | `V1` | `windows:P0; linux:P0` | current version maturity observation; 안정성/SLA 보장 없음 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| MCP | stdio / MCP tool calls | agent host → local server process | host가 부여한 tool/process/filesystem 권한을 사용 | [MCP tools](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L63-L70) |
| Remote API | HTTP REST / JSON KU | local client ↔ hosted/self-hosted store | read와 write auth가 다르며 write는 API key; tenant/RBAC runtime 미검증 | [remote config](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/README.md#L73-L108) |
| Schema | JSON Schema | producer → store → consumer | schema validity는 provenance·truth·safe content를 증명하지 않음 | [KU schema](https://github.com/mozilla-ai/cq/blob/4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd/schema/knowledge_unit.json#L1-L180) |

## 운영·보안·trust boundary

- 보호 자산은 KU 내용·provenance, local/remote DB, agent API key, tenant namespace, reviewer identity와 agent prompt/context다.
- skill 지침은 행동 유도이지 enforcement가 아니다. remote publish, PII/prompt-injection filter, 승인과 verification을 policy/evidence service에서 별도 강제해야 한다.
- `confirm` 수와 confidence는 독립 조직·모델·환경의 재현 evidence가 아니며 sybil/poisoning/staleness에 취약할 수 있다.
- local SQLite에서 remote로 이동할 때 data classification, tenant binding, deletion/retention과 audit receipt가 필요하다.

## 플랫폼

- Windows `P1/partial`: README의 Scoop와 install 문서의 Windows config path를 확인했지만 native install/MCP/SQLite/credential path는 실행하지 않았다.
- Linux `P1/partial`: XDG data path와 portable Go client를 확인했지만 WSL2 조사 host는 Linux host-native `P2`가 아니다.
- 양쪽에서 path/locking, process cancellation, key storage, offline queue와 network loss를 같은 fixture로 검증해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `cq-v2-source-20260821` | `V2` | `4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd` | GitHub metadata API, `git ls-remote`, `git clone --depth 1`, fixed source `rg/sed`; exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; Git 2.53.0 | origin, Apache-2.0, architecture/interface/security conflicts 확인 | 이 프로필 fixed-SHA locator | `cq-c1`~`cq-c6` | install/build/runtime/hosted service/native OS 미실행 |
| `v3plus-none-cq` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | source/test 존재를 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: query-before-retry와 compact KU schema, local-first store, confirm/flag feedback는 agent 간 반복 실패를 줄이기 위한 명확한 interaction pattern이다(`cq-c1`, `cq-c2`).
- 확인된 한계: confidence는 검증이 아니고(`cq-c3`), human graduation 설명과 immediate remote propose 경로의 경계를 사내 policy가 해소해야 한다(`cq-c4`).
- 미확인·추론: poison resistance, tenant isolation, semantic retrieval 품질, concurrent SQLite/remote drain, deletion cascade, offline conflict와 비용은 unknown이다.

## AX 설계 재료

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | query-before-retry, typed KU, confirm/flag와 local-first cache | `cq-c1`, `cq-c2` | Knowledge ingestion/retrieval layer와 반복 실패 방지 |
| Adapt | confidence를 source recency·environment·verifier receipt와 분리하고 tenant policy로 graduation | `cq-c3`, `cq-c4` | `AX-D002`, `AX-D003`, `AX-D008`, `AX-D012` |
| Avoid | skill prompt나 confidence threshold만으로 publish·truth·completion 승인 | `cq-c3`, `cq-c4` | fail-closed external write와 independent verification |
| Build | policy-enforced proposal queue, provenance signature, expiry/revalidation, poison quarantine와 deletion receipt | `cq-c3`~`cq-c5` | internal policy/evidence/knowledge service |

## 도입 판단

- 결정: 파일럿
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: local-first agent learning과 query-before-retry adapter 비교; hosted service나 자동 remote publish는 현재 채택하지 않음.
- 이유: `cq-c1`, `cq-c2`는 기존 asset memory와 다른 operational learning loop를 제공하지만 `cq-c3`~`cq-c5`의 검증·승인·credential 경계가 선결이다.
- 재검토 조건: V3 native build, V4 local MCP/SQLite, V5 poisoning·publish approval·tenant/revoke/delete failure fixture와 0.x version drift 검토.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `cq-test-native` | `cq-c1`, `cq-c2` | `V4/windows:P2; linux:P2` | 결정된 Windows/Linux native host | fixed SHA build, MCP initialize/tools, local propose/query/confirm/flag | 양쪽 OS 결과·DB state 동일, exit/log/digest 보존 | build/MCP transcript, DB snapshot, SBOM | dependency/network 승인 |
| `cq-test-publish-policy` | `cq-c3`~`cq-c5` | `V5/windows:P2; linux:P2` | isolated client/server와 two-tenant fixture | poisoned/PII KU, direct propose, reviewer reject, key revoke, offline drain/conflict | 승인 전 cross-tenant/shared visibility 0, revoked key write 0, state receipt 일치 | HTTP trace, DB diff, policy receipt, canary scan | security/privacy review |

## 관계

- `Tool HAS_VERSION tool-version:cq@4cd0220a5582f5bf71e0dc0b1625b3b93c2238fd`
- `ToolVersion FITS_ROLE KnowledgeConsumer/KnowledgeProposer/HumanReviewer`
- `ToolVersion PROVIDES query-before-retry/structured-knowledge-unit/local-knowledge-store`
- `ToolVersion SUPPORTS MCP/CLI/HTTP/SQLite`
- `Project EVALUATES ToolVersion` as agent operational-learning plane

## 변경 이력

- 2026-08-21: official `main` HEAD를 manifest-only로 고정하고 `I2/V2`, Windows/Linux `P1` 정적 분석을 추가함.
