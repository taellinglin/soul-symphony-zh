from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from screenrec import ScreenRecorder  # Import the ScreenRecorder class
from gamepadInput import GamepadInput
from bgm import BGM
from motionBlur import MotionBlur
from titleScreen import TitleScreen
from intro import Intro
from intro2 import Intro2
from intro3 import Intro3
from stageflow import Flow
from stageflow.panda3d import Panda3DSplash
from letterMatching import LetterMatching
from scoreboard import scoreboard
from room00 import room00
from stageflow.prefab import Quit
import os
import time  # Ensure you import time for timing the recording

class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.screen_recorder = ScreenRecorder(self)  # Create the screen recorder instance
        self.gamepad_input = GamepadInput()
        self.bgm = BGM()
        self.motion_blur = MotionBlur()
        self.disable_mouse()
        self.scoreboard = scoreboard()
        self.scoreboard.hide()
        self.fonts = self.get_fonts("fonts/text/")
        self.levels = ['room00', 'room01', 'room02', 'room03']

        # Setup stage flow
        self.flow = Flow(
            stages=dict(
                splash=Panda3DSplash(exit_stage='title_screen'),
                title_screen=TitleScreen(exit_stage='room00'),
                intro=Intro(exit_stage='intro2'),
                intro2=Intro2(exit_stage='intro3'),
                intro3=Intro3(exit_stage='lettermatching'),
                letter_matching=LetterMatching(exit_stage='room00'),
                room00=room00(exit_stage='quit', lvl=0),
                room01=room00(exit_stage='quit', lvl=1),
                room02=room00(exit_stage='quit', lvl=2),
                room03=room00(exit_stage='quit', lvl=3),
                quit=Quit()
            ),
            initial_stage='title_screen',
        )

        self.setup_input_events()

    def setup_input_events(self):
        """Bind input events for screenshots and recording."""
        self.accept('f11', self.handle_select_press)  # Screenshot on 'F11'
        self.accept('f12', self.handle_select_hold)   # Toggle recording on 'F12'

    def handle_select_press(self):
        """Handle single press of 'F11' for taking a screenshot."""
        print("F11 pressed (screenshot).")
        if not self.screen_recorder.recording:
            self.screen_recorder.take_screenshot()

    def handle_select_hold(self):
        """Handle holding 'F12' for toggling video recording."""
        print("F12 held (toggle recording).")
        if not self.screen_recorder.recording:
            self.screen_recorder.start_recording()
        else:
            elapsed = time.time() - self.screen_recorder.record_start_time if self.screen_recorder.record_start_time else 0
            if elapsed >= 3:
                self.screen_recorder.stop_recording()

    def get_fonts(self, folder_path):
        """Load fonts from the specified folder."""
        font_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.ttf'):
                    relative_path = os.path.join(root, file)
                    font_files.append(loader.load_font(relative_path))
                    print("Loaded: " + relative_path)
        return font_files


# Initialize the game
base = Base()

# Set up window properties
wp = WindowProperties()
wp.setFullscreen(1)
wp.setSize(1920, 1080)
base.openMainWindow()
base.win.requestProperties(wp)

# Run the game
base.run()
