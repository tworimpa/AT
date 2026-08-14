---
id: tool-<stable-id>
type: tool-profile
title: <Tool name>
status: observed
tags:
  - knowledge-base
  - tool
official_upstream: <https://github.com/org/repo>
license: <SPDX-or-reviewed-text>
maintenance_status: <active|archived|unknown>
observed_at: <YYYY-MM-DD>
origin_integrity: <I0|I1|I2>
verification_ceiling: <V0|V1|V2|V3|V4|V5|V6>
windows_evidence: <W0|W1|W2|W3>
version_kind: <commit|tag|image|api>
version_ref: <full-sha-tag-digest-or-revision>
parent_repo_head: <full-parent-commit>
---

# <Tool name>

[지식 베이스 홈](../index.md) · [도구 카탈로그](../tools/catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

<지속되는 Tool의 주 역할. 기능 검증 문장과 도입 판단을 섞지 않는다.>

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | <URL> |
| 고정 버전 | `<full ref>` |
| 로컬 gitlink 또는 artifact | <repository-relative link> |
| 조사일 | <YYYY-MM-DD> |
| 출처 무결성 | <I grade와 근거> |
| license | <파일/URL locator와 재사용 주의> |

## 역할과 연동

- AgentRole: <Planner/Scheduler/Worker/...>
- Capability: <정규화된 capability ID 목록>
- Integration: <ACP/MCP/CLI/PTY/HTTP/...>
- SecurityOperationalRequirement: <충족·필요·위반 관계>

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | V | W | 결과·한계 |
|---|---|---|---|---|---|
| `<claim-id>` | <한 문장> | <fixed-SHA permalink 또는 상대 경로+line/anchor> | `<V0~V6>` | `<W0~W3>` | <pass/fail/partial/unknown과 limitation> |

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| 없음 | build/runtime/E2E를 실행하지 않았으면 명시 | unknown | 없음 | 없음 |

## 도입 판단

- 결정: <채택|파일럿|참고|보류|역사>
- 적용 범위: <직접 통합, 표준 사용, clean-room 패턴, 비교 대상 등>
- 이유: <Claim과 Evidence를 참조>
- 재검토 조건: <새 ToolVersion, V3/V4 pilot, license 변경 등>

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE AgentRole`
- `ToolVersion PROVIDES Capability`
- `ToolVersion SUPPORTS Integration`
- `Project SELECTS/EVALUATES/REJECTS ToolVersion`
- 새 버전이면 `ToolVersion SUPERSEDES <previous ToolVersion>`

## 변경 이력

- <YYYY-MM-DD>: <관찰·Claim·Evidence 변경과 provenance>
