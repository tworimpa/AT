---
id: tool-agent-plugins-spec
type: tool-profile
title: Agent Plugins Specification 1.0.0
status: observed
profile_schema_version: 3
tool_key: agent-plugins-spec
tool_version_id: tool-version:agent-plugins-spec@bd383552095128f6effe895b9257cfd580a6d179
tags: [knowledge-base, tool, plugin-specification, agent-skills, mcp, packaging]
official_upstream: https://github.com/agentplugins/agent-plugins-spec
license: "CC-BY-4.0 (specification and documentation); Apache-2.0 (schemas and code)"
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: bd383552095128f6effe895b9257cfd580a6d179
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P0
version_kind: commit
version_ref: bd383552095128f6effe895b9257cfd580a6d179
parent_repo_head: 91d6d075d53185667e20996cc94ec7e10537d02c
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# Agent Plugins Specification 1.0.0

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [Agent Skills](./agent-skills.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Agent Skills와 MCP server를 단일 directory package, versioned closed manifest, 고정 discovery 위치와 component별 failure boundary로 배포하기 위한 portable plugin 형식이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/agentplugins/agent-plugins-spec |
| 기본 브랜치와 조사일 HEAD | `main` / `bd383552095128f6effe895b9257cfd580a6d179` (2026-08-15) |
| 고정 버전 | commit `bd383552095128f6effe895b9257cfd580a6d179`; 문서상 spec version `1.0.0`, status `Published` |
| pin과 최신 관찰 관계 | 조사 시점 HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; GitHub API로 official fixed-SHA license/spec/schema를 정적 확인 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: official upstream default branch HEAD와 immutable commit identity가 일치하고 fixed source를 직접 읽음 |
| 플랫폼 증거 | Windows `P0/unknown`; Linux `P0/unknown` — normative format이 platform 차이를 언급하지만 client 구현·native runtime을 확인하지 않음 |
| license | [fixed-SHA licensing notice](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/LICENSE.md#L1-L10): specification/documentation/examples는 CC-BY-4.0, schema/source/script는 Apache-2.0; third-party material은 별도 조건 |
| provenance limitation | normative spec·license·schema 위치를 정적으로 읽음; reference client, install/load/runtime, Windows/Linux conformance, MCP process/network와 credential behavior는 미실행 |
| source 관리 | `manifest-only`: portable 표준·설계 비교 대상이다. client loader/reference implementation을 직접 채택할 때 gitlink 전환을 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| `plugin.json` | spec version, name과 metadata, client extension namespace를 가진 closed portable manifest | client가 locally supported `$schema` 선택 → validate → component discovery; fatal schema error면 plugin reject | [manifest contract](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L129-L196) |
| Fixed component discovery | `skills/`의 immediate `SKILL.md`와 root `mcp.json`을 독립 component type으로 발견 | missing location은 허용; invalid type/entry는 가장 좁은 component boundary에서 skip/disable | [discovery and component types](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L235-L333) |
| MCP configuration | stdio, streamable HTTP, legacy SSE server entry와 transport-specific fields를 closed union으로 선언 | `mcp.json` version/schema 확인 → server별 validate → declared transport connect; 다른 component와 failure 격리 | [MCP configuration](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L297-L399) |
| Client extensions | reverse-domain namespace 아래 client-owned manifest data와 top-level directory 수용 | portable core는 unknown namespace를 ignore; implementing client가 자체 validation/loading/failure semantics 소유 | [extensions](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L401-L446) |
| Runtime roots | client가 immutable package root와 update 간 유지되는 writable data root를 분리 | stdio subprocess에 `PLUGIN_ROOT`·`PLUGIN_DATA` 제공 → args/env/cwd의 제한적 placeholder expansion | [environment and expansion](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L448-L481) |

## 역할과 연동

- AgentRole: Plugin Publisher, Plugin Registry/Installer, Client Loader, Policy Gate; agent worker나 executor 자체는 아님.
- Capability: `portable-plugin-package`, `versioned-closed-manifest`, `fixed-component-discovery`, `component-failure-isolation`, `plugin-root-containment`, `plugin-data-lifecycle`, `client-extension-namespace`.
- Integration: directory/JSON Schema, Agent Skills, MCP stdio·Streamable HTTP·legacy SSE, subprocess environment.
- SecurityOperationalRequirement: publisher provenance/signature, package revision pin, install approval, component capability/permission, subprocess sandbox, secret broker, egress, retention과 revoke는 portable format 밖의 AX gate로 구현해야 한다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | spec artifact 자체는 Markdown/JSON Schema; 실제 사용은 directory/filesystem, JSON validator, Agent Skills loader 및 선택한 MCP transport/process를 구현한 client 필요 | [minimum client requirements](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L524-L548); reference runtime 미확인 |
| Supported protocols / surfaces | root `plugin.json`, `skills/`, `mcp.json`; MCP stdio·streamable-http·sse; reverse-domain client extensions | [standard layout](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L106-L127), [component types](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L267-L399) |
| Rate limits | portable spec에 registry/download/MCP service rate limit 없음; remote MCP와 distribution service별 `unknown` | package format과 transport configuration만 정의하며 service quota는 client/provider policy 대상 |
| Timeout / retry | transport connect/start failure를 다른 component와 격리하나 공통 timeout/retry/fallback은 정의하지 않음 | [MCP loading rules](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L359-L399); declared transport 실패 후 fallback 미정의 |
| Fallback candidates | `agent-skills` | skill-only artifact면 Agent Skills를 직접 사용할 수 있으나 plugin manifest, MCP, data root, extension과 component failure semantics를 잃는다. authority·credential 범위가 달라 자동 전환하지 않음 |

fallback은 호환성·권한·안전성 보장이 아니라 검토 후보다. external write, credential audience, data boundary, 비용 또는 검증 등급이 바뀌면 자동 선택하지 않고 새 capability/policy 협상과 필요한 승인을 거친다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `aplug-c1-versioned-manifest` | interface | v1 package는 root `plugin.json`의 canonical `$schema`로 locally supported spec version을 선택하며 closed top-level schema의 fatal violation은 component 실행 전 plugin을 거부한다. | [official specification](https://agent-plugins.org/), 2026-08-15 | [manifest lines 129–196](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L129-L196) | `I2` | `V2` | `windows:P0; linux:P0` | normative contract 정적 확인; schema/client conformance runtime 미실행 |
| `aplug-c2-fixed-discovery-isolation` | architecture | v1은 `skills/`와 `mcp.json`만 portable component 위치로 정하고 invalid skill/server/process failure를 다른 독립 component와 분리한다. | [official specification](https://agent-plugins.org/), 2026-08-15 | [discovery/components lines 235–333](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L235-L333), [loading lines 393–399](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L393-L399) | `I2` | `V2` | `windows:P0; linux:P0` | partial availability contract; failure report durability와 recovery는 client 책임 |
| `aplug-c3-package-containment` | security | client는 symlink·junction·reparse point를 포함한 resolved package path가 plugin root 밖으로 벗어나면 가장 좁은 applicable boundary에서 거부해야 한다. | [official specification](https://agent-plugins.org/), 2026-08-15 | [containment lines 56–104](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L56-L104) | `I2` | `V2` | `windows:P0; linux:P0` | normative path rule일 뿐 Windows/Linux resolver 구현·TOCTOU/symlink race 미검증 |
| `aplug-c4-not-process-sandbox` | limitation | package path containment은 plugin subprocess를 sandbox하지 않고 runtime에 전달된 arbitrary path 접근도 제한하지 않는다. | 없음 | [explicit boundary lines 86–104](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L86-L104) | `I2` | `V2` | `windows:P0; linux:P0` | install/load conformance를 runtime isolation 보장으로 표현하면 안 됨 |
| `aplug-c5-explicit-mcp-transport` | interface | MCP server entry는 declared transport로 최초 연결하며 client는 unsupported transport/server failure를 skip하고 다른 component를 계속 load하되 transport fallback은 spec이 정의하지 않는다. | [official specification](https://agent-plugins.org/), 2026-08-15 | [transport/loading lines 359–399](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L359-L399) | `I2` | `V2` | `windows:P0; linux:P0` | connection/auth/handshake timeout, retry와 error receipt durability는 unknown |
| `aplug-c6-secret-boundary` | security | remote header와 stdio env 값은 visible package data이며 portable secret mechanism이 아니므로 plugin은 credential을 embed하면 안 된다. | 없음 | [HTTP header boundary lines 341–357](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L341-L357), [env boundary lines 471–481](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L471-L481) | `I2` | `V2` | `windows:P0; linux:P0` | OAuth, credential acquisition/storage/rotation과 redaction은 client/policy 책임 |
| `aplug-c7-root-data-separation` | architecture | stdio client는 package root와 plugin instance 전용 writable persistent data root를 별도 environment로 제공하며 data는 update 사이 보존할 수 있다. | [official specification](https://agent-plugins.org/), 2026-08-15 | [environment lines 448–481](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L448-L481) | `I2` | `V2` | `windows:P0; linux:P0` | update/rollback/retention/delete integrity, data sharing과 quota는 정의되지 않음 |
| `aplug-c8-platform-boundary` | platform | spec은 junction/reparse point와 platform environment-name semantics를 언급하지만 OS별 resolver·process·filesystem 구현이나 conformance artifact를 제공하지 않는다. | 없음 | [path rules lines 56–104](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L56-L104), [environment semantics lines 448–462](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L448-L462) | `I2` | `V2` | `windows:P0; linux:P0` | portable normative text를 native implementation/support evidence로 승격하지 않음 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| Plugin manifest | directory + closed JSON Schema | publisher package → client version select/validate → component discovery | publisher identity/signature/install approval은 format 밖; invalid core manifest는 reject | [manifest](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L129-L196) |
| Agent Skills | `skills/<name>/SKILL.md` | client가 immediate child를 discover/validate/load | Agent Skills content·script authority와 install review는 별도 | [skills loading](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L272-L303) |
| MCP stdio | process argv/env/cwd + MCP | client → subprocess start/handshake → session; process failure는 entry-local | base environment sanitization, secret materialization, sandbox와 kill-tree는 client 책임 | [stdio config](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L333-L382) |
| MCP remote | HTTPS Streamable HTTP 또는 legacy SSE | client → declared URL connect/auth/handshake | literal headers는 secret mechanism이 아님; OAuth/credential storage와 tenant policy는 client 책임 | [remote transport](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L341-L382) |
| Client extensions | reverse-domain JSON object/top-level directory | portable loader ignores unknown namespace; owner client interprets | namespace collision만 줄이며 extension permission/safety/conformance는 client-owned | [extensions](https://github.com/agentplugins/agent-plugins-spec/blob/bd383552095128f6effe895b9257cfd580a6d179/spec/1.0.0.md#L401-L446) |

## 운영·보안·trust boundary

- 보호 자산과 authority: plugin package/revision, executable scripts·MCP command, `PLUGIN_DATA`, ambient environment, remote header/credential, filesystem/network access, client extension behavior.
- package resolver, schema validator, Agent Skills loader, stdio executor, remote MCP connector, publisher/registry와 policy/secret broker를 서로 다른 trust domain으로 둔다.
- path containment은 package file origin을 좁힐 뿐 subprocess sandbox가 아니다. install approval 뒤에도 command capability, filesystem, process, network와 secret audience를 별도로 negotiate/enforce해야 한다.
- partial component loading은 availability를 높이지만 degraded capability가 명시적으로 report되지 않으면 fail-open이 된다. effective component set과 failure reason을 run/session evidence에 보존해야 한다.
- manifest version·name·repository/license metadata는 publisher authenticity, artifact signature, vulnerability-free status, runtime safety 또는 verification pass가 아니다.

## 플랫폼

- Windows `P0/unknown`: junction/reparse point와 environment-name semantics를 normative text가 언급하지만 Windows client resolver/process를 실행하거나 고정 구현으로 확인하지 않았다.
- Linux `P0/unknown`: symlink/path containment과 subprocess environment는 규정되지만 Linux client implementation/build/runtime artifact가 없다.
- 두 OS 모두 path case, separator, symlink/junction race, executable lookup, env-name comparison, permission, process-tree cleanup과 update/rollback을 native conformance suite로 검증해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `aplug-v2-source-20260815` | `V2` | `bd383552095128f6effe895b9257cfd580a6d179` | GitHub GraphQL default HEAD/license metadata와 fixed-SHA `LICENSE.md`, `spec/1.0.0.md` API read; exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; git 2.53.0 | official pin, dual license, package/interface/security/failure boundaries 확인 | 이 프로필 fixed-SHA URL | `aplug-c1`~`aplug-c8` | schema validator/client/build/runtime와 OS conformance 미실행 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | normative spec과 정적 schema를 구현·운영 evidence로 승격하지 않음 |

## 강점과 한계

- 강점: Agent Skills와 MCP를 하나의 versioned package에 결합하면서 closed manifest, fixed discovery, explicit transport와 component-local failure boundary를 제공한다(`aplug-c1`, `aplug-c2`, `aplug-c5`).
- 확인된 한계: containment는 subprocess sandbox가 아니고(`aplug-c4`), package env/header는 secret channel이 아니며(`aplug-c6`), persistent data의 retention/update semantics와 OS별 구현은 format 밖이다(`aplug-c7`, `aplug-c8`).
- 미확인·추론: publisher registry trust, signature/SBOM, reference client conformance, cross-client interoperability, malicious package detection, update/revoke/rollback과 performance는 unknown이다.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | versioned closed manifest, fixed component location, declared transport와 component-local failure boundary | `aplug-c1`, `aplug-c2`, `aplug-c5` | `RM-K3-skill-registry`; loader contract와 degraded component receipt |
| Adapt | `PLUGIN_ROOT`/`PLUGIN_DATA` 분리를 immutable package + tenant/project-scoped writable state와 lifecycle policy로 확장 | `aplug-c7` | `AX-D002`, `AX-D003`, `AX-D008`; ownership, quota, backup/delete/rollback 결정 필요 |
| Avoid | package containment, valid schema 또는 partial load를 process isolation·trusted publisher·complete capability로 해석 | `aplug-c3`, `aplug-c4`, `aplug-c8` | sandbox/permission/evidence가 없으면 install/run을 fail-closed |
| Build | signed revision/SBOM, publisher provenance, review/revoke, capability/secret/egress gate, cross-platform loader conformance와 effective-component receipt | `aplug-c2`, `aplug-c4`, `aplug-c6`, `aplug-c8` | `AD-PROP-012`, `RM-K4-skill-supply-chain`; SkillSpector scan은 보조 evidence이며 authority를 대체하지 않음 |

## 도입 판단

- 결정: 참고
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: Agent Skills와 MCP를 함께 배포하는 portable plugin artifact/loader contract 및 failure-boundary 참고; production installer/runtime 직접 채택 아님
- 이유: packaging과 component isolation은 비중복 설계 가치가 있으나 publisher trust, permission, secret, subprocess isolation, update/revoke와 OS runtime은 표준 밖이거나 미검증이다(`aplug-c1`~`aplug-c8`).
- 재검토 조건: 새 spec/schema version, independent client conformance suite, signed registry/installer 결정 또는 Windows/Linux `P2` loader pilot.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `aplug-test-schema-conformance` | `aplug-c1`, `aplug-c2` | `V3/windows:P2; linux:P2` | 결정된 Windows/Linux native JSON/schema runtime | official schema valid/invalid/unknown field/version mismatch와 independent component fixture | 양쪽 OS에서 동일 fatal/non-fatal/skip 결과와 diagnostic; schema hash 고정 | fixture corpus, result JSON, environment/dependency lock | dependency download 승인 |
| `aplug-test-path-containment` | `aplug-c3`, `aplug-c4`, `aplug-c8` | `V5/windows:P2; linux:P2` | isolated native filesystems | symlink, junction, reparse point, case/separator, race, runtime arbitrary-path와 subprocess escape fixture | package escape 전부 deny; runtime sandbox 부재가 숨겨지지 않고 separate gate가 차단 | resolver trace, filesystem/process audit, deny receipt | security review·격리 환경 승인 |
| `aplug-test-component-failure` | `aplug-c2`, `aplug-c5` | `V5/windows:P2; linux:P2` | synthetic skill/MCP clients | invalid skill, schema mismatch, unsupported transport, auth/handshake/timeout/crash를 조합 | valid component만 load, effective set·failure reason 보존, silent fallback/false-ready 0 | component matrix, event/diagnostic log | Agent Skills/MCP fixture 승인 |
| `aplug-test-secret-lifecycle` | `aplug-c6`, `aplug-c7` | `V5/windows:P2; linux:P2` | secret canary, deny-by-default network, update/uninstall fixture | ambient env, literal header, data root, update/rollback/revoke/delete와 log/report 검사 | package secret 0, audience-bound broker 외 materialization 0, retention/delete receipt 일치 | canary scan, network/process trace, lifecycle manifest | `AX-D002`, `AX-D005`, `AX-D008`, security/privacy review |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion PROVIDES portable-plugin-package/versioned-closed-manifest/component-failure-isolation`
- `ToolVersion SUPPORTS Agent Skills/MCP/directory/JSON Schema`
- `ToolVersion COMPLEMENTS tool-version:agent-skills@69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-15: official `main` HEAD와 published v1.0.0 spec을 manifest-only로 고정하고 package/MCP/security/platform/BAAB 경계를 `I2/V2`, Windows/Linux `P0`으로 기록.
