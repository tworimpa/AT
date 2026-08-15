---
id: kb-home
type: index
title: AI 에이전트 지식 베이스
status: active
aliases:
  - AI Tool Knowledge Base
tags:
  - knowledge-base
  - ai-agent
  - index
observed_at: 2026-08-14
source_parent_commit: 55227696af0ba94b934187876c6db6669dd2b574
---

# AI 에이전트 지식 베이스

이 디렉터리는 34개 AI 에이전트 도구·서비스의 조사 결과와 앞으로의 실험 증거를 Obsidian에서 계속 연결해 가는 저장소 내 지식 베이스다. 상세 분석과 요구사항은 기존 `planning/` 문서를 원본으로 유지하고, 여기서는 도구·역할·기능·출처·검증 상태 사이의 탐색 경로와 현재 결정을 제공한다.

## 지금 확인된 상태

| 항목 | 현재 상태 | 해석 |
|---|---|---|
| 조사 대상 | 34개 Tool, 34개 고정 ToolVersion | `.gitmodules`와 gitlink가 공식 upstream과 commit SHA를 고정한다. |
| 부모 기준점 | `caaae4a47a127808eedac657c394b6a8fd9be460` | Paseo 추가 조사와 지식 베이스 갱신을 시작할 때 읽은 로컬 `main` 스냅샷이다. |
| 출처 무결성 | 34/34 `I2` | 공식 upstream 확인과 fixed SHA gitlink 무결성까지 확인했다. |
| 기능 검증 | 최대 `V2` | 문서·고정 SHA 소스의 정적 분석까지다. 의존성 설치와 전체 build는 수행하지 않았다. |
| 실행 검증 | `V3+` evidence 0건 | build, 통제 runtime, E2E/failure injection, 운영 검증은 아직 없다. |
| 플랫폼 검증 | 최대 정적 `P1` | 기존 Windows 조사는 최대 legacy `W1`이며 실제 Windows/Linux native 실행(`P2`)과 플랫폼별 회귀 suite(`P3`)는 없다. Linux 지원 매트릭스는 아직 체계적으로 작성되지 않았다. |

`I2`, legacy `W1` 또는 플랫폼 `P1`은 `V3+`를 뜻하지 않는다. 출처가 정확하거나 특정 OS 코드가 존재해도 그 OS에서 빌드·실행·통합이 성공했다고 주장하지 않는다.

## 탐색 지도

- [AX 플랫폼 지속 컨텍스트](./ax-platform-context.md): 다음 세션이 먼저 읽을 목표, 현재 상태, 금지된 가정, 미결정과 다음 안전 단계
- [AX-AD-001 Cross-platform core 결정](./decisions/AX-AD-001-cross-platform-core.md): Windows와 Linux native executor를 모두 core로 두는 승인된 플랫폼 범위와 아직 미결인 support matrix
- [사내 AX reference architecture](./internal-ax-reference-architecture.md): Windows/Linux native를 포함한 cross-platform 계층 구조, 최소 코어·확장 옵션, Capability→AX Need→결정·로드맵 연결
- [34개 도구 역할·도입 카탈로그](./tools/catalog.md): 역할별 조사 목록, 공식 upstream, 고정 SHA, 도입 판단과 현재 증거 등급
- [34개 ToolVersion 프로필 커버리지](./tools/coverage.md): schema v2 프로필·필수 섹션·provenance·legacy `I/V/W`와 template v3 플랫폼 evidence 이관 현황
- [Paseo 고정 ToolVersion 프로필](./tools/paseo.md): multi-provider control plane, protocol, Windows 정적 근거와 명시적 한계
- [에이전트 실행 프로파일](./agent-profiles.md): 역할과 분리된 모델 등급·effort·권한·예산·증거·escalation 정책
- [공통 에이전트 운영 규칙](../AGENTS.md): 모든 작업에 지속 적용되는 범위·권한·증거·완료 보고 규칙
- [Cross-platform 에이전트 플랫폼 청사진](./platform-blueprint.md): 목표 구조, 에이전트 역할, 우선 로드맵과 결정 게이트
- [지식 베이스 규칙과 최소 지식 그래프 스키마](./knowledge-graph-schema.md): 노드·관계·provenance, `I/V`와 OS별 `P` 축, 새 도구 추가 절차
- [도구 프로필 템플릿](./templates/tool-profile.md): 새 ToolVersion을 같은 형식으로 기록하는 시작점
- [2026-08-14 프로필 통합 실행 기록](./execution-records/2026-08-14-tool-profile-integration.md): profile/model/environment, 정적 validation과 미실행 경계
- [2026-08-15 cross-platform 정합화 실행 기록](./execution-records/2026-08-15-cross-platform-scope-alignment.md): Windows/Linux core 결정, schema/template 전환, 정적 validation과 미실행 경계

## 원본 근거

- [34개 저장소 코드·GitHub 분석](../planning/REPOSITORY_GITHUB_ANALYSIS.md): 저장소별 구조, fixed-SHA source permalink, 설계 원칙과 라이선스 판단
- [도구·서비스 landscape](../planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md): 시장 범위, build/integrate/buy 판단과 pilot gate
- [멀티 에이전트 오케스트레이션 기획](../planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md): 상태 모델, scheduler, executor, evidence와 Phase 0~5
- [개발 환경 요구사항](../planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md): 기능·비기능 요구사항과 acceptance scenario
- [고정 소스 스냅샷 인덱스](../multi-agent-tools/README.md): 34개 gitlink, 라이선스, Windows 메모와 clone 기준점

## 읽는 순서

1. [지속 컨텍스트](./ax-platform-context.md)에서 목표, 현재 상태와 금지된 가정을 확인한다.
2. 도구를 찾을 때는 [카탈로그](./tools/catalog.md)와 [커버리지](./tools/coverage.md)에서 역할, 설계 재료와 누락을 확인한다.
3. 제품에 넣을 기능은 [reference architecture](./internal-ax-reference-architecture.md)와 [청사진](./platform-blueprint.md)의 결정·단계·acceptance에 연결한다.
4. 문서상 주장과 실제 증거는 [스키마](./knowledge-graph-schema.md)의 `Claim → SourceArtifact → Evidence` 구조로 기록한다.
5. 실행할 때는 [프로파일 카탈로그](./agent-profiles.md)에서 권한과 증거 요구를 선택하고 실제 model/version·effort·환경·cost/latency 관찰을 기록한다.
6. 새 자료는 기존 ToolVersion을 덮어쓰지 않고 새 버전과 `SUPERSEDES` 관계를 추가한다.

## 현재 경계

이 지식 베이스는 조사와 설계의 현재 상태를 설명한다. green 정적 검사나 gitlink 일치는 도구 설치, Windows/Linux native 실행, sandbox 격리, 실제 에이전트 작업 완료, 외부 서비스 가용성 또는 production 적합성을 증명하지 않는다. 실패·부분 성공·미확인도 성공 증거와 같은 수준으로 보존한다.
