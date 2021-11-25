from math import pi
from math import sin
from math import cos
import sys

from direct.showbase.PythonUtil import randFloat
from stageflow.core import Stage
from random import  choice
from random import  randint
from stageflow import Stage
from level import level
from player import player
from npc import npc
from dialog import dialog


from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import InputDevice
from panda3d.core import TextureStage
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.core import TextNode
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBodyNode

from direct.showbase.InputStateGlobal import inputState
class room00(Stage):
    def __init__(self, exit_stage = "main_menu", lvl = None):
        if lvl == None:
            self.lvl = 0
        else:
            self.lvl = lvl
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,0,1,1), (1,1,0,1), (1,0,1,1)]
        self.colors = []
        phase_frags = 6
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((cos(phase), 1, 0, 1))
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((0, 1, sin(phase), 1))
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((0, cos(phase), 1, 1))
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((sin(phase), 0, 1, 1))
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((1, 0, cos(phase), 1))
        for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
            self.colors.append((1, sin(phase), 0, 1))
        self.color_idx = -1
        self.clock = 0
        self.npcs =[]
        base.disableMouse()

        
    def enter(self, lvl = None):
        if lvl == None:
            lvl = self.lvl
        self.lvl = lvl
        print("Roll Test Area Entered...")
        base.cam.set_z(24)
        base.bgm.playMusic(None, True, 0.25)
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')
        inputState.watchWithModifiers('jump', 'gamepad-face_a')
        inputState.watchWithModifiers('jump', 'space')
        inputState.watchWithModifiers('cam-right', ']')
        inputState.watchWithModifiers('cam-left', '[')
        inputState.watchWithModifiers('cam-right', 'gamepad-trigger_right')
        inputState.watchWithModifiers('cam-left', 'gamepad-trigger_left')
        
        print("level: "+str(self.lvl))
        self.level = level(self.lvl)
        self.level.get_npcs(21)
        self.level.place_npcs()
        self.player = player()
        self.player.ballNP.reparentTo(self.level.worldNP)
        self.level.world.attachRigidBody(self.player.ballNP.node())
        self.player.ballNP.setPos(choice(self.level.portals).getPos()+(0,0,3))
        self.dialog = dialog()
        self.dialog_card = TextNode('dialog_card')
        self.dialog_card.align = 2
        self.dialog_card.setWordwrap(40)
        self.dialog_card_node = aspect2d.attach_new_node(self.dialog_card)
        self.dialog_card_node.setScale(0.08)

        self.level.audio.audio3d.attachListener(base.cam)

        base.accept("gamepad-face_a", self.actionA)
        base.accept("space", self.actionA)
        base.accept("gamepad-face_a-up", self.actionAUp)
        base.accept("space-up", self.actionAUp)
        base.accept("gamepad-face_b", self.actionB)
        base.accept("shift", self.actionB)
        base.accept("gamepad-face_b-up", self.actionBUp)
        base.accept("shift-up", self.actionBUp)
        
        

        
    def actionA(self):
        result = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.floorNP.node())
        if result.getNumContacts() > 0:
                contact = result.getContacts()[0]
                if contact.getNode1() == self.level.floorNP.node():
                    self.player.ballNP.node().applyCentralImpulse(Vec3(0,0,128+32))
                    base.bgm.playSfx('ball-jump')
                    if len(self.level.npc_mounts):
                        for n, npc_mount in enumerate(self.level.npc_mounts):
                            if((npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                                self.dialog_card.text = self.level.npcs[n].get('dialog')
                                self.dialog_card_node.show()
                                base.bgm.playSfx('start-dialog')
                                self.player.force = Vec3(0,0,0)
                                self.player.torque = Vec3(0,0,0)
                                self.player.ballNP.node().setLinearDamping(1)
                    if len(self.level.portals):
                        for p, portal in enumerate(self.level.portals):
                            if((portal.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                                self.dialog_card.text = choice(["Let's Trip!", "C'mon now!", "Yeah! Onward!", "We're out!", "Abscond!", "Let's get Lost!", "Sayonara!", "Nigeru!", "Outta here!"])
                                self.dialog_card_node.show()
                                self.player.force = Vec3(0,0,0)
                                self.player.torque = Vec3(0,0,0)
                                self.player.ballNP.node().setLinearDamping(1)
                    
                    

    def actionAUp(self):
        if(self.player.ballNP.node().getLinearDamping() == 1):
            self.player.ballNP.node().setLinearDamping(0)
        self.dialog_card_node.hide()
        for p, portal in enumerate(self.level.portals):
            if((portal.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                self.dialog_card.text = choice(["Ok!", "Alright!", "Affirmative!", "Totally!"])
                self.dialog_card_node.hide()
                base.bgm.stopSfx()
                base.bgm.playSfx('warp')
                self.transition(choice(base.levels))
                return
        
    def actionB(self):
        self.player.ballNP.node().setAngularDamping(0.82)
        self.player.ballNP.node().setLinearDamping(0.82)
         
    def actionBUp(self):
        self.player.ballNP.node().setAngularDamping(0)
        self.player.ballNP.node().setLinearDamping(0)
        

    def processInput(self, dt):
        force = Vec3(0,0,0)
        torque = Vec3(0,0,0)
        if(not base.gamepad_input.gamepad == None):
            self.left_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_x)
            self.left_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_y)
            self.right_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_x)
            self.right_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_y)
            self.leftAnalog = Vec3(self.left_x.value, self.left_y.value, 0)
            force = self.leftAnalog
            torque = Vec3(0,0,self.right_x.value)
        if inputState.isSet('cam-right'): base.cam.set_r(self.ballNP, 0.5)
        if inputState.isSet('cam-left'): base.cam.set_r(self.ballNP, -0.5)        
        if inputState.isSet('forward'): force.setY( 1.0)
        if inputState.isSet('reverse'): force.setY(-1.0)
        if inputState.isSet('left'):    force.setX(-1.0)
        if inputState.isSet('right'):   force.setX( 1.0)
        if inputState.isSet('turnLeft'):  torque.setZ( 1.0)
        if inputState.isSet('turnRight'): torque.setZ(-1.0)

        force *= 100.0
        torque *= 100.0
        
        #force = self.ballNP.getRelativeVector(Vec3(base.cam.get_h(), base, 0), force)
        #torque = base.cam.getRelativeVector(self.ballNP, torque)

        self.player.ballNP.node().setActive(True)
        self.player.ballNP.node().applyCentralForce(force)
        self.player.ballNP.node().applyTorque(torque)


        
    def update(self, task):
        self.level.audio.audio3d.setListenerVelocity(self.player.ballNP.get_node(0).getLinearVelocity())
        self.color_idx = (self.color_idx + 1) % len(self.colors)
        self.player.ball_roll.setPlayRate(0.05*(abs(self.player.ballNP.get_node(0).getLinearVelocity().getX())+abs(self.player.ballNP.get_node(0).getLinearVelocity().getY())+abs(self.player.ballNP.get_node(0).getLinearVelocity().getZ())))
        for n, npc_mount in enumerate(self.level.npc_mounts):
            nametag = npc_mount.find('**/npcNametag')
            if((npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                if nametag.isHidden():
                    nametag.show()
                    base.bgm.playSfx('hover')
                pass
                #PLAY THE SFX ONCE...
            else:
                nametag.hide()
                
        result = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.floorNP.node())
        result2 = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.wallsNP.node())
        if result.getNumContacts() > 0:
            contact = result.getContacts()[0]
            if contact.getNode1() == self.level.floorNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact.getManifoldPoint()
                    volume =  abs(mpoint.getDistance())
                    pitch = volume
                    base.bgm.playSfx(choice(self.player.boings), volume, 1)
        else:
            self.player.boing = False
        
        if result2.getNumContacts() > 0:
            contact2 = result2.getContacts()[0]
            if contact2.getNode1() == self.level.wallsNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact2.getManifoldPoint()
                    volume =  abs(mpoint.getDistance())
                    pitch = volume
                    base.bgm.playSfx(choice(self.player.boings), volume, 1)
        else:
            self.player.boing = False
        for p, portal in enumerate(self.level.portals):
            portal.set_h(portal, 3)
            portal.set_scale(0.8,0.8,abs(2*sin(self.clock*60)))
            portal.set_color(self.colors[self.color_idx])
            
        self.player.ballNP.set_color(choice(self.colors))
        for l, letter in enumerate(render.findAllMatches('**/letter**')):
            letter.set_h(letter, 1)
            letter.set_color(choice(self.colors))
            if((letter.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 3):
                base.bgm.playSfx('pickup', 1, randFloat(0.25, 8), False)
                letter.detachNode()
                letter.removeNode()
                print("Score + 1!")
        
        for o, obj in enumerate(self.level.ground.get_children()):
                obj.set_color(self.colors[self.color_idx])
        for o, obj in enumerate(self.level.floor.get_children()):
                obj.set_color(self.colors[self.color_idx])
        for o, obj in enumerate(self.level.walls.get_children()):
                obj.set_color(self.colors[self.color_idx])
        for o, obj in enumerate(self.level.ceil.get_children()):
            obj.set_color(self.colors[self.color_idx])      
        self.clock += 1
        dt = globalClock.getDt()
        self.processInput(dt)
        #print(self.level.groundNP.node().checkCollisionWith(self.level.ballNP.node()))
        base.cam.set_x(self.player.ballNP.get_x())
        base.cam.set_y(self.player.ballNP.get_y() - 48)
        base.cam.set_z(self.player.ballNP.get_z() + 16)
        base.cam.look_at(self.player.ballNP)
        
        self.level.world.doPhysics(dt, 25, 2.0/360.0)
        return task.cont
    
    def transition(self, exit_stage, lvl = None):
        if exit_stage == None:
            self.exit_stage = 'main_menu'
        else:
            self.exit_stage = exit_stage    
        base.flow.transition(self.exit_stage)
        
    def exit(self, data):
        self.player.ball_roll.stop()
        self.level.world.removeRigidBody(self.level.floorNP.node())
        self.level.world.removeRigidBody(self.level.wallsNP.node())
        
        self.level.world.removeRigidBody(self.player.ballNP.node())
        #self.level.world = None
        self.level.audio.stopLoopingAudio()
        #self.debugNP = None
        self.level.debugNP.detachNode()
        self.level.debugNP.removeNode()
        self.level.groundNP = None
        #self.player.ballNP = None
        self.player.ballNP.detachNode()
        self.player.ballNP.removeNode()
        for n, npc in enumerate(self.level.npc_mounts):
            npc.detachNode()
            npc.removeNode()
        for p, portal in enumerate(self.level.portals):
            portal.detachNode()
            portal.removeNode()
        self.level.worldNP.removeNode()
        base.ignore('enter')
        base.ignore("gamepad-face_a")
        base.ignore("space")
        base.ignore("gamepad-face_a-up")
        base.ignore("space-up")
        base.ignore("gamepad-face_b")
        base.ignore("shift")
        base.ignore("gamepad-face_b-up")
        base.ignore("shift-up")
        
        #self.ball.detachNode()
        base.bgm.stopMusic()
        base.cam.set_z(1)
        base.cam.set_x(0)
        base.cam.set_y(0)
        base.cam.set_hpr(0,0,0)
        base.taskMgr.remove('update')
        for n, node in enumerate(aspect2d.get_children()):
            node.detachNode()
            node.removeNode()
        return data