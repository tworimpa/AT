---
id: execution-run-gemini-direct-api-intake-2026-08-16
type: execution-record
title: Gemini 단일 REST 호출 링크 수집 전환 기록
status: historical-snapshot
observed_at: 2026-08-16
profile_id: implement-deep
profile_revision: 1
verification_ceiling: V2
tags:
  - knowledge-base
  - execution-record
  - github-actions
  - gemini
  - link-intake
---

# Gemini 단일 REST 호출 링크 수집 전환 기록

[지식 베이스 홈](../index.md) · [실행 프로파일](../agent-profiles.md) ·
[지속 컨텍스트](../ax-platform-context.md)

Gemini CLI의 내부 호출이 무료 API 요청 한도를 소진하던 경로를 제거하고, 링크 하나당
Gemini `generateContent` REST 요청을 정확히 한 번만 구성하도록 전환한 구현 기록이다.

## Run identity

| 필드 | 실제 기록 |
|---|---|
| task/run ID | `gemini-direct-api-intake-2026-08-16` |
| 역할·profile | worker / `implement-deep@1` |
| model provider·slug·version | OpenAI / `unknown` / `unknown` |
| requested/actual effort | `high` / `unknown` |
| 시작·종료 시각 | exact start `unknown`; local validation `2026-08-16T00:48:09+09:00` 이후 |
| base/head SHA | `6a1dc930bd75d8d896f854e9ed8fc837c84d9948` / uncommitted workspace |
| environment | Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; Python `3.14.4`; Git `2.53.0` |
| cost/latency | `unknown` / local checks only |

## 구현 결과

- `run-gemini-cli`와 Gemini CLI 설치·서브에이전트 경로를 제거했다.
- Python이 제출 URL의 HTML·text·JSON을 제한적으로 수집하고, KB 지속 컨텍스트·홈·도구
  카탈로그·스키마와 함께 단일 prompt를 만든다.
- 기본 모델은 무료 할당량 화면과 공식 REST 예시에 있는 `gemini-3.5-flash`이며,
  repository variable `GEMINI_MODEL`로 재정의할 수 있다.
- API 키는 query string이 아니라 `x-goog-api-key` header로만 전송한다.
- structured output JSON schema와 기존 renderer의 별도 schema 검사를 모두 적용한다.
- 소스 요청은 HTTPS, 기본 포트, 공개 DNS address, redirect 재검사, 1 MB 응답 제한과
  허용 content type을 fail-closed로 검사한다.

## 공식 API 계약

- [Gemini API reference](https://ai.google.dev/api)는 비대화형 작업에
  `generateContent` REST endpoint와 `x-goog-api-key` header를 설명한다.
- [GenerateContent reference](https://ai.google.dev/api/generate-content)는
  `responseJsonSchema`, JSON MIME type, candidate content 구조를 정의한다.

## Validation record

| 검사 | 결과·증거 범위 |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_kb_link_intake.py` | exit `0`; 10 tests. URL·prepare·add/skip 외에 HTML 정리, private DNS 거부, API 1회 호출과 key 비노출 검사 |
| `python3 -m py_compile ...` | exit `0`; Python syntax `V2` |
| PyYAML workflow parse와 직접 호출 assertion | exit `0`; 3 jobs, CLI 참조 없음, analyze 명령 1개, 기본 모델 확인 |
| `python3 scripts/validate_knowledge_base.py` | 중간 exit `0`; 58 Markdown. 이 기록 포함 최종 결과는 후속 검사에 기록 |
| `git diff --check` | 중간 exit `0` |

## Evidence and limitations

- 로컬 검증 상한은 정적 코드·fixture `V2`다. 실제 Gemini API, 외부 페이지, GitHub-hosted
  runner, Issue 댓글, branch push와 PR 생성은 이번 실행에서 호출하지 않았다.
- 모델 요청 수는 코드 경로와 mock call count로 1회임을 확인했지만 실제 provider가 quota를
  차감하는 방식, token 수와 모델 가용성은 `unknown`이다.
- DNS 검사와 실제 TLS 연결 사이의 rebinding 가능성을 stdlib 검사만으로 완전히 제거하지
  못한다. 신뢰된 repository 구성원만 자동 실행시키는 기존 gate를 유지한다.
- 소스 본문은 50,000자, 각 KB context는 20,000자로 잘리므로 전체 저장소 중복성 검사가
  아니라 제공된 index·catalog 범위의 자동 선별 판단이다.
- 외부 write, push, merge, 배포, credential 변경과 실제 비용 발생 호출은 수행하지 않았다.
