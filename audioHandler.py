
import pyaudio
import numpy as np
import threading
import queue
import time



    
class AudioHandler:
    def __init__(self, buffer_size=256, fs=96000):
        self.buffer_size = buffer_size
        self.fs = fs
        self.audio_amplitude = []  # Store amplitudes for analysis
        self.stream = None
        self.running = False
        self.audio_thread = None
        self.data_queue = queue.Queue()  # Thread-safe queue for audio data

    def compute_amplitude(self, data):
        """
        Calculate the root mean square (RMS) amplitude of audio data.
        """
        return np.sqrt(np.mean(data**2))

    def process_audio_eq(self, audio_data):
        """
        Example placeholder for EQ processing.
        Modify this to apply actual EQ logic.
        """
        # Simulating EQ processing (e.g., applying a filter)
        return audio_data * 0.5  # Example: Reduce amplitude

    def audio_callback(self, in_data, frame_count, time_info, status_flags):
        """
        PyAudio callback function for real-time audio capture.
        """
        if status_flags:
            print(f"Audio callback status: {status_flags}")

        try:
            # Convert input audio data to NumPy array
            audio = np.frombuffer(in_data, dtype=np.int16)
            self.data_queue.put(audio)  # Send data to the processing queue
        except Exception as e:
            print(f"Error in audio callback: {e}")

        return (None, pyaudio.paContinue)

    def start_audio(self):
        """
        Initialize and start the audio stream and processing thread.
        """
        if self.stream:
            print("Audio stream already running.")
            return

        p = pyaudio.PyAudio()
        try:
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.fs,
                input=True,
                frames_per_buffer=self.buffer_size,
                stream_callback=self.audio_callback,
            )
            self.running = True
            self.stream.start_stream()

            # Start the EQ processing thread
            self.audio_thread = threading.Thread(target=self._process_eq, daemon=True)
            self.audio_thread.start()

        except Exception as e:
            print(f"Failed to start audio stream: {e}")
            self.stop_audio()

    def _process_eq(self):
        """
        EQ processing thread: continuously process audio data from the queue.
        """
        while self.running:
            try:
                # Fetch audio data from the queue
                audio_data = self.data_queue.get(
                    timeout=0.1
                )  # Timeout prevents deadlock
                processed_audio = self.process_audio_eq(audio_data)
                amplitude = self.compute_amplitude(processed_audio)
                self.audio_amplitude.append(amplitude)

                # Log or handle the processed audio/amplitude
                print(f"Processed Amplitude: {amplitude}")

            except queue.Empty:
                # No data available in the queue, avoid busy-waiting
                time.sleep(0.01)

    def stop_audio(self):
        """
        Safely stop the audio stream and processing thread.
        """
        if self.stream:
            print("Stopping audio stream...")
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.running = False

    def cleanup(self):
        """
        Clean up audio resources and ensure proper thread termination.
        """
        self.stop_audio()
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()  # Wait for thread to finish
        print("Audio resources cleaned up.")