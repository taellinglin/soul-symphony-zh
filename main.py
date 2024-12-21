from direct.showbase.ShowBase import ShowBase
from stageflow import Flow
from screenrec import ScreenRecorder
from gamepadInput import GamepadInput
from bgm import BGM
from scoreboard import scoreboard
from titleScreen import TitleScreen
from loadingScreen import LoadingScreen
from worldcage import WorldCage
from panda3d.core import WindowProperties, PerspectiveLens
import os
from stageflow import Stage
from panda3d.core import Vec4
import functools
from panda3d.core import NodePath
from pyrecord import setup_sg
from panda3d.core import Lens
from motionBlur import MotionBlur
from splashscreen import SplashScreen

class Quit:
    def enter(self, data=None):
        self.userExit()
    def exit(self, data=None):
        return data

class Base(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.lvl = 0
        self.motion_blur = None
        # Set up fullscreen immediately after ShowBase init
        self.setup_fullscreen()
        # Initialize essential systems for splash/title
        self.screen_recorder = ScreenRecorder(self)
        setup_sg(self)
        self.gamepad_input = GamepadInput()
        self.bgm = BGM()
        self.disable_mouse()
        
        # Bind F11 to take a screenshot
        self.accept("f11", self.screen_recorder.take_screenshot)

        # Bind F12 to start/stop screen recording
        self.accept("f12", self.toggle_recording)
        
        # Load fonts needed for scoreboard
        self.load_scoreboard_fonts()

        # Initialize scoreboard
        self.scoreboard = scoreboard()
        self.scoreboard.hide()
        # Initialize flow with only splash and quit stages
        self.flow = Flow(
            stages={
                "splash": SplashScreen(exit_stage="title_screen"),
                "title_screen": TitleScreen(exit_stage="loading"),
                "loading": LoadingScreen(exit_stage="worldcage"),
                "worldcage": WorldCage(exit_stage="quit", lvl=self.lvl),
                "quit": Quit()
            },
            initial_stage="splash"
        )

        # Store stage classes for lazy loading
        self.stage_classes = {
        }

        # Define available levels
        self.levels = [
            "arcade/stage1.bam",
            "levels/level00.bam",
            "levels/level01.bam",
            "levels/level02.bam",
            "levels/level03.bam",
            "levels/maze02.bam"
        ]

    def setup_fullscreen(self):
        """Set up fullscreen at native resolution"""
        props = WindowProperties()
        props.setFullscreen(True)

        # Get the display information
        di = self.pipe.getDisplayInformation()

        # Get the native resolution of the primary display
        width = di.getDisplayModeWidth(0)
        height = di.getDisplayModeHeight(0)

        # Set the window size to match the display
        props.setSize(width, height)

        # Request the properties
        self.win.requestProperties(props)

        print(f"Setting fullscreen resolution to {width}x{height}")

    def load_scoreboard_fonts(self):
        """Load fonts needed for scoreboard"""
        self.fonts = []
        font_dir = "fonts/text"

        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith(('.ttf', '.otf')):
                    font_path = os.path.join(font_dir, font_file)
                    print(f"Loading font: {font_file}")
                    self.fonts.append(self.loader.loadFont(font_path))




    def print_node_tree(self, node: NodePath, indent=""):
        # Print the name of the current node
        print(indent + node.get_name())
        
        # Recursively print child nodes
        for child in node.get_children():
            #self.print_node_tree(child, indent + "  ")
            pass
            
    def print_running_tasks(self):
        tasks = taskMgr.getTasks()
        if not tasks:
            print("No tasks are currently running.")
        else:
            print(f"Currently running tasks ({len(tasks)}):")
            for task in tasks:
                print(f"Task {task.name} (ID: {task.id})")
    def print_system_status(self):
        print("\n=== Node Tree ===")
        self.print_node_tree(base.render)
        
        print("\n=== Currently Running Tasks ===")
        self.print_running_tasks()
        
    def toggle_recording(self):
        """Toggle screen recording on or off."""
        if self.screen_recorder.recording:
            self.screen_recorder.stop_recording()
        else:
            self.screen_recorder.start_recording()

    # The main part of the application
    def set_aspect_ratio(self,resolution):
        width, height = resolution
        aspect_ratio = width / height

        # Set the window size
        wp = WindowProperties()
        wp.setSize(width, height)
        base.win.requestProperties(wp)

        # Adjust the camera lens
        lens = PerspectiveLens()
        lens.setAspectRatio(aspect_ratio)
        base.cam.node().setLens(lens)

    # Example: Setting 16:9 or 4:3 aspect ratios
    def adjust_aspect_ratio_based_on_resolution(self):
        # Get the current resolution
        resolution = base.win.getSize()

        if resolution[0] / resolution[1] == 16 / 9:
            print("Setting 16:9 aspect ratio")
            self.set_aspect_ratio((1920, 1080))  # Example for 16:9
        elif resolution[0] / resolution[1] == 4 / 3:
            print("Setting 4:3 aspect ratio")
            self.set_aspect_ratio((1024, 768))  # Example for 4:3
        else:
            print("Setting default aspect ratio")
            self.set_aspect_ratio(resolution)  # Maintain the current resolution aspect ratio

    # Call this function at the start or on resolution change
    
if __name__ == "__main__":
    app = Base()
    #app.adjust_aspect_ratio_based_on_resolution()  # Call this early to set the right aspect ratio
    
    # Set the camera lens' aspect ratio
    lens = base.cam.node().getLens()
    window_width, window_height = base.win.get_size()
    #lens.setAspectRatio(window_width / float(window_height))

    # Apply the aspect ratio settings to the camera
    #base.cam.node().setLens(lens)
    app.camLens.setFov(70)

    # Continue with window properties and fullscreen setup
    pipe = app.win.getPipe()
    native_width = pipe.getDisplayWidth()
    native_height = pipe.getDisplayHeight()

    wp = WindowProperties()
    wp.setSize(native_width, native_height)  # Set to native screen resolution
    wp.setFullscreen(True)
    app.win.requestProperties(wp)

    app.run()


