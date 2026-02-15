import os
import time
import subprocess
import shutil
import pygame
import urllib.request
import zipfile

CREATE_NO_WINDOW = 0x08000000

class VoiceOutput: 
    def __init__(self):
        self.piper_url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip"
        self.voice_model_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/medium/en_US-ryan-medium.onnx?download=true"
        self.voice_config_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json?download=true"
        
        self.piper_dir = "piper_bin"
        self.piper_exe = os.path.join(self.piper_dir, "piper", "piper.exe")
        self.model_path = "en_US-ryan-medium.onnx" 
        self.config_path = "en_US-ryan-medium.onnx.json"

        self._setup_piper()
        self._setup_model()
        
        pygame.mixer.init()
        print("Voice Output initialized (Standalone Offline Engine).")

    def _setup_piper(self):
        if not os.path.exists(self.piper_exe):
            print("Piper executable not found. Downloading standalone version...")
            zip_path = "piper_windows.zip"

            urllib.request.urlretrieve(self.piper_url, zip_path)
            print("Download complete. Extracting...")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.piper_dir)

            os.remove(zip_path)
            print("Piper setup complete.")

    def _setup_model(self):
        if not os.path.exists(self.model_path):
            print(f"Downloading voice model... (approx 30MB)")
            urllib.request.urlretrieve(self.voice_model_url, self.model_path)
            urllib.request.urlretrieve(self.voice_config_url, self.config_path)
            print("Model download complete.")

    def speak(self, text: str):
        print(f"JARVIS says: {text}")
        output_file = "output.wav"

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload() 
        
        time.sleep(0.2)

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                output_file = f"output_{int(time.time())}.wav"
            
        try:
            command = [
                self.piper_exe,
                "--model", self.model_path,
                "--output_file", output_file
            ]
            
            process = subprocess.run(
                command,
                input=text.encode('utf-8'),
                capture_output=True,
                creationflags=CREATE_NO_WINDOW
            )
            
            if process.returncode != 0:
                print(f"Piper Error: {process.stderr.decode()}")
                return
            
            if os.path.exists(output_file):
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                pygame.mixer.music.unload()
            else:
                print("Error: Audio file was not generated.")
                
        except Exception as e:
            print(f"Voice Error: {e}")