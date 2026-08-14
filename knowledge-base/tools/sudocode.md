---
id: tool-sudocode
type: tool-profile
title: sudocode
status: observed
profile_schema_version: 2
tool_key: sudocode
tool_version_id: tool-version:sudocode@632de1910bc4e272f99db7a33dad8f22feb743d9
tags: [knowledge-base, tool, specification, issue, execution, knowledge-ingestion]
official_upstream: https://github.com/sudocode-ai/sudocode
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 632de1910bc4e272f99db7a33dad8f22feb743d9
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: tag
version_ref: v0.2.0
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-14
---

# sudocode

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

sudocode는 versioned specification(what), issue/how, execution, artifact를 연결하고 JSONL/Git과 SQLite cache, CLI/server/MCP로 노출하는 intent-to-work graph다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/sudocode-ai/sudocode` |
| 기본 브랜치와 조사일 HEAD | `main` / [`632de1910bc4e272f99db7a33dad8f22feb743d9`](https://github.com/sudocode-ai/sudocode/commit/632de1910bc4e272f99db7a33dad8f22feb743d9) (2026-08-14) |
| 고정 버전 | gitlink `632de1910bc4e272f99db7a33dad8f22feb743d9`, exact tag `v0.2.0`; root/CLI/server/types/MCP package version `0.2.0` |
| pin과 최신 관찰 관계 | 조사일 `main` HEAD와 pin이 동일. 현재 upstream observation과 immutable ToolVersion은 별도 필드이며 이후 자동 동일시하지 않는다. |
| 로컬 gitlink | [`multi-agent-tools/sudocode`](../../multi-agent-tools/sudocode/) |
| 출처 무결성 | `I2`: parent `.gitmodules`/gitlink와 official fixed-SHA/tag/package metadata 교차 확인 |
| license | fixed SHA [`LICENSE`](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/LICENSE#L2-L12)의 Apache-2.0 |
| provenance limitation | 통합 조사 worktree submodule body가 비어 parent gitlink와 official GitHub fixed-SHA tree/metadata로 `V2`를 수집했다. local parser/build/server/MCP/runtime/E2E/Windows 실행은 하지 않았다. |
| source 관리 | spec/issue/execution schema와 ingestion adapter에 직접 영향을 주므로 fixed-SHA submodule 유지 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Spec/Issue graph | intent와 delivery work 분리, 관계 연결 | spec → issue/relationship → execution/artifact | [concepts](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/README.md#L144-L205) |
| JSONL interchange | versioned records read/write | Git JSONL ↔ importer/exporter ↔ SQLite | [reader/writer](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/jsonl.ts#L1-L81) |
| Deterministic export | relationships/tags/feedback 정렬 | DB rows → stable JSONL | [sort/export](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/export.ts#L39-L55), [records](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/export.ts#L78-L168) |
| SQLite cache/schema | specs, issues, relations, execution state | WAL/FK tables, branch/worktree/model metadata | [schema](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/types/src/schema.ts#L1-L85), [execution](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/types/src/schema.ts#L131-L186) |
| MCP tool surface | read/write scope별 tools 노출 | MCP caller → scoped handler → store/worktree | [scopes](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/mcp/src/scopes.ts#L96-L145) |

## 역할과 연동

- AgentRole: Spec author, Issue planner, Executor, Artifact/evidence producer, Knowledge ingestor
- Capability: `versioned-intent-graph`, `spec-issue-separation`, `deterministic-jsonl-export`, `execution-record`
- Integration: CLI, MCP, server, Markdown, JSONL, SQLite, Git/worktree
- SecurityOperationalRequirement: schema validation, malformed-record quarantine, independent authorization, worktree/executor sandbox, provenance and approval linkage

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `sudocode-intent-separation` | architecture | spec/issue/execution/artifact를 구분하고 관계로 연결하는 model을 문서화한다. | [current pin](https://github.com/sudocode-ai/sudocode/commit/632de1910bc4e272f99db7a33dad8f22feb743d9), 2026-08-14 | [README](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/README.md#L144-L205), [schema](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/types/src/schema.ts#L30-L85) | `I2` | `V2` | `W0` | pass(문서+정적). 조직 approval/evidence 의미론은 별도다. |
| `sudocode-versioned-export` | capability | export는 relationship/tag/feedback을 포함하고 결정적으로 정렬한다. | 동일 | [export.ts](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/export.ts#L39-L168) | `I2` | `V2` | `W0` | pass(정적). multi-writer merge/round-trip runtime은 미검증. |
| `sudocode-jsonl-fail-modes` | security | async JSONL reader 기본은 malformed line에서 fail하지만 `skipErrors=true`면 생략할 수 있다. | 동일 | [jsonl.ts](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/jsonl.ts#L35-L81) | `I2` | `V2` | `W0` | pass/limitation. source-of-truth ingestion에서 skip은 fail-open 데이터 손실이므로 quarantine+explicit decision이 필요하다. |
| `sudocode-mcp-scope-not-auth` | limitation | MCP scope는 노출 tool 집합을 나누지만 독립된 호출자 인증·승인을 그 자체로 증명하지 않는다. | 동일 | [scopes.ts](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/mcp/src/scopes.ts#L96-L145) | `I2` | `V2` | `W0` | confirmed boundary. read/write scope를 사내 IAM/policy gate와 연결해야 한다. |
| `sudocode-multirepresentation-limit` | limitation | Markdown/JSONL/Git을 source로, SQLite를 cache로 두는 다중 표현과 자동 sync를 문서화한다. | 동일 | [source/cache](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/README.md#L257-L266) | `I2` | `V1` | `W0` | partial. “AI handles merge conflicts”는 governance/atomic consistency 증거가 아니다. |
| `sudocode-windows-crlf-source` | platform | JSONL reader는 `crlfDelay: Infinity`를 사용하고 feedback anchor parser는 Windows `\r`를 명시 처리한다. | 동일 | [JSONL CRLF](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/jsonl.ts#L47-L51), [anchor CR](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/operations/feedback-anchors.ts#L90-L110), [normalize](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/cli/src/operations/feedback-anchors.ts#L270-L288) | `I2` | `V2` | `W1` | pass(좁은 source). actual Windows round-trip/test 미실행이므로 `W2/W3` 아님. |
| `sudocode-windows-installer-risk` | security | PowerShell installer와 Windows package target이 있으나 문서가 remote script pipe-to-execute 사용을 안내한다. | 동일 | [install.ps1](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/scripts/install.ps1#L1-L14), [manifest/checksum path](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/scripts/install.ps1#L47-L95), [win package](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/build-scripts/package-sea.js#L29-L63) | `I2` | `V2` | `W1` | confirmed risk. 사내 설치는 pinned artifact, offline verification, allowlist로 대체해야 한다. |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| CLI/import-export | Markdown/JSONL/SQLite | human/agent ↔ versioned graph/cache | filesystem/Git authority, parser strictness | [formats](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/README.md#L144-L205) |
| MCP | MCP tool calls | agent client → scoped read/write handlers | scope는 tool exposure; identity/approval 별도 필요 | [scopes](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/mcp/src/scopes.ts#L96-L145) |
| Worktree execution | local Git/worktree/process | issue → branch/worktree execution record | worktree는 sandbox가 아니며 commit/external write gate 필요 | [execution schema](https://github.com/sudocode-ai/sudocode/blob/632de1910bc4e272f99db7a33dad8f22feb743d9/types/src/schema.ts#L131-L186) |

## 운영·보안·trust boundary

- versioned intent, mutable cache, execution artifact, approval/evidence를 서로 다른 authority로 취급한다.
- malformed JSONL은 authoritative ingestion에서 skip하지 않고 quarantine하며, sync/merge conflict는 agent 판단만으로 자동 승인하지 않는다.
- MCP scope는 permission hint이지 IAM/authz proof가 아니다. worktree도 credential/network/process sandbox가 아니다.
- 회사 업종, 데이터 분류, 규정, 승인, 망분리, knowledge retention은 unknown Decision Item이다.

## 플랫폼과 Windows

- explicit CRLF handling, PowerShell installer, win-x64 package config로 `W1`이다.
- remote script execution 안내는 내부 supply-chain 정책에 부적합하며 checksum code 존재만으로 end-to-end provenance를 증명하지 않는다.
- Windows install/parser/build/runtime을 실행하지 않아 `W2/W3`은 아니다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `sudocode-origin-static-20260814` | `I2/V2/W1` | `632de191...` / `v0.2.0` | gitlink/tag/package/upstream/fixed source inspection; exit 0 | Windows/PowerShell, parent `984cac0...` | partial pass | 위 permalinks | 모든 Claim | local body/runtime 미사용 |
| `sudocode-v3plus-none` | `V3~V6/W2~W3` | 동일 | build/parser round-trip/server/MCP/E2E 미실행 | unknown | unknown | 없음 | 없음 | static source만 검증 |

실행 기록: task/run `/root/implement_deep_collaboration_profiles`; profile `implement-deep` revision unknown; role `profile author`; model `OpenAI/gpt-5.6-sol`, exact build unknown; effort `high`; 시간·cost·latency unknown(2026-08-14 session); base/head `984cac0634b83d10af91d8e1814680816e67c53b`; artifact는 이 프로필뿐이다.

## 강점과 한계

- 강점: spec→issue→execution→artifact separation과 deterministic versioned export가 knowledge ingestion/control-plane 사이의 계약 설계에 유용하다.
- 확인된 한계: skipErrors, multi-representation conflict, MCP scope/auth 분리, remote script install은 내부 정책으로 보완해야 한다.
- 미확인: merge conflict correctness, schema migration, concurrent sync, MCP authorization, Windows round-trip과 execution isolation은 unknown이다.

## AX 설계 재료

이 표는 최종 vendor selection이 아니라 사내 AX 설계 재료다. 회사 조건은 추정하지 않는다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | spec→issue→execution→artifact separation과 deterministic graph export | `sudocode-intent-separation`, `sudocode-versioned-export` | `AXN-VERSIONED-INTENT` |
| Adapt | JSONL source/SQLite cache에 provenance, schema version, conflict quarantine, approval edge 추가 | `sudocode-jsonl-fail-modes`, `sudocode-multirepresentation-limit` | retention/data-classification 결정 필요 |
| Avoid | AI conflict resolution을 authority로 사용, `skipErrors`로 silent loss, `irm|iex`, worktree=sandbox 가정 | limitation Claims | fail-open/supply-chain/권한 혼동 방지 |
| Build | schema-governed knowledge ingestion, immutable snapshot, identity/approval/evidence links, Windows parser/install conformance | 모든 Claim | `AD-KNOWLEDGE-PROVENANCE-GATE` → `RM-INTENT-GRAPH-INGESTION` (proposed) |

관계: `versioned-intent-graph` → `AXN-VERSIONED-INTENT` → `AD-KNOWLEDGE-PROVENANCE-GATE` → `RM-INTENT-GRAPH-INGESTION`; evidence는 fixed-SHA Claims/Evidence다.

## 도입 판단

- 결정: 참고/knowledge adapter 후보
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: versioned intent graph와 ingestion schema pattern
- 재검토 조건: 새 ToolVersion/current upstream 분리 갱신, `V3` build/parser, `V4/V5` sync/conflict/auth, Windows `W2/W3`

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `sudocode-roundtrip` | `sudocode-versioned-export`, `sudocode-jsonl-fail-modes` | `V4/W2` | native Windows temp repo | LF/CRLF/malformed/concurrent import-export | no silent loss, deterministic diff, quarantine evidence | fixtures/diff/log | local runtime 승인 |
| `sudocode-auth-conflict` | `sudocode-mcp-scope-not-auth`, `sudocode-multirepresentation-limit` | `V4/V5` | isolated MCP/server | unauthorized writes, divergent edits, crash | deny-by-default, no silent overwrite, auditable resolution | protocol/store logs | identity policy 필요 |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion PROVIDES versioned-intent-graph/spec-issue-separation`
- `Capability ADDRESSES AXNeed`
- `AXNeed DRIVES ArchitectureDecision`
- `ArchitectureDecision CREATES RoadmapItem`
- `RoadmapItem IMPLEMENTS Capability`

## 변경 이력

- 2026-08-14: `v0.2.0` gitlink/tag와 조사일 upstream observation을 분리하고 official fixed-SHA source로 `I2/V2/W1` 작성.
