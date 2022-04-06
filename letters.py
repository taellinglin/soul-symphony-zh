from random import  choice
from panda3d.core import TextFont
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import TextProperties

class letters():
    def __init__(self):
        self.letters = ['a',
                        'b',
                        'c',
                        'd',
                        'e',
                        'f',
                        'g',
                        'h',
                        'i',
                        'j',
                        'k',
                        'l',
                        'm',
                        'n',
                        'o',
                        'p',
                        'q',
                        'r',
                        's',
                        't',
                        'u',
                        'v',
                        'w',
                        'x',
                        'y',
                        'z'
                        ]
        self.fonts = {
            'daemon': base.loader.load_font('fonts/konnarian/Daemon.otf'),
            'chesilin': base.loader.load_font('fonts/konnarian/Chesilin.otf'),
            #'crossbats': base.loader.load_font('fonts/symbols/crossbats.otf')    
        }
        self.letter_nodes = []
        
        for f, font in enumerate(self.fonts):
            
            for l, letter in enumerate(self.letters):
                self.letter_nodes.append(self.make_letter(font, letter))
                
                                         
    def enter(self):
        base.taskMgr.add(self.update, 'letter_update')
        
    def make_letter(self, font = None, letter = None):
        #font.setPixelsPerUnit(1024)
        textnode = TextNode('letter'+str(letter))
        textnode.text = letter
        textnode.setGlyphScale(6)
        textnode.setAlign(2)
        if font == None:
            textnode.font = choice(self.fonts)
            textnode.font.set_render_mode(TextFont.RMTexture)
            #textnode.font.setPageSize(1024, 1024)
            #textnode.font.setPixelsPerUnit(1024)
        else:
            if self.fonts.get(font):
                textnode.font = self.fonts.get(font)
                textnode.font.set_render_mode(TextFont.RMTexture)
                #textnode.font.setPageSize(1024, 1024)
                #textnode.font.setPixelsPerUnit(1024)
                
        return textnode
        
    def update(self, task):
        return task.cont