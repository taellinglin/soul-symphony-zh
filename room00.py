import sys
from stageflow.core import Stage
from random import  choice
from stageflow import Stage
from level import level

from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import InputDevice
from panda3d.core import Vec3
from panda3d.core import BitMask32
from direct.showbase.InputStateGlobal import inputState
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode



ACCEL = 100         # Acceleration in ft/sec/sec
MAX_SPEED = 6      # Max speed in ft/sec
MAX_SPEED_SQ = MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared
# Instead of length
BALL_SPEED = 10

class Room00(Stage):
    def __init__(self, exit_stage = "main_menu"):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
        self.npcs =[]
        self.gamepad = None
        devices = base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            self.connect(devices[0])
            
                # Accept device dis-/connection events
        base.accept("connect-device", self.connect)
        base.accept("disconnect-device", self.disconnect)

        # Accept button events of the first connected gamepad
        #self.accept("gamepad-back", exit)
        #s#elf.accept("gamepad-start", exit)
        #se#lf.accept("gamepad-face_x", self.reset)

        
        #self.accept("gamepad-face_b", self.action, extraArgs=["face_b"])
        #self.accept("gamepad-face_b-up", self.actionUp)
        #self.accept("gamepad-face_y", self.action, extraArgs=["face_y"])
        #self.accept("gamepad-face_y-up", self.actionUp)
        base.disableMouse()

        
    def enter(self,data):
        print("Roll Test Area Entered...")
        base.cam.set_z(24)
        base.bgm.playMusic('Ambience00', True)
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
        
        
        
        
        print(self.gamepad)
        self.level = level()
        self.load_ball()
        self.setup_ball_forces()
        
        base.accept("gamepad-face_a", self.actionA)
        base.accept("gamepad-face_a-up", self.actionAUp)
        base.accept("gamepad-face_b", self.actionB)
        base.accept("gamepad-face_b-up", self.actionBUp)
        
    def setup_ball_forces(self):
        self.force = Vec3(0,0,0)
        self.torque = Vec3(0,0,0)
        
    def actionA(self):
        self.ballNP.node().applyCentralImpulse(Vec3(0,0,128))
        print("[A] pressed")
         
    def actionAUp(self):
        print("[A] released")
        
    def actionB(self):
        self.ballNP.node().setAngularDamping(0.82)
        self.ballNP.node().setLinearDamping(0.82)
        print("[B]Brake pressed")
         
    def actionBUp(self):
        self.ballNP.node().setAngularDamping(0)
        self.ballNP.node().setLinearDamping(0)
        print("[B]Brake released")
        
    def connect(self, device):
        """Event handler that is called when a device is discovered."""

        # We're only interested if this is a gamepad and we don't have a
        # gamepad yet.
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            print("Found %s" % (device))
            self.gamepad = device

            # Enable this device to ShowBase so that we can receive events.
            # We set up the events with a prefix of "gamepad-".
            base.attachInputDevice(device, prefix="gamepad")


    def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.gamepad != device:
            # We don't care since it's not our gamepad.
            return

        # Tell ShowBase that the device is no longer needed.
        print("Disconnected %s" % (device))
        base.detachInputDevice(device)
        self.gamepad = None

        # Do we have any other gamepads?  Attach the first other gamepad.
        devices = base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if devices:
            self.connect(devices[0])
            
    def processInput(self, dt):
        self.left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
        self.left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
        self.right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
        self.right_y = self.gamepad.findAxis(InputDevice.Axis.right_y)
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

        self.ballNP.node().setActive(True)
        self.ballNP.node().applyCentralForce(force)
        self.ballNP.node().applyTorque(torque)

    def load_ball(self):
        shape = BulletSphereShape(1.5)
        self.ballNP = self.level.worldNP.attachNewNode(BulletRigidBodyNode('Sphere'))
        self.ballNP.node().setMass(4)
        self.ballNP.node().addShape(shape)
        self.ballNP.setPos(0, -10, 0)
        #self.ballNP.setScale(2, 1, 0.5)
        self.ballNP.setCollideMask(BitMask32.allOn())
        self.ballNP.node().setDeactivationEnabled(False)
        self.ballNP.node().setInertia(1)
        self.level.world.attachRigidBody(self.ballNP.node())
        visualNP = loader.loadModel('models/orb.bam')
        visualNP.clearModelNodes()
        visualNP.reparentTo(self.ballNP)
        
    def update(self, task):
        for n, npc in enumerate(self.npcs):
            face = render.find("**/npcFace")
            emblem = render.find("**/npcEmblem")
            name = npc.find("**/npcName")
            face.set_h(face, 0.5)
            emblem.set_h(emblem, -0.5)
            name.lookAt(base.cam)
            name.set_p(name, 90)
            name.set_r(name, 180)
            face.set_color(choice(self.colors))
            emblem.set_color(choice(self.colors))
            name.set_color(choice(self.colors))
            print(str(n)+": "+str(name.isHidden()))
            if((npc.getPos().getXy() - self.ballNP.getPos().getXy()).length() < 5):
                if name.isHidden():
                    print(str(n)+": "+str(name.isHidden()))
                    base.bgm.playSfx('hover')
                    print("playing sfx")
                    
            else:
                name.hide()
            
        self.ballNP.set_color(choice(self.colors))
        for o, obj in enumerate(self.level.ground.get_children()):
            obj.set_color(choice(self.colors))
        self.clock += 0.001
        dt = globalClock.getDt()
        self.processInput(dt)
        
        base.cam.set_x(self.ballNP.get_x())
        base.cam.set_y(self.ballNP.get_y() - 32)
        base.cam.set_z(self.ballNP.get_z() + 16)
        base.cam.look_at(self.ballNP)
        
        self.level.world.doPhysics(dt, 25, 2.0/360.0)
        return task.cont
    
    def transition(self, exit_stage):
        if exit_stage == None:
            self.exit_stage = 'main_menu'
        else:
            self.exit_stage = exit_stage    
        base.flow.transition(self.exit_stage)
        
    def exit(self, data):
        self.level.world.removeRigidBody(self.groundNP.node())
        self.level.world.removeRigidBody(self.ballNP.node())
        self.level.world = None

        self.debugNP = None
        self.level.groundNP = None
        self.ballNP = None

        self.level.worldNP.removeNode()
        #self.ball.detachNode()
        base.bgm.stopMusic()
        base.taskMgr.remove('update')
        return data