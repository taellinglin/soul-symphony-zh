from math import pi
from math import sin
from math import cos
import random
import sys
from direct.showbase.PythonUtil import randFloat
from stageflow import Stage
from random import choice
from random import randint
from stageflow import Stage
from level import Level
from player import player
from npc import npc
from motionBlur import MotionBlur
from soulparticles import SoulParticles
from dialog import dialog
from doormanager import DoorManager
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
from direct.particles import ForceGroup
from direct.particles import ParticleManagerGlobal
from direct.particles import Particles
from panda3d.physics import RectangleEmitter
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
import glob
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task.Task import Task
from level import Level
from panda3d.core import PerspectiveLens



# Define minimum and maximum FOV
MIN_FOV = 30  # Narrowest (closer zoom)
MAX_FOV = 90  # Widest (farthest zoom)

class WorldCage(Stage):
    # Add this as a class variable (outside __init__)
    _textures = None  # Class-level storage for textures

    def __init__(self, exit_stage="quit", lvl=None, arcade_lvl=None):
        super().__init__()  # Initialize the ShowBase
        if hasattr(self, "player"):
            self.player.removeNode()
        self.zooming_out = False
        self.zooming_in = False
        # Get the window width and height
        window_width = base.win.getXSize()
        window_height = base.win.getYSize()
    
        # Calculate the correct aspect ratio
        aspect_ratio = window_width / window_height

        # Update the camera lens
        lens = base.cam.node().getLens()  # Get the lens for the camera
        lens.setAspectRatio(aspect_ratio)
        if lvl is None and arcade_lvl is None:
            self.lvl = 0
        else:
            self.lvl = lvl
            self.arcade_lvl = arcade_lvl

        base.enableParticles()
        base.cam.node().get_lens().set_fov(45)
        self.exit_stage = exit_stage

        self.globalClock = globalClock

        self.rotation_speed = 60  # Degrees per second

        # Initialize colors (ROYGBIV)
        self.colors = []

        phase_frags = 6

        # Keep track of jump state
        self.on_ground = False

        self.jump_count = 0  # Tracks how many jumps have been performed

        # Define the ROYGBIV color pattern
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append(
                (1, sin(phase), 0, 1)
            )  # Red to Orange

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
        self.transparency = 0.05
        self.zoom_level = 30
        self.fs = 96000  # Sampling frequency
        self.buffer_size = 256  # Size of audio buffer
        self.audio_data = np.array([])  # Buffer for storing audio data
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        
        # Initialize color intervals for cycling through colors

        base.disableMouse()  # Disable mouse control

        self.font_path = "fonts/konnarian/Daemon.otf"

        self.texture_directory = "stars/"

        self.level_min_bound, self.level_max_bound = 1024, 1024

        self.textures_loaded = False  # Add this flag

        self.color_cycle_task = None  # Track the color cycling task

        self.current_color_index = 0

        self.motion_blur = MotionBlur()

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
        dt = globalClock.get_dt()
        new_hpr = self.imageObject2.getHpr() + LVector3(
            0, 
            0, 
            self.rotation_speed * dt
        )
        new_hpr2 = self.imageObject3.getHpr() + LVector3(
            0, 
            0, 
            -self.rotation_speed * dt
        )
        self.imageObject2.setHpr(new_hpr)
        self.imageObject3.setHpr(new_hpr2)
        return task.cont

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
        self.audio_data = np.zeros(
            self.buffer_size, 
            dtype=np.float32
        )  # Reset buffer
        
        def audio_callback(in_data, frame_count, time_info, status):
            audio_buffer = np.frombuffer(in_data, dtype=np.float32)
            self.audio_data = np.append(self.audio_data, audio_buffer)
            
            if len(self.audio_data) > self.fs:
                self.audio_data = self.audio_data[-self.fs:]
            
            return (None, pyaudio.paContinue)

        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paFloat32,
            channels=1,
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

    def enter(self, data=None):
        self.initialize_audio()
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

        self.cleanup()
       
        self.motion_blur = MotionBlur()
        if data is None:
            data = str(base.levels[self.lvl])

        #self.level = Level(player=self.player, lvl=self.lvl, arcade_lvl=None)

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
        base.cam.set_z(60)

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

        self.reset_level()
        
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
        #base.taskMgr.add(self.handle_zoom,  "HandleZoom
        taskMgr.add(self.processInput, "processInput")
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
            self.jump_count += 1
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
            # Check for portal interactions
            if len(self.level.portals) > 1:  # Need at least 2 portals to warp
                for p, portal in enumerate(self.level.portals):
                    if (portal.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                        # Find the next portal in sequence (wrap around to first if at end)
                        next_portal_index = (p + 1) % len(self.level.portals)
                        destination_portal = self.level.portals[next_portal_index]
                        
                        # Show teleport dialog
                        self.dialog_card.setFont(choice(base.fonts))
                        self.dialog_card.text = choice([
                            "传送！", "瞬移！", "闪现！", "穿越空间！",
                            "空间跳跃！", "传送门启动！", "空间转移！"
                        ])
                        self.dialog_card_node.show()
                        
                        # Play teleport sound
                        base.bgm.playSfx("warp")  # Add appropriate sound effect
                        
                        # Get destination position (slightly above portal to prevent immediate re-trigger)
                        dest_pos = destination_portal.getPos()
                        dest_pos.setZ(dest_pos.getZ() + 2)  # Lift player slightly above destination portal
                        
                        # Teleport player
                        self.player.ballNP.setPos(dest_pos)
                        
                        # Reset velocity to prevent carrying momentum through portal
                        self.player.ballNP.node().setAngularVelocity(Vec3(0, 0, 0))
                        
                        # Optional: Add visual effect at both portals
                        # You could add particle effects or other visual indicators here
                        
                        return  # Exit after teleporting

            # Check for door interactions
            if len(self.level.doors):
                for door in self.level.doors:
                    if (door.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                        self.dialog_card.setFont(choice(base.fonts))
                        self.dialog_card.text = choice([
                            "出发吧！", "快点！", "耶！前进！", "我们走了！",
                            "逃离！", "让我们迷失吧！", "再见！", "逃跑！", "离开这里！"
                        ])
                        self.dialog_card_node.show()
                        base.bgm.playSfx('door_open')
                        
                        # Set the current door in the door manager
                        self.level.door_manager.set_current_door(door)
                        print(f"Selected door: {door.getName()}")
                        self.level.cleanup()
                        self.reset_level()
                        
                        #load another level here
                        
                        return  # Exit after selecting a door
    def reset_level(self):
        
        """Reset level, music, and audio with proper cleanup"""
        print("Resetting level, music, and audio...")
        
        # Stop all tasks first
        #taskMgr.removeTasksMatching('*')
        #taskMgr.remove('level_update')
        
        taskMgr.remove('processInput')
        taskMgr.remove('update')
        taskMgr.remove('level_update')
        taskMgr.remove('HandleZoom')
        taskMgr.remove('process_audio')
        # Stop current music and effects
        if hasattr(base, 'bgm'):
            base.bgm.stopSfx()
            base.bgm.stopMusic()
        
        
        # Pick random level
        random_lvl = random.randrange(len(base.levels))
        print(f"Loading random level: {random_lvl}")
        if hasattr(self, 'level'):
            self.level.cleanup()
        self.player = player()
        self.level = Level(player=self.player, lvl=random_lvl)
        self.level.load_world()
        self.level.load_ground(lvl=random_lvl, arcade_lvl=None)
        self.player.ballNP.reparentTo(self.level.worldNP)
        
        self.level.world.attachRigidBody(self.player.ballNP.node())
        
        base.task_mgr.add(self.update, "update")
        base.task_mgr.add(self.level.update, "level_update")
        base.task_mgr.add(self.processInput, "processInput")
        
        self.start_color_cycling()
        # Play random music track
        if hasattr(base, 'bgm'):
            base.bgm.playMusic(None, True, 0.8)
        print(self.level.worldNP.ls())
        print("Level reset complete!")
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
        
        # Check for door interactions
        if len(self.level.doors):
            for door in self.level.doors:
                if (door.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                    self.dialog_card.setFont(choice(base.fonts))
                    self.dialog_card.text = choice([
                        "出发吧！", "快点！", "耶！前进！", "我们走了！",
                        "逃离！", "让我们迷失吧！", "再见！", "逃跑！", "离开这里！"
                    ])
                    self.dialog_card_node.show()
                    
                    
                    # Set the current door in the door manager
                    self.level.door_manager.set_current_door(door)
                    print(f"Selected door: {door.getName()}")
                    return  # Exit after selecting a door

    def actionAUp_wrapper(self):
        """Wrapper method to handle the button release without requiring a door parameter"""
        if hasattr(self, 'level') and hasattr(self.level, 'door_manager'):
            current_door = self.level.door_manager.get_current_door()
            if current_door:
                if current_door != self.level.door_manager.get_current_door():
                    print(f"Selected door: {current_door.getName()}")
                    self.level.door_manager.set_current_door(current_door)
                else:
                    print(f"Current door already set: {current_door.getName()}")
                self.actionAUp(current_door)  # Pass the door if available
                # Clear the current door after processing
                self.level.door_manager.set_current_door(None)
            else:
                print("No current door selected")
                self.actionAUp()  # Call actionAUp with no door (optional)
        else:
            print("No level or door manager available")
        self.actionAUp()  # Call actionAUp with no door (optional)

    def actionAUp(self, door=None):
        """Handle the 'A' button release action for doors"""
        if door is None:
            print("No door provided")
            return
        
        if not self.level or not self.level.door_manager:
            print("No level or door manager available")
            return
        
        # Get the door name/id from the NodePath
        door_name = door.getName()
        
        # Find the matching door configuration
        door_data = None
        for d in self.level.door_manager.door_data.get('doors', []):
            if d['id'] == door_name:
                door_data = d
                break
        
        if door_data and not door_data['locked']:
            # Get random level index
            random_lvl = random.randrange(len(base.levels))
            print(f"Transitioning to random level: {random_lvl}")
            
            # Cleanup and reinitialize
            
            self.level = Level(player=self.player, lvl=random_lvl)
            
        else:
            print(f"Door {door_name} is locked!")

    def update(self, task):
        # Get the linear velocity vector
        velocity = self.player.ballNP.get_node(0).getLinearVelocity()

        # Calculate the magnitude of the velocity vector
        velocity_magnitude = (
            velocity.length()
        )  # Get the length (magnitude) of the vector

        # Map the magnitude to a transparency value in the range [0.15, 1.0]
        max_velocity = (
            2000.0  # Define a maximum expected velocity (this may need tuning)
        )

        min_transparency = 0.0  # Minimum opacity (more transparent)

        max_transparency = 0.125  # Maximum opacity (fully opaque)

        # Normalize the transparency based on the velocity magnitude
        if velocity_magnitude > 0:
            # Normalize the velocity to a range between 0 and 1
            normalized_velocity = min(1, velocity_magnitude / max_velocity)

            # Set transparency so that lower velocity means higher transparency
            self.transparency = min_transparency + (
                max_transparency - min_transparency
            ) * (1 - normalized_velocity)

        else:
            # If the ball is stationary, set transparency to minimum (most transparent)
            self.transparency = max_transparency

        # Set the rotation speed based on the velocity
        self.rotation_speed = velocity_magnitude * 2

        # Initialize color intervals for cycling through colors
        # Update the listener's velocity based on the player's ball position
        self.level.audio.audio3d.setListenerVelocity(
            self.player.ballNP.get_node(0).getLinearVelocity()
        )

        # Update the color index for cycling through colors
        self.color_idx = (self.color_idx + 1) % len(self.colors)

        # Update ball roll speed based on linear velocity
        self.player.ball_roll.setPlayRate(
            0.05
            * (
                abs(self.player.ballNP.get_node(0).getLinearVelocity().getX())
                + abs(self.player.ballNP.get_node(0).getLinearVelocity().getY())
                + abs(self.player.ballNP.get_node(0).getLinearVelocity().getZ())
            )
        )
        
        # Check proximity to NPC mounts and show/hide nametags
        for n, npc_mount in enumerate(self.level.npc_mounts):
            nametag = npc_mount.find("**/npcNametag**")

            if (
                npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()
            ).length() < 5:
                if nametag:
                    if nametag.isHidden():
                        nametag.show()
                        base.bgm.playSfx("hover")
                    else:
                        nametag.hide()
                else:
                    print("Nametag does not exist.")
                    
# Initialize result and result2 to avoid referencing undefined variables
        result = None
        result2 = None

        # Check for contact with the floor
        if hasattr(self.level, 'floorNP') and self.level.floorNP is not None and \
        hasattr(self.player, 'ballNP') and self.player.ballNP is not None:
            result = self.level.world.contactTestPair(
                self.player.ballNP.node(), self.level.floorNP.node()
            )

        # Check for contact with the walls
        if hasattr(self.level, 'wallsNP') and self.level.wallsNP is not None and \
        hasattr(self.player, 'ballNP') and self.player.ballNP is not None:
            result2 = self.level.world.contactTestPair(
                self.player.ballNP.node(), self.level.wallsNP.node()
            )

        # Handle bouncing sound when contacting the floor
        if result is not None and result.getNumContacts() > 0:
            contact = result.getContacts()[0]
            if contact.getNode1() == self.level.floorNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact.getManifoldPoint()
                    volume = abs(mpoint.getDistance())
                    pitch = (volume / 4) + 0.5
                    base.bgm.playSfx(choice(self.player.boings), volume, pitch)
        else:
            self.player.boing = False

        # Handle bouncing sound when contacting the walls
        if result2 is not None and result2.getNumContacts() > 0:
            contact2 = result2.getContacts()[0]
            if contact2.getNode1() == self.level.wallsNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact2.getManifoldPoint()
                    volume = abs(mpoint.getDistance())
                    pitch = (volume / 4) + 0.5
                    base.bgm.playSfx(choice(self.player.boings), volume, pitch)
        else:
            self.player.boing = False


        # Iterate through each monster in the scene
        for monster in self.level.monsters:
            # Retrieve the combined node for the monster
            yin_yang_np = monster.yin_yang_np  # This holds the whole symbol

            # Perform contact tests with the Yin (black) and Yang (white) parts
            result_yin = self.level.world.contactTestPair(
                self.player.ballNP.node(), monster.yin_np.node()
            )  # Black part

            result_yang = self.level.world.contactTestPair(
                self.player.ballNP.node(), monster.yang_np.node()
            )  # White part

            # Decrease player's health if colliding with the Yin (black part)
            if result_yin.getNumContacts() > 0:
                contact_yin = result_yin.getContacts()[0]

                if contact_yin.getNode1() == monster.yin_np.node():
                    # Decrease player's health by 10%
                    new_health = self.player.health - (self.player.max_health * 0.1)

                    self.update_health(new_health)  # Update health bar and health value

                    print(
                        f"Player hit Yin (black part)! Health decreased: {self.player.health}"
                    )

            # Heal player's health if colliding with the Yang (white part)
            if result_yang.getNumContacts() > 0:
                contact_yang = result_yang.getContacts()[0]

                if contact_yang.getNode1() == monster.yang_np.node():
                    # Increase player's health by 10%, ensuring it doesn't exceed max
                    new_health = self.player.health + (self.player.max_health * 0.1)

                    self.player.health = min(self.player.max_health, new_health)

                    self.update_health(
                        self.player.health
                    )  # Update health bar and health value

                    print(
                        f"Player hit Yang (white part)! Health increased: {self.player.health}"
                    )

        # Update scoreboard and player color
        base.scoreboard.score_node.setColor(choice(self.colors))

        self.player.ballNP.set_color(choice(self.colors))

        # Check for interactions with letters
        for l, letter in enumerate(render.findAllMatches("**/letter**")):
            letter.set_h(letter, 1)

            letter.set_color(choice(self.colors))

            if (
                letter.getPos().getXy() - self.player.ballNP.getPos().getXy()
            ).length() < 3:
                base.bgm.playSfx("pickup", 1, randFloat(0.1, 2), False)

                letter.detachNode()

                letter.removeNode()

                base.scoreboard.addPoints(1)

                print("Score + 1!")

        if self.audio_data.size > 0:
            # Limit the number of samples processed to avoid overflow
            max_samples = 512

            if len(self.audio_data) > max_samples:
                self.audio_data = self.audio_data[:max_samples]

            samples = np.array(self.audio_data)[:max_samples]

            # Proceed with your FFT and transparency updates
            spectrum = np.fft.fft(samples)

            freqs = np.fft.fftfreq(len(samples), 1 / self.fs)

            band_indices = np.array_split(np.argsort(freqs), 7)

            amplitudes = [np.abs(spectrum[indices]).mean() for indices in band_indices]

            transparencies = np.clip(amplitudes / np.max(amplitudes), 0, 0.5)
                
            if hasattr(self.level, 'floorNP') and hasattr(self.level, 'wallsNP') and hasattr(self.level, 'ceil') and hasattr(self.player, 'ballNP'):
                try:
                    # Update the ground, floor, walls, and ceiling colors based on transparency
                    objects_to_update = {
                        "floor": self.level.floorNP.get_children(),
                        "walls": self.level.wallsNP.get_children(),
                        "ceil": self.level.ceil.get_children(),
                    }
                except AttributeError as e:
                    # Log and handle any unexpected issues
                    print(f"Error accessing children: {e}")
                    objects_to_update = {}
            else:
                objects_to_update = {}

            # Debugging output
            print("Objects to update:", objects_to_update)

            for i, (key, children) in enumerate(objects_to_update.items()):
                for obj in children:
                    if obj.isHidden():
                        obj.show()
                        obj.setTransparency(TransparencyAttrib.MAlpha)
                    color_choice = random.choice(
                        self.color_choices
                    )  # Randomly select a color

                    # Ensure the index for transparencies does not exceed its length
                    transparency_value = (
                        transparencies[i] if i < len(transparencies) else 0.05
                    )  # Default to 1.0 if out of bounds

                    obj.set_color(
                        *(color_choice + (transparency_value * 0.5,))
                    )  # Apply transparency

            for p, portal in enumerate(self.level.portals):
                # Find the base and flower nodes
                base_node = portal.find("**/base")

                flower_node = portal.find("**/flower")

                # Make flower rotate or adjust orientation based on time or clock
                flower_node.setHpr(self.clock * 30, self.clock * 30, self.clock * 30)

                flower_node.setScale(2 * ((sin(self.clock) + 1) / 2))

                base_node.setScale(sin(self.clock) * 2)

                # Apply transparency if necessary
                flower_node.setTransparency(
                    TransparencyAttrib.MAlpha
                )  # Make the part use alpha transparency

                # Set the color write to False using ColorWriteAttrib for the flower node
                flower_node.setDepthTest(True)

                base_node.setH(-self.clock)

                # Randomly choose a color from the color choices list
                color_choice = random.choice(self.color_choices)

                # Create the emissive color using the selected color_choice
                emission_color = LVecBase4f(
                    color_choice[0],
                    color_choice[1],
                    color_choice[2],
                    (sin(self.clock * 0.06) + 1) / 2,
                )  # Use RGB and set alpha to 1 for full opacity

                # Randomly choose a color from the color choices list
                color_choice = random.choice(self.color_choices)

                # Create the emissive color using the selected color_choice
                emission_color2 = LVecBase4f(
                    color_choice[0], color_choice[1], color_choice[2], 0.75
                )  # Use RGB and set alpha to 1 for full opacity

                flower_node.setColor(emission_color)

                base_node.setColor(emission_color2)

            for n, npc_node in enumerate(self.level.npc_mounts):
                # Find emblem and face nodes
                emblem = npc_node.find("**/npcEmblem")
                face = npc_node.find("**/npcFace")
                nametag = npc_node.find("**/npcNametag")
                
                # Check proximity for nametag
                if (npc_node.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                    if nametag and not nametag.isEmpty():
                        if nametag.isHidden():
                            nametag.show()
                            base.bgm.playSfx("hover")
                    else:
                        if nametag and not nametag.isEmpty():
                            nametag.hide()
                
                # Handle emblem and face colors only if they exist
                if emblem and not emblem.isEmpty():
                    color_choice = choice(self.color_choices)
                    emblem.setTransparency(TransparencyAttrib.MAlpha)
                    emblem.setColor(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 0.5))
                
                if face and not face.isEmpty():
                    color_choice = choice(self.color_choices)
                    face.setTransparency(TransparencyAttrib.MAlpha)
                    face.setColor(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 1))

                # Get the current time
                time = globalClock.getFrameTime()

                # Calculate Z position with a sine wave
                amplitude = 0.05  # Amplitude of the oscillation

                period = 2.0  # Duration of one full oscillation (2 seconds)

                frequency = (
                    2 * math.pi / period
                )  # Frequency to complete one oscillation in 2 seconds

                # Calculate the new Z offset based on sine wave
                bobbing_height = amplitude * math.sin(frequency * time)

                # Get the original position of the NPC (should be stored when the bobbing starts)
                original_pos = (
                    npc_node.getPos()
                )  # Get the current position (this should be the original position at start)

                # Apply the oscillation relative to the original position (only change the Z value)
                npc_node.setZ(original_pos.getZ() + bobbing_height)

                npc_node.setDepthTest(False)

        # Increment clock and get delta time
        self.clock += 1

        dt = globalClock.getDt()

        self.processInput(dt)

        # Camera positioning based on player's ball position
        self.level.world.doPhysics(dt, 25, 2.0 / 360.0)

        base.cam.set_x(self.player.ballNP.get_x())

        base.cam.set_y(self.player.ballNP.get_y() - 48)

        base.cam.set_z(self.player.ballNP.get_z() + self.zoom_level)

        base.cam.look_at(self.player.ballNP)

        # Perform physics update
        return task.cont

    def transition(self, exit_stage, lvl=None):
        """Generic transition method that can handle both worldcage and arcade transitions"""
        print(f"Transitioning to {exit_stage} level {lvl}")
        
        # Create a full-screen fade effect using a color fade
        fade_card = aspect2d.attachNewNode("fade_card")
        fade_card.setScale(2)  # Covers the entire screen
        fade_card.setTransparency(TransparencyAttrib.MAlpha)
        fade_card.setColor(0, 0, 0, 0)  # Start transparent

        # Create fade-out effect using LerpFunctionInterval
        def fade_color(t):
            fade_card.setColor(0, 0, 0, t)

        fade_out = LerpFunctionInterval(
            fade_color, duration=0.5, fromData=0, toData=1, blendType="easeInOut"
        )

        def complete_transition(task=None):
            fade_card.removeNode()
            self.exit_stage = exit_stage
            
            # Handle the transition based on the exit stage type
            if self.exit_stage == "arcade":
                # Pass both current worldcage level and arcade level
                transition_data = {
                    'worldcage_level': self.lvl,
                    'arcade_level': lvl
                }
                base.flow.transition(self.exit_stage, transition_data)
            else:  # worldcage
                base.flow.transition(self.exit_stage, lvl)
            return Task.done

        fade_out.setDoneEvent("fadeOutDone")
        fade_out.start()
        base.accept("fadeOutDone", complete_transition)

    def transition_to_current_arcade(self, lvl=None):
        # Get the current arcade level using the level's method
        current_arcade_level = self.level.arcade_levels[lvl]

        # Create a full-screen fade effect using a color fade
        fade_card = aspect2d.attachNewNode("fade_card")
        fade_card.setScale(2)  # Covers the entire screen
        fade_card.setTransparency(TransparencyAttrib.MAlpha)
        fade_card.setColor(0, 0, 0, 0)  # Start transparent

        # Create fade-out effect using LerpFunctionInterval
        def fade_color(t):
            fade_card.setColor(0, 0, 0, t)

        fade_out = LerpFunctionInterval(
            fade_color, duration=0.5, fromData=0, toData=1, blendType="easeInOut"
        )

        # Define the completion of the transition
        def complete_transition(task=None):
            fade_card.removeNode()
            self.exit_stage = "arcade"
            base.flow.transition(self.exit_stage, current_arcade_level)
            return Task.done

        fade_out.setDoneEvent("fadeOutDone")
        fade_out.start()
        base.accept("fadeOutDone", complete_transition)
    
    def exit(self, data):
        # Stop and close the audio stream
        if hasattr(self, "stream") and self.stream.is_active():  # Use is_active() instead of active
            self.stream.stop_stream()
            self.stream.close()

        # Reset the audio data array
        self.audio_data = np.array([])

        # Reset amplitude tracking index
        self.current_amplitude_idx = 0

        # Print confirmation of cleanup
        print(
            "Audio stream and associated resources have been successfully cleaned up."
        )
        # Cleanup particles if they exist
        self.motion_blur.cleanup()
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

        base.taskMgr.remove("update")

        for n, node in enumerate(aspect2d.findAllMatches("**/dialog_card")):
            node.detachNode()
            node.removeNode()

        self.stop_color_cycling()  # Stop color cycling when exiting

        return data

    def cleanup(self):
        if hasattr(self, 'renderParent'):
            del self.renderParent
        else:
            print("renderParent attribute not found. Skipping cleanup for it.")
        """Clean up any existing level resources before creating a new one"""
        self.stop_color_cycling()  # Stop color cycling before cleanup

        if self.motion_blur is not None:
            self.motion_blur.cleanup()
            self.motion_blur = None
        else:
            print("Warning: motion_blur is None and cannot be cleaned up.")

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