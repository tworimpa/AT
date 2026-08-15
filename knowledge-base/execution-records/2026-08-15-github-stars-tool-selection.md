---
id: execution-github-stars-tool-selection-2026-08-15
type: execution-record
title: GitHub stars 기반 AX 도구 선별·지식화 실행 기록
status: historical-snapshot
observed_at: 2026-08-15
profile_id: implement-deep
profile_revision: 1
verification_ceiling: V2
tags:
  - knowledge-base
  - execution-record
  - github-stars
  - tool-selection
---

# GitHub stars 기반 AX 도구 선별·지식화 실행 기록

[지식 베이스 홈](../index.md) · [도구 카탈로그](../tools/catalog.md) · [커버리지](../tools/coverage.md) · [지속 컨텍스트](../ax-platform-context.md)

이 문서는 `tworimpa`의 2026-08-15 공개 GitHub stars를 AX 플랫폼 설계 관점에서 triage하고 네 ToolVersion을 지식 베이스에 추가한 실행의 역사적 스냅샷이다. star는 관심 신호일 뿐 품질·도입·공식성을 증명하지 않으며, 현재 규칙은 active governance와 최신 accepted Decision을 우선한다.

## Run identity

| 필드 | 실제 기록 |
|---|---|
| task/run ID | `github-stars-tool-selection-2026-08-15-implement-deep` |
| 역할 | coordinator / researcher / knowledge-base documenter |
| profile | 후보 수집·중복 조사 `research-fast`; 문서 반영 `implement-deep`, revision 1 |
| model provider·slug·version | OpenAI / actual slug `unknown` / version `unknown` |
| requested/actual effort | research `low`, implementation `high` / actual `unknown` |
| 시작·종료 시각 | exact `unknown`; calendar observation 2026-08-15 |
| base/head SHA | base `91d6d075d53185667e20996cc94ec7e10537d02c`; 작업 트리는 미커밋 상태라 head commit은 동일 |
| branch | `main` |
| cost/latency | `unknown` / `unknown` |

## 작업 계약과 성공 기준

- 범위: [공개 stars 페이지](https://github.com/tworimpa?tab=stars)의 repository metadata를 수집하고 기존 35개 ToolVersion과 identity·capability·trust boundary를 비교해, 비중복 설계 가치가 큰 후보를 official fixed SHA로 등록한다.
- 비범위: dependency 설치, clone을 통한 전체 소스 보존, build/runtime/E2E, vendor selection, 비용 발생 provider, credential 사용, GitHub write, commit/push/merge/deploy.
- 성공 기준: 공식 upstream·license·immutable commit, `Borrow/Adapt/Avoid/Build`, OS별 evidence와 다음 검증이 있는 schema v3 profile; catalog/coverage/architecture linkage; KB validator green.
- 소스 관리: 네 후보 모두 현재는 비교·설계·표준 조사 대상이므로 `manifest-only`; adapter/reference implementation을 직접 채택할 때 gitlink 전환을 재검토한다.

## 모집단과 선별 결과

- GitHub REST pagination으로 공개 star 1,048개(100개 10 page + 48개 1 page)를 관찰했다.
- 최근 100개는 순서·설명·license를 수동 검토했고, 전체 집합은 name/description/topic의 agent·skill·MCP·sandbox·evaluation·security 관련 어휘로 넓게 필터링한 뒤 기존 35개 capability family와 대조했다.
- 기존 orchestration, UI, adapter, sandbox family와 동일한 branding/UI 차이는 신규 등록 이유로 세지 않았다.

| 판단 | 후보 | 고정 SHA | 이유 |
|---|---|---|---|
| 채택 재료 | [Agent Skills](../tools/agent-skills.md) | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | portable skill artifact와 progressive disclosure의 최소 계약; executable content의 provenance·permission·sandbox는 별도 Build gate |
| 참고 | [Entire CLI](../tools/entire-cli.md) | `7ddf2fc26c1ba521309ca2b5cf356d1e54228afb` | session/checkpoint/transcript를 Git object/ref와 연결하는 provenance 패턴; attribution·best-effort signing은 verifier proof가 아님 |
| 파일럿 | [promptfoo](../tools/promptfoo.md) | `ab84555c1b0ff74eca6b03abb7936ac9a0149242` | 기존 KB의 evaluation·red-team·trace-backed failure-injection 공백 보완 |
| 파일럿 | [NVIDIA SkillSpector](../tools/skillspector.md) | `5680c2c3008e63c9979bbbe08221ee4c2dcd17ee` | skill 설치 전 supply-chain scan과 incomplete/failed inspection을 숨기지 않는 ledger 패턴 |

## 보류·후속 후보

| 후보 | 판단 | 재검토 조건 |
|---|---|---|
| `agentplugins/agent-plugins-spec` | Agent Skills와 MCP를 묶는 후속 portable plugin 표준 | Agent Skills artifact contract가 안정되고 plugin package/credential 경계 결정이 필요할 때 |
| `joshuaswarren/remnic` | correction·provenance·memory extraction threat model은 유용하나 TencentDB memory plane과 중복 | 두 memory implementation을 동일 tenant/correction/eval fixture로 비교할 때 |
| `Agent-Threat-Rule/agent-threat-rules` | vendor-neutral detection schema는 유용하나 working-draft/TSC·telemetry가 미성숙 | rule portability와 action eligibility가 architecture decision이 될 때 |
| `cisco-ai-defense/skill-scanner` | SkillSpector와 기능 중복이 큼 | analyzability/policy preset 차이를 동일 corpus로 비교할 때 |
| `opensandbox-group/OpenSandbox`와 기타 sandbox | 기존 E2B·Vercel·Container Use·Cloudflare·Warren 커버리지와 중복 | self-hosted conformance에서 새 isolation/failure contract가 확인될 때 |

## Environment, commands와 결과

| 항목 | 값/결과 |
|---|---|
| repository | `/home/sh-cat-lee/workspaces/AT` |
| environment | WSL2 Linux `6.18.33.2-microsoft-standard-WSL2` x86_64; git `2.53.0`; Python version은 validator 출력에 별도 기록되지 않아 `unknown` |
| baseline | `git status --short --branch`; `git rev-parse HEAD`; exit 0 |
| stars population | `gh api --paginate users/tworimpa/starred?per_page=100 --jq length`; exit 0; page counts `100`×10 + `48` |
| recent triage | `gh api users/tworimpa/starred?per_page=100&page=1` with metadata projection; exit 0 |
| full-set filter | paginated GitHub API + jq name/description/topic filter; exit 0 |
| immutable metadata | GitHub GraphQL default branch HEAD/license/disk usage and fixed-SHA tree/content reads; exit 0 |
| first network attempt | sandboxed `gh api` connection failed, exit 1; approved read-only network retry succeeded; secret 원문은 출력하지 않음 |
| KB structural gate | `python3 scripts/validate_knowledge_base.py`; exit 0; 55 Markdown files의 frontmatter, lifecycle, unique IDs, relative links 통과 |
| whitespace gate | `git diff --check`; exit 0; 신규 파일 trailing whitespace는 별도 `rg` 검사 |
| artifacts | 네 fixed ToolVersion profile, catalog/coverage/index/context, reference architecture/blueprint, 이 execution record |

## Evidence boundary와 외부 효과

- official upstream과 조사 시점 default branch HEAD를 immutable commit으로 고정한 범위의 `I2`, 문서·source/config 정적 분석 `V2`다.
- Agent Skills와 promptfoo는 Windows/Linux `P0`; Entire은 양쪽 `P1`; SkillSpector는 Windows `P0`, Linux `P1`이다. 이는 각 프로필의 fixed path 범위이며 native 실행을 뜻하지 않는다.
- build `V3`, runtime `V4`, E2E/failure injection `V5`, 운영 `V6`, OS native `P2/P3`는 미수행이다.
- 외부 동작은 공개 GitHub read뿐이다. 파일 변경은 이 workspace 안의 지식 베이스 문서에 한정됐고 commit/push/merge/deploy, external message, credential/permission 변경, 비용 발생 service는 수행하지 않았다.

## 알려진 한계

- stars 정렬·목록은 관찰 이후 바뀔 수 있고 star 자체는 endorsement나 품질 evidence가 아니다.
- metadata 어휘 필터는 설명·topic이 부실한 후보를 놓칠 수 있다. 최근 100개 수동 검토와 기존 capability 비교로 이를 완화했지만 완전성은 보장하지 않는다.
- GitHub metadata license와 component license는 다를 수 있어 fixed license/NOTICE를 우선했으며 dependency license 전수 검토는 하지 않았다.
- green KB validator는 frontmatter/lifecycle/중복 ID/repository-relative link의 `V2` 구조만 지지하고 외부 URL·fixed-SHA 내용·runtime·production 적합성을 검증하지 않는다.
