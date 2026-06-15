import os
import base64
import requests
import cv2
import tempfile

class VideoService:
    def __init__(self, model_name: str = "moondream:latest", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_url = f"{ollama_url}/api/chat"

    def _extract_frames(self, video_path: str, interval_seconds: int = 5) -> list:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_seconds)
    
        frame_paths = []
        frame_count = 0
    
        # FIXED: Indented the entire while loop to sit inside _extract_frames
        while True:
            success, frame = cap.read()
            if not success:
                break
            if frame_count % frame_interval == 0:
                frame_path = f"{video_path}_frame_{frame_count}.jpg"
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
            frame_count += 1
    
        cap.release()
        return frame_paths

    def analyze_frame(self, file_path: str, prompt: str = "Describe what is happening in this image or video frame.") -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Frame file not found at: {file_path}")

        print(f"[VideoService] Extracting frames from: {file_path}...")
        frame_paths = self._extract_frames(file_path)

        descriptions = []
        for frame_path in frame_paths:
            try:
                with open(frame_path, "rb") as f:
                    image_b64 = base64.b64encode(f.read()).decode('utf-8')
                
                # Clean up the frame file immediately after reading
                os.remove(frame_path)

                payload = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt, "images": [image_b64]}],
                    "stream": False
                }

                res = requests.post(self.api_url, json=payload)
                res.raise_for_status()
                descriptions.append(res.json()["message"]["content"].strip())
                
            except requests.exceptions.RequestException as e:
                print(f"[VideoService] Error on frame {frame_path}: {e}")
                continue
            except FileNotFoundError:
                print(f"[VideoService] Could not find frame file: {frame_path}")
                continue

        return "\n---\n".join(descriptions)