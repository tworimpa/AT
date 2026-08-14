---
id: tool-deepseek-harness
type: tool-profile
title: DeepSeek Harness
status: observed
profile_schema_version: 2
tool_key: deepseek-harness
tool_version_id: tool-version:deepseek-harness@47f943859bef60e4160492346772ded9b24f765a
tags: [knowledge-base, tool, harness, acp, sandbox]
official_upstream: https://github.com/deepseek-ai/deepseek-harness
license: MIT-with-third-party-notices
maintenance_status: active
observed_at: 2026-08-15
upstream_default_branch: master
upstream_head_observed: 47f943859bef60e4160492346772ded9b24f765a
upstream_checked_at: 2026-08-15
origin_integrity: I2
verification_ceiling: V2
windows_evidence: W1
version_kind: commit
version_ref: 47f943859bef60e4160492346772ded9b24f765a
parent_repo_head: 984cac0634b83d10af91d8e1814680816e67c53b
source_management: fixed-sha-submodule
analysis_snapshot_date: 2026-08-15
---

# DeepSeek Harness

[지식 베이스 홈](../index.md) · [AX 컨텍스트](../ax-platform-context.md) · [카탈로그](./catalog.md) · [커버리지](./coverage.md)

## 한 줄 역할

DeepSeek Harness는 plugin/service graph로 agent, provider, session, sandbox capability를 조립하고 automation-only ACP JSON-RPC 표면을 제공하는 모듈형 harness 참고 구현이다.

## ToolVersion

| 필드 | 값 |
|---|---|
| 공식 upstream / 조사일 HEAD | `https://github.com/deepseek-ai/deepseek-harness` · `master` / `47f943859bef60e4160492346772ded9b24f765a` (2026-08-15) |
| 고정 버전 / gitlink | `47f943859bef60e4160492346772ded9b24f765a` · [`multi-agent-tools/deepseek-harness`](../../multi-agent-tools/deepseek-harness/) |
| pin 관계 | 조사일 default-branch HEAD와 같음 |
| license | [MIT LICENSE](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/LICENSE#L1-L21)와 [third-party notices](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/THIRD_PARTY_NOTICES.md#L1) |
| provenance limitation | parent gitlink와 official fixed-SHA package docs/source만 정적 검토. test file 존재는 V2이며 실행 증거가 아님 |

## 기술 구조

| 구성 요소 | 책임·흐름 | fixed-SHA 근거 |
|---|---|---|
| Plugin graph | service/function plugin을 조립하고 injection topology 관리 | [package rules](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/AGENTS.md#L1-L9) |
| ACP bridge | harness agent를 automation client에 JSON-RPC stdio로 노출 | [ACP overview](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/README.md#L1-L11) |
| ACP session owner | initialize/new/prompt/cancel/update/permission과 connection-owned sessions | [server contract](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/acp/README.md#L24-L56) |
| Confinement mechanism | Linux Landlock launcher; policy는 consumer가 결정 | [architecture](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/native/landlock-run/docs/architecture.md#L1-L7) |

## 역할과 연동

- AgentRole: Agent Runtime, Adapter Host, Session Service.
- Capability: `plugin-capability-graph`, `acp-automation-server`, `connection-session-ownership`, `sandbox-mechanism`.
- Integration: ACP JSON-RPC stdio, TypeScript plugins/services, provider/session/sandbox packages.

## Claims

| Claim ID | 종류 | 검증 가능한 주장 | fixed-SHA SourceArtifact | I | V | W | 결과·한계 |
|---|---|---|---|---|---|---|---|
| `dsh-plugin-graph` | architecture | 기능을 plugin/service package와 injection contract로 조립한다. | [package rules](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/AGENTS.md#L1-L9) | `I2` | `V2` | `W0` | topology-sensitive injection은 conformance가 필요 |
| `dsh-acp-transport` | interface | ACP는 presentation이 아닌 automation transport이며 JSON-RPC stdio server를 제공한다. | [overview](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/README.md#L1-L11), [contract](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/acp/README.md#L5-L40) | `I2` | `V2` | `W0` | typed transport 장점; runtime interoperability 미검증 |
| `dsh-acp-identity` | capability | connection이 session을 소유하고 committed output/teardown 경계를 둔다. | [contract](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/acp/README.md#L52-L81) | `I2` | `V2` | `W0` | fresh session만 지원; load/list/resume/fork 범위 제한 |
| `dsh-machine-permission` | security | ACP permission은 machine-policy channel이며 one-shot choice를 사용한다. | [ACP source](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/acp/src/index.ts#L212-L231) | `I2` | `V2` | `W0` | 조직 승인·actor identity/audit는 별도 설계 필요 |
| `dsh-windows-confinement-gap` | platform | Landlock launcher 문서는 Win32가 port가 아니라 별도 mechanism이라고 명시한다. | [support matrix](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/native/landlock-run/docs/support-matrix.md#L12-L15) | `I2` | `V2` | `W1` | Windows-specific negative evidence; Windows sandbox 지원 증거가 아님 |

## Interface와 protocol

| 표면 | transport·수명주기 | 권한 경계 | 근거 |
|---|---|---|---|
| ACP server | JSON-RPC over stdio; initialize→session/new→prompt/cancel→close | connection-owned identity, one-shot machine permission | [contract](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/acp/acp/README.md#L24-L81) |
| Plugin graph | in-process service injection | plugin topology/capability declaration을 신뢰 | [rules](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/AGENTS.md#L1-L9) |

## 운영·보안·trust boundary

- protocol session identity와 sandbox policy는 분리한다. ACP permission choice가 OS/filesystem/network confinement을 보장하지 않는다.
- provider/plugin이 선언한 capability와 실제 runtime capability는 executor conformance fixture로 확인해야 한다.

## 플랫폼과 Windows

- `W1 narrow`: Win32 confinement gap을 설명하는 fixed 문서만 확인했다. native Windows sandbox, process tree, ACL/egress는 `unknown`; W2/W3가 아니다.

## Evidence

| Evidence ID | 단계 | 방법 | 결과 | limitation |
|---|---|---|---|---|
| `dsh-static-20260815` | `I2/V2/W1` | parent pin + official fixed docs/source | partial pass | build/runtime/E2E 미실행 |
| `dsh-v3plus-none` | `V3~V6/W2~W3` | 미실행 | unknown | test source를 실행 증거로 승격하지 않음 |

## 강점과 한계

- 강점: typed ACP, connection-owned session, plugin seams가 adapter/runtime 분리에 유용하다.
- 한계: fresh-session-only ACP 범위와 Windows confinement 공백, topology-sensitive plugin 구성이 있다.

## AX 설계 재료

| 구분 | 패턴 | 근거 Claim | AX Need / 적용 조건 |
|---|---|---|---|
| Borrow | typed ACP lifecycle와 explicit session ownership | `dsh-acp-transport`, `dsh-acp-identity` | `AX-N-ADAPTER-INTEROP` |
| Adapt | plugin graph를 signed capability registry/conformance와 결합 | `dsh-plugin-graph` | provider별 capability drift 차단 |
| Avoid | permission protocol이나 Linux confinement을 Windows sandbox 보장으로 표현 | `dsh-machine-permission`, `dsh-windows-confinement-gap` | fail-closed trust boundary |
| Build | Windows executor mechanism + protocol/executor conformance suite | 위 Claims | `AD-TYPED-ADAPTER` / `RM-WINDOWS-EXECUTOR` |

## 도입 판단

- 결정: protocol/runtime 구조 참고. 최종 vendor 선택이 아니다.
- 재검토: pinned package build, ACP conformance, cancellation/teardown, Windows sandbox `V3~V5/W2`.

## 다음 검증

| Item ID | 대상 | 목표 | 시나리오 / pass 기준 |
|---|---|---|---|
| `dsh-v3-build` | package graph | `V3` | lockfile 고정 build/test |
| `dsh-v4-acp` | ACP claims | `V4` | initialize/new/prompt/cancel/close receipts와 session leak 0 |
| `dsh-w2-executor` | Windows gap | `W2` | Windows mechanism prototype에서 filesystem/process 정책 관찰 |

## 관계와 변경 이력

- `Capability acp-automation-server ADDRESSES AXNeed AX-N-ADAPTER-INTEROP`.
- 2026-08-15: `I2/V2/W1 narrow` fixed-SHA profile 작성.
