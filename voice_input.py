import pvporcupine
from pvrecorder import PvRecorder
import speech_recognition as sr
import time

class VoiceInput:
    def __init__(self, access_key):
        self.access_key = access_key 
        
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key, 
                keywords=['jarvis']
            )
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            raise

        self.recorder = PvRecorder(
            device_index=-1, 
            frame_length=self.porcupine.frame_length
        )
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 2.0 
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300 

    def wait_for_wake_word(self) -> bool:
        """Listens briefly for the wake word then releases control."""
        self.recorder.start()
        start_time = time.time()
        
        try:
            while time.time() - start_time < 1.0:
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)
                if result >= 0:
                    self.recorder.stop()
                    return True
            
            self.recorder.stop()
            return False
            
        except Exception as e:
            self.recorder.stop()
            return False

    def listen_for_command(self) -> str:
        """Active listening for the command with extended patience."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for command...")
            
            try:
                audio = self.recognizer.listen(
                    source, 
                    timeout=5, 
                    phrase_time_limit=20
                )
                
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"Heard: {text}")
                return text.lower()
                
            except sr.WaitTimeoutError:
                print("No speech detected.")
                return ""
            except sr.UnknownValueError:
                print("Could not understand the audio.")
                return ""
            except Exception as e:
                print(f"Speech error: {e}")
                return ""