from panda3d.bullet import BulletSphereShape

from panda3d.bullet import BulletRigidBodyNode

from panda3d.core import Vec3

from panda3d.core import BitMask32

from panda3d.core import Vec3

ACCEL = 100  # Acceleration in ft/sec/sec

MAX_SPEED = 6  # Max speed in ft/sec

MAX_SPEED_SQ = MAX_SPEED**2  # Squared to make it easier to use lengthSquared

# Instead of length

BALL_SPEED = 10



class player:
    def __init__(self):
        self.load_ball()
        self.setup_ball_forces()
        self.ball_roll = base.loader.load_sfx("audio/ball_roll.wav")
        self.ball_roll.setLoop(True)
        self.ball_roll.play()
        self.boings = ["boing00", "boing01", "boing02", "boing03", "boing04"]
        self.boing = False
        self.portal_loop = False
        self.previous_velocity = Vec3(0, 0, 0)  # Initialize previous velocity
    def update(self):
        # Store the velocity for the next frame
        self.previous_velocity = self.ballNP.node().getLinearVelocity()

    def get_previous_velocity(self):
        return self.previous_velocity
    def load_ball(self):
        shape = BulletSphereShape(1.5)
        self.ballNP = render.attachNewNode(BulletRigidBodyNode("Sphere"))
        self.ballNP.node().setMass(4)
        self.ballNP.node().addShape(shape)
        self.ballNP.setCollideMask(BitMask32.allOn())
        self.ballNP.node().setDeactivationEnabled(False)
        self.ballNP.node().setRestitution(0.75)
        visualNP = loader.loadModel("models/orb.bam")
        visualNP.clearModelNodes()
        visualNP.reparentTo(self.ballNP)

    def setup_ball_forces(self):
        self.force = Vec3(0, 0, 0)
        self.torque = Vec3(0, 0, 0)
    def get_impact_velocity_vector(self, contact):
        """
        Calculate the relative velocity vector for a given contact.
        """
        mpoint = contact.getManifoldPoint()
        velocity_a = self.ballNP.node().getLinearVelocity()  # Velocity of the ball
        velocity_b = Vec3(0, 0, 0)  # Assume the floor has no velocity

        # Calculate the relative velocity vector
        relative_velocity = velocity_a - velocity_b

        # Optionally, project onto the contact normal
        normal = Vec3(mpoint.getNormalWorldOnB())
        relative_velocity_normal = normal * relative_velocity.dot(normal)

        return relative_velocity_normal  # Returns a Vec3 vector
    def get_impact_velocity(self, contact):
        """
        Computes the impact velocity at the contact point.
        
        Args:
            contact (BulletContact): The contact point data from a collision.

        Returns:
            float: The relative velocity magnitude at the impact point.
        """
        node0 = contact.get_node0()
        node1 = contact.get_node1()

        # Ensure both nodes are rigid bodies
        if isinstance(node0, BulletRigidBodyNode):
            vel0 = node0.get_linear_velocity()
        else:
            vel0 = Vec3(0, 0, 0)

        if isinstance(node1, BulletRigidBodyNode):
            vel1 = node1.get_linear_velocity()
        else:
            vel1 = Vec3(0, 0, 0)

        # Calculate relative velocity
        relative_velocity = vel0 - vel1
        impact_velocity = relative_velocity.length()
        return impact_velocity

    def __destroy__(self):
        self.ball_roll.stop()
