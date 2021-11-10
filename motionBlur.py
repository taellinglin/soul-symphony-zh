from panda3d.core import CardMaker


class MotionBlur():
    def __init__(self):
        base.win.set_clear_color_active(False)
        self.cardmaker = CardMaker('background')
        self.cardmaker.set_frame(-1,1,-1,1)
        self.bg = base.cam.attach_new_node(self.cardmaker.generate())
        self.bg.set_y(2048)
        self.bg.set_transparency(True)
        self.bg.set_color((0,0,0,0.05))
        self.bg.set_scale(20000)
