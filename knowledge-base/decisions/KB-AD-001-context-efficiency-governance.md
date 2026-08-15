---
id: KB-AD-001
type: ArchitectureDecision
title: 지식 베이스의 점진적 조회, lifecycle과 검증 방식을 명시한다
status: accepted
decided_at: 2026-08-15
owner: project-requester
source_parent_commit: faad14543eba872834f9f5a321f0174c1e7d8788
verification_ceiling: V2
tags:
  - knowledge-base
  - architecture-decision
  - progressive-disclosure
  - lifecycle
  - validation
---

# KB-AD-001: 지식 베이스의 점진적 조회, lifecycle과 검증 방식을 명시한다

[지식 베이스 홈](../index.md) · [지속 컨텍스트](../ax-platform-context.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md) · [도구 프로필 템플릿](../templates/tool-profile.md)

## 결정 배경

외부 개선 제안은 frontmatter와 계층형 인덱스, 역할별 context slicing/MCP, 현재 SSOT와 역사 이력의 구분, 도구 메타데이터와 fallback의 기계 판독성, 저장소 검증 명령을 권고했다. 현재 저장소를 `faad14543eba872834f9f5a321f0174c1e7d8788`에서 정적 점검한 결과, 일부는 이미 구현돼 있고 일부는 운영 요구가 확인되지 않은 미래 확장이었다.

## 결정

| 제안 | 판단 | 적용 |
|---|---|---|
| 모든 문서 frontmatter와 L1→L2→L3 인덱스 | 부분 수용 | 기존 모든 KB Markdown의 YAML frontmatter와 `index.md` 요약 지도를 유지하고, 점진적 조회 순서와 lifecycle 의미를 인덱스에 명시한다. 모든 문서에 중복 `summary`를 일괄 추가하지 않는다. |
| context bundler와 KB MCP | 보류 | 현재는 repository-relative 링크와 선택적 파일 읽기가 기본이다. 반복되는 bundle 소비 계약이나 remote client의 query/권한 요구가 확인된 뒤 좁은 인터페이스로 설계한다. |
| SSOT와 이력 상태 분리 | 수용 | 문서 유형별 lifecycle enum을 정의하고 execution record를 `historical-snapshot`으로 표시한다. 현재 규칙과 충돌하면 active governance와 최신 accepted Decision을 우선한다. |
| 도구 메타데이터와 fallback | 부분 수용 | 신규·구조 갱신 프로필에 runtime/prerequisite, protocol, limit/timeout, fallback 조건과 capability/security/evidence loss를 기록한다. fallback은 자동 실행 권한이 아니다. |
| KB 검증 loop | 수용 | root `AGENTS.md`에 체크리스트와 `python3 scripts/validate_knowledge_base.py`를 추가한다. 검증 범위는 문서 구조 `V2`로 제한한다. |

## 수동 `catalog.json`을 두지 않는 이유

Markdown 프로필이 현재 source of truth이고 카탈로그·커버리지는 파생 인덱스다. 같은 사실을 Markdown과 JSON에 사람이 각각 편집하면 fixed SHA, 상태와 evidence grade가 서로 어긋날 수 있다. 따라서 JSON/JSONL은 기존 단계적 확장 계획대로 schema와 실제 질의가 안정된 뒤 Markdown에서 결정론적으로 생성하며 생성 파일은 수동 편집하지 않는다.

## Context bundler와 MCP의 도입 조건

다음 중 하나가 실제로 생기면 별도 결정으로 재검토한다.

- 동일한 역할·주제 bundle 요청이 반복되고 필요한 파일 집합과 최대 크기를 acceptance로 고정할 수 있음
- 저장소를 직접 읽지 못하는 remote agent/client와 갱신·캐시 무효화 계약이 필요함
- `search/get` 질의, caller identity, read scope, private source redaction, audit와 운영 owner가 정해짐
- 정적 파일 조회보다 server 운영·권한·버전 관리 비용이 낮다는 측정 근거가 있음

MCP를 도입하더라도 단순 검색 편의가 source authority를 바꾸지 않으며, 응답에는 문서 ID, revision 또는 commit, source locator와 lifecycle을 포함해야 한다.

## 결과와 한계

- 기존 35개 ToolVersion 프로필의 frontmatter나 본문을 일괄 변환하지 않는다. 신규·구조 갱신 문서부터 선택 제약을 적용하고 coverage에서 migration을 관리한다.
- 정적 validator는 YAML 구문, 공통 필드, lifecycle, 중복 ID와 내부 상대 링크만 검사한다. 외부 URL, Claim의 사실성, fixed-SHA 내용, build/runtime/E2E는 증명하지 않는다.
- 문서 수와 실제 검색 실패율, agent token 사용량을 측정하지 않았으므로 bundler/MCP의 효과를 수치로 주장하지 않는다.

## 재검토 조건

문서 schema를 새 major version으로 올리거나, 생성 JSON/JSONL·search service·MCP·외부 배포 bundle을 도입하거나, lifecycle enum이 새 문서 유형을 막을 때 재검토한다.
