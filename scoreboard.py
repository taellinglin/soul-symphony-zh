from panda3d.core import TextNode, AntialiasAttrib, Filename
import os
import random


class scoreboard:
    def __init__(self):
        self.score = 0
        self.score_text = TextNode("Scoreboard")
        self.score_text.text = "得分： " + str(self.score)
        self.score_text.setAlign(TextNode.ACenter)
        self.score_text.setTextScale(0.1)

        # Load all fonts from "fonts/text"
        self.fonts = self.load_fonts("fonts/text")
        if not self.fonts:
            print("Warning: No fonts found in 'fonts/text'. Using default font.")
            default_font = base.loader.loadFont("fonts/konnarian/Daemon.otf")
            if default_font:
                self.fonts = [default_font]
            else:
                print("Error: Default font 'Daemon.otf' not found.")

        print("Loaded fonts:", [font.getName() for font in self.fonts])

        self.score_node = aspect2d.attachNewNode(self.score_text)
        self.score_node.setAntialias(AntialiasAttrib.MNone)

        # Position the scoreboard at the top-right of the screen
        self.update_position()

    def load_fonts(self, directory):
        """Dynamically load all font files from the specified directory."""
        fonts = []
        directory_path = Filename.fromOsSpecific(directory).toOsSpecific()
        if os.path.exists(directory_path):
            for file in os.listdir(directory_path):
                if file.lower().endswith(('.ttf', '.otf')):
                    font_path = os.path.join(directory_path, file)
                    font = base.loader.loadFont(font_path)
                    if font:
                        fonts.append(font)
                    else:
                        print(f"Failed to load font: {font_path}")
        else:
            print(f"Font directory not found: {directory}")
        return fonts

    def update_position(self):
        """Position the scoreboard node in the top-right corner."""
        win_width = base.win.getXSize()
        win_height = base.win.getYSize()
        x_pos = 0.95  # Relative position for top-right corner
        y_pos = 0.90
        self.score_node.setPos(aspect2d, x_pos * win_width, 0, y_pos * win_height)

    def enter(self):
        base.taskMgr.add(self.update, "scoreboard_update")

    def addPoints(self, points):
        """Add points and update the scoreboard text."""
        self.score_text.setFont(random.choice(self.fonts))  # Randomize font
        self.score += points
        self.updateBoard()

    def getPoints(self):
        return self.score

    def show(self):
        if self.score_node.isHidden():
            self.score_node.show()

    def hide(self):
        if not self.score_node.isHidden():
            self.score_node.hide()

    def updateBoard(self):
        self.score_text.text = "得分： " + str(self.score)

    def reset(self):
        """Reset the scoreboard."""
        self.score = 0
        self.updateBoard()

    def update(self, task):
        return task.cont
