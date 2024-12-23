from panda3d.core import (
    Geom,
    GeomNode,
    GeomVertexFormat,
    GeomVertexData,
    GeomVertexWriter,
    NodePath,
    GeomTriangles,
    Vec3,
    LPoint3f,
)
from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletBoxShape, BulletWorld
import math
import random


class YinYangMonster(NodePath):
    def __init__(self, parent_node, world, size=1):
        super().__init__("YinYangMonster")
        self.parent_node = parent_node if isinstance(parent_node, NodePath) else render
        self.size = size
        self.radius = self.size / 2
        self.eye_radius = self.size / 8
        self.bullet_world = world

        # Create Yin-Yang Geometry
        self.yin_yang_np = self.create_yin_yang(self.radius, self.eye_radius)
        self.yin_yang_np.reparent_to(self)
        
        # Create Bullet collision body for Yin-Yang
        self.create_collision_bodies()

        # Initial motion
        self.kick_off()
        self.reparent_to(self.parent_node)
        base.taskMgr.add(self.update, "update_monster_task")

    def create_yin_yang(self, radius, eye_radius):
        format = GeomVertexFormat.get_v3n3c4()
        vertex_data_yin = GeomVertexData("yin_data", format, Geom.UHStatic)
        vertex_data_yang = GeomVertexData("yang_data", format, Geom.UHStatic)
        yin_vertex_writer = GeomVertexWriter(vertex_data_yin, "vertex")
        yin_normal_writer = GeomVertexWriter(vertex_data_yin, "normal")
        yin_color_writer = GeomVertexWriter(vertex_data_yin, "color")
        yang_vertex_writer = GeomVertexWriter(vertex_data_yang, "vertex")
        yang_normal_writer = GeomVertexWriter(vertex_data_yang, "normal")
        yang_color_writer = GeomVertexWriter(vertex_data_yang, "color")

        def add_vertex(writer_v, writer_n, writer_c, x, y, z, nx, ny, nz, r, g, b, a):
            writer_v.add_data3f(x, y, z)
            writer_n.add_data3f(nx, ny, nz)
            writer_c.add_data4f(r, g, b, a)

        segments = 32
        angle_step = 2 * math.pi / segments
        for i in range(segments):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            if i < segments // 2:
                add_vertex(yin_vertex_writer, yin_normal_writer, yin_color_writer, x, y, 0, 0, 0, 1, 0, 0, 0, 1)
            else:
                add_vertex(yang_vertex_writer, yang_normal_writer, yang_color_writer, x, y, 0, 0, 0, 1, 1, 1, 1, 1)

        self.add_eye(yang_vertex_writer, yang_normal_writer, yang_color_writer, radius * 0.4, eye_radius, 1, 1, 1, 1)
        self.add_eye(yin_vertex_writer, yin_normal_writer, yin_color_writer, radius * -0.4, eye_radius, 0, 0, 0, 1)

        triangles_yin, triangles_yang = GeomTriangles(Geom.UHStatic), GeomTriangles(Geom.UHStatic)
        for i in range(segments // 2 - 1):
            triangles_yin.add_vertices(i, i + 1, segments // 2 - 1)
        for i in range(segments // 2, segments - 1):
            triangles_yang.add_vertices(i - segments // 2, i - segments // 2 + 1, segments // 2 - 1)

        geom_yin, geom_yang = Geom(vertex_data_yin), Geom(vertex_data_yang)
        geom_yin.add_primitive(triangles_yin)
        geom_yang.add_primitive(triangles_yang)
        geom_node_yin, geom_node_yang = GeomNode("YinGeom"), GeomNode("YangGeom")
        geom_node_yin.add_geom(geom_yin)
        geom_node_yang.add_geom(geom_yang)
        yin_np, yang_np = NodePath(geom_node_yin), NodePath(geom_node_yang)
        self.yin_np = yin_np
        self.yang_np = yang_np
        yin_yang_np = NodePath("YinYangNode")
        yin_np.reparent_to(yin_yang_np)
        yang_np.reparent_to(yin_yang_np)
        
        return yin_yang_np

    def add_eye(self, vertex_writer, normal_writer, color_writer, x, y, r, g, b, a):
        segments = 8
        angle_step = 2 * math.pi / segments
        for i in range(segments):
            angle = i * angle_step
            eye_x = x + self.eye_radius * math.cos(angle)
            eye_y = y + self.eye_radius * math.sin(angle)
            vertex_writer.add_data3f(eye_x, eye_y, 0)
            normal_writer.add_data3f(0, 0, 1)
            color_writer.add_data4f(r, g, b, a)

    def create_collision_bodies(self):
        # Create collision meshes for both Yin and Yang
        yin_shape = BulletSphereShape(self.radius)
        yang_shape = BulletSphereShape(self.radius)
        
        # Create Bullet collision nodes for both parts
        self.yin_col = BulletRigidBodyNode('YinCollision')
        self.yin_col.add_shape(yin_shape)
        self.yin_col.set_mass(0.0)  # Set mass to 0 to make it a static object
        self.yin_col_np = NodePath(self.yin_col)
        self.yin_col_np.reparent_to(self.yin_np)  # Attach collision mesh directly to yin_np
        
        self.yang_col = BulletRigidBodyNode('YangCollision')
        self.yang_col.add_shape(yang_shape)
        self.yang_col.set_mass(0.0)  # Set mass to 0 to make it a static object
        self.yang_col_np = NodePath(self.yang_col)
        self.yang_col_np.reparent_to(self.yin_yang_np)  # Attach collision mesh to yang_np

        
        # Attach collision bodies to the bullet world
        self.bullet_world.attach(self.yin_col)
        self.bullet_world.attach(self.yang_col)

    def update(self, task):
        self.set_pos(self.get_pos())
        self.set_hpr(self.get_hpr())
        return task.cont

    def kick_off(self):
        direction = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.5, 1)).normalized()
        self.yang_col.set_linear_velocity(direction * 10)
        self.yin_col.set_linear_velocity(direction * 10)