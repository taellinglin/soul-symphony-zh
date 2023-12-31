
from letterMatching import LetterMatching
from scoreboard import scoreboard
from titleScreen import TitleScreen
from motionBlur import MotionBlur
from gamepadInput import GamepadInput
from bgm import BGM
from room00 import room00
from intro import Intro
from intro2 import Intro2
from intro3 import Intro3
from direct.showbase.ShowBase import ShowBase
from stageflow import Flow
from stageflow.panda3d import Panda3DSplash
from panda3d.core import WindowProperties
from panda3d.core import AntialiasAttrib
from direct.particles import Particles
from stageflow.prefab import Quit
import os

class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        base.accept('f11', self.drop_to_pdb)

    def drop_to_pdb(self):
        import pdb; pdb.set_trace()

    def get_fonts(self, folder_path):
        font_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.ttf'):
                    relative_path = os.path.join(root, file)
                    font_files.append(loader.load_font(relative_path))
                    print("Loaded:"+ relative_path)
        return font_files

base = Base()
wp = WindowProperties()
wp.setFullscreen(1)
#wp.setSize(640, 480)
wp.setSize(1920, 1080)
base.openMainWindow()
base.win.requestProperties(wp)
base.bgm = BGM()
base.motion_blur = MotionBlur()
base.disable_mouse()
base.fonts = base.get_fonts("fonts/text/")
#base.enableParticles()
base.levels =['room00', 'room01', 'room02','room03']
base.gamepad_input = GamepadInput()
base.scoreboard = scoreboard()
base.scoreboard.hide()
base.render.setAntialias(AntialiasAttrib.MNone)
base.flow = Flow(
    stages=dict(
        splash=Panda3DSplash(exit_stage='title_screen'),
        title_screen=TitleScreen(exit_stage='room00'),
        intro=Intro(exit_stage='intro2'),
        intro2=Intro2(exit_stage='intro3'),
        intro3=Intro3(exit_stage='lettermatching'),
        letter_matching=LetterMatching(exit_stage='room00'),
        room00=room00(exit_stage='quit', lvl = 0),
        room01=room00(exit_stage='quit', lvl = 1),
        room02=room00(exit_stage='quit', lvl = 2),
        room03=room00(exit_stage='quit', lvl = 3),
        quit=Quit()
    ),
    initial_stage = 'title_screen',
)
base.run()
