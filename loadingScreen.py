from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.interval.LerpInterval import LerpHprInterval, LerpPosInterval
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import TransparencyAttrib, TextNode, NodePath, LineSegs, Vec4, Point3
import math
import random
import glob
from stageflow import Stage
import os
from math import sin
from panda3d.core import CardMaker, NodePath
from direct.task.Task import Task
class LoadingScreen(Stage):
    def __init__(self, exit_stage="worldcage"):
        base.setBackgroundColor(0, 0, 0)  # RGB for black
        #self.reset_motion_blur()
        self.exit_stage = exit_stage
        self.lvl = base.lvl
        self.scale_speed = 1
        # Create procedural ring
        self.ring = self.create_ring()
        self.ring.reparentTo(base.aspect2d)
        self.ring.setScale(0.1)
        self.ring.setPos(0, 0, 0)
        
        # Load fonts from the /fonts/text/ directory
        self.fonts = self.load_fonts("fonts/text/")

        # Select a random font for the texts
        self.selected_font = self.select_random_font()
        
        # Create loading text (in Chinese)
        self.loading_text = OnscreenText(
            text="加载中...",  # "Loading..."
            pos=(0, -0.2),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            font=self.selected_font,
            shadowOffset=[0.03,0.03],
            shadow=[0,0,0,1]
        )

        # Create progress text (in Chinese)
        self.progress_text = OnscreenText(
            text="0%",  # Percentage
            pos=(0, -0.3),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            font=self.selected_font,
            shadowOffset=[0.03,0.03],
            shadow=[0,0,0,1]
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
        base.taskMgr.add(self.update_color, "UpdateLoadingRingColor")
        base.taskMgr.add(self.load_game_resources_task, "LoadGameResourcesTask")
        self.card = None

    def reset_motion_blur(self):
        # Create a black card
        cm = CardMaker('black_card')
        cm.setFrame(-1, 1, -1, 1)  # Full screen coordinates
        self.card = NodePath(cm.generate())  # Create the card

        # Set the card to black color
        self.card.setColor(0, 0, 0, 1)  # RGB for black

        # Reparent the card to render
        self.card.reparentTo(base.render)

        # Make the card disappear after 1 frame to reset blur
        base.taskMgr.doMethodLater(0.1, self.remove_card, "remove_black_card_task")

    def remove_card(self, task):
        if self.card:
            self.card.removeNode()  # Remove the card from the scene
        return task.done
    
    def color_cycle(self, task):
        self.progress_text.fg = random.choice(self.colors)
        self.loading_text.fg = random.choice(self.colors)
        return task.cont
    
    def grow_and_shrink(self, task):
        dt = globalClock.getDt()  # Get delta time to make it frame-rate independent
        
        # Use sine function to create oscillation, multiplying by scale range
        oscillation = sin(globalClock.getFrameTime() * self.scale_speed) * 0.5 + 1  # Oscillates between 0.5 and 1.5
        
        # Apply the oscillation to the scale of the object
        self.ring.setScale(oscillation, oscillation, oscillation)
        
        return task.cont  # Continue the task

    def load_fonts(self, directory):
        """Load font files from a directory."""
        font_files = glob.glob(os.path.join(directory, "*.ttf"))
        return [base.loader.loadFont(font_file) for font_file in font_files]

    def select_random_font(self):
        """Select a random font from the loaded fonts."""
        if not self.fonts:
            print("No fonts found in the directory. Using the default font.")
            return None
        return random.choice(self.fonts)
    
    def create_ring(self):
        """Create a procedural ring using LineSegs"""
        ls = LineSegs()
        ls.setThickness(1.0)  # Make the line thicker

        # Create ring segments
        segments = 3
        radius = 1
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
            duration=16,
            hpr=(0, 0, -360),
            startHpr=(0, 0, 0)
        )
        self.spin_seq = Sequence(spin, name="spinner")
        self.spin_seq.loop()

    def update_color(self, task):
        dt = globalClock.get_dt()
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
        """Update loading progress and message (in Chinese)"""
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
        base.taskMgr.remove("UpdateLoadingRingColor")
        base.taskMgr.remove("ColorCycle")
        base.taskMgr.remove("GrowAndShrink")
        

    def transition_to_next_stage(self):
        """Proceed with loading the next stage."""
        base.flow.transition(self.exit_stage)
        return

    def enter(self, exit_stage=None):
        if hasattr(self, "exit_stage") and exit_stage is not None:
            self.exit_stage = exit_stage
        # Reparent to aspect2d to make it visible and ensure scale/position
        self.ring.reparentTo(base.aspect2d)
        self.ring.setScale(0.1)
        self.ring.setPos(0, 0, 0)

        # Make sure loading text is visible and re-centered
        self.loading_text.reparentTo(base.aspect2d)
        self.loading_text.setText("加载中...")  # Reset the loading text
        self.loading_text.setPos(0, -0.2)

        # Reset and show the progress text
        self.progress_text.reparentTo(base.aspect2d)
        self.progress_text.setText("0%")
        self.progress_text.setPos(0, -0.3)

        # Reset progress and color cycling
        self.current_color = 0
        self.color_time = 0
        self.ring.setColorScale(self.colors[0])  # Start with the first color

        # Restart animations and tasks
        self.setup_animations()
        base.taskMgr.add(self.update_color, "UpdateLoadingRingColor")
        base.taskMgr.add(self.color_cycle, "ColorCycle")
        base.taskMgr.add(self.grow_and_shrink, "GrowAndShrink")
        base.taskMgr.add(self.load_game_resources_task, "LoadGameResourcesTask")

        # Print debug message to confirm loading screen has entered
        print("LoadingScreen: enter() called - Loading screen is now active.")


    def load_game_resources_task(self, task):
        """Load resources in small steps to avoid blocking."""
        texture_files = glob.glob("textures/*.png")
        for i, tex_file in enumerate(texture_files):
            progress = i / len(texture_files) * 0.25
            self.update_progress(progress, f"加载纹理... {tex_file}")  # "Loading textures..."
            yield task.cont  # Ensure the task continues to update the progress

        model_files = glob.glob("models/*.bam")  # Changed from .egg to .bam
        for i, model in enumerate(model_files):
            progress = 0.25 + (i / len(model_files) * 0.25)
            self.update_progress(progress, f"加载模型... {model}")  # "Loading models..."
            yield task.cont  # Ensure the task continues to update the progress

        sound_files = glob.glob("audio/*.wav")  # Assuming you have audio files
        for i, sound in enumerate(sound_files):
            progress = 0.5 + (i / len(sound_files) * 0.25)
            self.update_progress(progress, f"加载声音... {sound}")  # "Loading sounds..."
            yield task.cont  # Continue yielding for sound files

        # Final step: transition when all resources are loaded
        self.update_progress(1, "加载完成...")  # "Loading complete..."
        
        print("Cleanup Complete, Loading Next Stage...")
        return  # End the task to proceed to the next stage



    def exit(self):
        self.cleanup()
        self.transition_to_next_stage(self.lvl) 
        