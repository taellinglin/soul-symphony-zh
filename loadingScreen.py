
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import Task
from panda3d.core import CardMaker, TextNode



    
class LoadingScreen:
    def __init__(self, exit_stage="worldcage"):
        self.exit_stage = exit_stage
        self.progress = 0
        self.preload_steps = 0

    def enter(self, data, flow):
        """Called when this stage is entered"""
        self.flow = flow

        # Create black background
        cm = CardMaker("background")
        cm.setFrameFullscreenQuad()
        self.background = render2d.attachNewNode(cm.generate())
        self.background.setColor(0, 0, 0, 1)

        # Create loading text
        self.loading_text = OnscreenText(
            text="Loading...",
            pos=(0, 0),
            scale=0.1,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
        )

        # Start the preload task
        base.taskMgr.add(self.preload_assets, "preload-assets")

    def exit(self, data):
        """Called when this stage is exited"""
        self.cleanup()

    def cleanup(self):
        """Remove all nodes and cleanup"""
        if hasattr(self, "background"):
            self.background.removeNode()
        if hasattr(self, "loading_text"):
            self.loading_text.destroy()

    def update_progress(self, value):
        """Update the loading progress"""
        self.progress = value
        if hasattr(self, "loading_text"):
            self.loading_text.setText(f"Loading... {value}%")

    def preload_assets(self, task):
        """Preload game assets"""
        try:
            if self.preload_steps == 0:
                # Initialize basic resources
                self.update_progress(25)
            elif self.preload_steps == 1:
                # Load models
                self.update_progress(50)
            elif self.preload_steps == 2:
                # Load sounds
                self.update_progress(75)
            elif self.preload_steps == 3:
                # Final setup
                self.update_progress(100)
                # Transition to next stage
                self.flow.transition(self.exit_stage)
                return Task.done

            self.preload_steps += 1
            return Task.cont

        except Exception as e:
            print(f"Error in preload_assets: {e}")
            return Task.done