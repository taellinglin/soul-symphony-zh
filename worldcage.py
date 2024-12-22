
from math import pi

from math import sin

from math import cos

import random

import sys

from panda3d.core import PerspectiveLens

from direct.showbase.PythonUtil import randFloat

from stageflow import Stage

from random import choice

from random import randint

from stageflow import Stage

from level import level

from player import player

from npc import npc
from motionBlur import MotionBlur

from soulparticles import SoulParticles

from dialog import dialog

from panda3d.core import LVecBase4f

import string

from panda3d.core import BitMask32

from panda3d.core import NodePath

from panda3d.core import InputDevice

from panda3d.core import TextureStage

from panda3d.core import Vec3

from panda3d.core import BitMask32

from panda3d.core import TextNode

from panda3d.core import Material

from panda3d.bullet import BulletRigidBodyNode

from panda3d.bullet import BulletBodyNode

from panda3d.core import ClipPlaneAttrib, Plane, LVecBase3

from direct.interval.IntervalGlobal import Sequence, Wait, Parallel

from panda3d.core import (
    TransparencyAttrib,
    CardMaker,
    NodePath,
    Vec4,
    Vec3,
    Point3,
    LVector3,
    ColorWriteAttrib,
    Texture,
)

from panda3d.physics import LinearVectorForce

from direct.gui.OnscreenImage import OnscreenImage

from direct.interval.LerpInterval import (
    LerpScaleInterval,
    LerpColorInterval,
    LerpColorScaleInterval,
    LerpFunctionInterval,
)

from direct.interval.IntervalGlobal import Sequence, LerpPosInterval
import pyaudio
print(pyaudio.get_portaudio_version_text())
import os

os.environ["SD_ENABLE_ASIO"] = "1"


from pydub import AudioSegment

from pydub.playback import play

import numpy as np

import math

from direct.showbase.InputStateGlobal import inputState

from panda3d.core import KeyboardButton

from panda3d.core import PNMImage
from direct.task import Task


from healthbar import HealthBar

from direct.particles.ParticleEffect import ParticleEffect

from direct.particles import Particles

from direct.particles import ForceGroup  # Correct import for ForceGroup

from direct.particles import ParticleManagerGlobal

from direct.particles import Particles

from panda3d.physics import RectangleEmitter

from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer

from panda3d.physics import PointParticleFactory, SpriteParticleRenderer

from panda3d.physics import LinearNoiseForce, DiscEmitter

import glob

from panda3d.core import Filename

# Define minimum and maximum FOV
MIN_FOV = 30  # Narrowest (closer zoom)
MAX_FOV = 90  # Widest (farthest zoom)


class WorldCage(Stage):
    # Add this as a class variable (outside __init__)

    _textures = None  # Class-level storage for textures

    def __init__(self, exit_stage="worldcage", lvl=None, audio_amplitude=None):
    
    
        super().__init__()  # Initialize the ShowBase
        self.zooming_out = False
        self.zooming_in = False
        lens = PerspectiveLens()
        lens.setAspectRatio(16/9)
        base.cam.node().setLens(lens)

        if lvl is None:
            self.lvl = 0

        else:
            self.lvl = lvl

        base.enableParticles()

        self.exit_stage = exit_stage

        self.globalClock = globalClock

        self.rotation_speed = 60  # Degrees per second

        # Initialize colors (ROYGBIV)

        # Assuming player health is already initialized

        self.colors = []

        phase_frags = 6

        # Keep track of jump state

        self.on_ground = False

        self.jump_count = 0  # Tracks how many jumps have been performed

        # Define the ROYGBIV color pattern

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((1, sin(phase), 0, 1))  # Red to Orange

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((1 - sin(phase), 1, 0, 1))  # Orange to Yellow

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((0, 1, sin(phase), 1))  # Yellow to Green

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((0, 1 - sin(phase), 1, 1))  # Green to Cyan

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((sin(phase), 0, 1, 1))  # Cyan to Blue

        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((1, 0, 1 - sin(phase), 1))  # Blue to Violet

        # Maintain a base colors list for cycling

        self.base_colors = [
            (1, 0, 0, 1),  # Red
            (1, 0.5, 0, 1),  # Orange
            (1, 1, 0, 1),  # Yellow
            (0, 1, 0, 1),  # Green
            (0, 0, 1, 1),  # Blue
            (0.5, 0, 1, 1),  # Indigo
            (1, 0, 1, 1),  # Violet
        ]

        # Define a range of colors to choose from

        self.color_choices = [
            (1, 0, 0),  # Red
            (1, 0.5, 0),  # Orange
            (1, 1, 0),  # Yellow
            (0, 1, 0),  # Green
            (0, 0, 1),  # Blue
            (0.5, 0, 1),  # Indigo
            (1, 0, 1),  # Violet
        ]

        self.color_idx = -1

        self.clock = 0

        self.npcs = []
        self.transparency = 0.15
        self.zoom_level = 30
        self.fs = 96000  # Sampling frequency
        self.buffer_size = 1024  # Size of audio buffer
        self.audio_data = np.array([])  # Buffer for storing audio data
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        # Initialize color intervals for cycling through colors
        self.initialize_audio()
        base.disableMouse()  # Disable mouse control

        self.font_path = "fonts/konnarian/Daemon.otf"

        self.texture_directory = "stars/"

        self.level_min_bound, self.level_max_bound = 1024, 1024

        self.textures_loaded = False  # Add this flag

        self.color_cycle_task = None  # Track the color cycling task

        self.current_color_index = 0

    def star(self):
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

        # Call the method to create the pulsing effect for the star

        self.create_star_pulse()

        # Initialize a task to continuously rotate the star

        self.rotate_task = base.taskMgr.add(self.rotate_star, "rotate_star")

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

        # print(f"New parent position: {newNP.getPos()}")

        return newNP

    def initialize_audio(self):
        """Initialize and start the audio stream using pyaudio."""
        self.audio_data = np.zeros(self.buffer_size, dtype=np.float32)  # Reset buffer
        
        def audio_callback(in_data, frame_count, time_info, status):
            # Convert byte data to numpy array
            audio_buffer = np.frombuffer(in_data, dtype=np.float32)
            self.audio_data = np.append(self.audio_data, audio_buffer)
            
            # Truncate buffer if it exceeds a certain size
            if len(self.audio_data) > self.fs:
                self.audio_data = self.audio_data[-self.fs:]
            
            return (None, pyaudio.paContinue)

        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paFloat32,
            channels=1,  # Mono
            rate=self.fs,
            input=True,
            frames_per_buffer=self.buffer_size,
            stream_callback=audio_callback,
        )

        self.stream.start_stream()
        print("Audio stream initialized and started.")

    def process_audio(self):
        """Process the captured audio data."""
        if len(self.audio_data) > 0:
            # Perform FFT and other analyses
            samples = self.audio_data[-self.buffer_size:]  # Process the latest buffer
            spectrum = np.fft.fft(samples)
            freqs = np.fft.fftfreq(len(samples), 1 / self.fs)
            
            # Example: Split frequencies into bands and compute amplitudes
            band_indices = np.array_split(np.argsort(freqs), 7)
            amplitudes = [np.abs(spectrum[indices]).mean() for indices in band_indices]

            # Map amplitudes to transparency or other visual effects
            transparencies = np.clip(amplitudes / np.max(amplitudes), 0, 0.5)
            print("Transparencies:", transparencies)

    def cleanup_audio(self):
        """Stop and close the audio stream and cleanup resources."""
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
        
        self.pyaudio_instance.terminate()
        self.audio_data = np.array([])
        print("Audio stream and resources cleaned up.")

    def enter(self, lvl=None):
    
        
        print("Entered new level or portal, audio stream reset.")
        # Set initial fade state
        base.win.setClearColor(Vec4(0, 0, 0, 1))  # Start with opaque black background
        render2d.setColorScale(0, 0, 0, 1)  # Start fully black

        # Create fade in interval for render2d color scale
        fade_in = LerpColorScaleInterval(
            render2d,
            0.5,
            Vec4(1, 1, 1, 1),  # Fade to normal
            Vec4(0, 0, 0, 1),  # Start fully black
            blendType="easeInOut",
        )

        def cleanup_fade():
            # Restore normal state after fading
            render2d.clearColorScale()
            base.win.setClearColorActive(False)

        fade_in.setDoneEvent("fadeInDone")
        fade_in.start()
        base.accept("fadeInDone", cleanup_fade)

        #self.cleanup_level()
        if lvl == None:
            lvl = self.lvl

        self.lvl = lvl

        # Only load textures once
        if not self.textures_loaded:
            # Load textures and other persistent resources here
            self.load_textures()
            self.textures_loaded = True

        self.star()

        # Ensure healthbar is initialized
        if not hasattr(self, "healthbar"):
            self.healthbar = HealthBar(parent=base.aspect2d)  # Create the health bar

        self.healthbar.max_health = 100  # Directly setting the max health

        self.healthbar.update_health(
            self.healthbar.max_health
        )  # Set the initial health value

        self.star_color_cycle = Sequence(
            # ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(
                self.imageObject2,
                0.04,
                Vec4(1, 0, 0, self.transparency),
                startColor=Vec4(1, 0.5, 0, 0),
                blendType="easeInOut",
            ),  # Red to Orange
            LerpColorInterval(
                self.imageObject2,
                0.05,
                Vec4(1, 1, 0, self.transparency),
                startColor=Vec4(1, 0, 0, 0),
                blendType="easeInOut",
            ),  # Orange to Yellow
            LerpColorInterval(
                self.imageObject2,
                0.06,
                Vec4(0, 1, 0, self.transparency),
                startColor=Vec4(1, 1, 0, 0),
                blendType="easeInOut",
            ),  # Yellow to Green
            LerpColorInterval(
                self.imageObject2,
                0.07,
                Vec4(0, 0, 1, self.transparency),
                startColor=Vec4(0, 1, 0, 0),
                blendType="easeInOut",
            ),  # Green to Blue
            LerpColorInterval(
                self.imageObject2,
                0.08,
                Vec4(0.29, 0, 0.51, self.transparency),
                startColor=Vec4(0, 0, 1, 0),
                blendType="easeInOut",
            ),  # Blue to Indigo
            LerpColorInterval(
                self.imageObject2,
                0.09,
                Vec4(0.56, 0, 1, self.transparency),
                startColor=Vec4(0.29, 0, 0.51, 0),
                blendType="easeInOut",
            ),  # Indigo to Violet
            LerpColorInterval(
                self.imageObject2,
                0.1,
                Vec4(1, 0, 0, self.transparency),
                startColor=Vec4(0.56, 0, 1, 0),
                blendType="easeInOut",
            ),  # Violet to Red (loop)
        )

        # Initialize color intervals for cycling through colors for star3

        self.star_color_cycle2 = Sequence(
            # Mirrored ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(
                self.imageObject3,
                0.1,
                Vec4(0.56, 0, 1, self.transparency),
                startColor=Vec4(1, 0, 0, 0),
                blendType="easeInOut",
            ),  # Red to Violet
            LerpColorInterval(
                self.imageObject3,
                0.09,
                Vec4(0.29, 0, 0.51, self.transparency),
                startColor=Vec4(0.56, 0, 1, 0),
                blendType="easeInOut",
            ),  # Violet to Indigo
            LerpColorInterval(
                self.imageObject3,
                0.08,
                Vec4(0, 0, 1, self.transparency),
                startColor=Vec4(0.29, 0, 0.51, 0),
                blendType="easeInOut",
            ),  # Indigo to Blue
            LerpColorInterval(
                self.imageObject3,
                0.07,
                Vec4(0, 1, 0, self.transparency),
                startColor=Vec4(0, 0, 1, 0),
                blendType="easeInOut",
            ),  # Blue to Green
            LerpColorInterval(
                self.imageObject3,
                0.06,
                Vec4(1, 1, 0, self.transparency),
                startColor=Vec4(0, 1, 0, 0),
                blendType="easeInOut",
            ),  # Green to Yellow
            LerpColorInterval(
                self.imageObject3,
                0.05,
                Vec4(1, 0.5, 0, self.transparency),
                startColor=Vec4(1, 1, 0, 0),
                blendType="easeInOut",
            ),  # Yellow to Orange
            LerpColorInterval(
                self.imageObject3,
                0.04,
                Vec4(1, 0, 0, self.transparency),
                startColor=Vec4(1, 0.5, 0, 0),
                blendType="easeInOut",
            ),  # Orange to Red (loop)
        )

        # Loop the color sequence indefinitely

        self.star_color_cycle.loop()

        # Initialize color intervals for cycling through colors for star3

        self.star_color_cycle2.loop()

        # print("Roll Test Area Entered...")

        base.cam.set_z(24)

        base.bgm.playMusic(None, True, 0.8)

        base.task_mgr.add(self.update, "update")

        base.accept("escape", sys.exit)

        inputState.watchWithModifiers("forward", "w")

        inputState.watchWithModifiers("left", "a")

        inputState.watchWithModifiers("reverse", "s")

        inputState.watchWithModifiers("right", "d")

        inputState.watchWithModifiers("turnLeft", "q")

        inputState.watchWithModifiers("turnRight", "e")

        inputState.watchWithModifiers("jump", "gamepad-face_a")

        inputState.watchWithModifiers("jump", "space")

        inputState.watchWithModifiers("cam-right", "]")

        inputState.watchWithModifiers("cam-left", "[")

        inputState.watchWithModifiers("cam-right", "gamepad-trigger_right")

        inputState.watchWithModifiers("cam-left", "gamepad-trigger_left")

        inputState.watchWithModifiers("cam-right", "gamepad-shoulder_right")

        inputState.watchWithModifiers("cam-left", "gamepad-shoulder_left")

        print("level: " + str(self.lvl))

        self.level = level(base.lvl)

        self.level.get_npcs(21)

        self.level.place_npcs()

        self.player = player()

        self.player.ballNP.reparentTo(self.level.worldNP)

        self.level.world.attachRigidBody(self.player.ballNP.node())

        self.player.ballNP.setPos(random.choice(self.level.portals).getPos() + (0, 0, 3))

        self.dialog = dialog()

        self.dialog_card = TextNode("dialog_card")

        self.dialog_card.align = 2

        self.dialog_card.setWordwrap(40)

        self.dialog_card.setFont(choice(base.fonts))

        self.dialog_card_node = aspect2d.attach_new_node(self.dialog_card)

        self.dialog_card_node.setScale(0.08)

        base.scoreboard.show()

        self.level.audio.audio3d.attachListener(base.cam)

        self.particles = SoulParticles(self.texture_directory, self.level.worldNP)

        self.particles.create_matrix_effect(t=self.level.worldNP)

        base.accept("gamepad-face_a", self.actionA)

        base.accept("space", self.actionA)

        base.accept("gamepad-face_a-up", self.actionAUp)

        base.accept("space-up", self.actionAUp)

        base.accept("gamepad-face_b", self.actionB)

        base.accept("shift", self.actionB)

        base.accept("gamepad-face_b-up", self.actionBUp)

        base.accept("shift-up", self.actionBUp)

        # Watch for modifier combinations
        base.accept("gamepad-shoulder-left", self.set_zoom_out, [True])  # L1 pressed
        base.accept(
            "gamepad-shoulder-left-up", self.set_zoom_out, [False]
        )  # L1 released
        base.accept("gamepad-shoulder-right", self.set_zoom_in, [True])  # R1 pressed
        base.accept(
            "gamepad-shoulder-right-up", self.set_zoom_in, [False]
        )  # R1 released

        # Task to handle modifiers
        base.taskMgr.add(self.handle_zoom, "HandleZoom")

        self.start_color_cycling()  # Start color cycling once

    
    def set_zoom_out(self, state):
        print("Zoom Out")
        self.zooming_out = state

    
    def set_zoom_in(self, state):
        print("Zoom in")
        self.zooming_in = state

    
    def handle_zoom(self, task):
        if self.zooming_out:
            self.zoom_fov(-0.2)
        if self.zooming_in:
            self.zoom_fov(0.2)
        return task.cont

    
    def zoom_fov(self, delta):
        current_fov = base.camLens.get_fov()[0]
        new_fov = current_fov + delta
        new_fov = max(30, min(90, new_fov))  # Clamp FOV
        base.camLens.set_fov(new_fov)
        self.zoom_level = new_fov
        print(f"Zoom adjusted: FOV is now {new_fov}")

    def actionA(self):
        # Check if the player is touching the ground
    

        result = self.level.world.contactTestPair(
            self.player.ballNP.node(), self.level.floorNP.node()
        )

        if result.getNumContacts() > 0:
            self.on_ground = True

            self.jump_count = 0  # Reset the jump count when on the ground

        else:
            self.on_ground = False

        # If player is on the ground or has performed less than 2 jumps

        if self.jump_count < 2:
            # Apply a jump force when the action is triggered

            self.player.ballNP.node().applyCentralImpulse(Vec3(0, 0, 128 + 32))

            base.bgm.playSfx("ball-jump")

            # Increment the jump counter

            self.jump_count += 1

            # Perform extra actions if near NPC mounts

            if len(self.level.npc_mounts):
                for n, npc_mount in enumerate(self.level.npc_mounts):
                    if (
                        npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()
                    ).length() < 5:
                        self.dialog_card.text = self.level.npcs[n].get("dialog")

                        self.dialog_card.setFont(choice(base.fonts))

                        self.dialog_card_node.show()

                        base.bgm.playSfx("start-dialog")

                        self.player.force = Vec3(0, 0, 0)

                        self.player.torque = Vec3(0, 0, 0)

                        self.player.ballNP.node().setLinearDamping(1)

            # Perform actions if near portals

            if len(self.level.portals):
                for p, portal in enumerate(self.level.portals):
                    if (
                        portal.getPos().getXy() - self.player.ballNP.getPos().getXy()
                    ).length() < 5:
                        self.dialog_card.setFont(choice(base.fonts))

                        self.dialog_card.text = choice(
                            [
                                "出发吧！",
                                "快点！",
                                "耶！前进！",
                                "我们走了！",
                                "逃离！",
                                "让我们迷失吧！",
                                "再见！",
                                "逃跑！",
                                "离开这里！",
                            ]
                        )

                        self.dialog_card_node.show()

                        self.player.force = Vec3(0, 0, 0)

                        self.player.torque = Vec3(0, 0, 0)

                        self.player.ballNP.node().setLinearDamping(1)

    
    def actionAUp(self):
        if self.player.ballNP.node().getLinearDamping() == 1:
            self.player.ballNP.node().setLinearDamping(0)

        self.dialog_card_node.hide()

        for p, portal in enumerate(self.level.portals):
            if (
                portal.getPos().getXy() - self.player.ballNP.getPos().getXy()
            ).length() < 8:
                self.dialog_card.text = choice(
                    ["Ok!", "Alright!", "Affirmative!", "Totally!"]
                )

                self.dialog_card_node.hide()

                base.bgm.stopSfx()

                base.bgm.playSfx("warp")
                base.lvl = random.randint(0, len(base.levels) -1)
                self.transition("worldcage")

                return

    
    def actionB(self):
        self.player.ballNP.node().setAngularDamping(0.82)

        self.player.ballNP.node().setLinearDamping(0.82)

    
    def actionBUp(self):
        self.player.ballNP.node().setAngularDamping(0)

        self.player.ballNP.node().setLinearDamping(0)

    
    def processInput(self, dt):
        force = Vec3(0, 0, 0)

        torque = Vec3(0, 0, 0)

        if not base.gamepad_input.gamepad == None:
            self.left_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_x)

            self.left_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_y)

            self.right_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_x)

            self.right_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_y)

            self.leftAnalog = Vec3(self.left_x.value, self.left_y.value, 0)

            force = self.leftAnalog

            torque = Vec3(0, 0, self.right_x.value)

        if inputState.isSet("cam-right"):
            base.cam.set_r(self.ballNP, 0.5)

        if inputState.isSet("cam-left"):
            base.cam.set_r(self.ballNP, -0.5)

        if inputState.isSet("forward"):
            force.setY(1.0)

        if inputState.isSet("reverse"):
            force.setY(-1.0)

        if inputState.isSet("left"):
            force.setX(-1.0)

        if inputState.isSet("right"):
            force.setX(1.0)

        if inputState.isSet("turnLeft"):
            torque.setZ(1.0)

        if inputState.isSet("turnRight"):
            torque.setZ(-1.0)

        force *= 100.0

        torque *= 100.0

        # force = self.ballNP.getRelativeVector(Vec3(base.cam.get_h(), base, 0), force)

        # torque = base.cam.getRelativeVector(self.ballNP, torque)

        self.player.ballNP.node().setActive(True)

        self.player.ballNP.node().applyCentralForce(force)

        self.player.ballNP.node().applyTorque(torque)

    def update(self, task):
        velocity = self.player.ballNP.get_node(0).getLinearVelocity()
        velocity_magnitude = velocity.length()
        max_velocity = 2000.0
        min_transparency = 0.0
        max_transparency = 0.125

        if velocity_magnitude > 0:
            normalized_velocity = min(1, velocity_magnitude / max_velocity)
            self.transparency = min_transparency + (max_transparency - min_transparency) * (1 - normalized_velocity)
        else:
            self.transparency = max_transparency

        self.rotation_speed = velocity_magnitude * 2
        self.color_idx = (self.color_idx + 1) % len(self.colors)
        
        self.player.ball_roll.setPlayRate(
            0.05 * (abs(velocity.getX()) + abs(velocity.getY()) + abs(velocity.getZ()))
        )

        self.level.audio.audio3d.setListenerVelocity(velocity)

        for npc_mount in self.level.npc_mounts:
            nametag = npc_mount.find("**/npcNametag")
            if nametag and (npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                if nametag.isHidden():
                    nametag.show()
                    base.bgm.playSfx("hover")
            elif nametag:
                nametag.hide()

        result = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.floorNP.node())
        result2 = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.wallsNP.node())

        if result.getNumContacts() > 0:
            contact = result.getContacts()[0]
            if contact.getNode1() == self.level.floorNP.node() and not self.player.boing:
                self.player.boing = True
                mpoint = contact.getManifoldPoint()
                volume = abs(mpoint.getDistance())
                pitch = (volume / 4) + 0.5
                base.bgm.playSfx(choice(self.player.boings), volume, pitch)
        else:
            self.player.boing = False

        if result2.getNumContacts() > 0:
            contact2 = result2.getContacts()[0]
            if contact2.getNode1() == self.level.wallsNP.node() and not self.player.boing:
                self.player.boing = True
                mpoint = contact2.getManifoldPoint()
                volume = abs(mpoint.getDistance())
                pitch = (volume / 4) + 0.5
                base.bgm.playSfx(choice(self.player.boings), volume, pitch)
        else:
            self.player.boing = False

        for monster in self.level.monsters:
            yin_yang_np = monster.yin_yang_np
            result_yin = self.level.world.contactTestPair(self.player.ballNP.node(), monster.yin_np.node())
            result_yang = self.level.world.contactTestPair(self.player.ballNP.node(), monster.yang_np.node())

            if result_yin.getNumContacts() > 0:
                contact_yin = result_yin.getContacts()[0]
                if contact_yin.getNode1() == monster.yin_np.node():
                    new_health = self.player.health - (self.player.max_health * 0.1)
                    self.update_health(new_health)
                    print(f"Player hit Yin (black part)! Health decreased: {self.player.health}")

            if result_yang.getNumContacts() > 0:
                contact_yang = result_yang.getContacts()[0]
                if contact_yang.getNode1() == monster.yang_np.node():
                    new_health = self.player.health + (self.player.max_health * 0.1)
                    self.player.health = min(self.player.max_health, new_health)
                    self.update_health(self.player.health)
                    print(f"Player hit Yang (white part)! Health increased: {self.player.health}")

        base.scoreboard.score_node.setColor(choice(self.colors))
        self.player.ballNP.set_color(choice(self.colors))

        for letter in render.findAllMatches("**/letter**"):
            letter.set_h(letter, 1)
            letter.set_color(choice(self.colors))
            if (letter.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 3:
                base.bgm.playSfx("pickup", 1, randFloat(0.1, 2), False)
                letter.detachNode()
                letter.removeNode()
                base.scoreboard.addPoints(1)
                print("Score + 1!")

        if self.audio_data.size > 0:
            max_samples = 512
            if len(self.audio_data) > max_samples:
                self.audio_data = self.audio_data[:max_samples]
            samples = np.array(self.audio_data)[:max_samples]
            spectrum = np.fft.fft(samples)
            freqs = np.fft.fftfreq(len(samples), 1 / self.fs)
            band_indices = np.array_split(np.argsort(freqs), 7)
            amplitudes = [np.abs(spectrum[indices]).mean() for indices in band_indices]
            transparencies = np.clip(amplitudes / np.max(amplitudes), 0, 0.5)

            objects_to_update = {
                "floor": self.level.floor.get_children(),
                "walls": self.level.walls.get_children(),
                "ceil": self.level.ceil.get_children(),
            }

            for i, (key, children) in enumerate(objects_to_update.items()):
                for obj in children:
                    if obj.isHidden():
                        obj.show()
                        obj.setTransparency(TransparencyAttrib.MAlpha)
                    color_choice = random.choice(self.color_choices)
                    transparency_value = transparencies[i] if i < len(transparencies) else 0.05
                    obj.set_color(*(color_choice + (transparency_value * 0.5,)))

            for portal in self.level.portals:
                base_node = portal.find("**/base")
                flower_node = portal.find("**/flower")
                if base_node and flower_node:
                    flower_node.setHpr(self.clock * 30, self.clock * 30, self.clock * 30)
                    flower_node.setScale(2 * ((sin(self.clock) + 1) / 2))
                    base_node.setScale(sin(self.clock) * 2)
                    flower_node.setTransparency(TransparencyAttrib.MAlpha)
                    flower_node.setDepthTest(True)
                    base_node.setH(-self.clock)
                    color_choice = random.choice(self.color_choices)
                    emission_color = LVecBase4f(color_choice[0], color_choice[1], color_choice[2], (sin(self.clock * 0.06) + 1) / 2)
                    flower_node.setColor(emission_color)
                    color_choice = random.choice(self.color_choices)
                    emission_color2 = LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 0.75)
                    base_node.setColor(emission_color2)

            for npc_node in self.level.npc_mounts:
                emblem = npc_node.find("**/npcEmblem")
                face = npc_node.find("**/npcFace")
                if emblem and face:
                    color_choice = random.choice(self.color_choices)
                    emblem.set_color(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 0.5))
                    color_choice = random.choice(self.color_choices)
                    face.set_color(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 1))
                    time = globalClock.getFrameTime()
                    amplitude = 0.05
                    period = 2.0
                    frequency = 2 * math.pi / period
                    bobbing_height = amplitude * math.sin(frequency * time)
                    original_pos = npc_node.getPos()
                    npc_node.setZ(original_pos.getZ() + bobbing_height)
                    npc_node.setDepthTest(False)

        self.clock += 1
        dt = globalClock.getDt()
        self.processInput(dt)

        self.level.world.doPhysics(dt, 25, 2.0 / 360.0)
        base.cam.set_x(self.player.ballNP.get_x())
        base.cam.set_y(self.player.ballNP.get_y() - 48)
        base.cam.set_z(self.player.ballNP.get_z() + self.zoom_level)
        base.cam.look_at(self.player.ballNP)

        return task.cont

    def transition(self, exit_stage, lvl=None):
    
        # Create a full-screen fade effect using a color fade
        fade_card = aspect2d.attachNewNode("fade_card")
        fade_card.setScale(2)  # Covers the entire screen
        fade_card.setTransparency(TransparencyAttrib.MAlpha)
        fade_card.setColor(0, 0, 0, 0)  # Start transparent

        # Create fade-out effect using LerpFunctionInterval
        def fade_color(t):
            if hasattr(self, "fade_card"):
                fade_card.setColor(0, 0, 0, t)

        fade_out = LerpFunctionInterval(
            fade_color, duration=0.5, fromData=0, toData=1, blendType="easeInOut"
        )

        def complete_transition(task=None):
            if hasattr(self, "fade_card"):
                fade_card.removeNode()
            self.exit_stage = "main_menu" if exit_stage is None else exit_stage
            base.lvl = random.randint(0, len(base.levels) -1)
            print(f"Base Level:{base.lvl}")
            base.flow.transition("worldcage")
            return Task.done

        fade_out.setDoneEvent("fadeOutDone")
        fade_out.start()
        base.accept("fadeOutDone", complete_transition)
    

    def exit(self, data=None):
           # Stop and close the audio stream
        #if hasattr(self, "stream") and self.stream.is_active():  # Use is_active() instead of active
            #self.stream.stop_stream()
            #self.stream.close()

        # Reset the audio data array
        #self.audio_data = np.array([])

        # Reset amplitude tracking index
        self.current_amplitude_idx = 0

        # Print confirmation of cleanup
        print(
            "Audio stream and associated resources have been successfully cleaned up."
        )
        # Cleanup particles if they exist
        if hasattr(self, "particles"):
            # Disable the particle system

            self.particles.cleanup()  # Clean up any particle resources

            self.particles = None  # Dereference particles to fully clean up

        self.star_node.removeNode()

        self.star_decal.removeNode()

        self.imageObject2.removeNode()

        self.imageObject3.removeNode()

        base.taskMgr.remove("rotate_star")

        self.player.ball_roll.stop()

        self.level.world.removeRigidBody(self.level.floorNP.node())

        self.level.world.removeRigidBody(self.level.wallsNP.node())

        self.level.world.removeRigidBody(self.player.ballNP.node())

        # self.level.world = None

        self.level.audio.stopLoopingAudio()

        # self.debugNP = None

        self.level.debugNP.detachNode()

        self.level.debugNP.removeNode()

        self.level.groundNP = None

        # self.player.ballNP = None

        self.player.ballNP.detachNode()

        self.player.ballNP.removeNode()

        for n, npc in enumerate(self.level.npc_mounts):
            npc.detachNode()

            npc.removeNode()

        for p, portal in enumerate(self.level.portals):
            portal.detachNode()

            portal.removeNode()

        for l, letter in enumerate(render.findAllMatches("**/letter**")):
            letter.detachNode()

            letter.removeNode()

        self.level.worldNP.removeNode()

        base.ignore("enter")

        base.ignore("gamepad-face_a")

        base.ignore("space")

        base.ignore("gamepad-face_a-up")

        base.ignore("space-up")

        base.ignore("gamepad-face_b")

        base.ignore("shift")

        base.ignore("gamepad-face_b-up")

        base.ignore("shift-up")
        base.ignore("gamepad-shoulder_left")
        base.ignore("gamepad-shoulder_left-up")
        base.ignore("gamepad-shoulder_right")
        base.ignore("gamepad-shoulder_right-up")

        # self.ball.detachNode()

        base.bgm.stopMusic()

        base.cam.set_z(1)

        base.cam.set_x(0)

        base.cam.set_y(0)

        base.cam.set_hpr(0, 0, 0)

        base.taskMgr.remove("update")

        for n, node in enumerate(aspect2d.findAllMatches("**/dialog_card")):
            node.detachNode()

            node.removeNode()

        self.stop_color_cycling()  # Stop color cycling when exiting

        return data

    def cleanup_level(self):
        """Clean up any existing level resources before creating a new one"""
        self.stop_color_cycling()  # Stop color cycling before cleanup


        if hasattr(self, "level"):
            # Clean up physics world
            if hasattr(self.level, "world"):
                if hasattr(self.level, "floorNP") and self.level.floorNP:
                    self.level.world.removeRigidBody(self.level.floorNP.node())
                if hasattr(self.level, "wallsNP") and self.level.wallsNP:
                    self.level.world.removeRigidBody(self.level.wallsNP.node())

            # Clean up audio
            if hasattr(self.level, "audio"):
                self.level.audio.stopLoopingAudio()

            # Clean up debug visualization
            if hasattr(self.level, "debugNP"):
                self.level.debugNP.detachNode()
                self.level.debugNP.removeNode()

            # Clean up NPCs
            if hasattr(self.level, "npc_mounts"):
                for npc in self.level.npc_mounts:
                    npc.detachNode()
                    npc.removeNode()

            # Clean up portals
            if hasattr(self.level, "portals"):
                for portal in self.level.portals:
                    portal.detachNode()
                    portal.removeNode()

            # Clean up world node
            if hasattr(self.level, "worldNP"):
                self.level.worldNP.removeNode()

    def load_textures(self):
        """Load textures only if they haven't been loaded before"""
        if WorldCage._textures is None:  # Only load if not already loaded
            print("Loading textures from directory:", self.texture_directory)
            texture_files = sorted(
                [
                    f
                    for f in os.listdir(self.texture_directory)
                    if f.endswith(".png") or f.endswith(".jpg")
                ]
            )

            WorldCage._textures = [
                base.loader.loadTexture(os.path.join(self.texture_directory, texture))
                for texture in texture_files
            ]
            print(f"Total textures loaded: {len(WorldCage._textures)}")
        else:
            print("Using previously loaded textures")

        self.textures = WorldCage._textures  # Reference the class textures
        self.textures_loaded = True

    def create_matrix_effect(self):
        """Create matrix particle effect using cached textures"""
        print("Creating matrix effect...")
        if not self.textures_loaded:
            print("Loading textures from directory: stars/")
            self.load_textures()
        # Use self.textures for particle system setup
        # ... rest of particle system creation code ...

    def start_color_cycling(self):
        """Start the color cycling task if not already running"""
        if self.color_cycle_task is None:
            self.color_cycle_task = taskMgr.add(self.update_colors, "color_cycle_task")

    def stop_color_cycling(self):
        """Stop the color cycling task if running"""
        if self.color_cycle_task is not None:
            taskMgr.remove(self.color_cycle_task)
            self.color_cycle_task = None

    def update_colors(self, task):
        """Update colors for various game elements"""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        current_color = self.colors[self.current_color_index]

        # Apply the color to relevant objects
        # Add any objects you want to cycle colors for

        return task.cont