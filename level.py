from npc import npc
from math import sin
from math import cosh
from random import  choice
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.core import TextNode
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import TextFont
from panda3d.core import NodePath
DEBUG = False
class level():

    def __init__(self):
        self.npcs = []
        self.fonts = [
            base.loader.load_font('fonts/text/Alstoria.otf'),
            base.loader.load_font('fonts/text/Circus.otf'),
            base.loader.load_font('fonts/text/Copic.otf'),
            base.loader.load_font('fonts/text/Dayton.otf'),
            base.loader.load_font('fonts/text/Empire.otf'),
            base.loader.load_font('fonts/text/Festival.otf'),
            base.loader.load_font('fonts/text/Mallika.otf'),
            base.loader.load_font('fonts/text/Storybook.otf'),
            base.loader.load_font('fonts/text/Xenon.otf'),  
        ]
        self.levels = [
            base.loader.loadModel("levels/level00.bam"),
            base.loader.loadModel("levels/level01.bam"),
            base.loader.loadModel("levels/level02.bam"),
            base.loader.loadModel("levels/level03.bam")
        ]
        self.load_world()
        self.load_ground()
        self.clock = 0
        self.clock2 = 0
        base.task_mgr.add(self.update, 'level_update')
         
    def get_npcs(self, num_npcs):
        for n in range(num_npcs):
            new_npc = npc()
            self.npcs.append(new_npc.load_npc())
        
    def place_npcs(self):
        for n, npc in enumerate(self.npc_mounts):
            npcObject = self.npcs[n]
            name = self.npcs[n].get('name')
            face = self.npcs[n].get('face')
            emblem = self.npcs[n].get('emblem')
            name_node = TextNode("npcName_"+str(name))
            name_node.text = str(name)
            name_node.align = 2
            name_node.font = choice(self.fonts)
            npcObject.get('nametag').attach_new_node(name_node)
            #frame.set_pos(npc,(0,0,5))
            npcObject.get('model').attach_new_node(face.get_node(0))
            npcObject.get('model').instance_to(self.npc_mounts[n])
    def load_world(self):
        # World
        self.worldNP = render.attachNewNode('World')
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        self.debugNP.node().showWireframe(DEBUG)
        self.debugNP.node().showConstraints(DEBUG)
        self.debugNP.node().showBoundingBoxes(DEBUG)
        self.debugNP.node().showNormals(DEBUG)

        #self.debugNP.showTightBounds()
        #self.debugNP.showBounds()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81*8))
        self.world.setDebugNode(self.debugNP.node())
        
    def load_ground(self):
        self.ground = choice(self.levels)
        self.npc_mounts = self.ground.findAllMatches("**/npc**")  
        self.floor = self.ground.findAllMatches("**/levelFloor").getPath(0)
        self.walls = self.ground.findAllMatches("**/levelWall").getPath(0)
        self.player_start = self.ground.findAllMatches("**/playerStart").getPath(0)
        #self.wallshader = Shader.load(Shader.SL_GLSL, vertex="shaders/daemon.vert", fragment="shaders/daemon.frag")
        #self.maze02.setShaderInput("iTime", self.clock)
        #self.maze02.setShaderInput("iResolution", (1,1))        
        #self.maze02.setShader(self.wallshader)
        #self.npc00ts = TextureStage('npc00ts')
        #self.npc00marker = self.ground.findAllMatches("**/p1").getPath(0)
        #self.npc00name = self.ground.findAllMatches("**/pName").getPath(0)
        #self.maze02.set_two_sided(True)
        floorCol = self.ground.findAllMatches("**/floorCol").getPath(0).node().getGeom(0)
        wallCol = self.ground.findAllMatches("**/wallCol").getPath(0).node().getGeom(0)
        
        mesh = BulletTriangleMesh()
        mesh2 = BulletTriangleMesh()
        mesh.addGeom(floorCol)
        mesh2.addGeom(wallCol)
        shape = BulletTriangleMeshShape(mesh, dynamic=True)
        shape2 = BulletTriangleMeshShape(mesh2, dynamic=True) 
        body = BulletRigidBodyNode('Floor')
        body2 = BulletRigidBodyNode('Walls')
        bodyNP = self.worldNP.attachNewNode(body)
        bodyNP2 = self.worldNP.attachNewNode(body2)
        bodyNP.node().addShape(shape)
        bodyNP2.node().addShape(shape2)
        bodyNP.node().setRestitution(0.75)
        bodyNP2.node().setRestitution(0.75)
        bodyNP.node().setCollisionResponse(True)
        bodyNP2.node().setCollisionResponse(True)
        bodyNP.setPos(0, 0, 0)
        bodyNP2.setPos(0, 0, 0)
        bodyNP.setCollideMask(BitMask32.allOn())
        bodyNP2.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(bodyNP.node())
        self.world.attachRigidBody(bodyNP2.node())
        bodyNP.show()
        bodyNP2.show()
        self.floor.reparentTo(bodyNP)
        self.walls.reparentTo(bodyNP2)
        self.floorNP = bodyNP
        self.wallsNP = bodyNP2
        self.ground.reparentTo(render)
        
    def update(self, task):
        self.clock += 0.001
        self.clock2 += 0.1
        for stage in self.floor.find_all_texture_stages():
            self.floor.setTexOffset(stage, .5*sin(self.clock/6), .5*sin(self.clock/6))
            self.floor.setTexScale(stage, .05*sin(self.clock)+2.5, .05*sin(self.clock)+2.5, 1)
            
        for stage in self.walls.find_all_texture_stages():
            self.walls.setTexOffset(stage, .5*sin(self.clock/6), .5*sin(self.clock/6))
            self.walls.setTexScale(stage, .5*sin(self.clock)+2.5, .5*sin(self.clock)+2.5,1)
            
        return task.cont