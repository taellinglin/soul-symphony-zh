from random import choice

from panda3d.core import NodePath, TextNode, CullFaceAttrib


class Letters:
    def __init__(self):
        self.letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

        self.fonts = {
            "daemon": base.loader.loadFont("fonts/konnarian/Daemon.otf"),
            "chesilin": base.loader.loadFont("fonts/konnarian/Chesilin.otf"),
            "note": base.loader.loadFont("fonts/konnarian/Note.otf"),
            "music": base.loader.loadFont("fonts/konnarian/Music.otf"),
        }

        self.letter_nodes = []

        for f, font in enumerate(self.fonts):
            for l, letter in enumerate(self.letters):
                self.letter_nodes.append(self.make_letter(font, letter))

    def enter(self):
        base.taskMgr.add(self.update, "letter_update")

    def make_letter(self, font=None, letter=None):
        # Create a TextNode

        textnode = TextNode("letter_" + str(letter))

        textnode.setText(letter)

        textnode.setTextScale(4)

        textnode.setAlign(TextNode.A_center)

        # Set the font

        if font is None:
            textnode.setFont(choice(list(self.fonts.values())))

        else:
            if self.fonts.get(font):
                textnode.setFont(self.fonts.get(font))

        # Create a NodePath from TextNode

        letter_node = NodePath(textnode)

        letter_node.setAntialias(False)

        # Ensure two-sided rendering

        letter_node.setTwoSided(True)

        # Disable backface culling

        letter_node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))

        # Reparent it to the render tree (scene graph)

        letter_node.reparentTo(render)

        return letter_node

    def update(self, task):
        return task.cont
