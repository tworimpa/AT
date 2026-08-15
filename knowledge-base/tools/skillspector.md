---
id: tool-skillspector
type: tool-profile
title: NVIDIA SkillSpector
status: observed
profile_schema_version: 3
tool_key: skillspector
tool_version_id: tool-version:skillspector@5680c2c3008e63c9979bbbe08221ee4c2dcd17ee
tags:
  - knowledge-base
  - tool
  - skill-security
  - supply-chain
  - evidence
official_upstream: https://github.com/NVIDIA/SkillSpector
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: main
upstream_head_observed: 5680c2c3008e63c9979bbbe08221ee4c2dcd17ee
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
platform_evidence:
  windows: P0
  linux: P1
version_kind: commit
version_ref: 5680c2c3008e63c9979bbbe08221ee4c2dcd17ee
parent_repo_head: 91d6d075d53185667e20996cc94ec7e10537d02c
source_management: manifest-only
analysis_snapshot_date: 2026-08-15
---

# NVIDIA SkillSpector

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](./catalog.md) · [프로필 커버리지](./coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

agent skill과 연관 code·manifest·MCP metadata를 설치 전에 정적·선택적 semantic analyzer로 검사하고, finding뿐 아니라 검사 누락·실패를 ledger로 보고하는 skill 공급망 보안 gate다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | https://github.com/NVIDIA/SkillSpector |
| 기본 브랜치와 조사일 HEAD | `main` / `5680c2c3008e63c9979bbbe08221ee4c2dcd17ee` (2026-08-15) |
| 고정 버전 | `5680c2c3008e63c9979bbbe08221ee4c2dcd17ee` |
| pin과 최신 관찰 관계 | 조사 시점 default-branch HEAD와 동일; 이후 upstream 변경은 이 프로필에 소급하지 않음 |
| 로컬 gitlink 또는 artifact | gitlink 없음; official GitHub metadata와 fixed-SHA file/tree API를 읽고 permalink를 보존 |
| 조사일 | 2026-08-15 |
| 출처 무결성 | `I2`: NVIDIA verified GitHub 조직의 official upstream, default branch, full HEAD SHA와 fixed license/source를 확인 |
| 플랫폼 증거 | Windows `P0/unknown`; Linux `P1/partial` — fixed Docker 사용 경로가 Debian Linux image를 명시하지만 build/runtime하지 않음 |
| license | [fixed-SHA LICENSE](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/LICENSE#L1-L9): Apache-2.0; bundled YARA corpus, optional provider와 dependency license 전수 검토는 미수행 |
| provenance limitation | official fixed-SHA README, package manifest, MCP server, inspection ledger, analyzer tree를 정적으로 읽음; clone, install, rule 실행, OSV/LLM/provider 호출, build/runtime와 native OS 실행은 미수행 |
| source 관리 | `manifest-only`: 현재는 skill security/evidence 설계 비교 대상이며 adapter/reference implementation 직접 채택은 미결정. fixed-SHA source locator로 충분하고 submodule 전환은 통합 결정 뒤 재검토 |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| Input resolution/ingest | Git URL, file URL, zip, Markdown, directory를 작업 공간으로 해석하고 크기·member cap 적용 | target → bounded download/clone/extract → component inventory 또는 fail-closed ingest error | [input and limits](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L130-L154) |
| Analyzer graph | pattern/YARA/AST/taint/MCP 분석과 선택적 LLM semantic analysis를 단계화 | components → static findings → optional semantic/meta analysis → dedupe/report | [features](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L24-L31), [graph source](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/graph.py#L1-L80) |
| Inspection ledger | analyzer/path/range별 terminal outcome와 allowlisted omission/failure reason 기록 | planned work + events → completeness, exceptions, execution_successful | [ledger types](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/inspection_ledger.py#L19-L85), [completeness contract](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/inspection_ledger.py#L171-L185) |
| Reporting/baseline | risk finding을 terminal, JSON, Markdown, SARIF로 투영하고 fingerprint/glob suppression 적용 | findings + ledger + suppression → report/verdict; known finding과 new finding 분리 | [output and baseline](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L156-L199) |
| MCP server | 하나의 `scan_skill` tool로 scan verdict와 completeness/mode를 제공 | MCP stdio/HTTP caller → scan graph → structured result → cleanup | [MCP surface](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L303-L348), [server result](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/mcp_server.py#L137-L170) |

## 역할과 연동

- AgentRole: Skill Intake Scanner, Security Reviewer Assistant, Evidence Producer, CI/Install Gate Advisor; package approver나 sandbox executor 자체는 아님.
- Capability: `preinstall-skill-scanning`, `multi-engine-static-analysis`, `optional-semantic-analysis`, `inspection-completeness-ledger`, `finding-baseline`, `sarif-reporting`, `mcp-scan-gate`.
- Integration: CLI, Python package, MCP stdio/streamable HTTP, JSON/Markdown/SARIF, Git/URL/archive/directory input, optional OSV·LLM providers.
- SecurityOperationalRequirement: untrusted input 격리, bounded ingest, deny-by-default network, provider credential audience, immutable source/version, baseline approval provenance, scanner/tool version binding과 independent human/verifier review가 필요하다.

## 실행 선택 제약

| 항목 | 값 | 근거·시점·한계 |
|---|---|---|
| Runtime / prerequisites | Python `>=3.12`; CLI 기본 설치, MCP는 optional `mcp` extra; LLM semantic analysis는 선택 provider credential/network 필요; Docker 경로는 Python 3.12 slim-bookworm | [pyproject](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/pyproject.toml#L8-L23), [installation/Docker](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L37-L116) |
| Supported protocols / surfaces | CLI, MCP stdio, MCP streamable HTTP; terminal/JSON/Markdown/SARIF output; Git/URL/zip/file/directory input | [usage/output](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L119-L174), [MCP](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L303-L348) |
| Rate limits | scanner core 고정 서비스 limit `unknown`; OSV와 LLM provider limit은 외부 서비스/계정별, batch concurrency는 계정 limit과 충돌 가능 | [batch/provider note](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L176-L191); 2026-08-15 provider quota 미조회 |
| Timeout / retry | remote ingest byte/member cap은 확인; 공통 end-to-end timeout, provider retry, Git clone timeout의 고정 계약은 이번 조사에서 `unknown` | [ingest caps](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L137-L154); missing/failed work는 ledger와 scan mode로 별도 판정 필요 |
| Fallback candidates | `cisco-ai-skill-scanner`, `promptfoo` | Cisco 후보는 유사 multi-analyzer scanner이나 별도 profile/검증 필요; Promptfoo는 runtime red-team/eval에 강하지만 artifact 정적 inspection ledger의 동등 대체가 아님. 권한·provider·evidence 차이를 검토 후 수동 선택 |

fallback은 호환성·권한·안전성 보장이 아니라 검토 후보다. 전환으로 external write, credential audience, 데이터 경계, 비용 또는 검증 등급이 바뀌면 자동 선택하지 않고 새 capability/policy 협상과 필요한 승인을 거친다.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | 플랫폼별 P | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `ss-c1-layered-analysis` | architecture | scanner는 17개 범주의 pattern/YARA/AST/taint/MCP 정적 분석과 선택적 LLM semantic evaluation을 2단계로 제공한다. | [official README](https://github.com/NVIDIA/SkillSpector#features), 2026-08-15 | [README lines 24–31](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L24-L31), [analyzer tree](https://github.com/NVIDIA/SkillSpector/tree/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/nodes/analyzers) | `I2` | `V2` | `windows:P0; linux:P1` | 구현 경로 확인; 69 pattern coverage·precision·semantic 품질은 runtime 미검증 |
| `ss-c2-completeness-ledger` | architecture | analyzer/path/range의 terminal outcome과 omission/failure reason을 typed ledger로 모아 scan completeness와 execution_successful을 별도 계산한다. | 없음 | [ledger outcome/reason](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/inspection_ledger.py#L19-L85), [completeness fields](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/inspection_ledger.py#L171-L185) | `I2` | `V2` | `windows:P0; linux:P1` | fail/skip/coverage accounting 정적 확인; crash·concurrency·tamper failure injection 없음 |
| `ss-c3-bounded-ingest` | security | remote/archive ingest는 100 MiB와 zip 10000-member cap을 적용하며 초과 시 ingest error로 실패한다. | [official README](https://github.com/NVIDIA/SkillSpector#size-limits), 2026-08-15 | [README lines 137–154](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L137-L154) | `I2` | `V2` | `windows:P0; linux:P1` | 문서·source 경로 확인; zip traversal, symlink, clone amplification과 disk exhaustion runtime 미검증 |
| `ss-c4-evidence-baseline` | capability | exact fingerprint baseline은 source나 scanner version 변화 때 finding을 active로 유지하며 suppressed finding을 score에서 분리한다. | [official suppression docs](https://github.com/NVIDIA/SkillSpector#suppressing-false-positives-baseline), 2026-08-15 | [README lines 193–227](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L193-L227) | `I2` | `V2` | `windows:P0; linux:P1` | evidence-bound suppression 설계 확인; baseline 승인자·서명·tamper control은 별도 필요 |
| `ss-c5-mcp-verdict` | interface | MCP `scan_skill`은 risk/severity/recommendation/safe_to_install/findings와 execution/completeness, LLM 사용 여부를 구조화해 반환한다. | [official README](https://github.com/NVIDIA/SkillSpector#mcp-server), 2026-08-15 | [README lines 327–340](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L327-L340), [result fields](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/mcp_server.py#L137-L170) | `I2` | `V2` | `windows:P0; linux:P1` | `safe_to_install`은 scanner-derived recommendation이며 인증·human approval·runtime safety proof가 아님 |
| `ss-c6-http-trust-boundary` | limitation | MCP HTTP transport는 인증 없이 제공되며 HTTP caller의 local path/file URL은 거부하지만 routable bind는 외부 인증 proxy가 필요하다. | [official README](https://github.com/NVIDIA/SkillSpector#mcp-server), 2026-08-15 | [README lines 342–351](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L342-L351), [transport policy](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/mcp_server.py#L170-L226) | `I2` | `V2` | `windows:P0; linux:P1` | local-file read surface는 좁히지만 network auth, tenant isolation, quota/DoS를 제공하지 않음 |
| `ss-c7-analysis-mode-honesty` | security | MCP result는 LLM requested/available/used와 `static-only`/`static+llm` mode를 구분해 degraded semantic analysis를 표시한다. | [official README](https://github.com/NVIDIA/SkillSpector#mcp-server), 2026-08-15 | [README lines 327–340](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L327-L340), [mode fields](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/mcp_server.py#L153-L165) | `I2` | `V2` | `windows:P0; linux:P1` | 표시 계약 확인; downstream이 static-only를 allow로 해석하지 않는 policy gate 필요 |
| `ss-c8-platform-boundary` | platform | fixed Docker path는 Python 3.12 slim-bookworm Linux guest를 명시하지만 Windows native 지원 근거는 제공하지 않는다. | [official README](https://github.com/NVIDIA/SkillSpector#docker-no-python-required), 2026-08-15 | [README lines 82–116](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L82-L116) | `I2` | `V2` | `windows:P0; linux:P1` | Linux guest 정적 path만 partial; Linux host/Windows native build·runtime 미실행 |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| CLI | local process; target path/URL + terminal/JSON/Markdown/SARIF | operator/CI → one scan → report/output file → cleanup | shell identity의 filesystem/network/provider credential을 상속; scan이 install 권한을 갖지 않도록 분리 필요 | [basic usage/output](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L119-L174) |
| MCP stdio | FastMCP stdio, structured dict | local MCP client → long-lived server → per-call scan/cleanup | local client와 같은 trust boundary; local targets 허용 | [MCP transport](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L303-L340), [server run](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/src/skillspector/mcp_server.py#L210-L226) |
| MCP HTTP | FastMCP streamable HTTP | remote/A2A caller → server → remote URL scan | built-in auth 없음; local/file target 차단만 확인, reverse proxy auth·TLS·tenant quota 필요 | [HTTP trust model](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L342-L351) |
| Reports | JSON/Markdown/SARIF/terminal | scan state → human/CI/IDE projection | finding severity/recommendation은 derived; source/scanner hash와 verifier binding 필요 | [output formats](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L156-L174) |
| External analysis | OSV HTTP, configured LLM/provider API or local agent CLI | analyzer → external/local model/service → finding or degraded status | credential, prompt/code disclosure, egress, provider retention과 cost policy 필요 | [provider configuration](https://github.com/NVIDIA/SkillSpector/blob/5680c2c3008e63c9979bbbe08221ee4c2dcd17ee/README.md#L229-L301) |

## 운영·보안·trust boundary

- 보호 자산과 authority: untrusted skill/code/archive, local filesystem, Git/network input, provider credential, scanned source sent to semantic service, YARA/rule corpus, suppression baseline, report/SARIF와 install/allow decision.
- scanner process, input staging directory, Git/download endpoint, OSV/LLM provider, MCP caller, reverse proxy, CI artifact store와 installer를 별도 trust domain으로 둔다. scan proposal과 실제 install/enable/write authority를 결합하지 않는다.
- bounded ingest와 local-target rejection은 sandbox, malware containment, network authentication 또는 tenant isolation의 대체가 아니다. archive/symlink/process/network failure injection 뒤에만 enforcement 보장으로 승격한다.
- `safe_to_install`, risk score, green SARIF, static-only low score와 upstream CI는 derived signal이다. inspection completeness, source/scanner version, independent verifier와 human/policy approval 없이 안전 인증으로 읽지 않는다.

## 플랫폼

- Linux `P1/partial`: fixed README의 Debian 기반 Docker guest path를 확인했으나 image build/scan을 실행하지 않았다. container guest 증거를 Linux host-native로 확대하지 않는다.
- Windows `P0/unknown`: Python package라는 사실만으로 Windows native support를 추정하지 않는다. Windows CI/source contract와 native artifact를 이번 조사에서 확인하지 않았다.
- WSL·Docker·remote LLM/OSV 실행은 Windows native 또는 Linux host-native scanner evidence로 승격하지 않는다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `ss-v2-source-20260815` | `V2` | `5680c2c3008e63c9979bbbe08221ee4c2dcd17ee` | official GitHub repository/commit/tree/file API inspection; local `rg` duplicate search, exit 0 | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; connector version unknown | official HEAD, Apache-2.0 license, architecture/interface/security/platform limits과 KB 비중복성 확인 | 이 프로필의 official fixed-SHA URL | `ss-c1`~`ss-c8` | clone·install·build·scan/provider runtime 미실행; connector read가 native OS evidence는 아님 |
| `v3plus-none` | `V3~V6` | 동일 | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: artifact install 전 multi-engine scan(`ss-c1`), 누락·실패를 clean finding과 분리하는 typed completeness ledger(`ss-c2`, `ss-c7`), evidence-bound baseline(`ss-c4`)이 기존 KB의 skill supply-chain gate 공백을 채운다.
- 확인된 한계: `safe_to_install`은 derived verdict이고(`ss-c5`), HTTP는 unauthenticated이며(`ss-c6`), bounded ingest는 완전한 sandbox가 아니다(`ss-c3`).
- 미확인·추론: detection recall/precision, malicious archive containment, baseline tamper resistance, LLM/provider data retention, OSV/LLM outage behavior, Windows native와 Linux runtime은 unknown.

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | analyzer work를 terminal ledger outcome/reason/completeness로 투영하고 static/LLM mode를 명시 | `ss-c2`, `ss-c7` | Evidence layer의 incomplete/degraded fail-closed contract |
| Adapt | fingerprint baseline과 SARIF/MCP verdict를 source SHA·scanner SHA·rule pack·approval identity에 결합 | `ss-c4`, `ss-c5` | `AX-D003`, `AX-D008`, policy/verifier/human gate 필요 |
| Avoid | unauthenticated HTTP 공개, static-only low score 또는 `safe_to_install` boolean을 자동 install 권한으로 연결 | `ss-c5`, `ss-c6`, `ss-c7` | network auth·separation of duties·fail-closed 원칙 |
| Build | quarantined intake, signed scan receipt, rule/baseline provenance, scanner-independent negative fixture와 gated installer | `ss-c1`~`ss-c8` | `AD-PROP-009` guarded write, `RM-P4-threat-fixtures`, knowledge ingestion gate |

## 도입 판단

- 결정: 파일럿
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님.
- 적용 범위: skill artifact intake와 inspection completeness/evidence contract의 clean-room 참고; 현재 scanner/installer 직접 통합은 결정하지 않음.
- 이유: `ss-c1`~`ss-c4`, `ss-c7`은 현재 KB의 skill supply-chain/evidence 공백을 채우지만 `V2`, Windows `P0`, Linux `P1`이며 HTTP·provider·archive failure boundary가 미검증이다.
- 재검토 조건: fixed-SHA dependency/rule/license inventory, native OS V3, malicious corpus precision/recall, archive/network/provider failure injection, baseline/receipt tamper와 authenticated MCP deployment 검증.

## 다음 검증

| Item ID | 대상 Claim | 목표 V/P | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `ss-test-build-platforms` | `ss-c1`~`ss-c5`, `ss-c8` | `V3/windows:P2; V3/linux:P2` | 승인된 Windows/Linux native x86_64, Python 3.12 | fixed SHA install/build/unit + safe/malicious local fixture static scan | 두 OS에서 reproducible exit/result schema, completeness 100% 또는 명시적 exception | environment, lock/SBOM, test logs, report hash | dependency network 승인, `AX-D011` |
| `ss-test-ingest-failure` | `ss-c2`, `ss-c3` | `V5/linux:P2` | isolated no-secret filesystem/network sandbox | oversized stream, zip bomb/traversal/symlink, interrupted clone, unreadable/binary/large file | sandbox escape 0, bound 초과 fail-closed, 모든 planned work terminal ledger accounting | disk/network/process trace, ledger JSON | security review, synthetic corpus |
| `ss-test-provider-degrade` | `ss-c1`, `ss-c2`, `ss-c7` | `V5/linux:P2` | fake OSV/LLM endpoints | missing credential, timeout, malformed response, retry exhaustion, provider outage | scan mode/completeness가 degradation을 명시하고 policy가 full-scan requirement에서 deny | mock logs, result JSON, policy receipt | no external provider 우선; 비용 승인 시 별도 attempt |
| `ss-test-mcp-authz` | `ss-c5`, `ss-c6` | `V5/linux:P2` | loopback stdio와 authenticated reverse-proxy HTTP fixture | unauth caller, local/file URL, SSRF, concurrent DoS, cross-tenant request | unauth/local read/SSRF deny, quota와 tenant audit, installer authority 분리 | proxy/access log, packet trace, scan receipt | identity/TLS/tenant policy 결정 필요 |
| `ss-test-baseline-integrity` | `ss-c4`, `ss-c5` | `V5/linux:P2` | signed fixture repository | source/scanner/rule change, stale/tampered baseline, approval revoke | stale/tampered suppression active finding 유지, 승인 provenance 검증 | baseline diff, signature/receipt, SARIF | approval owner·key policy 필요 |

## 관계

- `Tool HAS_VERSION tool-version:skillspector@5680c2c3008e63c9979bbbe08221ee4c2dcd17ee`
- `ToolVersion FITS_ROLE SkillIntakeScanner/SecurityReviewerAssistant/EvidenceProducer`
- `ToolVersion PROVIDES preinstall-skill-scanning/multi-engine-static-analysis/inspection-completeness-ledger/finding-baseline/mcp-scan-gate`
- `ToolVersion SUPPORTS CLI/Python/MCP/JSON/Markdown/SARIF`
- `Project EVALUATES ToolVersion` as skill supply-chain gate pilot reference

## 변경 이력

- 2026-08-15: official `main` HEAD를 manifest-only immutable pin으로 등록하고 fixed-SHA `I2/V2`, Windows `P0`, Linux `P1` 분석을 추가함.
