
import sys

from glyphRings import GlyphRings

from panda3d.core import (
    TransparencyAttrib,
    CardMaker,
    NodePath,
    Vec4,
    Vec3,
    Point3,
    LVector3,
)

from direct.gui.OnscreenImage import OnscreenImage

from direct.interval.LerpInterval import (
    LerpColorInterval,
    LerpScaleInterval,
    LerpPosInterval,
)

from direct.interval.IntervalGlobal import Sequence, Wait, Parallel

from direct.particles.ParticleEffect import ParticleEffect

from direct.particles.Particles import Particles, BaseParticleEmitter

import math

from stageflow import Stage

from motionBlur import MotionBlur
from panda3d.core import TextureStage


class TitleScreen(Stage):

    def __init__(self, exit_stage=None):
        super().__init__()
        self.exit_stage = exit_stage
        base.motion_blur = MotionBlur()
        self.colors = [
            Vec4(1, 0, 0, 1),  # Red
            Vec4(1, 0.5, 0, 1),  # Orange
            Vec4(1, 1, 0, 1),  # Yellow
            Vec4(0, 1, 0, 1),  # Green
            Vec4(0, 0, 1, 1),  # Blue
            Vec4(0.29, 0, 0.51, 1),  # Indigo
            Vec4(0.56, 0, 1, 1),  # Violet
        ]

        self.rotation_speed = 60  # Degrees per second

        self.globalClock = globalClock  # Assuming globalClock is defined elsewhere

        self.wave_amplitude = 0.125  # Amplitude of the wave effect

        self.wave_frequency = 5.0
        #self.motion_blur = MotionBlur()

    def enter(self):
        base.accept("enter", self.transition, self.exit_stage)

        base.accept("gamepad-start", self.transition, self.exit_stage)

        base.enableParticles()

        base.cam.set_z(32)

        base.cam.look_at(render)

        self.glyph_rings = GlyphRings(
            font=base.loader.load_font("fonts/konnarian/Daemon.otf")
        )

        self.star_and_logo()

        self.current_color_index = 0

        # Define the stars' base radius from the center of the galaxy

        self.base_radius = 10.0

        # Variables to control time and direction

        self.time = 0.0

        self.spin_speed = 1.0  # Speed of the spinning

        self.scale_speed = 1.0  # Speed of the inward/outward scaling

        self.inward = True  # To track whether we're moving inward or outward

        base.bgm.playMusic("灵林 - 灵魂交响乐 - 魂交响乐", True, 1)

        base.bgm.playSfx("soul-symphony")

        self.update_task = base.task_mgr.add(self.update, "update")

        base.accept("escape", sys.exit)

    def cycle_colors(self, task):
        # Set the color of the object to the current color in the array
        self.imageObject.setColor(self.colors[self.current_color_index])

        # Move to the next color in the array

        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

        # Continue the task on the next frame

        return task.cont

    def transition(self, exit_stage):
        print(f"Transitioning to {exit_stage}")
        base.flow.transition(exit_stage)
        

    def create_logo_wave(self):
        # Define the wave parameters

    
        wave_scale_min = (1.45, 1, 0.65)  # Minimum scale values

        wave_scale_max = (1.55, 1, 0.55)  # Maximum scale values

        wave_duration = 1  # Total duration for one complete wave cycle

        y_offset_amplitude = 0.005  # Max offset in the y direction

        frequency = 2  # Frequency of the sine wave

        def update_wave(task):
            # Calculate the current time in the wave cycle

        
            current_time = (task.time % wave_duration) / wave_duration

            scale_factor = wave_scale_min[0] + (
                wave_scale_max[0] - wave_scale_min[0]
            ) * 0.5 * (1 + math.sin(2 * math.pi * frequency * current_time))

            y_offset = y_offset_amplitude * math.sin(
                2 * math.pi * frequency * current_time
            )

            # Update the object's scale and position

            self.imageObject.setScale(
                scale_factor, 1, 0.65
            )  # Assuming you want to keep y constant

            self.imageObject.setZ(self.imageObject.getZ() + y_offset)

            return task.cont  # Continue the task

        # Add the update_wave function to the task manager

        base.taskMgr.add(update_wave, "logo_wave_task")

    def star_and_logo(self):
        # Load the star image

        self.star_node = NodePath("star_node")

        self.star_card = CardMaker("star_card")

        self.star_card.set_frame(0, 0, 1, 1)

        self.imageObject2 = OnscreenImage(
            image="graphics/star.png", pos=(0.0, 0.0, 0.0), scale=(1, 1, 1)
        )

        self.imageObject2.setTransparency(TransparencyAttrib.MAlpha)

        self.imageObject3 = OnscreenImage(
            image="graphics/star2.png", pos=(0.0, 0.0, 0.0), scale=(1, 1, 1)
        )

        self.imageObject3.setTransparency(TransparencyAttrib.MAlpha)

        # Correctly attach the generated node

        self.star_spinner = self.star_node.attach_new_node(self.star_card.generate())

        self.star_spinner.setPos(0, 0, 0)  # Center it at the origin

        self.star_decal = self.centerPivot(self.star_spinner)

        self.star_decal.setScale(1.0, 1.0, 1.0)

        # Create particle effect programmatically

        self.particle = ParticleEffect()

        particles = Particles("particles")

        particles.setFactory("PointParticleFactory")

        particles.setRenderer("LineParticleRenderer")

        particles.setEmitter("PointEmitter")

        # Set pool size and particle properties

        particles.setPoolSize(2048)

        particles.setBirthRate(1)

        particles.setLitterSize(10)

        particles.setLitterSpread(2)

        particles.setSystemLifespan(0.0)

        particles.setLocalVelocityFlag(True)

        particles.setSystemGrowsOlderFlag(False)

        # Particle factory settings

        particles.factory.setLifespanBase(0.5)

        particles.factory.setLifespanSpread(0.2)

        particles.factory.setMassBase(1.0)

        particles.factory.setTerminalVelocityBase(400.0)

        # Particle renderer settings

        renderer = particles.renderer

        renderer.setHeadColor(Vec4(1, 1, 1, 1))  # White head

        renderer.setTailColor(Vec4(1, 1, 0, 0))  # Fades to transparent yellow

        renderer.setLineScaleFactor(1.0)

        # Particle emitter settings

        emitter = particles.emitter

        emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)

        emitter.setExplicitLaunchVector(Vec3(0.0, 1.0, 0.0))

        emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

        emitter.setAmplitude(1.2)

        emitter.setAmplitudeSpread(0.05)

        emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))

        self.logo_card = CardMaker("logo_card")

        self.logo_card.set_frame(0, 0, 1, 1)

        self.imageObject = OnscreenImage(
            image="graphics/SoulSymphonyLogoCN.png",
            pos=(-0.0, -0.0, 0.0),
            scale=(1, 1, 1),
        )

        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)

        self.bg2 = render.attach_new_node(self.logo_card.generate())

        # Start the color cycling task

        self.cycle_task = base.taskMgr.add(self.cycle_colors, "cycleColors")

        # Create the waving effect using scaling and position intervals

        self.create_logo_wave()

        # Attach particles to effect and star decal

        self.particle.addParticles(particles)

        self.particle.start(self.imageObject)

        # Initialize color intervals for cycling through colors

        self.star_color_cycle = Sequence(
            # ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(
                self.imageObject2,
                0.04,
                Vec4(1, 0, 0, 0.15),
                startColor=Vec4(1, 0.5, 0, 0),
                blendType="easeInOut",
            ),  # Red to Orange
            LerpColorInterval(
                self.imageObject2,
                0.05,
                Vec4(1, 1, 0, 0.15),
                startColor=Vec4(1, 0, 0, 0),
                blendType="easeInOut",
            ),  # Orange to Yellow
            LerpColorInterval(
                self.imageObject2,
                0.06,
                Vec4(0, 1, 0, 0.15),
                startColor=Vec4(1, 1, 0, 0),
                blendType="easeInOut",
            ),  # Yellow to Green
            LerpColorInterval(
                self.imageObject2,
                0.07,
                Vec4(0, 0, 1, 0.15),
                startColor=Vec4(0, 1, 0, 0),
                blendType="easeInOut",
            ),  # Green to Blue
            LerpColorInterval(
                self.imageObject2,
                0.08,
                Vec4(0.29, 0, 0.51, 0.15),
                startColor=Vec4(0, 0, 1, 0),
                blendType="easeInOut",
            ),  # Blue to Indigo
            LerpColorInterval(
                self.imageObject2,
                0.09,
                Vec4(0.56, 0, 1, 0.15),
                startColor=Vec4(0.29, 0, 0.51, 0),
                blendType="easeInOut",
            ),  # Indigo to Violet
            LerpColorInterval(
                self.imageObject2,
                0.1,
                Vec4(1, 0, 0, 0.15),
                startColor=Vec4(0.56, 0, 1, 0),
                blendType="easeInOut",
            ),  # Violet to Red (loop)
        )

        # Loop the color sequence indefinitely

        self.star_color_cycle.loop()

        # Initialize color intervals for cycling through colors

        self.star_color_cycle2 = Sequence(
            # ROYGBIV Color Interpolation
            # ROYGBIV Color Interpolation with staggered time for interference pattern
            # Mirrored ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(
                self.imageObject3,
                0.1,
                Vec4(0.56, 0, 1, 0.15),
                startColor=Vec4(1, 0, 0, 0),
                blendType="easeInOut",
            ),  # Red to Violet
            LerpColorInterval(
                self.imageObject3,
                0.09,
                Vec4(0.29, 0, 0.51, 0.15),
                startColor=Vec4(0.56, 0, 1, 0),
                blendType="easeInOut",
            ),  # Violet to Indigo
            LerpColorInterval(
                self.imageObject3,
                0.08,
                Vec4(0, 0, 1, 0.15),
                startColor=Vec4(0.29, 0, 0.51, 0),
                blendType="easeInOut",
            ),  # Indigo to Blue
            LerpColorInterval(
                self.imageObject3,
                0.07,
                Vec4(0, 1, 0, 0.15),
                startColor=Vec4(0, 0, 1, 0),
                blendType="easeInOut",
            ),  # Blue to Green
            LerpColorInterval(
                self.imageObject3,
                0.06,
                Vec4(1, 1, 0, 0.15),
                startColor=Vec4(0, 1, 0, 0),
                blendType="easeInOut",
            ),  # Green to Yellow
            LerpColorInterval(
                self.imageObject3,
                0.05,
                Vec4(1, 0.5, 0, 0.15),
                startColor=Vec4(1, 1, 0, 0),
                blendType="easeInOut",
            ),  # Yellow to Orange
            LerpColorInterval(
                self.imageObject3,
                0.04,
                Vec4(1, 0, 0, 0.15),
                startColor=Vec4(1, 0.5, 0, 0),
                blendType="easeInOut",
            ),  # Orange to Red (loop)
        )

        self.star_color_cycle2.loop()

        # Loop the color sequence indefinitely

        self.star_color_cycle3 = Sequence(
            LerpColorInterval(self.imageObject, 1, Vec4(1, 0, 0, 1)),  # Red
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(1, 0.5, 0, 1)),  # Orange
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(1, 1, 0, 1)),  # Yellow
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(0, 1, 0, 1)),  # Green
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(0, 0, 1, 1)),  # Blue
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(0.29, 0, 0.51, 1)),  # Indigo
            Wait(1),
            LerpColorInterval(self.imageObject, 1, Vec4(0.56, 0, 1, 1)),  # Violet
            Wait(1),
        )

        self.star_color_cycle3.loop()

        # Loop the color sequence indefinitely

        # Pulsing effect

        # Call the method to create the pulsing effect

        self.create_star_pulse()

        self.particle.reparentTo(self.star_node)

        # Initialize a task to continuously rotate the star

        self.rotate_task = base.task_mgr.add(self.rotate_star, "rotate_star")

    def load_textures(self):
        """Load textures from the directory and store them in a list."""

        for filename in os.listdir(self.textures_path):
            if filename.endswith(
                (".png", ".jpg", ".jpeg")
            ):  # Adjust for texture formats
                texture_path = os.path.join(self.textures_path, filename)

                texture = loader.loadTexture(texture_path)

                self.textures.append(texture)

        if not self.textures:
            print("No textures found in ./graphics/stars. Please check the directory.")

    def set_star_texture(self, texture_index):
        """Set the texture from the loaded list based on index."""

        if self.textures:
            texture_stage = TextureStage("starTexture")

            self.star_placeholder.setTexture(
                texture_stage, self.textures[texture_index]
            )

    def cycle_textures(self, task):
        """Cycle to the next texture and update the placeholder."""

        self.current_texture = (self.current_texture + 1) % len(self.textures)

        self.set_star_texture(self.current_texture)

        # Schedule next cycle

        return task.again

    def create_star_pulse(self):
        # Star 1 pulsing effect

        self.star_pulse = Sequence(
            LerpScaleInterval(
                self.imageObject2, 1, scale=(0, 0, 0), startScale=(4, 4, 4)
            ),  # Scale up
            Wait(0.5),  # Wait for half a second
            LerpScaleInterval(
                self.imageObject2, 1, scale=(4, 4, 4), startScale=(0, 0, 0)
            ),  # Scale down
            Wait(0.5),  # Wait for half a second before looping
        )

        self.star_pulse.loop()

        # Star 2 pulsing effect

        self.star_pulse2 = Sequence(
            LerpScaleInterval(
                self.imageObject3, 1, scale=(4, 4, 4), startScale=(0, 0, 0)
            ),  # Scale up
            Wait(0.5),  # Wait for half a second
            LerpScaleInterval(
                self.imageObject3, 1, scale=(0, 0, 0), startScale=(4, 4, 4)
            ),  # Scale down
            Wait(0.5),  # Wait for half a second before looping
        )

        self.star_pulse2.loop()

    
    def rotate_star(self, task):
        dt = self.globalClock.get_dt()

        new_hpr = self.imageObject2.getHpr() + LVector3(0, 0, self.rotation_speed * dt)

        new_hpr2 = self.imageObject3.getHpr() + LVector3(
            0, 0, -self.rotation_speed * dt
        )

        self.imageObject2.setHpr(new_hpr)  # Set the new HPR

        self.imageObject3.setHpr(new_hpr2)

        return task.cont  # Continue the task

    
    def centerPivot(self, NP):
        pivot = NP.getBounds().getCenter()

        parent = NP.getParent()

        newNP = parent.attachNewNode("StarSpinner")

        newNP.setPos(pivot)

        NP.wrtReparentTo(newNP)

        return newNP

    

    
    def update(self, task):
        dt = self.globalClock.get_dt()

        if self.glyph_rings:
            self.glyph_rings.update(dt)

        self.time += dt

        base.cam.setHpr(base.cam, (0.05, 0.05, 0.05))

        base.cam.look_at(render)

        base.cam.set_z((128 + dt + (math.sin(dt * 10))))

        return task.cont

    def cleanup(self):

        # Remove any tasks
        if hasattr(self, "cycle_task"):
            base.taskMgr.remove(self.cycle_task)

        if hasattr(self, "rotate_task"):
            base.taskMgr.remove(self.rotate_task)

        if hasattr(self, "update_task"):
            #base.taskMgr.remove(self.update_task)
            pass
        # Remove objects and nodes
        self.imageObject.removeNode()
        self.imageObject2.removeNode()
        self.imageObject3.removeNode()
        self.bg2.removeNode()
        self.star_spinner.removeNode()
        
        # Detach elements
        self.glyph_rings.center.detachNode()
        del self.glyph_rings
        del self.logo_card
        # Stop music and sound
        base.bgm.stopMusic()

        # Ignore events and tasks
        base.ignore("enter")
        base.ignore("gamepad-start")
        base.taskMgr.remove("update")
        base.taskMgr.remove("logo_wave_task")

    def exit(self):
        # Perform cleanup of the current stage
        self.cleanup() 
        # Additional exit logic (if any)
        # Example: Transition to the next stage
        # (You can add more code h  ere to handle specific exit actions)
        return
