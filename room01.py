from math import sin
import sys
from stageflow.core import Stage
from random import randint, choice
from stageflow import Stage

from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Material, LRotationf, NodePath
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LVector3, BitMask32
from panda3d.core import NodePath
from panda3d.physics import ActorNode
from panda3d.core import InputDevice
from panda3d.core import InputDeviceManager
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce

from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape

from direct.showbase.InputStateGlobal import inputState

DEBUG = False
ACCEL = 100         # Acceleration in ft/sec/sec
MAX_SPEED = 6      # Max speed in ft/sec
MAX_SPEED_SQ = MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared
# Instead of length
BALL_SPEED = 10

class Room01(Stage):
    def __init__(self, exit_stage = "main_menu"):
        self.exit_stage = exit_stage
        self.colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (1,0,1,1)]
        self.clock = 0
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
        base.accept("gamepad-face_a", self.actionA)
        base.accept("gamepad-face_a-up", self.actionAUp)
        base.accept("gamepad-face_b", self.actionB)
        base.accept("gamepad-face_b-up", self.actionBUp)
        
        #self.accept("gamepad-face_b", self.action, extraArgs=["face_b"])
        #self.accept("gamepad-face_b-up", self.actionUp)
        #self.accept("gamepad-face_y", self.action, extraArgs=["face_y"])
        #self.accept("gamepad-face_y-up", self.actionUp)
        base.disableMouse()

        
    def enter(self, data):
        self.data = data
        print("Roll Test Area Entered...")
        base.cam.set_z(24)
        base.bgm.playMusic(None, True)
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
        self.load_world()
        self.load_ground()
        #self.load_floor()
        self.load_ball()
        self.setup_ball_forces()
        
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
        force = Vec3(self.left_x.value, self.left_y.value, 0)
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
        
        #force = self.ballNP.getRelativeVector(base.cam, force)
        #torque = base.cam.getRelativeVector(self.ballNP, torque)

        self.ballNP.node().setActive(True)
        self.ballNP.node().applyCentralForce(force)
        self.ballNP.node().applyTorque(torque)
        
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
        
    def load_floor(self):
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.groundNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        self.groundNP.node().addShape(shape)
        self.groundNP.setPos(0, 0, -2)
        self.groundNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(self.groundNP.node())
        self.groundNP.node().setFriction(1)

    def load_ball(self):
        shape = BulletSphereShape(1.5)
        self.ballNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Sphere'))
        self.ballNP.node().setMass(4)
        self.ballNP.node().addShape(shape)
        self.ballNP.setPos(0, 0, 60)
        #self.ballNP.setScale(2, 1, 0.5)
        self.ballNP.setCollideMask(BitMask32.allOn())
        self.ballNP.node().setDeactivationEnabled(False)
        self.ballNP.node().setInertia(1)
        self.world.attachRigidBody(self.ballNP.node())
        visualNP = loader.loadModel('models/orb.bam')
        visualNP.clearModelNodes()
        visualNP.reparentTo(self.ballNP)
        
    def load_ground(self):
        self.ground = base.loader.loadModel("levels/terrain01.bam")
        #self.ground.set_two_sided(True)
        groundCol = self.ground.findAllMatches("**/+GeomNode").getPath(0).node().getGeom(0)
        mesh = BulletTriangleMesh()
        mesh.addGeom(groundCol)
        shape = BulletTriangleMeshShape(mesh, dynamic=True)

        body = BulletRigidBodyNode('Level')
        bodyNP = self.worldNP.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.setPos(0, 0, 0)
        bodyNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(bodyNP.node())
        bodyNP.show()

        self.ground.reparentTo(bodyNP)

        self.groundNP = bodyNP
        #self.ground.node().setIntoCollideMask(BitMask32.bit(0))
        self.ground.reparentTo(render)
        #self.ground.show()
        print("loaded ground...")
        

        
    def update(self, task):
        
        #self.ball.set_color(choice(self.colors))
        self.ballNP.set_color(choice(self.colors))
        
        self.ground.set_color(choice(self.colors))
        #print("looking at ball...")
        base.cam.set_x(self.ballNP.get_x())
        base.cam.set_y(self.ballNP.get_y()-32)
        base.cam.set_z(self.ballNP.get_z()+32)
        base.cam.look_at(self.ballNP)

        #self.pendulum.set_color(choice(self.colors))
        #elf.pendulum.set_h(self.pendulum, 6)
        #self.pendulum.set_r(self.pendulum, -6)
        #self.ball.set_x(base.camera, sin(self.clock)*10)
        #self.ball.set_y(base.camera, sin(self.clock)*10)
        
        #self.ball.set_p(self.ball, 0.025)
        #self.ball.set_h(self.ball, 0.05)
        self.clock += 0.001
        #print("------------")
        #print("Left("+str(self.left_x.state)+","+str(self.left_y.state)+")")
        #print("Right("+str(self.right_x.state)+","+str(self.right_y.state)+")")
        #print(str(self.left_x.value))
        #print("------------")
        dt = globalClock.getDt()

        self.processInput(dt)
        #self.world.doPhysics(dt)
        self.world.doPhysics(dt, 5, 2.0/360.0)
        #base.cam.look_at(self.ground)
        #base.camera.set_r(base.camera, 0)
        return task.cont
    
    def transition(self, exit_stage):
        if exit_stage == None:
            self.exit_stage = 'main_menu'
        else:
            self.exit_stage = exit_stage    
        base.flow.transition(self.exit_stage)
        
    def exit(self, data):
        self.world.removeRigidBody(self.groundNP.node())
        self.world.removeRigidBody(self.ballNP.node())
        self.world = None

        self.debugNP = None
        self.groundNP = None
        self.ballNP = None

        self.worldNP.removeNode()
        #self.ball.detachNode()
        base.bgm.stopMusic()
        base.taskMgr.remove('update')
        return data