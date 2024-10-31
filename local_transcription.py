print("Importing packages...")
import os
import whisper
import time
from datetime import timedelta

video_dir = input(f"\nEnter the path to the directory containing the video/audio files: ").strip()
transcript_dir = input(f"\nEnter the path to the directory where transcripts should be saved: ").strip()

while True:
    model_size = input(f"\nEnter the preferred Whisper model size (tiny, base, small, medium, large, large-v2): ").strip()
    try:
        model = whisper.load_model(model_size)
        break
    except RuntimeError as e:
        print(f"\nError loading Whisper model: {e}. Please enter a valid model size.")

file_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.mp3', '.wav', '.flac', '.aac', '.m4a')
try:
    media_files = [f for f in os.listdir(video_dir) if f.lower().endswith(file_extensions)]
except FileNotFoundError:
    print(f"\nThe specified video/audio directory does not exist.")
    exit(1)

if not os.path.exists(transcript_dir):
    os.makedirs(transcript_dir)

existing_transcripts = [f.replace('.txt', '') for f in os.listdir(transcript_dir) if f.endswith('.txt')]

untranscribed_files = [f for f in media_files if os.path.splitext(f)[0] not in existing_transcripts]
if not untranscribed_files:
    print(f"\nNo untranscribed files found. All files have already been processed :)")
    exit(0)

for media_file in untranscribed_files:
    media_name = os.path.splitext(media_file)[0]
    transcript_path = os.path.join(transcript_dir, f"{media_name}.txt")

    if os.path.exists(transcript_path):
        print(f"\nTranscript already exists for {media_file}. Skipping transcription.")
        continue

    print(f"\nProcessing: {media_file}")
    media_path = os.path.join(video_dir, media_file)

    start_time = time.time()

    with open(transcript_path, 'w') as transcript_file:
        try:
            result = model.transcribe(media_path, language='English', condition_on_previous_text=False, fp16=False, task="transcribe")
            segments = result.get('segments', [])
            for segment in segments:
                start_time_str = str(timedelta(seconds=int(segment['start'])))
                end_time_str = str(timedelta(seconds=int(segment['end'])))
                segment_text = f"[{start_time_str} - {end_time_str}] {segment['text']}"
                transcript_file.write(f"{segment_text}\n")
                print(segment_text)
        except Exception as e:
            print(f"\nError during transcription for {media_file}: {e}")
            continue

    end_time = time.time()
    transcription_time = end_time - start_time
    minutes, seconds = divmod(transcription_time, 60)
    print(f"\nTranscription time for {media_file}: {int(minutes)} minutes and {int(seconds)} seconds")

print(f"\nTranscription process completed :)")
