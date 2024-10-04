
# Private Video Transcription Tool

## Overview

This script is a video transcription tool that utilizes OpenAI's Whisper model to transcribe video files into text. The transcription process includes both extracting spoken content from videos and creating timestamped transcripts, which are saved as text files. This tool is designed for individuals or organizations who need a simple, efficient, and local transcription solution, with a focus on ensuring privacy by avoiding cloud-based processing.

## Features

- **Local Video Transcription:** Transcribes the content of video files on your local machine, ensuring no data is transmitted over the internet, thereby maintaining the privacy of your files.
- **Supported Video Formats:** Supports common video formats, including `.mp4`, `.mkv`, `.avi`, and `.mov`.
- **Audio Stream Check:** Automatically checks whether the video file contains an audio stream before attempting transcription. If no audio is found, it creates an empty transcript to signify that there is no transcribable content.
- **Progress Tracking:** Displays progress for each file and estimates the remaining time for transcription based on the size of the files.
- **Automatic Saving:** Saves the generated transcripts with timestamps into a specified directory, ensuring an organized and easy-to-use output.

## Usage

### Prerequisites

- **Python 3.x** is required to run this script.
- Install the **Whisper library** by OpenAI: 
  ```
  pip install openai-whisper
  ```
- **FFmpeg** must be installed for audio extraction. You can install FFmpeg by following the instructions on [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).

### Running the Script

1. Clone or download this repository.
2. Navigate to the directory containing the script.
3. Run the script using Python:
   ```bash
   python transcribe_videos.py
   ```
4. Enter the path to the directory containing your video files when prompted.
5. Enter the path to the directory where you want to save the transcripts.

### Example

```
Enter the path to the directory containing the video files: /path/to/your/videos
Enter the path to the directory where transcripts should be saved: /path/to/save/transcripts
```

The script will then process each video file and generate corresponding transcripts.

## Expected Model Size and RAM Requirements

- **Model Size:** This script uses the `large-v2` Whisper model, which is approximately **3GB** in size. Ensure that your system has sufficient disk space to store the model.
- **RAM Requirements:** Transcribing video files using the `large-v2` model is memory-intensive. It is recommended to have **at least 16GB of RAM** to ensure smooth performance. Systems with lower RAM may experience slow performance or memory errors, especially for longer video files.

## Privacy Considerations

- **Local Processing Only:** This transcription tool performs all operations locally on your machine, meaning that **no data is sent to external servers**. This ensures that your video files and generated transcripts remain private.
- **No Cloud Dependencies:** The Whisper model is downloaded and executed on your local hardware, avoiding the need for cloud-based APIs or third-party servers. This is particularly beneficial for users with sensitive or confidential video content.
- **Temporary Storage:** The script does not create any temporary files that persist beyond the scope of the transcription process, minimizing the risk of unintended data exposure.

## Limitations

- **Hardware Requirements:** Due to the size and computational requirements of the Whisper `large-v2` model, running this script on machines with low computational power may lead to significant delays or may not be feasible.
- **Audio Stream Dependency:** The script checks for an audio stream in each video before transcription. If no audio stream is detected, an empty transcript is generated.

## License

This tool is open-source and distributed under the MIT License. Feel free to modify and use it as per your requirements.

## Credits

- Built using [OpenAI Whisper](https://github.com/openai/whisper) for transcription.
- FFmpeg is used for video and audio processing.
# private_transcription
