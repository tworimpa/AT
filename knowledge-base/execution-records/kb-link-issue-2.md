---
id: execution-run-kb-link-issue-2
type: execution-record
title: "KB 링크 수집: hubble.md - 사람과 에이전트를 위한 마크다운/HTML 기반 협업 노트패드"
status: historical-snapshot
observed_at: 2026-08-15
profile_id: research-fast
profile_revision: 1
verification_ceiling: V1
source_url: "https://news.hada.io/topic?id=32516"
intake_decision: add
tags:
  - knowledge-base
  - execution-record
  - link-intake
  - gemini
---

# KB 링크 분석 기록

이 문서는 외부 링크를 Gemini로 분석한 시점의 자동 생성 스냅샷이다. 원문 주장과
모델 분석은 독립 검증되지 않았으며, 현재 규칙이나 승인된 결정의 source of truth가 아니다.

## Intake

| 필드 | 값 |
|---|---|
| source URL | <https://news.hada.io/topic?id=32516> |
| submission | <https://github.com/tworimpa/AT/issues/2> |
| submitter | `tworimpa` |
| repository | `tworimpa/AT` |
| submitted at | `2026-08-15T15:52:39+00:00` |
| workflow run | `31893948777` |

## 제출 메모

&#35;&#35;&#35; 링크
https://news.hada.io/topic?id=32516

&#35;&#35;&#35; 메모
실제 링크 수집·분석·판단·PR 또는 사유 댓글 경로를 검증합니다.

## 추가 판단 근거

사람과 AI 에이전트가 공유 워크스페이스를 통해 실시간으로 협업하는 새로운 UX 패턴을 제시하며, 크로스 플랫폼 지원 및 MIT 라이선스로 사내 AX 플랫폼의 협업 인터페이스 설계에 유용한 참고 자료가 됩니다.

## 간략 분석

hubble.md는 사람과 AI 에이전트가 함께 사용하도록 설계된 마크다운 및 HTML 기반 오픈소스 노트 앱입니다. 에이전트 연동을 통한 실시간 편집 및 라이브 리로드, 노트 폴더를 동적 HTML 뷰(표, 지도 등)로 변환하는 기능 등을 제공하며 Electron 기반으로 멀티 플랫폼을 지원합니다.

### 핵심 내용

- 사람과 에이전트의 공동 작성을 위한 마크다운 및 HTML 기반 오픈소스 노트 앱
- 에이전트 연동을 통한 실시간 노트 편집 및 라이브 리로드 협업 지원
- HTML 앱 뷰를 통해 노트 폴더를 표, 책장, 지도 등의 동적 뷰로 변환 가능
- Electron 기반 데스크톱 앱으로 macOS, Windows, Linux 크로스 플랫폼 지원
- MIT 라이선스 기반이며 자체 저장소는 Warp Factory 에이전트로 자동 운영됨

### AX 지식 베이스 관련성

사내 AX 플랫폼의 '로컬 관제 및 운영 UI', '사람-에이전트 협업', '공유 워크스페이스 및 컨텍스트 관리' 설계 시 에이전트의 작업 결과를 실시간 시각화하고 사람이 검증하는 인터페이스 설계 패턴으로 활용 가능합니다.

### 한계

- Electron 기반 데스크톱 앱으로 인한 로컬 시스템 리소스 소모 가능성
- HTML 앱 뷰 생성을 위해 별도 스킬 설치 및 코딩 에이전트 연동 필요
- 에이전트의 로컬 파일 시스템 접근에 대한 보안 격리 및 권한 제어 모델 검증 필요

## 실행·증거 경계

- provider: Google Gemini API
- requested model: `gemini-3.5-flash`; actual version/effort: `unknown`
- 모델은 제출된 URL과 저장소의 지속 컨텍스트·스키마를 읽도록 요청받았다.
- 결과는 모델 생성 분석 `V1`이며, source 내용의 정확성·고정 버전·라이선스·runtime은 검증하지 않았다.
- 자동 생성 PR은 사람 검토 전까지 승인된 지식이나 운영 증거가 아니다.
