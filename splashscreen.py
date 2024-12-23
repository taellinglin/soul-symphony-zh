from stageflow import Stage
from RainbowSplash import RainbowSplash
from panda3d.core import Vec4
from direct.showbase import ShowBase
from motionBlur import MotionBlur
from panda3d_logos.splashes import Pattern
from panda3d_logos.splashes import Colors
class SplashScreen(Stage):
    def __init__(self, exit_stage="title_screen"):

        self.exit_stage = exit_stage
        self.splash_colors = [
            Vec4(1, 0, 0, 1),  # Red
            Vec4(1, 0.5, 0, 1),  # Orange
            Vec4(1, 1, 0, 1),  # Yellow
            Vec4(0, 1, 0, 1),  # Green
            Vec4(0, 0, 1, 1),  # Blue
            Vec4(0.29, 0, 0.51, 1),  # Indigo
            Vec4(0.56, 0, 1, 1),  # Violet
        ]
        
    def enter(self, data=None):
        
        
        # Stop any existing sounds first
        if hasattr(base, 'bgm'):
            base.bgm.stopSfx()
        
        self.splash = RainbowSplash(
            pattern=Pattern.FLICKERING,
            colors=Colors.RAINBOW,
            pattern_freq=13,
            cycle_freq=31
        )
        self.interval = self.splash.setup()
        
        # Start the interval
        self.interval.start()
        
        # Schedule the transition with a consistent delay
        delay = self.interval.getDuration() + 0.5
        base.taskMgr.doMethodLater(
            delay,
            self.transition_out, 
            'transition_from_splash'
        )
        return data
    def cleanup(self):
        self.splash.teardown()
        
    def transition_out(self, task):
        self.cleanup()
        #self.base.load_stage(stage_name="title_screen", lvl=0)  # Load title screen before transitioning
        base.flow.transition("title_screen")
        return task.done
    def exit(self, data=None):
        if hasattr(self, 'splash'):
            self.splash.teardown()
        return data