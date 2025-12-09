import cv2


class RestrictedZone:
    def __init__(self, zone_data, frame_shape):
        self.class_id = int(zone_data[0])
        x_center = zone_data[1]
        y_center = zone_data[2]
        width = zone_data[3]
        height = zone_data[4]
        
        h, w = frame_shape[:2]
        self.x1 = int((x_center - width/2) * w)
        self.y1 = int((y_center - height/2) * h)
        self.x2 = int((x_center + width/2) * w)
        self.y2 = int((y_center + height/2) * h)
    
    def contains_point(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def draw(self, frame, color=(0, 0, 255)):
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), color, 2)
        cv2.putText(frame, "RESTRICTED", (self.x1, self.y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
