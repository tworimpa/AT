---
id: tool-container-use
type: tool-profile
title: Container Use
status: observed
tags:
  - knowledge-base
  - tool
  - local-executor
  - container
  - mcp
official_upstream: https://github.com/dagger/container-use
license: Apache-2.0
maintenance_status: active
observed_at: 2026-08-14
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W0
version_kind: commit
version_ref: 2e43e625e95216b719ec9338f4034fd3a0be2734
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
---

# Container Use

[지식 베이스 홈](../index.md) · [도구 카탈로그](./catalog.md) · [스키마와 작성 규칙](../knowledge-graph-schema.md)

## 한 줄 역할

Container Use는 coding agent마다 Git branch와 Dagger container 상태를 결합한 개발 환경을 만들고 MCP/CLI에서 명령·파일·서비스·검토 흐름을 제공하는 local container executor 후보이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream | `https://github.com/dagger/container-use` |
| 기본 브랜치와 고정 버전 | `main` · `2e43e625e95216b719ec9338f4034fd3a0be2734` |
| 조사일 현재 관찰 | 2026-08-14 GitHub API 기준 `main` HEAD도 위 SHA이며 archived/disabled가 아님. 이는 활동 관찰이지 지원 SLA가 아님 |
| 로컬 gitlink | [`multi-agent-tools/container-use`](../../multi-agent-tools/container-use/) |
| 출처 무결성 | `I2`: parent `.gitmodules` 공식 URL과 `git ls-tree` gitlink SHA를 대조하고 공식 GitHub fixed-SHA tree/metadata를 검토 |
| license | root [`LICENSE`](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/LICENSE#L1-L6)의 Apache-2.0 text와 GitHub SPDX metadata가 일치 |

## 조사 provenance와 ceiling

병렬 조사 worktree에서는 submodule 디렉터리 본문이 비어 있어 로컬 checkout 본문을 근거로 읽지 못했다. 따라서 parent `.gitmodules`와 `git ls-tree`로 pin을 `I2` 확인하고, 실제 Claim은 공식 GitHub의 동일 fixed-SHA tree·blob에서 수집했다. 이 프로필 작성에서 local submodule body를 분석 근거로 사용하지 않았고 install/build/runtime/agent E2E/Windows 실행도 하지 않았으므로 ceiling은 `V2 / W0`이다.

## 목적과 기술 구조

- host의 Git repository를 기준으로 환경별 branch/worktree lineage를 만들고, Dagger `ContainerID`를 환경 state에 저장해 후속 명령의 container state를 이어간다.
- agent-facing surface는 `container-use stdio` MCP server이며, 사람은 CLI로 list/log/diff/checkout/merge/terminal 작업을 수행한다.
- Dagger container는 source directory, setup/install command, environment/secret variable, service binding을 합성하고 변경 후 새 immutable container ID를 state에 기록한다.
- 파일 변경은 container filesystem에 적용된 뒤 Git propagation 대상으로 이어진다. submodule 내부 쓰기는 정적으로 거부한다.

## 역할과 연동

- AgentRole: Executor, Workspace manager, human intervention surface
- Capability: `branch-container-lineage`, `command-execution`, `file-operation`, `service-tunnel`, `execution-log`, `human-checkout`
- Integration: MCP stdio, CLI, Dagger API, Git branch/worktree
- SecurityOperationalRequirement: host repository 권한 최소화, engine/socket 신뢰 경계, egress 통제, secret audience 제한, log/redaction 검증, merge 전 사람 검토

## Claims

| Claim ID | 검증 가능한 주장 | SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|
| `container-use-mcp-environment` | MCP-compatible agent가 `container-use stdio`를 통해 agent별 Git branch와 container 환경을 사용할 수 있다. | [README](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/README.md#L19-L31), [setup contract](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/README.md#L51-L65) | `I2` | `V2` | `W0` | 정적 pass. MCP handshake와 agent 호환 E2E는 미실행 |
| `container-use-container-state` | Environment가 Dagger client와 container ID를 보유하고 새 state 평가 후 ID를 갱신한다. | [environment.go](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/environment.go#L23-L70), [state.go](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/state.go#L9-L24) | `I2` | `V2` | `W0` | 정적 pass. cache reuse·restart recovery 성능은 미검증 |
| `container-use-files-and-git` | file read/write/edit/delete를 container에 적용하고 submodule 내부 쓰기를 거부한다. | [filesystem.go](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/filesystem.go#L13-L55), [submodule guard](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/filesystem.go#L200-L240) | `I2` | `V2` | `W0` | 정적 pass. symlink/path traversal과 concurrent Git mutation failure fixture는 미실행 |
| `container-use-services` | container service를 bind하고 host tunnel endpoint를 만든다. | [service.go](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/service.go#L30-L97) | `I2` | `V2` | `W0` | 정적 pass. egress/ingress isolation과 port collision은 미검증 |
| `container-use-secret-path` | configured secret는 Dagger secret variable로 container command와 service에 주입된다. | [environment secret injection](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/environment.go#L154-L186), [secret documentation](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/docs/secrets.mdx#L7-L24) | `I2` | `V2` | `W0` | 구현 경로 존재. 문서의 redaction·“model never sees” 주장은 공격적 command/egress/side-channel V5 없이 secret-safe 보장이 아님 |
| `container-use-not-security-boundary` | Git branch/worktree와 container lineage는 충돌·재현성 경계이지 credential·engine·host socket까지 포함한 완전한 보안 경계가 아니다. | [README environment claim](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/README.md#L25-L35), [container and secret construction](https://github.com/dagger/container-use/blob/2e43e625e95216b719ec9338f4034fd3a0be2734/environment/environment.go#L154-L186) | `I2` | `V2` | `W0` | confirmed limitation. 별도 policy/egress/credential broker가 필요 |

## 인터페이스와 protocol

- Agent: MCP over stdio (`container-use stdio`).
- Operator: `container-use`/`cu` CLI와 interactive terminal.
- Runtime: Go client가 Dagger API를 호출하고 `dagger.ContainerID`를 state handle로 사용한다.
- Source transition: environment mutation → container state → Git branch/worktree 검토/checkout/merge. 이 lineage는 project의 명시적 run/session ID와 fencing을 대체하지 않는다.

## 운영·보안 trust boundary

- host의 Git repository, Dagger engine, container image, mounted source, network tunnel, secret provider는 서로 다른 authority로 취급한다.
- secret reference와 log masking은 유용한 방어층이지만, secret을 사용하는 임의 code가 network·timing·derived artifact로 값을 누출하지 못한다는 증거는 없다.
- agent가 만든 branch를 proposal로 취급하고 verifier/human approval 뒤 별도 committer가 적용해야 한다. container 성공은 merge나 production 성공이 아니다.

## 플랫폼과 Windows

공식 quick start는 “all platforms” 설치 문구를 포함하지만 이 프로필은 Windows 전용 구현·build/runtime를 근거로 검증하지 않았다. container workload는 Linux shell·image를 전제로 하므로 Windows host, WSL/Docker backend, Linux guest를 분리해 검증하기 전까지 `W0`이다.

## 강점과 한계

- 강점: agent별 Git lineage와 container state를 한 운영 표면으로 묶고 로그·terminal·diff로 사람이 개입할 수 있다.
- 강점: MCP-compatible agent를 같은 executor surface에 연결하는 비교적 작은 local adapter 후보이다.
- 한계: experimental/early-development 표기이며 branch/worktree는 OS sandbox가 아니다.
- 한계: Dagger engine과 image supply chain, host repository write, service tunnel, secret injection을 아우르는 별도 policy가 필요하다.
- 한계: runtime identity·lease·generation fence의 명시적 conformance evidence가 없다.

## AX 설계 재료

- **Borrow**: `container-use-mcp-environment`, `container-use-container-state`의 agent별 branch+container lineage와 human-visible log/diff/terminal surface.
- **Adapt**: `container-use-files-and-git`를 사내 proposal branch → verifier → 승인 → committer 흐름과 명시적 run/session generation에 연결한다.
- **Avoid**: `container-use-secret-path` 문서 주장만으로 secret-safe를 선언하거나 `container-use-not-security-boundary`의 branch/container를 권한 격리로 간주하지 않는다.
- **Build**: executor conformance fixture, opaque secret handle, deny-by-default egress, retention/cleanup evidence, stale owner fence를 사내 control plane에 구현한다.
- **Unknown / decision items**: 회사 업종, data classification, 규정, 승인 주체는 미정이다. 허용 sandbox class, secret audience/TTL, network allowlist owner, branch/log/container retention과 삭제 승인 기준을 소유자가 결정해야 한다.

## 도입 판단

- 결정: 파일럿
- 적용 범위: 벤더 선정의 최종 답이 아니라 사내 AX 플랫폼용 local container executor와 human-reviewable branch lineage 설계 재료; remote sandbox adapter와 동일 executor conformance fixture에 연결
- 이유: `container-use-mcp-environment`와 `container-use-container-state`는 local-first executor에 유용하지만 `container-use-not-security-boundary` 때문에 secret-safe 기본값으로 채택할 수 없다.
- 재검토 조건: 고정 SHA 갱신, Linux/Windows host V3 build, command/files/service V4, cancel/restart/concurrent branch V5, adversarial secret-exfiltration·egress fixture

## Evidence와 다음 검증

| Evidence ID | 방법·환경 | 결과 | artifact locator | 지원·반증 Claim |
|---|---|---|---|---|
| `container-use-pin-static-20260814` | parent `.gitmodules` + `git ls-tree`, official GitHub fixed-SHA metadata/tree 정적 검토 | partial pass | `dagger/container-use@2e43e625e95216b719ec9338f4034fd3a0be2734` | 위 `V2` Claim |
| `container-use-v3plus-none` | local body/build/runtime/E2E/Windows 실행 미수행 | unknown | 없음 | `V3+`, `W1+` Claim 없음 |

다음 검증은 (1) clean Linux와 Windows+WSL/Docker에서 V3 build, (2) 동일 conformance fixture로 command/stdio/cancel/files/service V4, (3) engine restart와 concurrent branch cleanup V5, (4) scoped opaque secret handle·deny-by-default egress·redaction 공격 fixture V5 순서로 수행한다.

## 관계

- `Tool HAS_VERSION ToolVersion`
- `ToolVersion FITS_ROLE Executor/WorkspaceManager`
- `ToolVersion PROVIDES branch-container-lineage/command-execution/file-operation`
- `ToolVersion SUPPORTS MCP/CLI/Dagger/Git`
- `Project EVALUATES ToolVersion`

## 변경 이력

- 2026-08-14: official fixed-SHA tree와 parent gitlink를 대조해 `I2 / V2 / W0` 상세 프로필 작성. build/runtime/E2E는 미수행.
