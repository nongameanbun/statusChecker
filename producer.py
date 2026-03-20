
from utils.base import *
import time

from utils.exp_tracker import get_exp_status

def set_capture(on: bool):
    global capture_enabled
    capture_enabled = on

def capture_game_status() :
    liecheck_model = "liecheck_251129"

    condition_exception = False
    cnt = 0
    try :
        while True :
            time.sleep(0.1)
            # 0. capture off 이면 대기
            if not capture_enabled:
                continue

            # 1. Update Rune Status
            with status.lock:
                status.rune.update()

            # 2. Liecheck Detection
            condition_liecheck = (len(find_in_screen_yolo(liecheck_model)) >= 1)

            # 3. Viol, Shape, Elbo Detection
            detection_results = find_in_screen_multiple("notice_viol, notice_shape, elbo, notice_dead")
            
            condition_viol = detection_results.get("notice_viol", []) != []
            condition_shape = detection_results.get("notice_shape", []) != []
            condition_elbo = detection_results.get("elbo", []) != []
            condition_dead = detection_results.get("notice_dead", []) != []

            # 4. Update deques
            with status.lock:
                status.liecheck.append(condition_liecheck)
                status.viol.append(condition_viol)
                status.shape.append(condition_shape)
                status.elbo.append(condition_elbo)
                status.dead.append(condition_dead)

            # 5. Exception Detection
            if cnt == 0:
                condition_exception = get_exp_status()
                with status.lock:
                    status.exception.append(condition_exception)
            cnt = (cnt + 1) % 15

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("error")
        return
    
