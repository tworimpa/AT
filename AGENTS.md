# Repository agent rules

이 파일은 이 저장소에서 실행되는 모든 에이전트의 지속 공통 규칙이다. 역할별 책임은 작업 계약이 정하고, 모델·effort·권한·예산을 묶는 실행 정책은 [agent profile catalog](knowledge-base/agent-profiles.md)가 정한다. Profile은 역할이 아니며 역할 이름만으로 권한이나 검증 등급을 추정하지 않는다.

## 작업 계약과 성공 기준

- 시작 전에 요청 범위, 비범위, 기준 branch/SHA, 허용된 변경·외부 동작, 성공 기준과 필요한 증거를 짧게 명시한다.
- 발견한 추가 문제는 현재 성공 기준에 필요하지 않으면 고치지 않고 별도 관찰로 보고한다.
- 기존 사용자 변경과 untracked 개인 설정을 보존하고, 변경 대상만 명시적으로 stage한다.

## Profile 선택

- 작업 성격과 위험에 맞는 profile ID를 선택하고 실행 기록에 남긴다. 사용자가 지정한 profile이 있으면 우선한다.
- profile이 요구하는 모델 등급이나 effort를 실행기가 지원하지 않으면 조용히 대체하지 말고 실제 선택값과 제한을 기록한다. 권한·위험이 넓어지는 대체는 사람 승인을 받는다.
- 읽기 작업에서 쓰기 작업으로, 정적 검토에서 runtime/외부 서비스로 범위가 바뀌면 profile과 작업 계약을 다시 확인한다.

## 실행 기록과 증거

- 최소 기록: task/run ID, profile ID/revision, 역할, model provider·slug·version, effort, 시작/종료 시각, base/head SHA, environment fingerprint, 실행 명령·exit code, 변경 artifact, cost/latency 관찰값과 알려진 제한.
- model/version, 비용, latency를 관찰하지 못했으면 `unknown`으로 남기며 추정값을 사실처럼 기록하지 않는다.
- 문서 주장 `V1`, fixed-SHA 정적 코드 `V2`, build `V3`, 통제 runtime `V4`, E2E/failure injection `V5`, 운영 `V6`를 분리한다. Windows 정적 경로 `W1`을 실제 Windows 실행 `W2/W3`로 승격하지 않는다.
- agent 자기보고, green 정적 검사, gitlink 일치, CI는 각각 해당 범위의 증거일 뿐 merge·배포·외부 서비스·production 성공을 자동 증명하지 않는다.

## 권한과 사람 승인

- 최소 권한과 fail-closed를 기본으로 한다. secret 원문을 출력·기록·커밋하지 않는다.
- 명시 승인 없이 push, merge, 배포, production 변경, 외부 메시지/승인, 비용 발생 서비스, credential·권한 변경, 데이터 삭제를 수행하지 않는다.
- destructive 또는 복구가 어려운 동작은 정확한 대상과 복구 경계를 확인하고 필요한 사람 승인을 받은 뒤 수행한다.

## 재시도와 escalation

- 같은 실패를 무한 반복하지 않는다. profile의 retry budget 안에서 원인 가설과 입력을 바꾼 좁은 재시도만 수행하고 각 attempt를 보존한다.
- 권한 부족, 요구 충돌, base drift, secret 필요, 반복 실패, 예산/시간 한계, 증거 부족이면 안전한 상태에서 중단하고 blocker·시도·필요 결정을 보고한다.
- 더 강한 모델, 높은 effort, 넓은 권한, runtime/E2E 또는 외부 시스템으로 승격하면 새 profile/attempt로 기록하고 승인 조건을 적용한다.

## 완료 보고

- 결과, 변경 파일, commit/head SHA, 수행한 검증과 exit 결과, 미수행 항목·남은 한계, 외부 write/push/deploy 여부를 함께 보고한다.
- 성공 기준이 충족되지 않았으면 `complete`로 표현하지 않는다. 부분 성공과 미확인 증거를 분리한다.
