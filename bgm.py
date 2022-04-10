from random import choice


class BGM():
    def __init__(self):
        self.songs = [
            'Flag', 
            'Excellent', 
            'FlagTracker', 
            'HallofSunrise',
            'NightDrive', 
            'SpaceField', 
            'StarlightVocals',
            'Trich', 
            'WalkThePath', 
            'Whisper', 
            'WishingWell', 
            'Womper',
            'YouMightBeRight', 
            'The_Spirit_Flag_Instrumental', 
            'Through_my_Heart_Instrumental', 
            'Today2', 
            'TitleScreen',
            'Celestial',
            'TheGreatJourney',
            'TheSpiritsTwo',
            'SpiritsMarch',
            'SuperSignal',
            'Ambience00',
            'The_Spirits'
        ]
        self.music = {}
        for song in self.songs:
            self.music[song] = base.loader.load_sfx("music/{}.ogg".format(song))
        self.propSfxList = {}
        self.fallSfxList = {}
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
        self.propSfx = [
            'prop00',
            'prop01',
            'prop02',
            'prop03',
        ]
        self.fallSfx = [
            'fallout00',
            'fallout01',
            'fallout02',
            'fallout03',
            'fallout04'
        ]
        for propsfx in self.propSfx:
            self.propSfxList[propsfx] = base.loader.load_sfx("audio/{}.wav".format(propsfx))
        for fallsfx in self.fallSfx:
            self.fallSfxList[fallsfx] = base.loader.load_sfx("audio/{}.wav".format(fallsfx))
        self.endsong = base.loader.load_sfx("music/{}.ogg".format('EndRoom'))
        self.sfx = {}
        for s in self.sfx_names:
            self.sfx[s] = base.loader.load_sfx("audio/{}.wav".format(s))

        self.current_sfx = self.sfx['soul-symphony']
        #base.playSfx(self.current_sfx)
        self.current_music = self.music[choice(self.songs)]
        #base.playMusic(self.current_music, 1, 1, None, 0)
            
        
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
    def playPropSfx(self, volume = 1, pitch = 1, loop = False):
        self.current_sfx = self.propSfxList[choice(self.propSfx)]
        print("Playing: " + str(self.current_sfx))
        self.current_sfx.setPlayRate(pitch)
        self.current_sfx.setVolume(volume)
        self.current_sfx.setLoop(loop)
        self.current_sfx.play()
        
    def playFallSfx(self, volume = 1, pitch = 1, loop = False):
        self.current_sfx = self.fallSfxList[choice(self.fallSfx)]
        print("Playing: " + str(self.current_sfx))
        self.current_sfx.setPlayRate(pitch)
        self.current_sfx.setVolume(volume)
        self.current_sfx.setLoop(loop)
        self.current_sfx.play()
    def playEndSong(self):
        self.stopMusic()
        self.endsong.setLoop(True)
        self.endsong.play()
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