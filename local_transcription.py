import os
import whisper
import subprocess
import time
from subprocess import CalledProcessError
from datetime import timedelta

# Accept user input for directories
video_dir = input("Enter the path to the directory containing the video files: ").strip()
transcript_dir = input("Enter the path to the directory where transcripts should be saved: ").strip()

# Load the Whisper model
model = whisper.load_model("large-v2") # Ran a few tests, and observed notably better performance on large model. Worth the extra compute time!

# Get list of only video files
video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]

# Create transcript directory if it doesn't exist
if not os.path.exists(transcript_dir):
    os.makedirs(transcript_dir)

# Get list of existing transcript files
existing_transcripts = [f.replace('.txt', '') for f in os.listdir(transcript_dir) if f.endswith('.txt')]

# Calculate total size of untranscribed files
untranscribed_files = [f for f in video_files if os.path.splitext(f)[0] not in existing_transcripts]
total_size = sum(os.path.getsize(os.path.join(video_dir, f)) for f in untranscribed_files)

# Process each video file
for video_file in video_files:
    video_name = os.path.splitext(video_file)[0]

    # Check if transcript already exists
    if video_name not in existing_transcripts:
        print(f"Processing: {video_file}")
        
        video_path = os.path.join(video_dir, video_file)
        
        # Check if the video contains an audio stream
        try:
            # Using ffmpeg to check for audio streams
            cmd = [
                'ffmpeg', '-i', video_path, '-hide_banner', '-loglevel', 'error',
                '-vn', '-acodec', 'pcm_s16le', '-f', 'null', '-'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Start timing the transcription
            start_time = time.time()
            
            # Transcribe the video
            result = model.transcribe(video_path, verbose=True, language='English', condition_on_previous_text=False)
            
            # End timing the transcription
            end_time = time.time()
            transcription_time = end_time - start_time
            
            # Save the transcription to a text file
            transcript_path = os.path.join(transcript_dir, f"{video_name}.txt")
            with open(transcript_path, 'w') as transcript_file:
                for segment in result["segments"]:
                    start_time_str = str(timedelta(seconds=int(segment['start'])))
                    end_time_str = str(timedelta(seconds=int(segment['end'])))
                    transcript_file.write(f"[{start_time_str} - {end_time_str}] {segment['text']}\n")
            
            print(f"Transcript saved: {transcript_path}")
            
            # Calculate and display estimated remaining time
            file_size = os.path.getsize(video_path)
            total_size -= file_size
            estimated_remaining_time = (transcription_time / file_size) * total_size if total_size > 0 else 0
            print(f"Estimated remaining time: {estimated_remaining_time / 60:.2f} minutes")
        
        except CalledProcessError:
            # If there's no audio stream, create an empty transcript
            transcript_path = os.path.join(transcript_dir, f"{video_name}.txt")
            with open(transcript_path, 'w') as transcript_file:
                transcript_file.write("")  # Create an empty file
            
            print(f"No audio stream found. Empty transcript created: {transcript_path}")
    else:
        print(f"Transcript already exists for: {video_file}")

print("Transcription process completed.")
