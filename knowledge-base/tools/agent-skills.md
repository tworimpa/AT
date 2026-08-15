---
id: tool-agent-skills
type: tool-profile
title: Agent Skills
status: observed
profile_schema_version: 3
tool_key: agent-skills
tool_version_id: tool-version:agent-skills@69ef37e9424c0a7ea9dd2293b559e43ec8176379
tags: [knowledge-base, tool, agent-skills, procedural-knowledge, open-format]
official_upstream: https://github.com/agentskills/agentskills
license: "Apache-2.0 (code); CC-BY-4.0 (documentation)"
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 69ef37e9424c0a7ea9dd2293b559e43ec8176379
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P0
version_kind: commit
version_ref: 69ef37e9424c0a7ea9dd2293b559e43ec8176379
parent_repo_head: 91d6d075d53185667e20996cc94ec7e10537d02c
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# Agent Skills

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

`SKILL.md`와 선택적 script·reference·asset을 묶어 에이전트가 필요할 때 단계적으로 읽는 절차 지식을 이식 가능한 파일 패키지로 정의하는 공개 형식이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/agentskills/agentskills |
| 기본 브랜치와 조사일 HEAD | `main` / `69ef37e9424c0a7ea9dd2293b559e43ec8176379` (2026-08-15) |
| 고정 버전 | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` |
| pin과 최신 관찰 관계 | 조사 시점 default-branch HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; official upstream의 fixed-SHA tree·blob을 원격 정적 검사하고 이 manifest-only 프로필에 locator를 보존 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: 공식 Agent Skills 조직 저장소와 `git ls-remote --symref`의 `main` HEAD를 대조하고 fixed-SHA source를 직접 읽음 |
| 플랫폼 증거 | Windows `P0/unknown`, Linux `P0/unknown` — 형식은 플랫폼 중립을 지향하지만 client·script runtime을 어느 OS에서도 실행하지 않음 |
| license | [fixed-SHA Apache-2.0 LICENSE](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/LICENSE#L1-L4); 문서는 [CC-BY-4.0](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/README.md#L57-L59). 개별 skill과 bundled dependency license는 별도 검토 필요 |
| provenance limitation | clone·install 없이 official fixed-SHA README, specification, parser와 validator를 정적으로 읽음. client activation, script 실행, permission enforcement, Windows/Linux native 동작은 미검증 |
| source 관리 | `manifest-only`: 표준·문서 비교 대상이며 현재 adapter/reference implementation을 직접 채택하지 않음. client conformance 구현을 차용할 때 gitlink 전환 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Skill package | root `SKILL.md`와 선택적 `scripts/`, `references/`, `assets/`를 하나의 절차 지식 단위로 구성 | filesystem package → client discovery·activation → instruction/resource load | [format lines 10–32](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L10-L32) |
| `SKILL.md` metadata | `name`, `description`과 선택적 license·compatibility·metadata·allowed-tools를 선언 | YAML frontmatter → client discovery metadata; Markdown body → activated instructions | [frontmatter lines 19–55](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L19-L55) |
| Progressive disclosure | 전체 skill corpus를 한 번에 넣지 않고 metadata, instructions, resources 순으로 지연 로드 | startup metadata → task match activation → 필요한 resource만 읽음 | [progressive disclosure lines 216–237](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L216-L237) |
| `skills-ref` | YAML frontmatter parse와 이름·길이·필수 필드·허용 필드를 검증하는 reference library/CLI | local skill directory → parse/metadata validation → error list | [validator lines 14–22](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L14-L22), [validation lines 118–177](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L118-L177) |

## 역할과 연동

- AgentRole: Skill Author, Knowledge Curator, Skill Client/Loader; agent executor·scheduler·verifier 자체는 아님.
- Capability: `portable-procedural-knowledge`, `progressive-skill-disclosure`, `skill-metadata-discovery`, `skill-format-validation`.
- Integration: filesystem directory, Markdown+YAML frontmatter, optional local scripts/resources, `skills-ref` CLI/library; transport protocol이나 remote registry는 정의하지 않음.
- SecurityOperationalRequirement: publisher/source revision, package review·revoke, script integrity, explicit capability/permission gate, sandbox·egress·secret policy와 activation audit가 별도 필요하다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | 형식 자체는 runtime 없음; reference validator는 Python library/CLI와 YAML parser를 사용. bundled script의 Python/Bash/JavaScript 등 실제 요구사항은 skill별 선언에 의존 | [script runtime guidance](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L187-L198), [parser import](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/parser.py#L1-L8). Python 최소 버전·OS package·credential·network는 이번 조사에서 확정하지 않음 |
| Supported protocols / surfaces | filesystem `SKILL.md`, YAML frontmatter, Markdown instructions, relative resource references, `skills-ref validate` CLI | [file reference and validation](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L226-L247); remote distribution·MCP·HTTP·activation API는 이 형식의 범위 밖 |
| Rate limits | 해당 없음(local static format); hosted registry/client 한도는 unknown | fixed specification에 service rate-limit 계약 없음; 2026-08-15 |
| Timeout / retry | 형식 수준 값 없음; client와 bundled script가 별도 결정 | execution lifecycle을 표준화하지 않으므로 fail-closed 기본값으로 추정하지 않음 |
| Fallback candidates | `agent-plugins-spec` | [Agent Plugins profile](./agent-plugins-spec.md)은 skill을 `plugin.json` package와 MCP surface에 넣는 wrapper 후보다. client conformance·credential·subprocess 경계가 달라 자동 전환하지 않으며 별도 승인 필요 |

fallback은 호환성·권한·안전성 보장이 아니라 검토 후보다. 전환으로 external write, credential audience, 데이터 경계, 비용 또는 검증 등급이 바뀌면 자동 선택하지 않고 새 capability/policy 협상과 필요한 승인을 거친다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `askill-c1-package-contract` | interface | skill은 `SKILL.md`를 필수로 하고 scripts, references, assets를 선택적으로 포함하는 directory package다. | [official README](https://github.com/agentskills/agentskills#what-are-agent-skills), 2026-08-15 | [spec lines 10–32](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L10-L32) | `I2` | `V2` | `windows:P0; linux:P0` | 형식 정적 확인; 어느 client에서도 package load 미실행 |
| `askill-c2-progressive-disclosure` | architecture | client는 discovery metadata, activated instructions, on-demand resources의 세 단계로 context를 로드하도록 형식을 사용할 수 있다. | [official README](https://github.com/agentskills/agentskills#how-do-agent-skills-work), 2026-08-15 | [spec lines 216–224](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L216-L224) | `I2` | `V2` | `windows:P0; linux:P0` | 정보 구조 contract 확인; activation 정확도·token 절감·client 준수는 미검증 |
| `askill-c3-metadata-validation` | capability | reference validator는 필수 name/description, 허용 frontmatter field, 길이와 directory-name 일치를 검사한다. | [validation section](https://agentskills.io/specification#validation), 2026-08-15 | [validator lines 10–67](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L10-L67), [lines 118–177](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L118-L177) | `I2` | `V2` | `windows:P0; linux:P0` | 구현 경로 정적 확인; validator 설치·test 미실행 |
| `askill-c4-executable-content-boundary` | security | skill body에는 형식 제한이 없고 executable script를 포함할 수 있으며 `allowed-tools`는 experimental이다. | [official specification](https://agentskills.io/specification), 2026-08-15 | [allowed-tools/body lines 163–185](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L163-L185), [scripts lines 187–198](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L187-L198) | `I2` | `V2` | `windows:P0; linux:P0` | confirmed boundary; package conformance는 script 안전성·permission·sandbox를 보장하지 않음 |
| `askill-c5-validator-not-trust-gate` | limitation | reference validator는 metadata 구조를 검사하지만 body, script, publisher provenance, signature, capability effect를 심사하지 않는다. | 없음 | [validation implementation lines 118–177](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L118-L177), [body freedom](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L176-L198) | `I2` | `V2` | `windows:P0; linux:P0` | 정적 confirmed limitation; malicious-package failure test는 미실행 |
| `askill-c6-platform-runtime-outside-spec` | platform | format은 supported language와 execution behavior를 client implementation에 맡기므로 portable package가 Windows/Linux native 실행을 자동 증명하지 않는다. | [official specification](https://agentskills.io/specification#scripts), 2026-08-15 | [script support lines 191–198](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L191-L198) | `I2` | `V2` | `windows:P0; linux:P0` | 양쪽 OS runtime evidence unknown; compatibility metadata도 enforcement가 아닌 선언 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| Skill discovery | local filesystem directory + YAML frontmatter | client startup/index → name·description catalog | package read authority와 publisher trust는 client 책임 | [frontmatter contract](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L19-L55) |
| Skill activation | Markdown instructions | task match → full `SKILL.md` load → agent context | activation policy, prompt-injection defense와 instruction precedence는 client 책임 | [progressive disclosure](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L216-L224) |
| Resource/script access | relative filesystem path and client-selected interpreter/tool | activated skill → on-demand read or execution | `allowed-tools`는 experimental이며 OS process·network·secret 권한을 표준이 강제하지 않음 | [references/scripts](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx#L187-L237) |
| Reference validation | Python CLI/library | author/CI → parse/validate → errors | syntax·metadata gate일 뿐 trust/security approval이 아님 | [validator](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py#L118-L177) |

## 운영·보안·trust boundary

- 보호 자산과 authority: skill instructions, bundled executable·template, repository/workspace, client tool authority, network/secret/credential, publisher identity와 installed revision이다.
- 형식 conformance와 신뢰를 분리한다. `SKILL.md`가 valid해도 script·instruction의 악성 동작, dependency supply chain, data exfiltration 또는 destructive action이 안전하다는 뜻이 아니다(`askill-c4`, `askill-c5`).
- progressive disclosure는 context 사용량을 구조화하지만 authorization이나 prompt-injection isolation이 아니다. activation 시 source revision, reviewer, granted capability, data scope와 실행 receipt를 기록해야 한다.
- local package path, remote distribution, update/revoke, signature, sandbox, egress, secret injection과 audit store는 client 또는 사내 policy layer가 제공해야 한다.
- client UI의 “installed/valid/activated” 표시는 format·load 상태의 projection일 뿐 task 완료, script safety 또는 verification evidence가 아니다.

## 플랫폼

- specification은 language/runtime 지원을 client에 맡기며 이번 fixed SHA에서 Windows/Linux native conformance implementation을 확정하지 않았다. 따라서 양쪽 모두 `P0/unknown`이다.
- `compatibility`는 환경 요구를 기술하는 metadata이고 실제 dependency·network·OS 지원을 검증하거나 강제하지 않는다.
- WSL·container·remote guest에서 script가 실행돼도 Windows/Linux host-native 지원 근거로 자동 승격하지 않는다.
- 향후 client pilot은 같은 benign/malicious skill fixture를 Windows와 Linux native에서 각각 실행하고 process, path, permission, network와 cleanup artifact를 별도로 보존해야 한다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `askill-v2-source-20260815` | `V2` | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | `git ls-remote --symref`와 official fixed-SHA README/spec/parser/validator 원격 정적 inspection, 최종 exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; git 2.53.0 | official pin, license, format, progressive load와 validation/security boundary 확인 | 이 프로필의 official fixed-SHA locator | `askill-c1`~`askill-c6` | install/test/client runtime 미실행; 최초 sandbox DNS attempt exit 128 뒤 승인된 read-only network로 재시도 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: `askill-c1`, `askill-c2`가 팀 절차 지식을 작고 이식 가능한 package와 progressive retrieval 구조로 만든다. TencentDB Agent Memory의 skill asset registry와 달리 client 간 파일 contract를 설계 재료로 제공한다.
- 확인된 한계: `askill-c4`, `askill-c5` 때문에 schema-valid skill도 executable content·publisher·permission 관점에서 untrusted다. `askill-c6`은 portable format과 native runtime 지원을 분리한다.
- 미확인·추론: client 간 semantic compatibility, activation precision, context 절감량, malicious skill 저항, update/revoke propagation, Windows/Linux native parity는 unknown이다.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | 최소 `SKILL.md` contract와 metadata→instructions→resources progressive disclosure | `askill-c1`, `askill-c2` | `AD-PROP-010` fixed-version knowledge provenance와 context-efficient retrieval |
| Adapt | skill metadata에 immutable publisher/source revision, owner, review/revoke, data classification과 capability request를 연결 | `askill-c3`, `askill-c5` | `AX-D002`, `AX-D003`, `AX-D008`, `AX-D012` 결정 필요 |
| Avoid | format validation 또는 `allowed-tools` 선언을 code safety·authorization·native compatibility proof로 사용 | `askill-c4`~`askill-c6` | prompt/script supply-chain과 fail-open permission 방지 |
| Build | signed skill registry, review/revoke/quarantine, activation audit, sandboxed script runner와 Windows/Linux conformance fixture | `askill-c1`~`askill-c6` | `RM-K1-generated-index`, `RM-K2-memory-plane-evaluation`과 policy/evidence layer 연계 |

## 도입 판단

- 결정: 참고
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: 사내 procedural knowledge/skill package contract와 progressive retrieval 표준의 clean-room 참고; 현재 reference validator 또는 client 직접 통합은 결정하지 않음.
- 이유: `askill-c1`과 `askill-c2`가 기존 TencentDB memory asset plane과 비중복인 portable file contract를 제공한다. 다만 `askill-c4`~`askill-c6`의 trust·runtime 공백 때문에 표준 채택과 안전한 실행은 분리해야 한다.
- 재검토 조건: 새 specification revision, license 변화, target client 선정, signed provenance·permission schema 결정, Windows/Linux `V3+/P2` conformance와 malicious package `V5` 결과.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `askill-test-validator` | `askill-c1`, `askill-c3` | `V3/windows:P2; linux:P2` | 결정된 Windows/Linux native Python 환경 | fixed SHA `skills-ref` build/test와 valid/invalid fixture validation | 양쪽 OS에서 동일 acceptance/error class, dependency lock와 exit 0 | environment fingerprint, dependency lock, test log | dependency download 승인 |
| `askill-test-client-load` | `askill-c2`, `askill-c6` | `V4/windows:P2; linux:P2` | 승인된 target agent client | metadata-only discovery, activation, resource on-demand load와 unsupported runtime fixture | context load 단계와 source revision이 receipt에 기록되고 unsupported capability가 fail-closed | prompt/context trace, event receipt, resource access log | target client·data classification 결정 |
| `askill-test-malicious-package` | `askill-c4`, `askill-c5` | `V5/windows:P2; linux:P2` | isolated native executor와 synthetic secrets | path escape, prompt injection, undeclared tool/network, obfuscated exfiltration, revoke 중 실행 | policy deny, secret 비노출, revoke 후 신규 activation 차단, append-only audit | sandbox trace, deny log, secret canary report | security review·격리 환경 승인 |

## 관계

- `Tool HAS_VERSION tool-version:agent-skills@69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- `ToolVersion FITS_ROLE SkillAuthor/KnowledgeCurator/SkillClient`
- `ToolVersion PROVIDES portable-procedural-knowledge/progressive-skill-disclosure/skill-format-validation`
- `ToolVersion SUPPORTS filesystem/Markdown/YAML/skills-ref-CLI`
- `Project EVALUATES ToolVersion` as procedural knowledge package standard reference

## 변경 이력

- 2026-08-15: official `main` HEAD를 manifest-only immutable pin으로 등록하고 fixed-SHA `I2/V2`, Windows `P0`, Linux `P0` 프로필을 작성함. install/runtime/E2E와 외부 write는 미수행.
