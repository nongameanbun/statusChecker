# nongameanbun - statusChecker

## 프로젝트 구조
```text
.
├── main.py # 게임 상태 확인 API 라우터 (Status, Info, Cycle, Capture 등)
├── gateway.py # 타 마이크로서비스 API 연동을 위한 게이트웨이
├── producer.py # 화면을 캡처하여 주기적으로 상태 정보 갱신 (거짓말탐지기, 위반 등)
├── state_alert.py # 감지된 상태에 대한 알림 쿨다운 관리 및 엔드포인트
├── .env.example # 환경 변수 예시 파일
├── exp_check.png # 경험치 상태 추적을 위한 템플릿 매칭 이미지
└── utils # 상태 관리 및 추적 유틸리티
    ├── base.py # 공통 상태 관리(StatusManager), 큐 및 스레드 락
    └── exp_tracker.py # 경험치 변화량 트래킹 유틸리티
```

## 사전 요구 사항

### 환경 변수 세팅 (`.env`)
환경에 맞게 각 포트 번호를 지정하여 프로젝트 루트에 `.env` 파일을 생성합니다.

```powershell
Copy-Item .env.example .env
```

`.env.example` 포맷 예시:
```ini
inputHandler_API_PORT=8001
statusChecker_API_PORT=8002
alarmHandler_API_PORT=8003
intrAction_API_PORT=8004
mainAction_API_PORT=8005
subaction_API_PORT=8006
streaning_API_PORT=8007
objectDetector_API_PORT=8008
runeSolver_API_PORT=8020
```

## 실행 방법

```bash
pip install -r requirements.txt
python main.py
```

`localhost:8002/docs` 로 swagger 명세를 확인 가능
