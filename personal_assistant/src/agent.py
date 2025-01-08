import os
import wave
import asana
import pyttsx3
import whisper
import numpy as np
import pyaudio  # Needed for WakeWordDetector (and if you're streaming audio)

from src.asana_integration import AsanaIntegration
from src.weaviate_integration import WeaviateIntegration
from src.ollama_integration import OllamaIntegration
from src.file_handling import FileHandler
from src.web_scraping import WebScraper


class WakeWordDetector:
    """
    A simple placeholder class for wake word detection.
    You might need a more sophisticated approach (e.g., Snowboy, Precise, VAD-based).
    Right now, it just sets up a PyAudio stream and listens for fixed audio duration
    to check if the user says the wake word.
    """
    def __init__(self, wake_word="hey miles", sample_rate=16000, chunk_size=1024):
        self.wake_word = wake_word.lower()
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def listen_for_wake_word(self):
        """
        Dummy method: listens for a short time and 'pretends' it found the wake word.
        Replace with your actual wake word detection logic.
        """
        print("Listening for wake word... (simulated 2-second wait)")
        # You might do a loop reading from self.stream until you detect your wake word
        # Here we just read 2 seconds of audio and assume we found it
        duration = 2  # seconds
        _ = self.stream.read(int(self.sample_rate * duration), exception_on_overflow=False)

        # In a real scenario, you'd process the audio buffer to check for 'hey miles'
        # We'll just print a line to show it's 'detected.'
        print("Wake word presumably detected.")


class PersonalAssistantAgent:
    """
    A personal assistant agent that uses:
      - Whisper for STT
      - pyttsx3 for TTS
      - Ollama for LLM-based responses
      - Weaviate for storing or querying knowledge
      - Asana for tasks
      - Web scraping for external data
    """

    def __init__(self):
        # 1. Initialize integrations
        #    (Replace 'your_asana_api_key' with an env variable or secure retrieval in production.)
        self.client = asana.Client.access_token(os.getenv('ASANA_ACCESS_TOKEN'))
        self.weaviate = WeaviateIntegration(url="http://localhost:8080")
        self.ollama = OllamaIntegration(url="http://localhost:11434", model="ollama3.1-8b")
        
        # Define storage_dir before using it
        storage_dir = "C:/Users/Jareds AI/Documents/personal_agent_file_storage"
        os.makedirs(storage_dir, exist_ok=True)
        self.file_handler = FileHandler(storage_dir=storage_dir)
        
        self.web_scraper = WebScraper()

        # 2. Initialize text-to-speech (TTS) engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", 150)    # Speed of speech
        self.tts_engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)
        # Optional: Change voice if you like
        # voices = self.tts_engine.getProperty('voices')
        # self.tts_engine.setProperty('voice', voices[0].id)

        # 3. Wake word detector (PyAudio-based)
        self.wake_word_detector = WakeWordDetector(wake_word="Hey Miles")

        # 4. Load Whisper model (medium can be large; consider 'base' or 'small' if speed is an issue)
        self.stt_model = whisper.load_model("medium")

    def speak(self, text: str):
        """
        Convert text to speech using pyttsx3.
        """
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, record_seconds: int = 5) -> str:
        """
        Convert speech to text using Whisper.
        - Records `record_seconds` from the microphone
        - Writes the audio to a temporary WAV file with the correct header
        - Transcribes using Whisper
        - Removes the temp file
        """
        sample_rate = 16000  # 16 kHz
        print("Listening for user speech...")

        # Record audio from the existing PyAudio stream
        raw_data = self.wake_word_detector.stream.read(
            int(record_seconds * sample_rate),
            exception_on_overflow=False
        )

        # Convert to a NumPy array
        audio_array = np.frombuffer(raw_data, dtype=np.int16)

        # Save the audio to a temporary WAV file with a proper header
        temp_wav = "temp.wav"
        with wave.open(temp_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(sample_rate)
            wf.writeframes(audio_array.tobytes())

        # Transcribe the audio using Whisper
        print("Transcribing...")
        result = self.stt_model.transcribe(temp_wav)
        transcript = result.get("text", "").strip()
        print(f"You said: {transcript}")

        # Cleanup the temp file
        try:
            os.remove(temp_wav)
        except OSError:
            pass

        return transcript

    def fetch_and_store_tasks(self):
        """
        Example method for fetching tasks from Asana and storing them in Weaviate or elsewhere.
        Replace with your actual logic (e.g., AsanaIntegration / WeaviateIntegration usage).
        """
        print("Fetching tasks from Asana and storing them...")
        tasks = self.asana.get_tasks()  # e.g., returns a list of tasks
        # Pseudocode for storing tasks in Weaviate
        # for task in tasks:
        #     self.weaviate.store_task(task)
        print("Tasks retrieved and stored (dummy).")

    def scrape_and_store_data(self):
        """
        Example method for scraping data from the web and storing it locally or in Weaviate.
        Replace with your actual logic.
        """
        print("Scraping data from a website...")
        data = self.web_scraper.scrape("https://example.com")
        # Pseudocode for storing data
        # self.file_handler.save(data, "web_data.txt")
        print("Scraped data saved (dummy).")

    def run(self):
        """
        Main loop for the personal assistant:
          1. Wait for the wake word
          2. Fetch and store tasks
          3. Scrape data
          4. Listen to user speech
          5. Generate a response with Ollama
          6. Speak the response
        """
        try:
            print("Ready. Waiting for wake word...")
            self.wake_word_detector.listen_for_wake_word()
            print("Wake word detected!")

            # Example workflow
            self.fetch_and_store_tasks()
            self.scrape_and_store_data()

            # Listen to user input
            user_input = self.listen(record_seconds=5)
            if user_input:
                response = self.ollama.generate_response(user_input)
                if response:
                    print("Response:", response)
                    self.speak(response)
                else:
                    print("No response generated.")
            else:
                print("No input received.")

        except Exception as e:
            print(f"Error in run(): {e}")