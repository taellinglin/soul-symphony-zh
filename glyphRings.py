import math
from panda3d.core import TextFont
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from random import randint, choice


class GlyphRings():
    def __init__(self, font, number_of_rings=16, characters_in_ring=16):
        self.font = font
        self.font.set_render_mode(TextFont.RMSolid)

        self.rings = []
        self.center = NodePath('center')
        for r in range(number_of_rings):
            ring = self.center.attach_new_node('ring_'+str(r))
            for c in range(characters_in_ring):
                ring.set_h(ring, 360/characters_in_ring)
                glyph_text = TextNode('glyph_'+str(c))
                glyph_text.font = self.font
                glyph_text.setFlattenFlags(1)
                glyph_text.text = choice('abcdefghijklmnopqrstuvwxyz')
                glyph_node = render.attach_new_node(glyph_text)
                glyph_node.set_y(math.pi)
                glyph_node.set_sy(0.05)
                glyph_node.set_p(90) # Flip up
                glyph_node.set_two_sided(1)
                glyph_node.set_r(90*randint(0,4))
                glyph_node.wrt_reparent_to(ring)
                glyph_node.setRenderMode(TextFont.RMSolid, 2.0)
            ring.set_scale(16-r)
            self.rings.append(ring)
        self.center.reparent_to(render)

        self.colors = [(1,0,0,1), (0,1,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
        self.ring_speed = 1
        self.char_speed = 0.01


    def update(self, dt):
        self.clock = dt
        for r, ring in enumerate(self.rings):
            ring.set_h(ring, self.ring_speed*r*dt)
            ring.set_p(ring, self.ring_speed*r*dt)
            for c, char in enumerate(ring.get_children()):
                char.set_h(ring,dt*self.char_speed*c)
                char.set_r(ring, self.char_speed*r*dt)
                char.set_color(choice(self.colors))
