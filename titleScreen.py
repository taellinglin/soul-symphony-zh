import sys
from panda3d.core import TransparencyAttrib
from panda3d.core import CardMaker

from bgm import BGM
from glyphRings import GlyphRings
from motionBlur import MotionBlur
from direct.gui.OnscreenImage import OnscreenImage

from stageflow import Stage
from stageflow.panda3d import Cutscene

class TitleScreen(Stage):
    def __init__(self, exit_stage = 'main_menu'):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,1,1), (1,1,0,1), (1,0,1,1), (0,1,0,1), (0,0,1,1)]

    def enter(self, data):
        self.data = data
        base.accept("enter", self.transition, [self.exit_stage])
        base.accept("gamepad-start", self.transition, [self.exit_stage])
        
        base.cam.set_z(256)
        base.vr.tracking_space.setZ(256)
        base.vr.tracking_space.setPos(0,0,0)
        base.cam.look_at(render)
        self.logo()
        self.press_start()
        self.glyph_rings = GlyphRings(font=base.loader.load_font('fonts/konnarian/Daemon.otf'))
        base.bgm.playMusic('TitleScreen', 0.5, True)
        base.bgm.playSfx('soul-symphony')
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)

    def transition(self, exit_stage):
        base.flow.transition(self.exit_stage)
        
    def logo(self):
        self.logo = CardMaker('logo')
        self.logo.set_frame(0 ,0 ,1,1)
        self.imageObject = OnscreenImage(image='graphics/SoulSymphonyLogo.png', pos=(-0.2, 1, 0.5), scale=(1,0.5,0.5))
        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)
        self.bg2 = render.attach_new_node(self.logo.generate())

    def press_start(self):
        press_start = base.loader.loadModel("models/press_start.bam")
        press_start.set_p(90)
        press_start.set_x(-0.55)
        press_start.set_y(-3)
        press_start.set_z(-0.7)
        press_start.set_scale(0.15,0.15,0.75)
        press_start.reparent_to(base.cam2d)
        self.subtitle = press_start


    def update(self, task):
        dt = globalClock.get_dt()
        if self.glyph_rings:
            self.glyph_rings.update(dt)
        base.camera.set_hpr(base.camera, (0.05, 0.05, 0.05))
        base.cam.look_at(base.camera)
        
        return task.cont

    def exit(self, data):
        self.subtitle.detachNode()
        self.glyph_rings.center.detachNode()
        self.bg2.detachNode()
        self.imageObject.detachNode()
        base.cam.reparentTo(render)
        base.camera.detachNode()
        base.bgm.stopMusic()
        base.ignore('enter')
        base.ignore('gamepad-start')
        base.taskMgr.remove('update')
        return data