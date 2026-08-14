---
id: tool-gh-aw
type: tool-profile
title: GitHub Agentic Workflows
status: observed
tags:
  - knowledge-base
  - tool
  - automation
  - privilege-separation
official_upstream: https://github.com/github/gh-aw
license: MIT
maintenance_status: active
observed_at: 2026-08-14
upstream_default_branch: main
upstream_head_observed: 9052088f5f61a79fd454dbcb4d6ab2add261676a
upstream_checked_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# GitHub Agentic Workflows

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

GitHub Agentic Workflows(`gh-aw`)는 Markdown 의도를 검증 가능한 GitHub Actions workflow로 compile하고, 기본 read-only agent job의 제안과 scoped `safe-outputs` write job을 분리하는 repository automation compiler다.

## ToolVersion과 공식 최신 관찰

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/github/gh-aw` |
| 조사일 기본 브랜치 HEAD | `main` · `9052088f5f61a79fd454dbcb4d6ab2add261676a` |
| 고정 버전 | `ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7` |
| pin과 최신 HEAD | 조사일 기준 최신 HEAD가 pin보다 24 commits 앞섬. 아래 기술 주장은 pin에만 적용 |
| 로컬 gitlink | [`multi-agent-tools/gh-aw`](../../multi-agent-tools/gh-aw/) |
| 조사일 | 2026-08-14 (Asia/Seoul) |
| 출처 무결성 | `I2`: `.gitmodules`, parent `git ls-tree`, 공식 GitHub fixed commit/tree를 대조 |
| 유지보수 관찰 | GitHub metadata에서 archived/disabled가 아니며 조사일 push가 관찰됨. support SLA나 runtime 안정성 증거는 아님 |
| license | fixed [`LICENSE`](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/LICENSE#L1-L20)의 MIT text와 GitHub SPDX metadata가 일치 |

## 기술 구조

| 구성 | 책임 | fixed-SHA 근거 |
|---|---|---|
| Markdown source | YAML frontmatter에 trigger·permission·tool·engine을, 본문에 agent 목표를 선언 | [README](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L50-L54) |
| Compiler | source를 parse/validate하고 Actions YAML lock file을 생성 | [compiler entry](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler.go#L58-L90) |
| Agent job | reasoning과 도구 호출을 수행하는 기본 read-only/sandboxed stage | [security contract](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L82-L88) |
| Safe-output job | buffered proposal을 별도 job에서 처리하고 필요한 GitHub permission을 계산 | [job builder](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_job.go#L110-L134) |
| Trusted commit/push handler | push credential은 untrusted agent가 아니라 safe-output handler만 사용 | [checkout boundary](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_steps.go#L34-L39) |

흐름은 `Markdown intent → Actions DAG compile → read-only agent proposal → threat detection/policy/human gate → narrow safe-output committer`로 읽는다. compile 결과가 안전한 배포나 실행 성공을 자동 증명하지는 않는다.

## 역할과 연동

- AgentRole: Policy, Automation Compiler, Verifier 보조, scoped Committer
- Capability: `compiled-agent-workflow`, `permission-derivation`, `safe-output-buffer`, `privilege-separated-write`, `multi-engine-runner`
- Integration: GitHub CLI extension, GitHub Actions YAML, MCP, GitHub API, artifact/step outputs
- SecurityOperationalRequirement: workflow source review, action pinning, minimal token permission, network/sandbox review, safe-output validation과 사람 승인

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `ghaw-markdown-compiler` | capability | Markdown+frontmatter source를 표준 GitHub Actions workflow로 compile한다. | [README](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L50-L54), [compiler](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler.go#L58-L90) | `I2` | `V2` | `W0` | pass(정적). 실제 compile 미실행 |
| `ghaw-lock-validation` | architecture | compiler가 생성 YAML과 lock file 출력을 별도 단계로 검증·기록한다. | [generate/validate](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler.go#L127-L132), [write output](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler.go#L250-L255) | `I2` | `V2` | `W0` | pass(정적). generated lock의 runtime correctness는 미검증 |
| `ghaw-safe-output-split` | security | agent job은 기본 read-only/sandbox이고 threat detection 뒤 write는 buffered safe-output 별도 job에서 scoped permission으로 적용된다. | [security](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L82-L88), [safe-output permissions](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_job.go#L110-L134) | `I2` | `V2` | `W0` | pass(정적). 설정으로 완화할 수 있으므로 배포별 검토 필수 |
| `ghaw-trusted-committer` | trust-boundary | push credential consumer를 trusted safe-output handler로 제한하는 코드 경계가 있다. | [credential boundary](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_steps.go#L34-L39) | `I2` | `V2` | `W0` | pass(정적). token audience·repo scope의 실제 enforcement는 E2E 미검증 |
| `ghaw-not-ci-replacement` | limitation | deterministic build/test/deploy를 대체하는 도구가 아니라 reasoning이 필요한 automation을 보완한다. | [scope statement](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L50-L54) | `I2` | `V2` | `W0` | confirmed limitation |
| `ghaw-safe-update-bypass` | limitation | safe-update는 generated lock 변화에 warning/gate를 제공하지만 operator의 `--approve`로 우회 가능한 배포 절차이며 immutable policy enforcement가 아니다. | [safe-update enforcement](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/safe_update_enforcement.go#L1), [spec](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/docs/src/content/docs/specs/safe-update-specification.md#L1) | `I2` | `V2` | `W0` | confirmed limitation; 사람 승인·정책 기록 필요 |
| `ghaw-proxy-scope-limit` | limitation | 제공 proxy 경로는 HTTP/HTTPS traffic 범위이며 non-HTTP 또는 DNS egress 차단을 포괄적으로 증명하지 않는다. | [proxy environment setup](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/actions/setup/sh/proxy_env_lib.sh#L1) | `I2` | `V2` | `W0` | confirmed scope limit; runner/network control 별도 필요 |
| `ghaw-windows-cli-source` | platform | Windows runner에서 CLI integration을 다루는 고정 workflow 구성이 있다. | [Windows CLI workflow](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/.github/workflows/windows-cli-integration.yml#L1) | `I2` | `V2` | `W1` | narrow static path. agent Actions runtime의 Windows 동작 증거는 아님 |

## Interface와 protocol

| 표면 | 계약 | 권한·상태 경계 | 근거 |
|---|---|---|---|
| `gh aw compile` | Markdown → `.lock.yml` Actions workflow | compile-time validation; 실행과 분리 | [README](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L82-L86) |
| GitHub Actions | trigger/job/step/artifact | job별 token permission과 sandbox 경계 | [safe-output builder](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_job.go#L110-L134) |
| MCP/engine adapters | Copilot, Claude, Codex, Gemini, Pi 등 agent engine | engine capability와 credential은 별도 배포 설정 | [engine list](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/README.md#L50-L54) |
| safe outputs | proposal artifact → validated external write | agent와 committer credential audience 분리 | [trusted handler](https://github.com/github/gh-aw/blob/ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7/pkg/workflow/compiler_safe_outputs_steps.go#L34-L39) |

## 운영·보안·trust boundary

- agent의 자연어 출력은 external write 권한이 아니라 proposal이다.
- compiler validation, threat/policy verifier, 필요 시 human approval을 통과한 proposal만 별도 committer가 적용해야 한다.
- workflow·action·container pin, network egress, MCP server와 token scope가 실제 trust boundary다. `safe-outputs` 이름만으로 안전을 보장하지 않는다.
- 신규 플랫폼에서는 credential 원문 대신 audience/repository/action scope가 붙은 opaque handle을 committer에게만 resolve하는 패턴으로 확장한다.

## 플랫폼과 Windows

- fixed source에 Windows CLI integration workflow가 있어 좁은 정적 근거 `W1`을 부여한다.
- 핵심 agent Actions runtime은 Linux 경로로 읽으며 Windows CLI workflow를 전체 Windows runtime 지원으로 확장하지 않는다.
- Windows runner에서 compile·sandbox·safe-output을 수행한 로그가 없어 `W2/W3`가 아니다.
- HTTP/HTTPS proxy 설정은 non-HTTP와 DNS egress를 차단했다는 증거가 아니다.

## Evidence

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `ghaw-origin-20260814` | parent `.gitmodules`+`git ls-tree`, GitHub repo/branch/compare/license metadata | pass | `github/gh-aw@ef14fabf6dc17e6f5862dd5de7c905ea0e9299f7` | origin과 ToolVersion |
| `ghaw-fixed-static-20260814` | 공식 GitHub fixed README와 compiler/safe-output/safe-update/proxy/Windows workflow 정적 검토 | partial pass | 위 fixed-SHA permalink | 모든 `V2`, `W1` Claim |
| `ghaw-v3plus-none` | compile/build/Actions runtime/safe-output E2E를 수행하지 않음 | unknown | 없음 | `V3+`, `W2+` Claim 없음 |

병렬 조사 worktree의 submodule 본문은 비어 있어 로컬 본문을 읽지 않았다. `I2`는 부모 `.gitmodules`와 gitlink, 공식 GitHub fixed commit/tree로 확인했고, 코드·문서 `V2`도 공식 GitHub fixed-SHA에서만 수집했다. 로컬 submodule build/runtime/E2E는 읽거나 실행하지 않았다.

## 강점과 한계

- 강점: `ghaw-markdown-compiler`는 자연어 automation을 review 가능한 lock manifest로 낮춘다.
- 강점: `ghaw-safe-output-split`과 `ghaw-trusted-committer`는 proposal과 external write 권한을 구조적으로 분리한다.
- 한계: `ghaw-not-ci-replacement`처럼 deterministic CI의 대체물이 아니고 Actions·GitHub trust domain에 강하게 결합된다.
- 한계: 설정 가능한 sandbox·permission·network 때문에 안전성은 workflow별 정책 검증과 runtime evidence가 필요하다.
- 한계: `ghaw-safe-update-bypass`와 `ghaw-proxy-scope-limit` 때문에 compile warning과 HTTP proxy를 강제 승인·전 egress 통제로 과장할 수 없다.

## AX 설계 재료

| 구분 | 연결 Claim | 사내 AX 플랫폼에서의 사용 |
|---|---|---|
| Borrow | `ghaw-markdown-compiler`, `ghaw-lock-validation` | review 가능한 intent와 deterministic Actions DAG/lock 분리 |
| Adapt | `ghaw-safe-output-split`, `ghaw-trusted-committer` | proposal을 threat detection·policy·verifier·human gate 뒤 narrow committer로 전달 |
| Avoid | `ghaw-safe-update-bypass`, `ghaw-proxy-scope-limit` | warning/`--approve`와 HTTP proxy를 immutable approval 또는 전체 egress 보장으로 간주하지 않음 |
| Build | `ghaw-not-ci-replacement`, `ghaw-windows-cli-source` | deterministic CI, non-HTTP/DNS network enforcement, Windows runner conformance를 별도 구축 |

회사 업종, 데이터 분류, 규제 범위, 승인자 역할, automation이 접근할 repository·external system, human bypass 허용 여부는 모두 `unknown/decision item`이다. 이 프로필은 벤더 선정이나 최종 AX 답이 아니라 설계 재료다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: `proposal → policy/verifier/human → committer` 표준, compiled manifest와 permission-drift review의 clean-room 기준
- 이유: `ghaw-markdown-compiler`, `ghaw-safe-output-split`, `ghaw-trusted-committer`가 권한 분리 청사진과 직접 맞지만 실제 Actions E2E는 없다.
- 재검토 조건: Windows/Linux runner compile, malicious proposal, tampered artifact, over-scoped token, safe-output reject/apply failure injection

## 다음 검증

| Item ID | 목표 Claim/등급 | 환경·시나리오 | 통과 기준 | 보존 artifact |
|---|---|---|---|---|
| `ghaw-v3-compile` | `ghaw-markdown-compiler` / `V3` | fixed SHA CLI로 fixture compile | exit 0, deterministic lock diff | command, environment, lock hash, log |
| `ghaw-v5-write-boundary` | `ghaw-safe-output-split` / `V5` | malicious/tampered proposal과 permission 축소 failure injection | agent job direct write 0, invalid output apply 0 | workflow run, token permissions, audit artifacts |
| `ghaw-w2-runner` | Windows 상태 / `W2` | Windows Actions runner compile+safe-output dry run | documented fixture와 동일 결과 | runner image, logs, generated lock |

## 관계와 변경 이력

- `ToolVersion PROVIDES compiled-agent-workflow/privilege-separated-write`
- `ToolVersion SUPPORTS GitHub-Actions/MCP/GitHub-API`
- `Project EVALUATES ToolVersion`
- 2026-08-14: official GitHub fixed-SHA 정적 프로필 작성. `I2 / V2 / W1`(Windows CLI 좁은 정적 경로); runtime 미수행.
