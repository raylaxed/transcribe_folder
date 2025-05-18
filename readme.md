# 🎧 Audio Transcription Pipeline with Silence Removal & Whisper

This Python project automates the transcription of `.m4a` audio files using OpenAI's Whisper. It removes silent segments to improve transcription quality and speed, then generates text files for each cleaned audio file.

---

## 📁 Folder Structure

```
your-project/
├── input_m4a/           # Raw .m4a files (input)
├── output_cut/          # Cleaned audio files (.mp3)
├── output_text/         # Transcription text files
├── process_audio.py     # Main processing script
├── requirements.txt     # Dependency list
└── README.md            # Project documentation
```

🚀 Quick Start
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
2. Install dependencies
Make sure FFmpeg is installed system-wide.

Then install Python packages:


pip install -r requirements.txt


3. Add audio files
Place your .m4a files into the input_m4a/ folder.

4. Run the script

python process_audio.py


Processed audio will go into output_cut/, and transcripts will be saved in output_text/.

⚙️ Configuration
You can adjust these variables at the top of process_audio.py:

SILENCE_THRESHOLD = -35       # dBFS threshold for silence removal
CHUNK_LENGTH_MS = 500         # Duration of each chunk (ms)
MODEL_NAME = "small"          # Whisper model: base, small, medium, large


🧠 Dependencies
pydub

mutagen

openai-whisper

FFmpeg – must be installed separately

📄 License
MIT License – free to use and modify.
