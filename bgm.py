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

        sfx_names = [
            'soul-symphony',
            'correct_guess',
            'incorrect_guess',
            'hover',
            'start-dialog',
            'ball-jump',
            'boing00',
            'boing01',
            'boing02',
            'boing03',
            'boing04',
        ]
        self.sfx = {}
        for s in sfx_names:
            self.sfx[s] = base.loader.load_sfx("audio/{}.wav".format(s))

        self.current_sfx = self.sfx['soul-symphony']
        #base.playSfx(self.current_sfx)
        self.current_music = self.music[choice(self.songs)]
        #base.playMusic(self.current_music, 1, 1, None, 0)
            
        
    def playMusic(self, track = None, loop = True):
        print("Starting Music...")
        if(self.current_music.status == 2):
            self.current_music.stop()
        
        if track == None:
            self.current_music = self.music[choice(self.songs)]
        else:
            print(self.songs.index(track))
            self.current_music = self.music[track]
        self.current_music.setLoop(loop)
        self.current_music.play()
        
        
    def stopMusic(self):
        #if (self.current_music.status()== 2):
        self.current_music.stop()
            
    def playSfx(self, sfx = None, volume = 1, pitch = 1):
        if sfx == None:
            print("No sfx provided.")
            return
        if self.current_sfx.status != self.current_sfx.PLAYING:
            self.current_sfx = self.sfx[sfx]
            self.current_sfx.setPlayRate(pitch)
            self.current_sfx.setVolume(volume)
            self.current_sfx.play()
    
    def is_playing_sfx(self):
        if self.current_sfx.status == self.current_sfx.PLAYING:
            return True
        else:
            return False