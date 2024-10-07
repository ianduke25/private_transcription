import os
import whisper
import subprocess
import time
from subprocess import CalledProcessError, SubprocessError
from datetime import timedelta

# Accept user input for directories
video_dir = input("Enter the path to the directory containing the video files: ").strip()
transcript_dir = input("Enter the path to the directory where transcripts should be saved: ").strip()

# Load the Whisper model
model = whisper.load_model("large-v2") # This model works best, but uses quite a bit of RAM. Feel free to play with other model sizes!

# Get list of only video files
video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.MP4'))]

# Create transcript directory if it doesn't exist
if not os.path.exists(transcript_dir):
    os.makedirs(transcript_dir)

# Get list of existing transcript files
existing_transcripts = [f.replace('.txt', '') for f in os.listdir(transcript_dir) if f.endswith('.txt')]

# Calculate total size of untranscribed files
untranscribed_files = [f for f in video_files if os.path.splitext(f)[0] not in existing_transcripts]
total_size = sum(os.path.getsize(os.path.join(video_dir, f)) for f in untranscribed_files)

# Process each untranscribed video file
for video_file in untranscribed_files:
    video_name = os.path.splitext(video_file)[0]

    print(f"Processing: {video_file}")
    video_path = os.path.join(video_dir, video_file)

    # Check if the video contains an audio stream
    skip_audio_check = False
    try:
        # Using ffprobe to check for audio streams
        cmd = ['ffprobe', '-i', video_path, '-show_streams', '-select_streams', 'a', '-loglevel', 'error']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not result.stdout.strip():
            # No audio stream found
            transcript_path = os.path.join(transcript_dir, f"{video_name}.txt")
            with open(transcript_path, 'w') as transcript_file:
                transcript_file.write("")  # Create an empty file
            print(f"No audio stream found. Empty transcript created: {transcript_path}")
            continue
    except FileNotFoundError:
        # ffprobe not found, skipping audio check
        skip_audio_check = True
        print("ffprobe not found. Skipping audio stream check.")
    except SubprocessError as e:
        print(f"Error occurred while checking audio stream for {video_file}: {e}")
        continue

    # Start timing the transcription
    start_time = time.time()

    # Open the transcript file in append mode to write segments as they are processed
    transcript_path = os.path.join(transcript_dir, f"{video_name}.txt")
    with open(transcript_path, 'w') as transcript_file:
        try:
            # Transcribe the video and write segments as they are processed
            result = model.transcribe(video_path, verbose=True, language='English', condition_on_previous_text=False,
                                      fp16=False, task="transcribe")
            for segment in result['segments']:
                start_time_str = str(timedelta(seconds=int(segment['start'])))
                end_time_str = str(timedelta(seconds=int(segment['end'])))
                transcript_file.write(f"[{start_time_str} - {end_time_str}] {segment['text']}\n")
        except Exception as e:
            print(f"Error during transcription for {video_file}: {e}")
            continue

    # End timing the transcription
    end_time = time.time()
    transcription_time = end_time - start_time

    # Calculate and display estimated remaining time
    file_size = os.path.getsize(video_path)
    total_size -= file_size
    estimated_remaining_time = (transcription_time / file_size) * total_size if total_size > 0 else 0
    print(f"Estimated remaining time: {estimated_remaining_time / 60:.2f} minutes")

print("Transcription process completed.")