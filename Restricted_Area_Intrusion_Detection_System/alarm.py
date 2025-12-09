import cv2
import time


class AlarmSystem:
    def __init__(self, cooldown=3.0):
        self.active = False
        self.last_intrusion_time = 0
        self.cooldown = cooldown
    
    def update(self, intrusion_detected):
        current_time = time.time()
        
        if intrusion_detected:
            self.active = True
            self.last_intrusion_time = current_time
        else:
            if self.active and (current_time.time() - self.last_intrusion_time) > self.cooldown:
                self.active = False
    
    def draw(self, frame):
        if not self.active:
            return
        
        h, w = frame.shape[:2]
        text = "ALARM!"
        font_scale = 3
        thickness = 5
        
        (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        cv2.rectangle(frame, (w//2 - text_w//2 - 20, 50 - text_h - 20),
                     (w//2 + text_w//2 + 20, 50 + 20), (0, 0, 0), -1)
        
        cv2.putText(frame, text, (w//2 - text_w//2, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
