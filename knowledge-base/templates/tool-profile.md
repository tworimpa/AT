---
id: tool-<stable-id>
type: tool-profile
title: <Tool name>
status: observed
profile_schema_version: 2
tool_key: <gitlink-basename>
tool_version_id: tool-version:<gitlink-basename>@<full-sha>
tags:
  - knowledge-base
  - tool
official_upstream: <https://github.com/org/repo>
license: <SPDX-or-reviewed-text>
maintenance_status: <active|archived|unknown>
observed_at: <YYYY-MM-DD>
upstream_default_branch: <branch-or-unknown>
upstream_head_observed: <full-sha-or-unknown>
upstream_checked_at: <YYYY-MM-DD>
origin_integrity: <I0|I1|I2>
verification_ceiling: <V0|V1|V2|V3|V4|V5|V6>
windows_evidence: <W0|W1|W2|W3>
version_kind: <commit|tag|image|api>
version_ref: <full-sha-tag-digest-or-revision>
parent_repo_head: <full-parent-commit>
source_management: <fixed-sha-submodule|manifest-only>
analysis_snapshot_date: <YYYY-MM-DD>
---

# <Tool name>

[지식 베이스 홈](../index.md) · [AX 플랫폼 지속 컨텍스트](../ax-platform-context.md) · [도구 카탈로그](../tools/catalog.md) · [프로필 커버리지](../tools/coverage.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

<지속되는 Tool의 주 역할. 기능 검증 문장과 도입 판단을 섞지 않는다.>

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | <URL> |
| 기본 브랜치와 조사일 HEAD | <branch> / `<full SHA>` (<YYYY-MM-DD>) |
| 고정 버전 | `<full ref>` |
| pin과 최신 관찰 관계 | <same|ahead|diverged|unknown; fixed profile은 자동 갱신하지 않음> |
| 로컬 gitlink 또는 artifact | <repository-relative link> |
| 조사일 | <YYYY-MM-DD> |
| 출처 무결성 | <I grade와 근거> |
| license | <fixed-SHA LICENSE/NOTICE locator, component 예외와 재사용 주의> |
| provenance limitation | <local body를 읽었는지, official fixed tree/API만 읽었는지, 미수행 범위> |
| source 관리 | <fixed-SHA submodule 또는 versioned manifest와 선택 이유> |

## 기술 구조

| 구성 요소 | 책임 | 상태·데이터 흐름 | fixed-SHA 근거 |
|---|---|---|---|
| <component> | <responsibility> | <state/input/output> | <immutable file URL+line/anchor> |

## 역할과 연동

- AgentRole: <Planner/Scheduler/Worker/...>
- Capability: <정규화된 capability ID 목록>
- Integration: <ACP/MCP/CLI/PTY/HTTP/...>
- SecurityOperationalRequirement: <충족·필요·위반 관계>

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | 공식 최신 근거·조사일 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|---|
| `<claim-id>` | <capability|architecture|interface|security|platform|limitation> | <한 문장> | <canonical URL+heading+date 또는 없음> | <40-SHA permalink+file line/anchor> | `<I0~I2>` | `<V0~V6>` | `<W0~W3>` | <pass/fail/partial/unknown과 limitation> |

## Interface와 protocol

| 표면 | transport·format | 방향·수명주기 | auth·permission 경계 | fixed-SHA 근거 |
|---|---|---|---|---|
| <CLI/API/ACP/MCP/PTY/...> | <protocol> | <caller→callee, session/run identity> | <authority and approval> | <immutable locator> |

## 운영·보안·trust boundary

- 보호 자산과 authority: <code, credential, repository, external write 등>
- 격리·credential·network·persistence 경계: <confirmed source와 unknown 분리>
- UI·agent 자기보고·upstream CI는 derived projection 또는 V1/V2 source일 뿐 완료 증거가 아니다.

## 플랫폼과 Windows

- control client, agent host, sandbox guest/server를 분리해 기록한다.
- WSL·Docker·remote Linux guest를 native Windows runtime으로 표현하지 않는다.
- `W1+`에는 Windows 전용 fixed-SHA locator 또는 실행 artifact가 필요하다.

## Evidence

| Evidence ID | 단계 | 고정 버전 | 방법·명령·exit | environment fingerprint | 결과 | artifact locator | 지원·반증 Claim | limitation |
|---|---|---|---|---|---|---|---|---|
| `v3plus-none` | `V3~V6` | `<full ref>` | build/runtime/E2E 미실행 | unknown | unknown | 없음 | 없음 | 정적 분석을 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: <Claim ID를 참조한 적용 범위 한정 문장>
- 확인된 한계: <limitation Claim ID와 근거>
- 미확인·추론: <없음의 증거로 표현하지 않고 unknown으로 기록>

## AX 설계 재료

이 표는 특정 도구의 최종 도입·구매 결론이 아니라 사내 AX 플랫폼을 설계하기 위한 재료다. 회사 업종, 데이터 분류, 규정, 망분리와 승인 체계가 정해지지 않은 부분은 추정하지 않고 `unknown` 또는 Decision Item으로 남긴다.

| 구분 | 패턴·capability | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | <직접 참고할 패턴> | `<claim-id>` | `<ax-need-id>` |
| Adapt | <조건부로 변형할 패턴> | `<claim-id>` | <조직·보안·Windows 조건> |
| Avoid | <가져오지 않을 패턴·위험> | `<claim-id>` | <위험과 fail-closed 이유> |
| Build | <우리 플랫폼에서 직접 구현할 capability> | `<claim-id>` | `<architecture-decision 또는 roadmap item>` |

## 도입 판단

- 결정: <채택|파일럿|참고|보류|역사>
- 성격: 사내 AX reference architecture를 위한 잠정 설계 재료이며 최종 vendor selection이 아님
- 적용 범위: <직접 통합, 표준 사용, clean-room 패턴, 비교 대상 등>
- 이유: <Claim과 Evidence를 참조>
- 재검토 조건: <새 ToolVersion, V3/V4 pilot, license 변경 등>

## 다음 검증

| Item ID | 대상 Claim | 목표 V/W | 환경 | 명령·시나리오 | pass 기준 | 보존 artifact | 승인·의존성 |
|---|---|---|---|---|---|---|---|
| `<item-id>` | `<claim-id>` | `<V3/W2 등>` | <fingerprint 계획> | <재현 가능한 단계> | <관찰 가능한 결과> | <log/report/path> | <human/external/cost gate> |

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE AgentRole`
- `ToolVersion PROVIDES Capability`
- `ToolVersion SUPPORTS Integration`
- `Project SELECTS/EVALUATES/REJECTS ToolVersion`
- 새 버전이면 `ToolVersion SUPERSEDES <previous ToolVersion>`

## 변경 이력

- <YYYY-MM-DD>: <관찰·Claim·Evidence 변경과 provenance>
