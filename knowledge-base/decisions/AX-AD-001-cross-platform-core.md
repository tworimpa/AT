---
id: AX-AD-001
type: ArchitectureDecision
title: Windows와 Linux native executor를 모두 core로 둔다
status: accepted
decided_at: 2026-08-15
owner: project-owner
source_parent_commit: 0ca049319ad73ff8e2709957467b57768e1b7ff0
verification_ceiling: V1
tags:
  - knowledge-base
  - architecture-decision
  - cross-platform
  - windows
  - linux
---

# AX-AD-001: Windows와 Linux native executor를 모두 core로 둔다

[지식 베이스 홈](../index.md) · [지속 컨텍스트](../ax-platform-context.md) · [reference architecture](../internal-ax-reference-architecture.md) · [플랫폼 청사진](../platform-blueprint.md)

## 결정

사내 AX 에이전트 플랫폼은 Windows 전용 또는 Windows-first 제품으로 한정하지 않는다. Windows native와 Linux native executor를 모두 minimal core의 first-class 구현으로 둔다.

두 executor는 Task/Run/Event, command/environment, structured stdio·PTY event, capability negotiation, cancel/timeout/kill-tree, workspace/resource lease, artifact/receipt와 environment fingerprint의 공통 contract를 구현한다. 공통 interface가 플랫폼 동등성을 뜻하지는 않으며 OS별 process·PTY·filesystem·credential semantics와 failure boundary를 capability profile과 독립 evidence로 드러낸다.

WSL, container, SSH와 cloud sandbox는 Windows/Linux host-native evidence를 대신하지 않는 별도 provider다.

## 결정 근거와 권한

- 2026-08-15 프로젝트 owner가 “프로젝트는 Windows만을 위한 기획이 아니며 Linux도 당연히 고려해야 한다”고 명시하고 cross-platform 방향으로 문서 수정을 요청했다.
- 기존 문서의 Windows 강조는 Linux-default 가정으로 Windows 검증을 생략하지 않기 위한 문제의식으로 한정한다. 제품 범위를 Windows로 제한하는 근거로 사용하지 않는다.
- 이 기록은 owner의 제품 범위 결정을 보존하는 `V1` 문서 evidence이며 구현·build·runtime 또는 Windows/Linux parity를 증명하지 않는다.

## 검토한 대안

| 대안 | 판단 | 이유 |
|---|---|---|
| Windows native만 core, Linux는 remote/optional | rejected | 승인된 제품 범위와 맞지 않고 Linux native lifecycle을 부차화함 |
| Linux를 암묵적 기본값으로 두고 Windows만 별도 adapter | rejected | 플랫폼별 차이와 Windows failure boundary를 다시 숨길 수 있음 |
| 단일 generic executor가 OS 차이를 내부에서 숨김 | rejected | capability·isolation·cancel·filesystem semantics의 거짓 parity 위험 |
| 공통 contract + Windows/Linux native 구현 + OS별 evidence | accepted | 공통 control plane을 유지하면서 플랫폼별 보장과 한계를 분리 가능 |

## 결과와 제약

- Windows native와 Linux native executor는 roadmap `P1` local core에 함께 포함한다.
- 양쪽은 공통 conformance suite와 OS별 failure fixture를 각각 통과해야 한다.
- 기존 Windows `W0~W3` 조사값은 역사 evidence로 보존하고, 신규·갱신 Claim은 OS별 `P0~P3`을 사용한다.
- 한 OS의 성공 evidence, WSL/container/remote guest 또는 CI 존재를 다른 OS의 native 지원 증거로 사용하지 않는다.
- 기존 Windows 중심 일정 추정은 더 이상 commitment가 아니며 target support matrix가 결정된 뒤 재산정한다.

## 아직 결정되지 않은 사항

- Windows edition/version/architecture와 PowerShell 지원 범위
- Linux distribution/version/architecture와 shell·init/service manager 지원 범위
- 두 OS의 release parity 수준과 지원 수명
- 첫 pilot 업무·사용자군·실행 환경·성공 및 중단 기준
- macOS를 core, 후속 또는 비범위로 둘지 여부

## 재검토 조건

지원 대상 OS가 추가·제거되거나, 특정 플랫폼을 core에서 optional provider로 바꾸거나, platform parity 정책을 결정할 때 재검토한다. owner, 대안, 영향, migration과 evidence 계획을 기록하지 않고 이 결정을 암묵적으로 변경하지 않는다.
