from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.interval.LerpInterval import LerpHprInterval, LerpPosInterval
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import TransparencyAttrib, TextNode, NodePath, LineSegs, Vec4, Point3
import math
import random
import glob
from direct.task.Task import Task
from stageflow import Stage

class LoadingScreen(Stage):
    def __init__(self, base, exit_stage="worldcage", lvl=None, arcade_lvl=None):
        super().__init__(base)  # Ensure parent class is initialized
        self.exit_stage = exit_stage
        self.lvl = lvl
        self.arcade_lvl = arcade_lvl
        # Create procedural ring
        self.ring = self.create_ring()
        self.ring.reparentTo(self.base.aspect2d)
        self.ring.setScale(0.1)
        self.ring.setPos(0, 0, 0)

        # Create loading text
        self.loading_text = OnscreenText(
            text="Loading...",
            pos=(0, -0.2),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        # Create progress text
        self.progress_text = OnscreenText(
            text="0%",
            pos=(0, -0.3),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        # Setup color cycling
        self.colors = [
            Vec4(1, 0, 0, 1),      # Red
            Vec4(1, 0.5, 0, 1),    # Orange
            Vec4(1, 1, 0, 1),      # Yellow
            Vec4(0, 1, 0, 1),      # Green
            Vec4(0, 0, 1, 1),      # Blue
            Vec4(0.29, 0, 0.51, 1),# Indigo
            Vec4(0.93, 0.51, 0.93, 1) # Violet
        ]
        self.current_color = 0
        self.color_time = 0

        # Setup animations
        self.setup_animations()

        # Add tasks
        self.base.taskMgr.add(self.update_color, "UpdateLoadingRingColor")
        self.base.taskMgr.add(self.load_game_resources_task, "LoadGameResourcesTask")

    def create_ring(self):
        """Create a procedural ring using LineSegs"""
        ls = LineSegs()
        ls.setThickness(3.0)  # Make the line thicker

        # Create ring segments
        segments = 32
        radius = 1.0
        for i in range(segments + 1):
            angle = (i / segments) * 2.0 * math.pi
            x = math.cos(angle) * radius
            y = 0
            z = math.sin(angle) * radius

            if i == 0:
                ls.moveTo(x, y, z)
            else:
                ls.drawTo(x, y, z)

        node = ls.create()
        return NodePath(node)

    def setup_animations(self):
        """Setup spinning and bouncing animations"""
        # Spin animation
        spin = LerpHprInterval(
            self.ring,
            duration=2.0,
            hpr=(0, 0, -360),
            startHpr=(0, 0, 0)
        )
        self.spin_seq = Sequence(spin, name="spinner")
        self.spin_seq.loop()

    def update_color(self, task):
        dt = globalClock.getDt()
        self.color_time += dt

        if self.color_time >= 0.5:  # Change color every 0.5 seconds
            self.color_time = 0
            self.current_color = (self.current_color + 1) % len(self.colors)
            next_color = (self.current_color + 1) % len(self.colors)

            # Interpolate between colors
            c1 = self.colors[self.current_color]
            c2 = self.colors[next_color]
            t = self.color_time / 0.5

            color = Vec4(
                c1[0] + (c2[0] - c1[0]) * t,
                c1[1] + (c2[1] - c1[1]) * t,
                c1[2] + (c2[2] - c1[2]) * t,
                1
            )
            self.ring.setColorScale(color)

        return task.cont

    def update_progress(self, progress, message=""):
        """Update loading progress and message"""
        if self.progress_text:
            self.progress_text.setText(f"{int(progress * 100)}%")
        if message and self.loading_text:
            self.loading_text.setText(message)

    def cleanup(self):
        """Remove loading screen and transition to the next stage."""
        self.spin_seq.finish()
        self.ring.removeNode()
        self.loading_text.destroy()
        self.progress_text.destroy()
        self.base.taskMgr.remove("UpdateLoadingRingColor")
        self.base.taskMgr.remove("LoadGameResourcesTask")
        self.base.taskMgr.remove("UpdateColor")
        self.base.taskMgr.remove("UpdateProgress")
        # Transition to the next stage
        self.base.taskMgr.doMethodLater(0.5, self.transition_to_next_stage, "TransitionToNextStage")

    def transition_to_next_stage(self, task):
        """Proceed with loading the next stage."""
        self.base.load_stage(self.exit_stage, 0, None)
        return task.done

    def load_game_resources_task(self, task):
        """Load resources in small steps to avoid blocking."""
        # Step 1: Load textures
        texture_files = glob.glob("textures/*.png")
        for i, tex_file in enumerate(texture_files):
            progress = i / len(texture_files) * 0.25  # Textures are 25% of loading
            self.update_progress(progress, f"Loading textures... {tex_file}")
            yield Task.cont

        # Step 2: Load models
        model_files = glob.glob("models/*.egg")
        for i, model in enumerate(model_files):
            progress = 0.25 + (i / len(model_files) * 0.25)  # Models are next 25%
            self.update_progress(progress, f"Loading models... {model}")
            yield Task.cont

        # Step 3: Load sounds
        sound_files = glob.glob("sounds/*.wav")
        for i, sound in enumerate(sound_files):
            progress = 0.5 + (i / len(sound_files) * 0.25)  # Sounds are next 25%
            self.update_progress(progress, f"Loading sounds... {sound}")
            yield Task.cont

        # Step 4: Initialize systems
        systems = ["Physics", "Particles", "AI", "Network"]
        for i, system in enumerate(systems):
            progress = 0.75 + (i / len(systems) * 0.25)  # Systems are final 25%
            self.update_progress(progress, f"Initializing {system}...")
            yield Task.cont

        # Finish loading
        self.update_progress(1.0, "Loading complete!")
        yield Task.done

        # Cleanup and transition
        self.cleanup()
        return Task.done
