from random import  choice
from panda3d.core import TextFont
from panda3d.core import NodePath
from panda3d.core import TextNode
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
            'sama': base.loader.load_font('fonts/terrestrial/Sama.otf'),
            'crossbats': base.loader.load_font('fonts/symbols/crossbats.otf')    
        }
        self.letter_nodes = []
        for f, font in enumerate(self.fonts):
            for l, letter in enumerate(self.letters):
                self.letter_nodes.append(self.make_letter(font, letter))
                
                                         
    def enter(self):
        base.taskMgr.add(self.update, 'letter_update')
        
    def make_letter(self, font = None, letter = None):
        textnode = TextNode('letter'+str(letter))
        textnode.text = letter
        textnode.setAlign(2)
        if font == None:
            textnode.font = choice(self.fonts)
        else:
            if self.fonts.get(font):
                textnode.font = self.fonts.get(font)
        return textnode
        
    def update(self, task):
        return task.cont