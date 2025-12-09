
import cv2
import json
from pathlib import Path
from ultralytics import YOLO
from zone import RestrictedZone
from alarm import AlarmSystem

try:
    from google.colab.patches import cv2_imshow
    IN_COLAB = True
except ImportError:
    IN_COLAB = False


class IntrusionDetector:
    def __init__(self, video_path, zones_file, model_name):
        self.video_path = video_path
        self.zones_file = zones_file
        self.model = YOLO(model_name)
        self.zones = []
        self.alarm = AlarmSystem()
        
    def load_zones(self, frame_shape):
        if not Path(self.zones_file).exists():
            print(f"Warning: {self.zones_file} not found")
            return
        
        with open(self.zones_file, 'r') as f:
            zones_data = json.load(f)
        
        for zone_data in zones_data['zones']:
            self.zones.append(RestrictedZone(zone_data, frame_shape))
        
        print(f"Loaded {len(self.zones)} zone(s)")
    
    def check_intrusion(self, detections):
        for detection in detections:
            x1, y1, x2, y2, confidence, class_id = detection
            class_name = self.model.names[int(class_id)]
            
            if class_name == 'person':
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                
                for zone in self.zones:
                    if zone.contains_point(center_x, center_y):
                        return True
        return False
    
    def process_video(self, output_path=None):
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open {self.video_path}")
            return
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Video: {width}x{height}, {fps} FPS, {total_frames} frames")
        
        ret, first_frame = cap.read()
        if not ret:
            print("Error: Could not read first frame")
            return
        
        self.load_zones(first_frame.shape)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        alarm_frames = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                results = self.model(frame, verbose=False)
                detections = results[0].boxes.data.tolist()
                
                intrusion = self.check_intrusion(detections)
                self.alarm.update(intrusion)
                
                if self.alarm.active:
                    alarm_frames += 1
                
                annotated = results[0].plot()
                
                for zone in self.zones:
                    zone.draw(annotated)
                
                self.alarm.draw(annotated)
                
                if out:
                    out.write(annotated)
                
                if frame_count % 100 == 0:
                    print(f"Processed {frame_count}/{total_frames} (Alarms: {alarm_frames})")
        
        finally:
            cap.release()
            if out:
                out.release()
            
            print(f"\n{'='*50}")
            print(f"Complete: {frame_count} frames")
            print(f"Alarms: {alarm_frames} ({(alarm_frames/frame_count)*100:.1f}%)")
            if output_path:
                print(f"Saved: {output_path}")
            print(f"{'='*50}")
