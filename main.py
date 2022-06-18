
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
from p3dopenvr.p3dopenvr import *
from panda3d.core import ExecutionEnvironment

class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.vr = P3DOpenVR()
        self.vr.init()
        base.accept('f11', self.drop_to_pdb)

    def drop_to_pdb(self):
        import pdb; pdb.set_trace()


base = Base()


wp = WindowProperties()
wp.setCursorHidden(True)
wp.setFullscreen(1)
#wp.setSize(640, 480)
wp.setSize(1920, 1080)
base.openMainWindow()
base.win.requestProperties(wp)
base.bgm = BGM()
base.motion_blur = MotionBlur()
base.disable_mouse()
#base.enableParticles()
base.levels =['arcade01', 'arcade00', 'room00', 'room01', 'room02','room03', 'room04']
base.gamepad_input = GamepadInput()
base.scoreboard = scoreboard()
base.scoreboard.hide()
base.render.setAntialias(AntialiasAttrib.MNone)
base.flow = Flow(
    stages=dict(
        splash=Panda3DSplash(exit_stage='title_screen'),
        title_screen=TitleScreen(exit_stage='arcade00'),
        intro=Intro(exit_stage='intro2'),
        intro2=Intro2(exit_stage='intro3'),
        intro3=Intro3(exit_stage='lettermatching'),
        letter_matching=LetterMatching(exit_stage='room00'),
        arcade00 = room00(exit_stage='quit', lvl = 0),
        arcade01 = room00(exit_stage='quit', lvl = 1),
        room00=room00(exit_stage='quit', lvl = 2),
        room01=room00(exit_stage='quit', lvl = 3),
        room02=room00(exit_stage='quit', lvl = 4),
        room03=room00(exit_stage='quit', lvl = 5),
        room04=room00(exit_stage='quit', lvl = 6),
        
        
        quit=Quit()
    ),
    initial_stage = 'title_screen',
)
base.run()
