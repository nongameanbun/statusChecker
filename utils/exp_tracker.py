import cv2
import numpy as np
from PIL import ImageGrab


def get_exp_status():
    try:
        x1, y1 = (400 + 171, 788)
        x2, y2 = (624 + 171, 802)

        cur_img_pil = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        cur_img = cv2.cvtColor(np.array(cur_img_pil), cv2.COLOR_RGB2BGR)

        prev_img = cv2.imread('exp_check.png')
        if prev_img is None:
            cv2.imwrite('exp_check.png', cur_img)
            return False

        if cur_img.shape != prev_img.shape:
            prev_img = cv2.resize(prev_img, (cur_img.shape[1], cur_img.shape[0]))

        cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(cur_gray, prev_gray, cv2.TM_CCOEFF_NORMED)
        similarity = float(res[0][0])

        threshold = 0.9

        if similarity > threshold:
            return True
        return False

    except Exception as e:
        print(f"Exception in get_exp_status: {e}")
        return False

    finally:
        # 마지막 캡처 이미지를 파일로 저장 (디버깅/업데이트용)
        try:
            cv2.imwrite('exp_check.png', cur_img)
        except Exception:
            pass
