
from random import choice
import os



    
class BGM:
    def __init__(self, default_volume=1):
        self.default_volume = default_volume  # Default volume to be used for all tracks

        self.songs = self.get_music("music/")
        self.available_songs = (
            self.songs.copy()
        )  # A list to keep track of unplayed songs

        self.music = {}
        for song in self.songs:
            self.music[song] = base.loader.load_sfx("music/{}.ogg".format(song))

        self.sfx_names = [
            "soul-symphony",
            "correct_guess",
            "incorrect_guess",
            "hover",
            "start-dialog",
            "ball-jump",
            "portal_loop",
            "warp",
            "boing00",
            "boing01",
            "boing02",
            "boing03",
            "boing04",
            "pickup",
        ]
        self.sfx = {}
        for s in self.sfx_names:
            self.sfx[s] = base.loader.load_sfx("audio/{}.wav".format(s))

        self.current_sfx = self.sfx["soul-symphony"]
    
        self.current_music = self.select_random_song()

    def get_music(self, directory):
        wav_filenames = []
        for filename in os.listdir(directory):
            if filename.endswith(".ogg"):
                wav_filenames.append(os.path.splitext(filename)[0])
    
        return wav_filenames

    def select_random_song(self):
        # Check if there are any available songs left
        if not self.available_songs:
            self.available_songs = self.songs.copy()  # Reset available songs
            print("All songs have been played. Resetting playlist.")

        # Choose a song randomly from available ones
        selected_song = choice(self.available_songs)
        self.available_songs.remove(
    
            selected_song
        )  # Remove the selected song to avoid repeats
        return self.music[selected_song]

    def playMusic(self, track=None, loop=True, volume=None):
        print("Starting Music...")

        if self.current_music.status == 2:
            self.current_music.stop()

        if track is None:
            self.current_music = self.select_random_song()
        else:
            self.current_music = self.music[track]

        # Use the provided volume, or default if not provided
        volume = volume if volume is not None else self.default_volume
    

        self.current_music.setLoop(loop)
    
        self.current_music.setVolume(volume)  # Set equalized volume here
        self.current_music.play()

    def stopMusic(self):
        self.current_music.stop()

    def playSfx(self, sfx=None, volume=None, pitch=1, loop=False):
        if sfx is None:
            print("No sfx provided.")
            return

        if self.current_sfx.status != self.current_sfx.PLAYING:
            self.current_sfx = self.sfx[sfx]

            # Use the provided volume, or default if not provided
    
            volume = volume if volume is not None else self.default_volume

            self.current_sfx.setPlayRate(pitch)
            self.current_sfx.setVolume(volume)  # Set equalized volume here
            self.current_sfx.setLoop(loop)
    
            self.current_sfx.play()

    def stopSfx(self, sfx=None):
        if sfx is None:
            sfx = self.current_sfx
        if self.current_sfx.status == self.current_sfx.PLAYING:
            sfx.stop()

    def is_playing_sfx(self):
        return self.current_sfx.status == self.current_sfx.PLAYING