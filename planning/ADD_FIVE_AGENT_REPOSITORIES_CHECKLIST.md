# 5개 공식 에이전트 저장소 추가 작업 목록

문서 상태: In progress (로컬 구현·정적 검증 완료, commit/PR 대기)

작성일: 2026-08-14

## 목표

현재 28개인 조사 대상을 33개로 확장한다. 네트워크와 GitHub 접근이 가능한 후속 작업 환경에서 아래 5개 공식 저장소를 shallow Git submodule로 추가하고, 고정 checkout을 근거로 관련 기획 문서를 갱신한다.

| 프로젝트 | 공식 저장소 | submodule 경로 |
|---|---|---|
| DeepSeek Harness | `https://github.com/deepseek-ai/deepseek-harness.git` | `multi-agent-tools/deepseek-harness` |
| Hermes Agent | `https://github.com/NousResearch/hermes-agent.git` | `multi-agent-tools/hermes-agent` |
| OpenClaw | `https://github.com/openclaw/openclaw.git` | `multi-agent-tools/openclaw` |
| OpenAI Codex | `https://github.com/openai/codex.git` | `multi-agent-tools/codex` |
| Cline | `https://github.com/cline/cline.git` | `multi-agent-tools/cline` |

## 완료 조건

- [x] 5개 저장소가 `.gitmodules`와 mode `160000` gitlink에 등록돼 있다.
- [x] 각 gitlink는 조사 시점의 실제 기본 브랜치 HEAD를 가리킨다.
- [x] 라이선스 gate를 통과한 저장소만 분석 대상에 포함한다.
- [x] 조사 대상 수와 분류, 근거 permalink가 모든 관련 문서에서 일치한다.
- [x] 확인한 정적 사실과 실행하지 않은 검증을 명확히 구분한다.
- [ ] 검증 명령이 통과하고 변경사항이 하나의 재현 가능한 PR로 제출된다.

## 1. 사전 확인

- [x] 작업 시작 시 작업 트리가 clean인지 확인한다: `git status --short --branch`.
- [x] 저장소 루트와 상위 경로를 포함해 적용되는 모든 `AGENTS.md`를 확인한다(부모 저장소에 적용 파일 없음).
- [x] 다음 파일의 현재 구조, 표 형식과 증거 작성 방식을 다시 확인한다.
  - [x] `README.md`
  - [x] `.gitmodules`
  - [x] `multi-agent-tools/README.md`
  - [x] `planning/REPOSITORY_GITHUB_ANALYSIS.md`
  - [x] `planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md`
  - [x] `planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md`
  - [x] `planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md`
- [x] 기존 28개 submodule의 변경이나 dirty 상태가 없는지 확인한다.

## 2. Submodule 추가

각 저장소에 대해 기본 브랜치를 원격에서 확인한 후 `git submodule add --depth 1 <URL> <PATH>`로 추가한다.

- [x] DeepSeek Harness를 `multi-agent-tools/deepseek-harness`에 추가한다.
- [x] Hermes Agent를 `multi-agent-tools/hermes-agent`에 추가한다.
- [x] OpenClaw를 `multi-agent-tools/openclaw`에 추가한다.
- [x] OpenAI Codex를 `multi-agent-tools/codex`에 추가한다.
- [x] Cline을 `multi-agent-tools/cline`에 추가한다.
- [x] 각 저장소의 기본 브랜치 이름과 `git rev-parse HEAD` 결과를 기록한다.
- [x] 부모 저장소의 gitlink가 해당 SHA와 정확히 일치하는지 확인한다.
- [x] `.gitmodules`의 URL과 경로가 위 표의 공식 값과 일치하는지 확인한다.
- [x] 임의 SHA, branch 이름 추측 또는 존재하지 않는 placeholder gitlink를 사용하지 않는다.

## 3. 라이선스 gate

각 저장소는 상세 분석 전에 다음 순서로 확인한다.

- [x] 루트 `LICENSE`, `LICENSE.*`, `NOTICE`, README의 license 절을 확인한다.
- [x] source-available 조건, 사용 분야 제한, 분석·벤치마크 제한 등 추가 rider를 검색한다.
- [x] 하위 패키지와 vendored component에 별도 라이선스가 있는지 확인한다.
- [ ] 사용 또는 분석을 제한하는 rider가 있으면 해당 저장소의 분석과 submodule 등록을 중단하고 근거만 기록한다.
- [x] MIT 또는 Apache-2.0이고 root 분석 제한 rider가 없을 때만 분석을 계속한다.
- [x] SPDX 이름만 신뢰하지 않고 고정 checkout의 실제 license text와 notice를 근거로 삼는다.

## 4. 저장소별 조사 항목

5개 저장소 각각에 대해 다음 항목과 근거 파일 경로를 기록한다.

- [ ] 실제 checkout SHA와 기본 브랜치
- [ ] LICENSE, NOTICE와 추가 rider
- [ ] README의 설치·실행·지원 범위
- [ ] 루트 `AGENTS.md` 및 적용 범위
- [ ] 핵심 아키텍처 문서와 구현 경로
- [ ] Windows 네이티브·WSL·원격 지원 구분
- [ ] session 생성, 영속화, resume 및 owner semantics
- [ ] approval, permission과 credential 경계
- [ ] host, process, container, VM sandbox 및 network policy
- [ ] MCP 또는 ACP 지원과 protocol/version negotiation
- [ ] subagent, delegation 및 orchestration
- [ ] memory, skill, plugin과 장기 상태
- [ ] CLI, TUI, IDE, app-server, daemon, gateway 등 실행 surface
- [ ] 정적으로 확인한 사실과 build/E2E 미검증 사항

### DeepSeek Harness 분류 기준

- [ ] plugin-composed agent harness/runtime으로 분류한다.
- [ ] Cordis plugin tree와 plugin lifecycle을 확인한다.
- [ ] durable session event와 capability seam 구현을 확인한다.
- [ ] ACP 연결 경로를 확인한다.
- [ ] Codex/Claude Code subagent 연결 경로를 확인한다.
- [ ] local provider와 E2B provider의 capability 차이를 확인한다.

### Hermes Agent 분류 기준

- [ ] self-improving personal agent runtime으로 분류한다.
- [ ] persistent memory와 skill learning의 저장·갱신 경계를 확인한다.
- [ ] cron과 isolated subagent lifecycle을 확인한다.
- [ ] multi-channel gateway의 sender identity와 credential 범위를 확인한다.
- [ ] local, Docker, SSH, Modal, Daytona, Vercel terminal backend를 구분한다.

### OpenClaw 분류 기준

- [ ] single-operator assistant gateway/control plane으로 분류한다.
- [ ] Gateway의 session/tool/event/channel 모델을 확인한다.
- [ ] plugin과 skill lifecycle을 확인한다.
- [ ] companion node의 identity와 연결 경계를 확인한다.
- [ ] host tool과 sandbox 사이의 trust boundary를 확인한다.

### OpenAI Codex 분류 기준

- [ ] local coding-agent runtime으로 분류한다.
- [ ] CLI, app-server, TUI를 별도 capability profile로 조사한다.
- [ ] structured JSON-RPC와 exec surface를 확인한다.
- [ ] session resume와 approval flow를 확인한다.
- [ ] sandbox 및 network policy를 확인한다.
- [ ] MCP 지원과 Windows 지원 범위를 확인한다.

### Cline 분류 기준

- [ ] IDE/CLI coding agent로 분류한다.
- [ ] VS Code, JetBrains와 headless CLI를 별도 surface로 조사한다.
- [ ] hub daemon과 provider abstraction을 확인한다.
- [ ] tool/MCP approval과 checkpoint를 확인한다.
- [ ] 별도 Kanban 연동을 핵심 runtime과 구분한다.

## 5. 문서 갱신

### `README.md`

- [x] “28개 저장소 코드·GitHub 분석”을 “33개 저장소 코드·GitHub 분석”으로 변경한다.

### `multi-agent-tools/README.md`

- [x] 조사 대상 수를 33개로 변경한다.
- [x] 빠른 분류 표에 5개 프로젝트를 추가한다.
- [x] Windows 검토 순서에 5개 프로젝트를 추가한다.
- [x] 정확한 클론 기준점 표에 실제 기본 브랜치와 checkout SHA를 추가한다.
- [x] 각 프로젝트의 라이선스와 실행 미검증 경계를 표시한다.

### `planning/REPOSITORY_GITHUB_ANALYSIS.md`

- [x] 분석 대상을 33개로 변경한다.
- [x] coding-agent runtime형에 Codex와 Cline을 추가한다.
- [x] personal assistant runtime·gateway형에 Hermes Agent와 OpenClaw를 추가한다.
- [x] plugin-composed agent harness형에 DeepSeek Harness를 추가한다.
- [x] 각 저장소의 강점, 한계와 고정 SHA permalink를 추가한다.
- [ ] agent 이름이 아니라 실행 surface별 capability를 협상한다는 원칙을 추가한다.
- [ ] personal assistant gateway가 coding workspace보다 넓은 trust domain을 가진다는 원칙을 추가한다.
- [ ] runtime이 capability seam과 durable event를 함께 가져야 한다는 원칙을 추가한다.
- [x] 라이선스 표를 고정 checkout 근거로 갱신한다.

### `planning/AI_CODING_AGENT_TOOLS_AND_SERVICES_LANDSCAPE.md`

- [x] 조사 대상을 33개로 변경한다.
- [x] 5개 프로젝트를 제품 계층별로 추가한다.
- [x] 확인한 사실과 실행 미검증 사항을 별도 문장으로 구분한다.

### `planning/FAST_MULTI_AGENT_ORCHESTRATION_PLAN.md`

- [x] 근거 문서를 33개 저장소 분석으로 변경한다.
- [x] Codex app-server/exec/TUI를 서로 다른 capability profile로 취급한다.
- [x] Cline IDE/CLI/hub surface를 서로 다른 capability profile로 취급한다.
- [x] Hermes/OpenClaw channel request를 task intake로 바꾸는 Assistant Gateway Connector를 추가한다.
- [x] sender identity, workspace, credential audience, sandbox profile을 원자적으로 binding한다.
- [x] 불완전하거나 만료된 binding을 fail-closed하도록 명시한다.

### `planning/AI_AGENT_DEVELOPMENT_ENVIRONMENT_REQUIREMENTS.md`

- [x] 실행 surface별 capability snapshot과 protocol version 추적 요구사항을 추가한다.
- [x] gateway channel provenance와 durable intake event 요구사항을 추가한다.
- [x] sender identity, workspace, credential audience, sandbox profile binding 요구사항을 추가한다.
- [x] memory, skill, cron 및 companion node에서 유래한 요청의 provenance 요구사항을 추가한다.
- [x] assistant gateway와 coding workspace의 trust domain 분리 인수 조건을 추가한다.

## 6. 검증

- [x] `git submodule status`에 기존 28개와 신규 5개가 모두 나타나는지 확인한다.
- [ ] 깨끗한 별도 clone에서 `git submodule update --init --recursive --depth 1`을 실행한다.
- [x] 5개 checkout의 `git rev-parse HEAD`와 부모 gitlink를 비교한다.
- [x] 5개 checkout의 현재 branch와 기록한 기본 브랜치를 구분한다.
- [x] 문서에서 오래된 `28개` 표현을 검색하고 의도된 역사적 문맥 외에는 제거한다.
- [x] 신규 GitHub source link가 고정 checkout SHA permalink인지 확인한다.
- [x] 라이선스 표와 각 저장소의 실제 license text가 일치하는지 확인한다.
- [x] `git diff --check`와 staged diff check를 실행한다.
- [x] 변경된 Markdown의 로컬 링크를 검사한다.
- [x] 의존성 설치·build·Windows·remote provider·실 agent E2E를 명시적으로 미검증으로 남긴다.

## 7. 전달

- [ ] `git diff`와 staged diff를 최종 검토한다.
- [ ] 문서와 5개 gitlink를 같은 변경 단위로 commit한다.
- [ ] PR 본문에 고정 SHA, 라이선스 gate 결과, 수행한 검증과 미검증 항목을 요약한다.
- [ ] Codex Cloud GitHub 연동을 통해 PR을 생성한다.

## 현재 차단 이력

2026-08-14의 최초 시도에서는 GitHub HTTPS 연결이 `CONNECT tunnel failed, response 403`으로 차단됐고 GitHub CLI 인증도 제공되지 않았다. 이후 같은 날 GitHub HTTPS 접근이 복구되어 원격 기본 브랜치·HEAD, checkout SHA, license text와 source permalink를 검증하고 로컬 변경을 완료했다. commit, 별도 clean clone 재현과 PR 생성은 아직 수행하지 않았다.
