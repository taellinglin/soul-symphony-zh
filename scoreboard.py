from panda3d.core import TextNode

from panda3d.core import AntialiasAttrib

from random import choice

import os



class scoreboard():

    def __init__(self):

        self.score = 0

        self.fonts = base.get_fonts("fonts/text")

        self.score_text = TextNode("Scoreboard")

        self.score_text.text = "得分： "+str(self.score)

        self.score_text.setAlign(1)

        self.score_text.setTextScale(0.1)

        self.score_text.font = choice(self.fonts)

        self.score_node = aspect2d.attachNewNode(self.score_text)

        # Get the window size (resolution)

        win_width = base.win.getXSize()

        win_height = base.win.getYSize()



        # Calculate top-right position, and then move a bit down (e.g., 50 pixels)

        x_pos = win_width * 0.98  # 90% from the left (right edge)

        y_pos = win_height * 0.94  # 90% from the top (top edge)



        # Set the position of the score_node in screen coordinates (relative to aspect2d)

        # The y_pos value is adjusted down by a small amount (e.g., 50 pixels)

        self.score_node.setPos(aspect2d, x_pos / win_width, 0, (y_pos - 50) / win_height)



        self.score_node.setAntialias(AntialiasAttrib.MNone)

    

    def enter(self):

        base.taskMgr.add(self.update, 'scoreboard_update')

        

    def addPoints(self, points):

        #Randomize the font every letter you get! Comment out to disable.

        self.score_text.font = choice(self.fonts)

        self.score += points

        self.updateBoard()

    

    def getPoints(self):

        return self.score

    

    def show(self):

        if self.score_node.isHidden():

            self.score_node.show()

            

    def hide(self):

        if  not self.score_node.isHidden():

            self.score_node.hide()

            

    def updateBoard(self):

        self.score_text.text = "得分： "+str(self.score)

    

    def reset(self):

        if not len([aspect2d.find('Scoreboard')]):

            self.score_text = TextNode("Scoreboard")

            self.score_text.text = "得分： "+str(self.score)

            self.score_text.setAlign(1)

            self.score_text.setTextScale(0.1)

            self.score_text.font = base.loader.load_font('fonts/konnarian/Daemon.otf')

            self.score_node = aspect2d.attachNewNode(self.score_text)

            #self.score_node.setPos(aspect2d, (0.9,0,0.9))

            self.score_node.setAntialias(AntialiasAttrib.MNone)

            

    def update(self, task):

        return task.cont