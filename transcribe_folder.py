import os
from datetime import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import whisper
from mutagen.mp4 import MP4

# --- Settings ---
INPUT_FOLDER = "input_m4a"
CUT_FOLDER = "output_cut"
TEXT_FOLDER = "output_text"
SILENCE_THRESHOLD = -35  # dBFS
CHUNK_LENGTH_MS = 500
MODEL_NAME = "small"  # Whisper model: base, small, medium, large

# --- Ensure Output Folders Exist ---
os.makedirs(CUT_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

# --- Load Whisper Model Once ---
model = whisper.load_model(MODEL_NAME)

def get_timestamp_from_metadata_or_file(file_path):
    try:
        audio = MP4(file_path)
        date_tag = audio.tags.get('©day', [None])[0]
        if date_tag:
            # Handle cases like "2024-12-01T14:32:00Z"
            dt = datetime.strptime(date_tag.split("T")[0], "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"⚠️ Metadata read error: {e}")
    
    # Fallback to file system time
    t = os.path.getmtime(file_path)
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d_%H-%M-%S")

def remove_silence(input_file, output_file, silence_thresh, chunk_length_ms):
    audio = AudioSegment.from_file(input_file, format="m4a")
    chunks = make_chunks(audio, chunk_length_ms)
    loud_chunks = [chunk for chunk in chunks if chunk.dBFS > silence_thresh]
    
    if loud_chunks:
        output_audio = loud_chunks[0]
        for chunk in loud_chunks[1:]:
            output_audio += chunk
        output_audio.export(output_file, format="mp3")
        return True
    else:
        return False

def process_all_files():
    for filename in sorted(os.listdir(INPUT_FOLDER)):  # Ensures predictable order
        if filename.endswith(".m4a"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            timestamp_prefix = get_timestamp_from_metadata_or_file(input_path)
            base_name = os.path.splitext(filename)[0]
            
            cut_filename = f"{timestamp_prefix}_{base_name}_cut.mp3"
            cut_path = os.path.join(CUT_FOLDER, cut_filename)

            print(f"\n🔊 Processing: {filename}")

            # Step 1: Remove silence
            success = remove_silence(input_path, cut_path, SILENCE_THRESHOLD, CHUNK_LENGTH_MS)
            if not success:
                print(f"⚠️ Skipped {filename} — all audio was below threshold.")
                continue

            # Step 2: Transcribe
            print(f"📝 Transcribing: {cut_filename}")
            result = model.transcribe(cut_path)

            transcript_filename = f"{timestamp_prefix}_{base_name}_transcript.txt"
            transcript_path = os.path.join(TEXT_FOLDER, transcript_filename)

            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(result["text"])

            print(f"✅ Saved transcript: {transcript_path}")

if __name__ == "__main__":
    process_all_files()
