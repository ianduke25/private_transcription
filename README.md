# Private Video Transcription Tool

## Overview

This repository contains comprehensive script of a video transcription tool locally employing OpenAI's Whisper model to transcribe audio and video files into text. The transcription process includes both extracting spoken content from video/audio files and creating timestamped transcripts. This tool is designed for individuals or organizations who need a simple, efficient, and local transcription solution, with a focus on ensuring privacy by avoiding cloud-based processing and/or API calls. The model used in provided code is specifically configured to handle videos with long periods of silence -- such as law enforcement body camera files.

## Features

- **Local Video Transcription:** Transcribes the content of video files on your local machine, ensuring no data is transmitted over the internet, maintaining the privacy of processed files.
- **Model Size Selection:** Provides users with the ability to select an appropriate Whisper model size based on their agency's specific processing speed requirements.
- **Audio Stream Check:** Automatically checks whether the video file contains an audio stream before attempting transcription. If no audio is found, it creates an empty transcript to signify that there is no transcribable content.
- **Automatic Saving:** Saves the generated transcripts with timestamps into a specified directory, ensuring an organized and easy-to-use output.

## Usage

### Prerequisites

- **Python 3.9 or above is required to run this script.
- Install the **Whisper library** by OpenAI: 
  ```
  pip install openai-whisper
  ```
- Install the **ffmpeg library**: 
  ```
  pip install ffmpeg-python
  ```
### Running the Script

1. Clone or download this repository.
2. Navigate to the directory containing the script.
3. Run the script using Python:
   ```bash
   python transcribe_videos.py
   ```
4. Enter the path to the directory containing your video files when prompted.
5. Enter the path to the directory where you want to save the transcripts.

The script will then process each video file and generate corresponding transcripts.

## Expected Model Size and RAM Requirements

- **Model Size:** The largest model this script uses is the Whisper `large-v2` neural network, which is approximately **3GB** in size. Ensure that your system has sufficient disk space to store the model.
- **RAM Requirements:** Transcribing video files using the `large-v2` model is memory-intensive. It is recommended to have **at least 16GB of RAM** to ensure smooth performance. Systems with lower RAM may experience slow performance or memory errors, especially for longer video files.

## Privacy Considerations

- **Local Processing Only:** This transcription tool performs all operations locally on your machine, meaning that **no data is sent to external servers**. This ensures that your video files and generated transcripts remain private.
- **No Cloud Dependencies:** The Whisper model is downloaded and executed on your local hardware, avoiding the need for cloud-based APIs or third-party servers. This is particularly beneficial for users with sensitive or confidential video content.

## Credits

- Built using [OpenAI Whisper](https://github.com/openai/whisper) for transcription.
