from collections import deque
from threading import RLock
from gateway import *

class Rune :
    def __init__(self):
        self.Q = deque(maxlen=1)

    def check(self) :
        if len(self.Q) == 0:
            return None
        elem = self.Q[0]
        print(f"Rune Position: {elem}")
        return elem

    def update(self) :
        pos = find_in_screen("rune", "0, 0, 300, 250", conf=0.9)
        if pos:
            c = (int(pos['center'][0]), int(pos['center'][1]))
            if c in self.Q:
                return
            self.Q.append(c)
        return

    def clear(self) :
        self.Q.clear()
        print("Rune Cleared")
        return

class MyPos :
    def __init__(self):
        self.img = "me"
        self.img_LR = ["me_L", "me_R"]

    def check(self, stack = 0) :
        
        detection_res = find_in_screen_multiple("me, me_L, me_R", xywh="0, 0, 300, 250", confs="0.9, 0.99, 0.99")
        _me   = detection_res.get("me",   [])
        _me_L = detection_res.get("me_L", [])
        _me_R = detection_res.get("me_R", [])
        me   = _me[0]   if _me   else None
        me_L = _me_L[0] if _me_L else None
        me_R = _me_R[0] if _me_R else None
        
        if(me == None):
            if(me_L != None):
                me = (int(301), int(me_L['center'][1]))
            elif(me_R != None):
                me = (int(-1), int(me_R['center'][1]))
            else:
                me = (1050, 1050)
        else :
            c = me["center"]
            me = (int(c[0]), int(c[1]))

        if me != (1050, 1050):
            return me
        if stack < 3 :
            return self.check(stack + 1)
        return me

class statusQ() :
    def __init__(self):
        self.lock = RLock()
        self.liecheck = deque(maxlen = 20)
        self.viol = deque(maxlen = 5)
        self.shape = deque(maxlen = 5)
        self.dead = deque(maxlen = 5)
        self.elbo = deque(maxlen = 30)
        self.exception = deque(maxlen = 20)
        self.rune = Rune()
        self.mypos = MyPos()
        self.exp_cycle = 10

    def snapshot(self):
        with self.lock:
            return {
                "liecheck": sum(self.liecheck) / self.liecheck.maxlen if self.liecheck else 0.0,
                "viol": sum(self.viol) / self.viol.maxlen if self.viol else 0.0,
                "shape": sum(self.shape) / self.shape.maxlen if self.shape else 0.0,
                "elbo": sum(self.elbo) / self.elbo.maxlen if self.elbo else 0.0,
                "dead": sum(self.dead) / self.dead.maxlen if self.dead else 0.0,
                "exception": sum(self.exception) / self.exception.maxlen if self.exception else 0.0,
                "exp_cycle": self.exp_cycle,
            }

    def clear_status_values(self):
        with self.lock:
            self.liecheck.clear()
            self.viol.clear()
            self.shape.clear()
            self.elbo.clear()
            self.dead.clear()
            self.exception.clear()

status = statusQ()
capture_enabled = False             # off by default — runner가 on() 호출해야 감지 시작

