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
from panda3d.core import Lens
from splashscreen import SplashScreen
import random

class Quit:
    def enter(self, data=None):
        self.userExit()
    def exit(self, data=None):
        return data

class Base(ShowBase):
    def __init__(self):
        super().__init__(self)
        
        # Set up fullscreen immediately after ShowBase init
        self.setup_fullscreen()
        # Initialize essential systems for splash/title
        self.screen_recorder = ScreenRecorder(self)
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



        # Store stage classes for lazy loading

        # Define available levels
        self.levels = [
            "levels/level00.bam",
            "levels/level01.bam",
            "levels/level02.bam",
            "levels/level03.bam",
            "levels/level04.bam",
            "levels/level05.bam",
        ]
        self.lvl = random.randint(0, len(self.levels) -1)

        self.flow = Flow(
            stages={
                "splash": SplashScreen(exit_stage="titlescreen"),
                "title_screen": TitleScreen,
                "loading": LoadingScreen,
                "worldcage": WorldCage(exit_stage="quit", lvl=self.lvl),
                "quit": Quit,
            },
            initial_stage="splash"
        )
        
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
        
    def get_fonts(self, folder_path):
        """Load fonts from the specified folder."""

        font_files = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".ttf"):
                    relative_path = os.path.join(root, file)

                    font_files.append(loader.load_font(relative_path))

                    print("Loaded: " + relative_path)

        return font_files

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
      # Call this early to set the right aspect ratio
    
    # Set the camera lens' aspect ratio
    lens = base.cam.node().getLens()

    

    # Continue with window properties and fullscreen setup
    pipe = app.win.getPipe()
    native_width = pipe.getDisplayWidth()
    native_height = pipe.getDisplayHeight()
    lens = PerspectiveLens()
    lens.setAspectRatio(16/9)
    base.cam.node().setLens(lens)


    wp = WindowProperties()
    wp.setFullscreen(True)
    print(f"native width:{native_width}")
    print(f"native width:{native_height}")
    wp.setSize(native_width, native_height)  # Set to native screen resolution
    
    app.win.requestProperties(wp)

    app.run()

