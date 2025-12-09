
import json
from pathlib import Path
from detector import IntrusionDetector
import config


def create_zones_file():
    zones_data = {
        "zones": [
            [0, 0.798758, 0.807556, 0.155078, 0.381611]
        ]
    }
    
    with open(config.ZONES_FILE, 'w') as f:
        json.dump(zones_data, f, indent=2)
    
    print(f"Created {config.ZONES_FILE}")


def main():
    if not Path(config.ZONES_FILE).exists():
        create_zones_file()
    
    detector = IntrusionDetector(
        video_path=config.VIDEO_PATH,
        zones_file=config.ZONES_FILE,
        model_name=config.MODEL_NAME
    )
    
    detector.process_video(output_path=config.OUTPUT_PATH)


if __name__ == "__main__":
    main()
