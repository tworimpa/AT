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
| base/first implementation SHA | `6a1dc930bd75d8d896f854e9ed8fc837c84d9948` / `47b3c8489ed3180bbeed1def9ddb47bc07e075c7` |
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

- 로컬 검증 상한은 정적 코드·fixture `V2`다. 후속 GitHub-hosted runner에서 외부 페이지와
  Gemini API 응답 저장까지 관찰했지만 Issue 결과 댓글과 PR 생성은 아직 실행되지 않았다.
- 모델 요청 수는 코드 경로와 mock call count로 1회임을 확인했다. 실제 run에서도 응답은
  저장됐지만 provider의 quota 차감 방식과 token 수는 `unknown`이다.
- DNS 검사와 실제 TLS 연결 사이의 rebinding 가능성을 stdlib 검사만으로 완전히 제거하지
  못한다. 신뢰된 repository 구성원만 자동 실행시키는 기존 gate를 유지한다.
- 소스 본문은 50,000자, 각 KB context는 20,000자로 잘리므로 전체 저장소 중복성 검사가
  아니라 제공된 index·catalog 범위의 자동 선별 판단이다.
- 승인 범위에서 `main` push와 Issue 상태 변경을 수행했다. merge, 배포와 credential 변경은
  수행하지 않았다. Gemini API의 실제 비용은 관찰하지 못해 `unknown`이다.

## GitHub Actions 재실행 관찰

- commit `47b3c8489ed3180bbeed1def9ddb47bc07e075c7`을 `main`에 push하고 Issue #2와
  #3을 닫았다가 다시 열었다.
- Issue #2 run `31893846690`은 source fetch와 단일 Gemini API 응답 저장까지 완료했으나,
  상대 `response_path`를 절대 `REPO_ROOT`에 바로 `relative_to`한 사후 로그 출력 결함으로
  exit `1`이 됐다. API 호출 실패나 quota 오류가 아니다.
- Issue #3 run `31893848795`는 사설 IP URL을 Gemini 호출 전에 거부해 예상대로 exit `1`이었다.
- 관찰된 결함은 상대 출력 경로를 `REPO_ROOT` 기준으로 정규화하고 동일 상대경로 fixture를
  추가해 수정한다. 수정 후 실제 정상 분기 E2E 결과는 후속 run에서 별도로 확인한다.

## 지식 후보 산출물 전환

PR #4 재검토에서 자동화가 `execution-record` 하나만 만들고 실제 source of truth인
`knowledge-base/tools/<tool>.md`와 탐색 index를 갱신하지 않아, 실행 추적 외에는 재사용 가능한
지식을 축적하지 못하는 결함을 확인했다.

- `add` 산출물을 template v3 형태의 `tool-profile`로 변경한다.
- profile과 함께 `knowledge-base/index.md`, `tools/catalog.md`, `tools/coverage.md`에 검토 후보
  연결을 추가한다.
- 모델이 제안한 GitHub URL은 공개 repository, default branch full HEAD SHA, license metadata를
  GitHub API로 재확인한다. repository URL 또는 repository homepage가 제출 원문에 연결되지
  않으면 모델 판단을 `skip`으로 강등한다.
- 자동 profile의 상한은 `I1/V1/windows:P0/linux:P0`로 제한한다. full SHA를 확보해도 Claim별
  fixed-SHA README·코드와 component license를 사람이 검토하기 전에는 `I2/V2`로 올리지 않는다.
- 신규 profile을 포함한 전체 KB diff를 staged binary patch artifact로 전달하고 publish job에서
  적용·재검증해 profile과 index가 한 PR에서 atomic하게 review되도록 한다.
- 링크 intake별 execution record 생성은 중단한다. 이 구현 기록은 자동화 자체의 변경·실패
  경계를 보존하는 별도 실행 증거다.
