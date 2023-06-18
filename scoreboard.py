from panda3d.core import TextNode
from panda3d.core import AntialiasAttrib
from random import choice
import os

class scoreboard():
    def __init__(self):
        self.score = 0
        self.fonts = base.get_fonts("fonts/text")
        self.score_text = TextNode("Scoreboard")
        self.score_text.text = "Score: "+str(self.score)
        self.score_text.setAlign(1)
        self.score_text.setTextScale(0.1)
        self.score_text.font = choice(self.fonts)
        self.score_node = aspect2d.attachNewNode(self.score_text)
        self.score_node.setPos(aspect2d, (0.9,0,0.9))
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
        self.score_text.text = "Score: "+str(self.score)
    
    def reset(self):
        if not len([aspect2d.find('Scoreboard')]):
            self.score_text = TextNode("Scoreboard")
            self.score_text.text = "Score: "+str(self.score)
            self.score_text.setAlign(1)
            self.score_text.setTextScale(0.1)
            self.score_text.font = base.loader.load_font('fonts/konnarian/Daemon.otf')
            self.score_node = aspect2d.attachNewNode(self.score_text)
            self.score_node.setPos(aspect2d, (0.9,0,0.9))
            self.score_node.setAntialias(AntialiasAttrib.MNone)
            
    def update(self, task):
        return task.cont