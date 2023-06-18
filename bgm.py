from random import choice
import os

class BGM():
    def __init__(self):
        self.songs = self.get_music("music/")

        self.music = {}
        for song in self.songs:
            self.music[song] = base.loader.load_sfx("music/{}.ogg".format(song))

        self.sfx_names = [
            'soul-symphony',
            'correct_guess',
            'incorrect_guess',
            'hover',
            'start-dialog',
            'ball-jump',
            'portal_loop',
            'warp',
            'boing00',
            'boing01',
            'boing02',
            'boing03',
            'boing04',
            'pickup',
        ]
        self.sfx = {}
        for s in self.sfx_names:
            self.sfx[s] = base.loader.load_sfx("audio/{}.wav".format(s))

        self.current_sfx = self.sfx['soul-symphony']
        #base.playSfx(self.current_sfx)
        self.current_music = self.music[choice(self.songs)]
        #base.playMusic(self.current_music, 1, 1, None, 0)
            
    def get_music(self, directory):
        wav_filenames = []
        for filename in os.listdir(directory):
            if filename.endswith('.ogg'):
                wav_filenames.append(os.path.splitext(filename)[0])
        return wav_filenames

    def playMusic(self, track = None, loop = True, volume = 1):
        print("Starting Music...")
        if(self.current_music.status == 2):
            self.current_music.stop()
        
        if track == None:
            self.current_music = self.music[choice(self.songs)]
        else:
            print(self.songs.index(track))
            self.current_music = self.music[track]
        self.current_music.setLoop(loop)
        self.current_music.setVolume(volume)
        self.current_music.play()
        
        
    def stopMusic(self):
        #if (self.current_music.status()== 2):
        self.current_music.stop()
            
    def playSfx(self, sfx = None, volume = 1, pitch = 1, loop = False):
        if sfx == None:
            print("No sfx provided.")
            return
        if self.current_sfx.status != self.current_sfx.PLAYING:
            self.current_sfx = self.sfx[sfx]
            self.current_sfx.setPlayRate(pitch)
            self.current_sfx.setVolume(volume)
            self.current_sfx.setLoop(loop)
            self.current_sfx.play()
            
    def stopSfx(self, sfx = None):
        if sfx == None:
            sfx = self.current_sfx
        if self.current_sfx.status == self.current_sfx.PLAYING:
            sfx.stop()
        
    def is_playing_sfx(self):
        if self.current_sfx.status == self.current_sfx.PLAYING:
            return True
        else:
            return False