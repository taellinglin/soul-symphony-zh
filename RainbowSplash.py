from panda3d_logos.splashes import Pattern
from panda3d_logos.splashes import Colors
from panda3d.core import VBase2, VBase3, VBase4, Shader
from direct.actor.Actor import Actor
from motionBlur import MotionBlur
from direct.interval.LerpInterval import LerpFunc
from direct.interval.IntervalGlobal import *
from direct.interval.SoundInterval import SoundInterval


class RainbowSplash:
    def __init__(self, pattern=Pattern.SQUARESTAR, colors=Colors.RGB_BANDS, pattern_freq=2, cycle_freq=10):
        self.pattern = pattern
        self.colors = colors
        self.pattern_freq = pattern_freq
        self.cycle_freq = cycle_freq
        self.motion_blur = MotionBlur()  # Initialize MotionBlur
        self.time = 0  # For update function

    def setup(self):
        asset_path = str("assets")
        # Store current values
        self.entry_background_color = VBase4(base.win.get_clear_color())
        self.entry_cam_pos = VBase3(base.cam.get_pos())
        self.entry_cam_hpr = VBase3(base.cam.get_hpr())
        self.entry_cam_scale = VBase3(base.cam.get_scale())
        self.entry_cam_fov = VBase2(base.cam.node().get_lens().get_fov())

        # Set values for splash
        base.win.set_clear_color((0, 0, 0, 1))
        cam_dist = 2
        base.cam.set_pos(0, -2.2 * cam_dist, 0)
        base.cam.set_hpr(0, 0, 0)
        base.cam.set_scale(1)
        base.cam.node().get_lens().set_fov(45 / cam_dist)

        # Set up the splash itself
        self.logo_animation = base.loader.loadModel("assets/panda3d_logo.bam")
        self.logo_animation.reparent_to(render)
        self.logo_animation.set_two_sided(True)
        self.logo = self.logo_animation.findAllMatches("**panda-logo")
        print(self.logo)
        self.circle = self.logo_animation.findAllMatches("**circle")

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="assets/panda3d_logo.vert",
            fragment="assets/panda3d_logo.frag",
        )
        self.logo_animation.set_shader(shader)
        self.logo_animation.set_shader_input("fade", 0.0)
        self.logo_animation.set_shader_input("pattern", self.pattern.value)
        self.logo_animation.set_shader_input("colors", self.colors.value)
        self.logo_animation.set_shader_input("pattern_freq", self.pattern_freq)
        self.logo_animation.set_shader_input("cycle_freq", self.cycle_freq)
        self.logo_sound = base.loader.loadSfx("assets/panda3d_logo.wav")

        # Start enabling the motion blur when the splash begins
        self.motion_blur.enable_blur()

        # Add spinning intervals
        self.spin_logo = LerpFunc(
            lambda t: self.logo[0].set_hpr(0, 0, t * 360),
            fromData=0,
            toData=1,
            duration=2.0,
            blendType='noBlend'
        )

        self.spin_circle = LerpFunc(
            lambda t: self.circle[0].set_hpr(0, 0, -t * 360),
            fromData=0,
            toData=1,
            duration=2.0,
            blendType='noBlend'
        )

        # Timing
        effects = Parallel(
            SoundInterval(
                self.logo_sound,
                loop=False,
            ),
            Sequence(
                LerpFunc(
                    self.shader_time,
                    fromData=0,
                    toData=1,
                    duration=3.878,
                ),
                LerpFunc(
                    self.fade_background_to_white,
                    fromData=0,
                    toData=1,
                    duration=1.0,
                ),
                Wait(1.5),
                LerpFunc(
                    self.fade_to_black,
                    fromData=0,
                    toData=1,
                    duration=1.741,
                ),
            )
        )
        return effects

    # Helper functions moved to instance methods
    def shader_time(self, t):
        self.logo_animation.set_shader_input("time", t)

    def fade_background_to_white(self, t):
        base.win.set_clear_color((t, t, t, 1))
        self.logo_animation.set_shader_input("time", t / 3.878)
        self.logo_animation.set_shader_input("fade", t)

    def fade_to_black(self, t):
        base.win.set_clear_color((1 - t, 1 - t, 1 - t, 1))

    def update(self, task):
        """Update function to rotate both the logo and the circle node"""
        self.time += globalClock.get_dt()

        # Rotation for the circle node (around both X and Y axes)
        rotation_speed = 20  # Adjust the speed as needed
        self.logo[0].setHpr(self.time * rotation_speed, self.time * rotation_speed, 0)
        print(self.logo)
        # Rotate the panda logo around the Y axis (up/down)
        logo_rotation_speed = -20  # Adjust the speed as needed
        self.circle[0].set_hpr(0, self.time * logo_rotation_speed, 0)

        taskMgr.add(self.update, "update_logo")
        return task.cont  # Keeps the update loop running

    def teardown(self):
        # Disable motion blur before teardown
        self.motion_blur.disable_blur()
        # Stop spinning intervals
        self.spin_logo.finish()
        self.spin_circle.finish()
        # Restore initial values and clean up
        base.win.set_clear_color(self.entry_background_color)
        base.cam.set_pos(self.entry_cam_pos)
        base.cam.set_hpr(self.entry_cam_hpr)
        base.cam.set_scale(self.entry_cam_scale)
        base.cam.node().get_lens().set_fov(self.entry_cam_fov)

        self.logo_animation.removeNode()
        # FIXME: Destroy self.logo_sound
