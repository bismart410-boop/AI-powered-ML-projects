# Intrusion Detection System

Person detection in restricted zones using YOLOv8.

## Features

- Detect people in restricted zones
- Visual alarm when intrusion detected
- 3-second alarm cooldown
- Save processed video
- Works on CPU/GPU

## Project Structure

```
intrusion-detection/
├── config.py          # Configuration
├── zone.py            # Zone handling
├── alarm.py           # Alarm system
├── detector.py        # Main detector
├── utils.py           # Helper functions
├── main.py            # Entry point
├── requirements.txt   # Dependencies
├── restricted_zones.json  # Zone coordinates
└── test.mp4          # Input video
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py`:

```python
VIDEO_PATH = 'test.mp4'
ZONES_FILE = 'restricted_zones.json'
MODEL_NAME = 'yolov8n.pt'
OUTPUT_PATH = 'output_intrusion.mp4'
ALARM_COOLDOWN = 3.0
```

## Zone Format

Edit `restricted_zones.json`:

```json
{
  "zones": [
    [0, 0.798758, 0.807556, 0.155078, 0.381611]
  ]
}
```

Format: `[class_id, x_center, y_center, width, height]` (normalized 0-1)

## Usage

### Basic Run

```bash
python main.py
```

### In Python

```python
from detector import IntrusionDetector

detector = IntrusionDetector(
    video_path='test.mp4',
    zones_file='restricted_zones.json',
    model_name='yolov8n.pt'
)

detector.process_video(output_path='output.mp4')
```

### Convert Output (Colab)

```python
from utils import convert_video

convert_video('output_intrusion.mp4', 'output_final.mp4')

from google.colab import files
files.download('output_final.mp4')
```

## Models

Available YOLO models:
- `yolov8n.pt` - fastest
- `yolov8s.pt` - small
- `yolov8m.pt` - medium
- `yolov8l.pt` - large
- `yolov8x.pt` - most accurate

## How It Works

1. Load restricted zones from JSON
2. Process video frame by frame
3. Detect people using YOLO
4. Check if person center is in zone
5. Trigger alarm if intrusion detected
6. Alarm stays on for 3 seconds after person leaves
7. Save annotated video

## Output

```
Video: 1920x1080, 30 FPS, 2061 frames
Loaded 1 zone(s)
Processed 100/2061 (Alarms: 15)
Processed 200/2061 (Alarms: 34)
...
==================================================
Complete: 2061 frames
Alarms: 250 (12.1%)
Saved: output_intrusion.mp4
==================================================
```

## Troubleshooting

**Video won't play:**
```bash
apt-get install -y ffmpeg
python -c "from utils import convert_video; convert_video('output_intrusion.mp4', 'final.mp4')"
```

**No GPU:**
- Use `yolov8n.pt` for faster processing
- GPU is auto-detected if available

**False alarms:**
- Use larger model (`yolov8l.pt`)
- Adjust zone coordinates
- Increase `ALARM_COOLDOWN`

## License

MIT
