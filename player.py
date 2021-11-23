from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3
from panda3d.core import BitMask32

ACCEL = 100         # Acceleration in ft/sec/sec
MAX_SPEED = 6      # Max speed in ft/sec
MAX_SPEED_SQ = MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared
# Instead of length
BALL_SPEED = 10

class player():
    def __init__(self):
        self.load_ball()
        self.setup_ball_forces()
        self.ball_roll = base.loader.load_sfx('audio/ball_roll.wav')
        self.ball_roll.setLoop(True)
        self.ball_roll.play()
        self.boings = [
            'boing00',
            'boing01',
            'boing02',
            'boing03',
            'boing04',
            
        ]
        self.boing = False
        self.portal_loop = False
        
    def load_ball(self):
        shape = BulletSphereShape(1.5)
        self.ballNP = render.attachNewNode(BulletRigidBodyNode('Sphere'))
        self.ballNP.node().setMass(4)
        self.ballNP.node().addShape(shape)
        #self.ballNP.setScale(2, 1, 0.5)
        self.ballNP.setCollideMask(BitMask32.allOn())
        self.ballNP.node().setDeactivationEnabled(False)
        self.ballNP.node().setInertia(1)
        self.ballNP.node().setRestitution(.75)
        visualNP = loader.loadModel('models/orb.bam')
        visualNP.clearModelNodes()
        visualNP.reparentTo(self.ballNP)
        
    def setup_ball_forces(self):
        self.force = Vec3(0,0,0)
        self.torque = Vec3(0,0,0)
    
    def __destroy__(self):
        self.ball_roll.stop()