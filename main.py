from fastapi import FastAPI, APIRouter
from threading import Thread
import uvicorn
from producer import capture_game_status, status, set_capture
from state_alert import *

app = FastAPI(title="Status Checker API", description="게임 상태 체크 API")

# ───────────── Status API Endpoints ─────────────
status_router = APIRouter(prefix="/status", tags=["Status"])

@status_router.get("/get", summary="현재 게임 상태 가져오기")
async def get_status():
    with status.lock:
        snapshot = status.snapshot()
        return {"resp" : snapshot}

    
@status_router.post("/clear", summary="게임 상태 초기화")
async def clear_status():
    with status.lock:
        status.clear_status_values()
        return {"resp" : None}
    
app.include_router(status_router)
# ──────────────────────────────────────────────

# ───────────── Info API Endpoints ─────────────
info_router = APIRouter(prefix="/info", tags=["Info"])

@info_router.get("/rune", summary="현재 룬 상태 가져오기")
async def get_rune_status():
    with status.lock:
        rune = status.rune.check()
        return {"resp" : rune}

@info_router.post("/rune_clear", summary="룬 상태 초기화")
async def clear_rune_status():
    with status.lock:
        status.rune.clear()
        return {"resp" : None}
    
@info_router.get("/mypos", summary="현재 위치 상태 가져오기")
async def get_mypos_status():
    with status.lock:
        mypos = status.mypos.check()
        return {"resp" : mypos}
    
app.include_router(info_router)
# ──────────────────────────────────────────────

# ───────────── Cycle API Endpoints ─────────────
cycle_router = APIRouter(prefix="/cycle", tags=["Cycle"])

@cycle_router.get("/get", summary="현재 사이클 정보 가져오기")
async def get_exp_cycle():
    with status.lock:
        current_cycle = status.exp_cycle
        return {"resp" : current_cycle}

@cycle_router.post("/set", summary="다음 사이클로 이동")
async def set_exp_cycle(cycle: int):
    with status.lock:
        status.exp_cycle = cycle
        return {"resp" : None}

app.include_router(cycle_router)
# ──────────────────────────────────────────────

# ───────────── Capture Control Endpoints ─────────────
capture_router = APIRouter(prefix="/capture", tags=["Capture"])

@capture_router.post("/on", summary="상태 감지 시작")
async def capture_on():
    set_capture(True)
    return {"resp": 0, "message": "Capture ON"}

@capture_router.post("/off", summary="상태 감지 중지")
async def capture_off():
    set_capture(False)
    with status.lock:
        status.clear_status_values()
    return {"resp": 0, "message": "Capture OFF"}

app.include_router(capture_router)
# ──────────────────────────────────────────────

# ───────────── State Alert Endpoints ─────────────
alert_router = APIRouter(prefix="/alert", tags=["Alert"])

@alert_router.post("/reset_cooldown", summary="상태 알림 쿨다운 초기화")
async def reset_cooldown_endpoint() :
    reset_cooldown()
    return {"resp": 0, "message": "Cooldown Reset"}

app.include_router(alert_router)

if __name__ == "__main__":
    Thread(target=capture_game_status, daemon=True).start()
    Thread(target=background_task, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="warning")