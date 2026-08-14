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
source_parent_commit: caaae4a47a127808eedac657c394b6a8fd9be460
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
| Windows 검증 | 최대 `W1` | 일부 Windows 코드 경로를 정적으로 확인했지만 실제 실행(`W2`)과 회귀 suite(`W3`)는 없다. |

`I2`나 `W1`은 `V3+`를 뜻하지 않는다. 출처가 정확하거나 Windows 코드가 존재해도 빌드·실행·통합이 성공했다고 주장하지 않는다.

## 탐색 지도

- [34개 도구 역할·도입 카탈로그](./tools/catalog.md): 역할별 조사 목록, 공식 upstream, 고정 SHA, 도입 판단과 현재 증거 등급
- [Paseo 고정 ToolVersion 프로필](./tools/paseo.md): multi-provider control plane, protocol, Windows 정적 근거와 명시적 한계
- [Windows-first 에이전트 플랫폼 청사진](./platform-blueprint.md): 목표 구조, 에이전트 역할, 우선 로드맵과 결정 게이트
- [지식 베이스 규칙과 최소 지식 그래프 스키마](./knowledge-graph-schema.md): 노드·관계·provenance, `V/I/W` 축, 새 도구 추가 절차
- [도구 프로필 템플릿](./templates/tool-profile.md): 새 ToolVersion을 같은 형식으로 기록하는 시작점

## 원본 근거

- [34개 저장소 코드·GitHub 분석](../planning/REPOSITORY_GITHUB_ANALYSIS.md): 저장소별 구조, fixed-SHA source permalink, 설계 원칙과 라이선스 판단
- [도구·서비스 landscape](../planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md): 시장 범위, build/integrate/buy 판단과 pilot gate
- [멀티 에이전트 오케스트레이션 기획](../planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md): 상태 모델, scheduler, executor, evidence와 Phase 0~5
- [개발 환경 요구사항](../planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md): 기능·비기능 요구사항과 acceptance scenario
- [고정 소스 스냅샷 인덱스](../multi-agent-tools/README.md): 34개 gitlink, 라이선스, Windows 메모와 clone 기준점

## 읽는 순서

1. 도구를 찾을 때는 [카탈로그](./tools/catalog.md)에서 역할과 도입 판단을 확인한다.
2. 제품에 넣을 기능은 [청사진](./platform-blueprint.md)의 단계와 acceptance에 연결한다.
3. 문서상 주장과 실제 증거는 [스키마](./knowledge-graph-schema.md)의 `Claim → SourceArtifact → Evidence` 구조로 기록한다.
4. 새 자료는 기존 ToolVersion을 덮어쓰지 않고 새 버전과 `SUPERSEDES` 관계를 추가한다.

## 현재 경계

이 지식 베이스는 조사와 설계의 현재 상태를 설명한다. green 정적 검사나 gitlink 일치는 도구 설치, Windows 실행, sandbox 격리, 실제 에이전트 작업 완료, 외부 서비스 가용성 또는 production 적합성을 증명하지 않는다. 실패·부분 성공·미확인도 성공 증거와 같은 수준으로 보존한다.
