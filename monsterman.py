from panda3d.core import Geom, GeomNode, GeomVertexFormat, GeomVertexData, GeomVertexWriter, NodePath
from panda3d.core import GeomTriangles, Material, Texture, Vec3, LVector3f, LVecBase3f, LPoint3f
import math
import random

class YinYangMonster(NodePath):
    def __init__(self, parent_node, size=1):
        super().__init__("YinYangMonster")
        self.parent_node = parent_node if isinstance(parent_node, NodePath) else render
        print(f"MonsterManager initialized with parent: {self.parent_node}")

        # Parameters for the Yin and Yang symbol
        self.size = size
        self.radius = self.size / 2
        self.eye_radius = self.size / 8  # Small eye radius for the two "eyes" inside Yin and Yang

        # Create the YinYang shape
        self.yin_yang_np = self.create_yin_yang(self.radius, self.eye_radius)
        self.yin_yang_np.reparent_to(self)  # Attach to this monster's node (self)

        # Now, access the individual parts (Yin and Yang)
        self.yin_np = self.yin_yang_np.find('**/YinGeom')  # Reference to the Yin part
        self.yang_np = self.yin_yang_np.find('**/YangGeom')  # Reference to the Yang part

        # Initial velocity and rotation speed
        self.position = LPoint3f(0, 0, 0)  # Initial position set to origin
        self.velocity = Vec3(0, 0, 0)
        self.kick_power = 10
        self.rotation_speed = random.uniform(10.0, 30.0)  # Speed of rotation
        self.gravity = Vec3(0, 0, -9.81)  # Simple gravity force (downward)
        self.kick_off()
        self.reparent_to(self.parent_node)  # Reparent to the parent node
        base.taskMgr.add(self.update, "update_monster_task")

    def create_yin_yang(self, radius, eye_radius):
        """Create the Yin Yang symbol procedurally with separate collision nodes for Yin and Yang."""
        format = GeomVertexFormat.get_v3n3c4()

        # Create separate GeomVertexData for Yin and Yang
        vertex_data_yin = GeomVertexData('yin_data', format, Geom.UHStatic)
        vertex_data_yang = GeomVertexData('yang_data', format, Geom.UHStatic)

        # Writers for Yin and Yang
        yin_vertex_writer = GeomVertexWriter(vertex_data_yin, 'vertex')
        yin_normal_writer = GeomVertexWriter(vertex_data_yin, 'normal')
        yin_color_writer = GeomVertexWriter(vertex_data_yin, 'color')

        yang_vertex_writer = GeomVertexWriter(vertex_data_yang, 'vertex')
        yang_normal_writer = GeomVertexWriter(vertex_data_yang, 'normal')
        yang_color_writer = GeomVertexWriter(vertex_data_yang, 'color')

        # Function to add vertices
        def add_vertex(writer_v, writer_n, writer_c, x, y, z, nx, ny, nz, r, g, b, a):
            writer_v.add_data3f(x, y, z)
            writer_n.add_data3f(nx, ny, nz)
            writer_c.add_data4f(r, g, b, a)

        segments = 32  # Number of segments for the circle
        angle_step = 2 * math.pi / segments

        # Add vertices for Yin and Yang halves
        for i in range(segments):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            if i < segments // 2:  # Yin (black)
                add_vertex(yin_vertex_writer, yin_normal_writer, yin_color_writer, x, y, 0, 0, 0, 1, 0, 0, 0, 1)
            else:  # Yang (white)
                add_vertex(yang_vertex_writer, yang_normal_writer, yang_color_writer, x, y, 0, 0, 0, 1, 1, 1, 1, 1)

        # Add eye geometry
        self.add_eye(yang_vertex_writer, yang_normal_writer, yang_color_writer, radius * 0.4, eye_radius, 1, 1, 1, 1)
        self.add_eye(yin_vertex_writer, yin_normal_writer, yin_color_writer, radius * -0.4, eye_radius, 0, 0, 0, 1)

        # Create triangles for Yin and Yang
        triangles_yin = GeomTriangles(Geom.UHStatic)
        triangles_yang = GeomTriangles(Geom.UHStatic)

        # Triangles for Yin (first half)
        for i in range(segments // 2 - 1):
            triangles_yin.add_vertices(i, i + 1, segments // 2 - 1)  # Adjust as needed

        # Triangles for Yang (second half)
        for i in range(segments // 2, segments - 1):
            triangles_yang.add_vertices(i - segments // 2, i - segments // 2 + 1, segments // 2 - 1)  # Adjust as needed

        # Create Geoms
        geom_yin = Geom(vertex_data_yin)
        geom_yin.add_primitive(triangles_yin)

        geom_yang = Geom(vertex_data_yang)
        geom_yang.add_primitive(triangles_yang)

        # Create GeomNodes and NodePaths
        geom_node_yin = GeomNode('YinGeom')
        geom_node_yin.add_geom(geom_yin)

        geom_node_yang = GeomNode('YangGeom')
        geom_node_yang.add_geom(geom_yang)

        yin_np = NodePath(geom_node_yin)
        yang_np = NodePath(geom_node_yang)
        # Create a parent node to combine both parts
        yin_yang_np = NodePath('YinYangNode')

        # Reparent the individual parts to the parent node
        yin_np.reparent_to(yin_yang_np)
        yang_np.reparent_to(yin_yang_np)

        # Return the combined NodePath
        return yin_yang_np

    def add_eye(self, vertex_writer, normal_writer, color_writer, x, y, r, g, b, a):
        """Add the small circular eye to the Yin Yang symbol."""
        segments = 8
        angle_step = 2 * math.pi / segments
        for i in range(segments):
            angle = i * angle_step
            eye_x = x + self.eye_radius * math.cos(angle)
            eye_y = y + self.eye_radius * math.sin(angle)
            vertex_writer.add_data3f(eye_x, eye_y, 0)
            normal_writer.add_data3f(0, 0, 1)
            color_writer.add_data4f(r, g, b, a)

    def update(self, task):
        print("Updating monster")
        delta_time = globalClock.get_dt()
        self.update_velocity(delta_time)
        self.update_position(delta_time)
        self.update_hpr()
        return task.cont  # Continue the task


        
    def kick_off(self):
        """Kick the monster in a random direction."""
        direction = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0).normalized()
        self.velocity = direction * self.kick_power  # Apply the kick power to the velocity
        print(f"Initial velocity after kick-off: {self.velocity}")


    def update_velocity(self, delta_time):
        self.velocity += LVector3f(0, 0, -9.8) * delta_time  # Apply gravity
        print(f"Velocity: {self.velocity}")



    def update_position(self, delta_time):
        self.position += self.velocity * delta_time
        self.set_pos(self.position)  # Update the NodePath's position in the scene graph
        print(f"Position: {self.position}")

        
    def update_hpr(self):
        if self.velocity.length() > 0:
            direction = self.velocity.normalized()
            self.hpr = LVecBase3f(direction.getX(), direction.getY(), 0)  # Update heading
            print(f"Updated hpr: {self.hpr}")


class MonsterManager:
    def create_yin_yang(self):
        return YinYangMonster(parent_node=render)

    def __init__(self, parent=None):
        self.parent_node = parent
        self.monsters = []

    def create_monster(self, index):
        """Create a monster object and assign properties (health, type, etc.)."""
        # Pass render explicitly if self.parent is None
        monster = YinYangMonster(self.parent_node, size=random.uniform(1.0, 2.0))
        monster.name = f"Monster_{index}"
        monster.health = 100
        monster.type = "Flower"
        monster.set_scale(1)
        print(f"Created {monster.name} with health {monster.health} and type {monster.type}.")
        return monster

    def place_monsters(self, monsters, num_monsters=10):
        """Place monsters randomly in the world."""
        for i in range(num_monsters):
            monster = self.create_monster(i)
            if self.parent_node is not None:
                monster.reparent_to(self.parent_node)  # Attach the monster to the parent node
            else:
                raise ValueError("Parent NodePath is None. Cannot reparent the monster.")
            monsters.append(monster)
        
        return monsters

    def update_monsters(self, dt):
        """Update all monsters (e.g., move them, apply velocities)."""
        for monster in self.monsters:
            monster.update(dt)  # Update position based on velocity

            # Every few seconds, apply a "kick" to a random monster
            if random.random() < 0.1:  # Chance to kick off
                monster.kick_off()