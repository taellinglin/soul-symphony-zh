import os
import wave
import time
import numpy as np
import sounddevice as sd
import imageio
import subprocess
from datetime import datetime


class ScreenRecorder:
    def __init__(self, base):
        self.base = base  # Reference to the ShowBase instance
        self.recording = False
        self.video_writer = None
        self.audio_filename = None
        self.audio_frames = []
        self.audio_stream = None
        self.screenshot_folder = "screenshots"
        self.screencapture_folder = "screencaptures"
        self.sample_rate = 192000  # 192 kHz for stereo audio
        self.channels = 2  # Stereo audio

        # Setup folders and input events
        self.setup_folders()
        self.setup_input_events()

    def setup_folders(self):
        """Ensure the required folders exist."""
        for folder in [self.screenshot_folder, self.screencapture_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")
            else:
                print(f"Folder already exists: {folder}")

    def setup_input_events(self):
        """Bind input events for screenshots and recording."""
        self.base.accept("f11", self.handle_select_press)  # Screenshot on 'F11'
        self.base.accept("f12", self.handle_select_hold)  # Toggle recording on 'F12'

    def handle_select_press(self):
        """Handle single press of 'F11' for taking a screenshot."""
        print("F11 pressed (screenshot).")
        if not self.recording:
            self.take_screenshot()

    def handle_select_hold(self):
        """Handle holding 'F12' for toggling video recording."""
        print("F12 held (toggle recording).")
        if not self.recording:
            self.start_recording()
        else:
            elapsed = (
                time.time() - self.record_start_time if self.record_start_time else 0
            )
            if elapsed >= 3:
                self.stop_recording()

    def take_screenshot(self):
        """Capture and save a screenshot."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.screenshot_folder, f"screenshot_{timestamp}.png")
        print(f"Attempting to save screenshot to: {filename}")
        success = self.base.win.saveScreenshot(filename)
        if success:
            print(f"Screenshot saved as: {filename}")
        else:
            print("Failed to save screenshot!")

    def start_recording(self):
        """Initialize video and audio recording."""
        try:
            capture_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            video_filename = os.path.join(
                self.screencapture_folder, f"capture_{capture_datetime}.mp4"
            )
            audio_filename = os.path.join(
                self.screencapture_folder, f"audio_{capture_datetime}.wav"
            )

            print(
                f"Starting video recording to: {video_filename} and audio to {audio_filename}"
            )
            self.recording = True
            self.record_start_time = time.time()

            # Set up imageio video writer (60 FPS)
            self.video_writer = imageio.get_writer(video_filename, fps=60)
            if not self.video_writer:
                print("Error: Video writer failed to open!")
                self.recording = False
                return

            # Start audio recording using sounddevice
            self.audio_filename = audio_filename
            self.audio_stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                dtype="int16",
                callback=self.audio_callback,
            )
            self.audio_stream.start()
            print("Audio stream opened successfully.")

            # Start tasks to capture frames and audio
            self.base.taskMgr.add(self.record_frame, "RecordFrameTask")
            print("Video and audio recording started.")
        except Exception as e:
            print(f"Error starting video and audio recording: {e}")
            self.recording = False

    def stop_recording(self):
        """Finalize video and audio recording."""
        if self.recording:
            try:
                self.recording = False
                self.video_writer.close()
                self.audio_stream.stop()

                # Save the recorded audio
                wf = wave.open(self.audio_filename, "wb")
                wf.setnchannels(self.channels)  # Stereo audio
                wf.setsampwidth(2)  # 2 bytes (16-bit)
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(self.audio_frames))
                wf.close()

                # Combine video and audio using ffmpeg
                output_file = self.audio_filename.replace(".wav", "_final.mp4")
                video_file = self.audio_filename.replace("audio", "capture").replace(
                    ".wav", ".mp4"
                )
                audio_file = self.audio_filename
                print(f"Combining video and audio using ffmpeg into {output_file}")
                self.combine_audio_video(video_file, audio_file, output_file)
                print("Video and audio recording stopped.")
            except Exception as e:
                print(f"Error stopping video and audio recording: {e}")
            finally:
                self.base.taskMgr.remove("RecordFrameTask")
                self.video_writer = None
                self.audio_stream = None
                self.audio_frames = []

    def record_frame(self, task):
        """Capture the current frame and write it to the video file."""
        if not self.recording or self.video_writer is None:
            return task.done

        try:
            # Capture the current frame as a numpy array (RGB)
            tex = self.base.win.getScreenshot()
            img_data = tex.getRamImageAs("RGB")
            img = np.frombuffer(img_data, dtype=np.uint8).reshape(
                tex.getYSize(), tex.getXSize(), 3
            )

            # Flip the image vertically (Panda3D stores images upside-down)
            img = np.flipud(img)

            # Write the frame to the video
            self.video_writer.append_data(img)
        except Exception as e:
            print(f"Error recording frame: {e}")
            return task.done

        return task.cont

    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio capture."""
        if status:
            print(f"Audio stream status: {status}")
        if self.recording:
            # Flatten and store the audio data for future use
            audio_data = indata.flatten()
            print(f"Captured {len(audio_data)} audio samples")

            # Save audio data into audio_frames
            self.audio_frames.append(audio_data.tobytes())  # Ensure it's in byte format

    def combine_audio_video(self, video_file, audio_file, output_file):
        """Combine video and audio using ffmpeg."""
        try:
            video_file = video_file.replace("\\", "/")
            audio_file = audio_file.replace("\\", "/")
            output_file = output_file.replace("\\", "/")

            # Run the FFmpeg command to combine video and audio
            command = [
                "ffmpeg",
                "-i",
                video_file,
                "-i",
                audio_file,
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-b:a",
                "44.1k",
                "-strict",
                "experimental",
                output_file,
            ]
            subprocess.run(command, check=True)
            print(f"Output video with audio saved as {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error combining video and audio: {e}")
