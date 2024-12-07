from panda3d.core import WindowProperties

from direct.showbase.ShowBase import ShowBase

from screenrec import ScreenRecorder  # Import the ScreenRecorder class

from gamepadInput import GamepadInput

from bgm import BGM

from titleScreen import TitleScreen

from stageflow import Flow

from stageflow.panda3d import Panda3DSplash


from scoreboard import scoreboard

from worldcage import WorldCage

from stageflow.prefab import Quit

import os

import time  # Ensure you import time for timing the recording

from panda3d.core import GraphicsPipe


# Now you can use native_width and native_height


class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.screen_recorder = ScreenRecorder(
            self
        )  # Create the screen recorder instance

        self.gamepad_input = GamepadInput()

        self.bgm = BGM()

        # self.motion_blur = MotionBlur()

        self.disable_mouse()

        self.scoreboard = scoreboard()

        self.scoreboard.hide()

        self.fonts = self.get_fonts("fonts/text/")

        self.levels = ["worldcage"]

        # Setup stage flow

        self.flow = Flow(
            stages=dict(
                splash=Panda3DSplash(exit_stage="title_screen"),
                title_screen=TitleScreen(exit_stage="worldcage"),
                worldcage=WorldCage(exit_stage="quit", lvl=0),
                quit=Quit(),
            ),
            initial_stage="title_screen",
        )

        self.setup_input_events()

    def setup_input_events(self):
        """Bind input events for screenshots and recording."""

        self.accept("f11", self.handle_select_press)  # Screenshot on 'F11'

        self.accept("f12", self.handle_select_hold)  # Toggle recording on 'F12'

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
            elapsed = (
                time.time() - self.screen_recorder.record_start_time
                if self.screen_recorder.record_start_time
                else 0
            )

            if elapsed >= 3:
                self.screen_recorder.stop_recording()

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


# Run the game


def main():
    base = Base()

    # Get the default graphics pipe

    pipe = base.win.getPipe()

    # Get the native resolution of the screen

    native_width = pipe.getDisplayWidth()

    native_height = pipe.getDisplayHeight()

    print(native_height)

    print(native_width)

    # Set up window properties

    wp = WindowProperties()

    wp.setFullscreen(1)

    wp.setSize(native_width, native_height)  # Set to native screen resolution

    base.openMainWindow()

    base.win.requestProperties(wp)
    base.run()


if __name__ == "__main__":
    main()
