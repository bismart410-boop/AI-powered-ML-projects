
import subprocess


def convert_video(input_path, output_path):
    try:
        print(f"Converting {input_path}...")
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-vcodec', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-y',
            output_path
        ], check=True, capture_output=True)
        print(f"Saved: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except FileNotFoundError:
        print("Install ffmpeg: apt-get install -y ffmpeg")
        return None
