# AT — AI coding agent tools research workspace


AI 코딩 에이전트 개발 환경, 멀티 에이전트 오케스트레이션, agent protocol, local/remote sandbox와 관련 서비스를 비교·기획하는 연구 workspace다.

## 구성

- [`knowledge-base/`](./knowledge-base/): Obsidian 탐색용 지식 베이스, 도구 카탈로그, 플랫폼 청사진, provenance·검증 규칙
- [`planning/`](./planning/): 도구·서비스 landscape, 소스/GitHub 분석, 오케스트레이션 기획, 신규 도구 요구사항
- [`multi-agent-tools/README.md`](./multi-agent-tools/README.md): 분석 대상 분류, 라이선스, 정확한 clone SHA
- `multi-agent-tools/<project>/`: 각 공식 upstream을 가리키는 Git submodule

부모 저장소는 문서와 조사 구성을 관리한다. 분석 대상 소스는 부모 저장소에 복제해 커밋하지 않고 submodule gitlink로 정확한 검토 SHA를 고정한다.

## Checkout

```powershell
git clone https://github.com/tworimpa/AT.git
Set-Location AT
git submodule update --init --recursive
```

빠른 소스 스냅샷만 필요하면 다음처럼 shallow submodule checkout을 시도할 수 있다.

```powershell
git submodule update --init --recursive --depth 1
```

upstream의 현재 HEAD가 아니라 이 저장소가 검토한 SHA를 재현하는 것이 기본 동작이다. `git submodule update --remote`는 카탈로그·라이선스·소스 분석을 함께 갱신할 때만 사용한다.

## 주요 문서

- [AI 에이전트 지식 베이스 홈](./knowledge-base/index.md)
- [AI 코딩 에이전트 도구·서비스 landscape](./planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md)
- [34개 저장소 코드·GitHub 분석](./planning/REPOSITORY_GITHUB_ANALYSIS.md)
- [빠른 멀티 에이전트 실행·오케스트레이션 기획](./planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md)
- [AI 에이전트 기반 개발 환경 요구사항](./planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md)
- [5개 공식 에이전트 저장소 추가 작업 목록](./planning/ADD_FIVE_AGENT_REPOSITORIES_CHECKLIST.md)

## 모바일 링크 수집

GitHub 모바일 앱이나 모바일 브라우저에서 **New issue → KB 링크 추가** 양식을 열고
공개 HTTPS URL과 메모를 제출한다. 저장소 `OWNER`, `MEMBER`, `COLLABORATOR`가 만든
`[KB 링크]` Issue만 Gemini 분석이 실행되며, 결과는
KB 추가 여부에 따라 분기된다. 추가할 가치가 있으면 `knowledge-base/execution-records/`의
간략 분석 문서와 검토용 PR을 만들고, 추가하지 않으면 원본 Issue에 사유를 댓글로 남긴다.
자동 merge는 하지 않는다.

- 필수 secret: `GEMINI_API_KEY`
- 선택 variable: `GEMINI_MODEL` — 없으면 `gemini-3.7-flash`
- 수동 실행: **Actions → KB Link Intake with Gemini → Run workflow**
- GitHub 설정: Actions의 `GITHUB_TOKEN`이 브랜치 push와 PR 생성을 할 수 있어야 한다.
- 데이터 경계: 제출 링크와 메모는 Gemini API로 전송하므로 민감정보를 넣지 않는다.

워크플로는 공개 HTTPS URL만 받고 로컬·사설 IP와 사용자정보가 포함된 URL을 거부한다.
Gemini 단계에는 저장·셸·GitHub 도구를 제공하지 않으며, 생성 PR은 사람이 원문과 분석을
검토한 뒤에만 병합한다.

## 증거 경계

현재 결과는 고정된 source SHA, 저장소 구조, 테스트 구조, 공식 문서와 조사일의 GitHub 공개 메타데이터에 대한 정적 분석이다. 모든 프로젝트의 의존성 설치·전체 build·실 agent E2E나 유료 서비스 실행을 증명하지 않는다.

NTM은 로컬 clone 뒤 사용·분석 제한 rider를 확인해 즉시 조사에서 제외했으며 이 저장소와 submodule 목록에 포함하지 않는다.
