# jarvis-gemini-assistant
//J.A.R.V.I.S.// - GEMINI AI ASSISTANT

![J.A.R.V.I.S. Interface]("D:\jarvis.png")

An interactive vocal assistant inspired by the Iron Man movies A.I, powered by Google Gemini 2.0 Flash.
This assistant features a custom-built transparent widget style GUI, persistent SQLite memory for project management, Spotify playback control, and seamless voice interactions using local wake-word detection and offline Text-to-Speech (TTS).

//FEATURES//

- AI Brain: Utilizes Google's gemini-2.0-flash model with automatic function calling (tool use) to manage tasks and execute commands
- Voice Activated: Local, ultra-fast wake-word detection using Picovoice Porcupine (Say "Jarvis" to wake him up).
- Speech-to-Text: Uses Google Speech Recognition to accurately process your commands.
- Futuristic GUI: beautifully animated customtkinter interface featuring a pulsing orb that reacts to speech, real-time CPU/RAM monitoring, a scrolling command console, and boot-up glitch animations.
- Project & Task Management: Built-in SQLite database to track engineering projects, add todos, set priorities, and manage project characteristics. JARVIS can read, write, and update these entirely via natural language.
- Spotify Integration: Ask JARVIS to play specific songs, pause music, or skip tracks directly through your Spotify Premium account.

//REQUIREMENTS//

-Google Gemini API Key : https://aistudio.google.com/\
-Picovoice Access Key : https://developer.spotify.com/dashboard
-Spotify Developer Credentials : Create an app on the Spotify Developer Dashboard to get your Client ID and Client Secret. (Note: Playback control requires a Spotify Premium account).

//INSTALLATION//

-Clone repository:
git clone https://github.com/tudor-n/jarvis-gemini-assistant.git
cd jarvis-gemini-assistant

-Ensure you have Python 3.12 and install dependencies (I recommend creating a venv):
pip install google-genai python-dotenv customtkinter spotipy pvporcupine pvrecorder SpeechRecognition pygame psutil

-Set up a .env file with the API keys:
GEMINI_API_KEY=your_gemini_api_key_here
PICO_API_KEY=your_picovoice_access_key_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

//USAGE//

Run "python main.py" to boot up!

How to interact:
- Wait for the boot sequence to finish and the console to state SYSTEM | LISTENING.
- Say "Jarvis" to activate the assistant.
- Speak your command.
 (or, of course, you can just type your command if you prefer so, in that case no need for the wake word)

Example Commands:
- "Jarvis, create a new project called DUM-E robot arm."
- "Add a high priority task to the DUM-E project to calibrate the sensors."
- "What tasks do I have pending for DUM-E?"
- "Play Back in Black on Spotify."
- "Pause the music."
- "Clear your console."

If left idle, JARVIS will occasionally chime in with witty remarks or suggestions based on your active database projects!

//NOTES//

-First Run: On the very first run, voice_output.py will automatically download the Piper executable and the voice model (~30MB). It may take a moment before he speaks for the first time.

-Spotify Redirect: The first time you ask him to play a song, your browser will open to authenticate Spotify. After logging in, you will be redirected to a localhost URL. Copy that URL and paste it into the console if prompted, or let Spotipy cache it automatically.

-Spotify Use: Spotify must determine an active connection, which entails playing a few songs for 10 seconds manually before JARVIS can properly interact with spotify, it's a quirk but once it works the session will not expire!
