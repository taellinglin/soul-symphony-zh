import os
import time
import imageio
import numpy as np
import pyaudio
import wave
from panda3d.core import GraphicsOutput, Texture
from panda3d.core import PNMImage
from datetime import datetime

class ScreenRecorder:
    def __init__(self, window, folder="screencapture", fps=60, audio_rate=96000, audio_channels=2):
        self.window = window
        self.folder = folder
        self.fps = fps
        self.audio_rate = audio_rate
        self.audio_channels = audio_channels

        self.video_writer = None
        self.audio_frames = []
        self.recording = False
        self.screenshot_count = 0

        self.audio_format = pyaudio.paInt16
        self.chunk_size = 128
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None

        self.setup_folders()

    def setup_folders(self):
        os.makedirs(self.folder, exist_ok=True)
        self.screenshot_folder = os.path.join(self.folder, "screenshots")
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def take_screenshot(self):
        # Create a PNMImage object
        screenshot_image = PNMImage()
        
        # Capture the screenshot and store it in the PNMImage object
        self.window.win.getScreenshot(screenshot_image)
        
        # Get the current datetime
        current_time = datetime.now()
        
        # Format the datetime manually with East Asian characters
        formatted_time = "{0}年{1}月{2}日_{3}时{4}分{5}秒".format(
            current_time.year, current_time.month, current_time.day,
            current_time.hour, current_time.minute, current_time.second)
        
        # Create the filename with East Asian characters in it
        screenshot_filename = "SoulSymphony_{}.png".format(formatted_time)
        
        # Save the screenshot with the generated filename
        screenshot_image.write(screenshot_filename)

    def start_recording(self):
        if self.recording:
            print("Recording already in progress.")
            return

        video_filename = os.path.join(self.folder, f"SoulSymphonyRec_{int(time.time())}.mp4")
        self.video_writer = imageio.get_writer(video_filename, fps=self.fps, macro_block_size=None)

        audio_filename = os.path.join(self.folder, f"audio_{int(time.time())}.wav")
        self.audio_file = audio_filename

        self.audio_stream = self.audio.open(
            format=self.audio_format,
            channels=self.audio_channels,
            rate=self.audio_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        self.recording = True
        print(f"Recording started: {video_filename}")

    def stop_recording(self):
        if not self.recording:
            print("No recording to stop.")
            return

        self.recording = False

        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio.terminate()

        if self.video_writer:
            self.video_writer.close()

        self.save_audio()
        print("Recording stopped and saved.")

    def record_frame(self):
        if not self.recording:
            return

        tex = Texture()
        self.window.win.getScreenshot(tex)
        np_image = np.frombuffer(tex.getRamImageAs("RGBA"), dtype=np.uint8)
        np_image = np_image.reshape((tex.getYSize(), tex.getXSize(), 4))
        np_image = np.flip(np_image, axis=0)

        self.video_writer.append_data(np_image)

        audio_data = self.audio_stream.read(self.chunk_size, exception_on_overflow=False)
        self.audio_frames.append(audio_data)

    def save_audio(self):
        if not self.audio_frames:
            return

        with wave.open(self.audio_file, 'wb') as wf:
            wf.setnchannels(self.audio_channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.audio_rate)
            wf.writeframes(b''.join(self.audio_frames))

        print(f"Audio saved to {self.audio_file}")

# Example usage in a Panda3D application
# recorder = ScreenRecorder(window=base)
# base.accept("f1", recorder.take_screenshot)
# base.accept("f2", recorder.start_recording)
# base.accept("f3", recorder.stop_recording)
# taskMgr.add(lambda task: recorder.record_frame() or task.cont, "record_frame")
