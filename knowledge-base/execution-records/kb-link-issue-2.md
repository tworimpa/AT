---
id: execution-run-kb-link-issue-2
type: execution-record
title: "KB 링크 수집: hubble.md - 사람과 에이전트를 위한 협업 노트패드"
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
| submitted at | `2026-08-15T15:55:01+00:00` |
| workflow run | `31894056860` |

## 제출 메모

&#35;&#35;&#35; 링크
https://news.hada.io/topic?id=32516

&#35;&#35;&#35; 메모
실제 링크 수집·분석·판단·PR 또는 사유 댓글 경로를 검증합니다.

## 추가 판단 근거

사람과 AI 에이전트가 공동으로 작업할 수 있는 마크다운 및 HTML 기반의 오픈소스 노트 앱으로, 에이전트 폴더 연동 및 라이브 리로드 기능을 제공하여 사내 AX 플랫폼의 인간-에이전트 협업 인터페이스 및 작업 메모리 설계에 유용한 참고 자료가 됨.

## 간략 분석

hubble.md는 사람과 에이전트의 협업을 위해 설계된 마크다운/HTML 기반 오픈소스(MIT) 노트 앱입니다. Notion 스타일의 작성 경험, 에이전트 연동을 통한 실시간 라이브 리로드, 마크다운을 HTML 뷰(표, 지도 등)로 변환하는 기능 등을 제공하며 Electron 기반으로 크로스 플랫폼을 지원합니다.

### 핵심 내용

- 사람과 에이전트가 공유 폴더를 통해 협업하고 에이전트 편집 시 실시간 라이브 리로드 지원
- 마크다운 단축키, 프로퍼티, frontmatter 및 슬래시(/) 명령어 지원
- 마크다운 노트를 표, 책장, 지도 등의 HTML 앱 뷰로 변환하는 확장성 제공
- Electron 기반 데스크톱 앱으로 macOS, Windows, Linux 크로스 플랫폼 지원
- MIT 라이선스 기반의 오픈소스 프로젝트

### AX 지식 베이스 관련성

사내 AX 플랫폼의 '인간-에이전트 협업(Human-Agent Collaboration)', '로컬 관제 및 UI', '작업 메모리(Task Memory)' 영역에서 에이전트가 직접 읽고 쓸 수 있는 파일 기반 인터페이스 설계 패턴(Borrow)으로 활용 가능.

### 한계

- Electron 기반 데스크톱 앱으로 개별 클라이언트 설치 및 리소스 오버헤드 존재
- 에이전트와의 동기화가 로컬 파일 시스템 폴더 연동에 의존하여 다중 사용자 환경에서의 동시성 제어 한계
- 보안 및 권한 분리(RBAC/ABAC) 모델이 내장되어 있지 않아 사내 망분리 및 감사 요구사항에 맞춘 추가 설계 필요

## 실행·증거 경계

- provider: Google Gemini API
- requested model: `gemini-3.5-flash`; actual version/effort: `unknown`
- 모델은 제출된 URL과 저장소의 지속 컨텍스트·스키마를 읽도록 요청받았다.
- 결과는 모델 생성 분석 `V1`이며, source 내용의 정확성·고정 버전·라이선스·runtime은 검증하지 않았다.
- 자동 생성 PR은 사람 검토 전까지 승인된 지식이나 운영 증거가 아니다.
