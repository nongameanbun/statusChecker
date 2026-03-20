import dotenv
import os
import requests
import time

from gateway import add_intr, get_status


message_recent = {}

COOLDOWN_SEC = 20

def _should_fire(intr_type):
    """첫 감지 → 즉시 발동, 이후 COOLDOWN_SEC 내 재발동 차단."""
    now = time.time()
    last = message_recent.get(intr_type)
    if last is None or now - last >= COOLDOWN_SEC:
        message_recent[intr_type] = now
        return True
    return False

def reset_cooldown():
    """쿨다운 기록 초기화 — 새 빌드 시작 시 호출"""
    global message_recent
    message_recent = {}
    print("[state_alert] cooldown reset")

def background_task():
    global message_recent
    while True :
        try :
            while True :
                time.sleep(0.1)
                status = get_status()

                for key in ("liecheck", "viol", "shape", "dead", "exception"):
                    if status.get(key, 0) > 0.8 and _should_fire(key):
                        add_intr(key)

        except Exception as e:
            pass
    