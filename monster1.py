
from panda3d.core import (
    NodePath,
    Vec3,
    Vec4,
    GeomNode,
    CollisionNode,
    CollisionSphere,
    CollisionBox,
    CollisionRay,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    Geom,
    GeomTriangles,
    BitMask32,
    CollisionHandlerEvent,
    CollisionTraverser,
)

from direct.task import Task

from direct.showbase.DirectObject import DirectObject

import random

import math

from procweapon import ProceduralWeaponSwinger



    
class ProceduralMonster(NodePath):
    def __init__(self, parent=None, event_handler=None):
        super().__init__("ProceduralMonster")

        # These are the nodes for the petals and monster (bulb)

        self.petalsNP = NodePath("Petals")

        self.monsterNP = NodePath("MonsterBulb")

        self.event_handler = event_handler  # Pass event handler

        # Set up the collision traverser and handler

        self.collision_traverser = CollisionTraverser("monsterTraverser")

        self.collision_handler = CollisionHandlerEvent()

        # Specify collision event names

        self.collision_handler.add_in_pattern("%fn-into-%in")

        self.collision_handler.add_out_pattern("%fn-out-%in")

        # Add tasks and setup

        self.reparent_to(parent if parent else base.render)

        # Store body parts for animation and collisions

        self.body_parts = []

        self.collision_nodes = []

        self.is_colliding = False

        self.setup_collision_system()

        self.health = 100  # Health for the flower

        self.player_health = 100  # Health for the player

        # Generate the monster's appearance

        self.generate_monster()

        self.create_flower_petal()

        # Setup animations

        taskMgr.add(self.idle_animation, "IdleAnimation")

        self.is_attacking = False

        self.is_moving = False

        # Add the collision checking task

    
    def setup_collision_system(self):
        # Add all collision nodes to the traverser

        for node in self.collision_nodes:
            self.collision_traverser.add_collider(node, self.collision_handler)

        # Optionally display collision geometry for debugging
    

        self.collision_traverser.show_collisions(base.render)

    def handle_collision_in(self, entry):
    
        print(
            f"Collision detected! From: {entry.get_from_node_path()} To: {entry.get_into_node_path()}"
        )

    def handle_collision_out(self, entry):
        print(
            f"Collision ended! From: {entry.get_from_node_path()} To: {entry.get_into_node_path()}"
        )

    def generate_monster(self):
        """Generates a flower creature with petal-like body parts."""

        num_parts = random.randint(
            5, 8
        )  # Increased number of parts for more complexity

        colors = [
            Vec4(1, 0, 0, 1),
            Vec4(1, 0.5, 0, 1),
            Vec4(1, 1, 0, 1),
            Vec4(0, 1, 0, 1),
            Vec4(0, 0, 1, 1),
            Vec4(0.5, 0, 0.5, 1),
        ]

        # Generate the body (center) of the flower creature

        body_size = random.uniform(0.3, 0.5)

        body_color = Vec4(1, 1, 1, 1)  # White or bright center for flower

        body = self.create_primitive("sphere", body_size)

        body.set_color(body_color)

        body.set_pos(Vec3(0, 0, 0))

        body.reparent_to(self)

        self.body_parts.append(body)

        # Add collision for the body (flower bulb)

        body_collision = CollisionNode("flower_body")

        body_collision.add_solid(CollisionSphere(0, 0, 0, body_size))

        body_collision.set_from_collide_mask(BitMask32.bit(1))  # Player collision layer

        body_collision.set_into_collide_mask(
            BitMask32.bit(0)
        )  # Ignore other collisions

        body.attach_new_node(body_collision)

        # Accept the collision event through the main event handler (ShowBase object)

        if self.event_handler:
            self.event_handler.accept("flower_body-into", self.on_body_collision)

        # Generate the petals (random count and placement around body)

        num_petals = random.randint(5, 8)

        for i in range(num_petals):
            petal_size = random.uniform(0.2, 0.4)

            angle = (i / num_petals) * 360  # Even distribution around center

            petal_position = Vec3(
                math.cos(math.radians(angle)) * 1.0,
                math.sin(math.radians(angle)) * 1.0,
                0,
            )

            petal_color = random.choice(colors)

            petal = self.create_primitive("cone", petal_size)

            petal.set_color(petal_color)

            petal.set_pos(petal_position)

            petal.set_h(angle)  # Rotate petal to face outward

            petal.reparent_to(self)

            # Add collision for the petal

            petal_collision = CollisionNode("petal_{}".format(i))

            petal_collision.add_solid(CollisionSphere(petal_position, petal_size))

            petal_collision.set_from_collide_mask(
                BitMask32.bit(1)
            )  # Player collision layer

            petal_collision.set_into_collide_mask(
                BitMask32.bit(0)
            )  # Ignore other collisions

            petal.attach_new_node(petal_collision)

            # Accept the collision event through the main event handler (ShowBase object)

            if self.event_handler:
                self.event_handler.accept(
                    "petal_{}-into".format(i), self.on_petal_collision
                )

            self.create_physics_cage()

            self.body_parts.append(petal)

    def create_flower_petal(self):
        """Creates an additional feature for flower creature: a procedurally created flower petal."""

        petal_size = random.uniform(0.2, 0.4)

        petal_angle = random.uniform(0, 360)

        petal_position = Vec3(0, 1, 0)  # Place petal above body

        petal = self.create_primitive("cone", petal_size)

        petal.set_color(Vec4(1, 0.5, 0, 1))  # Choose a petal color

        petal.set_pos(petal_position)

        petal.set_h(petal_angle)

        petal.reparent_to(self)

        self.body_parts.append(petal)

        # Add collision shape for the petal

        petal_collision = CollisionNode("petal_0")

        petal_collision.add_solid(CollisionSphere(petal_position, petal_size))

        petal_collision.set_from_collide_mask(
            BitMask32.bit(1)
        )  # Player collision layer

        petal_collision.set_into_collide_mask(
            BitMask32.bit(0)
        )  # Ignore other collisions

        petal.attach_new_node(petal_collision)

        # Accept the collision event through the main event handler (ShowBase object)

        if self.event_handler:
            self.event_handler.accept("petal_0-into", self.on_petal_collision)

        # Add collision shape for the petal

        self.add_collision(petal, "cone", petal_size)

    def on_petal_collision(self, entry):
        """Handles collision with petals, hurting the player."""

        if self.player_health > 0:
            self.player_health -= 10  # Decrease player health on petal touch

            print("Player hurt by petal! Player health: ", self.player_health)

    def on_body_collision(self, entry):
        """Handles collision with the flower body (bulb), causing it to lose health."""

        if self.health > 0:
            self.health -= 10  # Decrease flower health on body touch

            print("Flower hurt! Flower health: ", self.health)

    def create_sword(self):
        """Creates a procedural sword, scales it, and attaches it to the monster, with swinging."""

        sword_length = 5.0  # Scaling up the sword to be large

        sword_width = 0.1  # Keeping the width smaller for the visual effect

        # Create the procedural weapon swinger to handle swinging and color cycling

        weapon_swinger = ProceduralWeaponSwinger(self, weapon_type="sword")

        # Set the properties for the sword (scale and color)

        weapon_swinger.sword.set_scale(sword_length, sword_width, sword_width)

        weapon_swinger.sword.set_color(
            Vec4(0.7, 0.7, 0.7, 1)
        )  # Set the sword's color to grey

        # Position the sword in front of the monster (adjust based on your model)

        weapon_swinger.sword.set_pos(
            0.5, 0, 0
        )  # Example: positioned at (0.5, 0, 0) relative to the monster

        # Attach the sword to the monster (could be attached to the hand or another body part)

        weapon_swinger.sword.reparent_to(self)

        # Add a task to swing the sword every few seconds

        taskMgr.add(
            self.swing_weapon_task,
            "SwingWeaponTask",
            extraArgs=[weapon_swinger],
            interval=2,
        )

        # Return the weapon swinger so it can be accessed later if needed

        return weapon_swinger

    def swing_weapon_task(self, weapon_swinger, task):
        """Periodically swings the sword with a random swing interval."""

        if weapon_swinger.is_moving:
            return Task.cont

        # Randomly decide when to trigger the swing (e.g., every 2-5 seconds)

        swing_interval = random.uniform(2, 5)

        if task.time > swing_interval:
            self.start_attack(weapon_swinger)  # Trigger attack (swing the sword)

            task.time = 0  # Reset the timer

        return Task.cont

    def start_attack(self, weapon_swinger):
        """Trigger the attack (swing animation)."""

        weapon_swinger.is_moving = True

        # Add a rotation or swinging motion to the sword

        weapon_swinger.sword.set_h(
            weapon_swinger.sword.get_h() + 45
        )  # Rotate the sword for swinging effect

        print("Weapon Swinging!")

    def stop_attack(self, weapon_swinger):
        """Stop the attack and reset sword position."""

        weapon_swinger.is_moving = False

        # Optionally reset sword position or add a delay

        weapon_swinger.sword.set_h(
            weapon_swinger.sword.get_h() - 45
        )  # Reset the sword rotation to neutral

    def create_primitive(self, primitive_type, size):
        """Creates a primitive shape procedurally."""

        if primitive_type == "sphere":
            return self.create_sphere(size)

        elif primitive_type == "box":
            return self.create_box(size)

        elif primitive_type == "cone":
            return self.create_cone(size)

    def add_collision(self, part, part_type, size):
        """Adds a collision shape to a body part."""

        collision_node = CollisionNode(f"collision_{part_type}")

        if part_type == "sphere":
            collision_solid = CollisionSphere(0, 0, 0, size)

        elif part_type == "box":
            half_size = size / 2

            collision_solid = CollisionBox((0, 0, 0), half_size, half_size, half_size)

        elif part_type == "cone":
            # For cones, use a simple box for collision, but could use a more precise shape if desired

            half_size = size / 2

            collision_solid = CollisionBox(half_size, half_size, half_size, size)

        collision_node.add_solid(collision_solid)

        # Attach the collision node to the part

        collision_np = part.attach_new_node(collision_node)

        # Make sure it's added to the list of collision nodes for future references

        self.collision_nodes.append(collision_np)

        # Ensure the collision node is set to interact with the correct layers

        collision_node.set_from_collide_mask(
            BitMask32.bit(1)
        )  # This layer will collide with the player

        collision_node.set_into_collide_mask(
            BitMask32.all_off()
        )  # Don't interact with other objects

        # Accept collision events if necessary

        if self.event_handler:
            self.event_handler.accept(
                f"{part.get_name()}-into", self.on_petal_collision
            )
    

    # Add collision for the entire flower (physics cage around petals and body)

    def create_physics_cage(self):
        # Create a bounding box or sphere around the entire flower creature


        min_x = (
            min(petal.get_pos().x for petal in self.body_parts) - 1.0
        )  # Adjust for padding

        max_x = max(petal.get_pos().x for petal in self.body_parts) + 1.0

        min_y = min(petal.get_pos().y for petal in self.body_parts) - 1.0

        max_y = max(petal.get_pos().y for petal in self.body_parts) + 1.0

        min_z = min(petal.get_pos().z for petal in self.body_parts) - 1.0

        max_z = max(petal.get_pos().z for petal in self.body_parts) + 1.0

        # Create a physics cage using a collision box or sphere that bounds the monster's body

        cage_collision_node = CollisionNode("flower_cage")

        cage_collision_node.add_solid(
            CollisionBox(
                Vec3((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2),
                max_x - min_x,
                max_y - min_y,
                max_z - min_z,
            )
        )

        cage_collision_node.set_from_collide_mask(
            BitMask32.bit(1)
        )  # Allow player collisions

        cage_collision_node.set_into_collide_mask(
            BitMask32.bit(0)
        )  # Ignore other collisions

        # Attach the cage to the monster's root node (self)

        self.attach_new_node(cage_collision_node)

    def create_sphere(self, radius):
        """Procedurally creates a sphere."""

        vertices = []

        indices = []

        segments = 16

        rings = 8

        # Create vertices for the sphere

        for i in range(rings + 1):
            phi = math.pi * i / rings

            for j in range(segments + 1):
                theta = 2 * math.pi * j / segments

                x = radius * math.sin(phi) * math.cos(theta)

                y = radius * math.sin(phi) * math.sin(theta)

                z = radius * math.cos(phi)

                vertices.append((x, y, z))

        # Create indices for triangles (each face is a triangle)

        for i in range(rings):
            for j in range(segments):
                current = i * (segments + 1) + j

                next = current + segments + 1

                indices.append((current, next, current + 1))

                indices.append((next, next + 1, current + 1))

        # Set up the GeomVertexData

        format = (
            GeomVertexFormat.get_v3n3c4()
        )  # Vertex format with position, normal, and color

        vdata = GeomVertexData("sphere", format, Geom.UH_static)

        vertex = GeomVertexWriter(vdata, "vertex")

        normal = GeomVertexWriter(vdata, "normal")

        color = GeomVertexWriter(vdata, "color")

        # Write vertex data

        for vert in vertices:
            vertex.add_data3f(*vert)

            normal.add_data3f(
                *vert
            )  # Normals are the same as the vertex positions for spheres

            color.add_data4f(1.0, 1.0, 1.0, 1.0)  # Default to white color

        # Create the geometry

        triangles = GeomTriangles(Geom.UH_static)

        for tri in indices:
            triangles.add_vertices(*tri)

        geom = Geom(vdata)

        geom.add_primitive(triangles)

        # Attach to a GeomNode and return as a NodePath

        node = GeomNode("sphere")

        node.add_geom(geom)

        return NodePath(node)

    def create_box(self, size):
        """Procedurally creates a box (cube)."""

        half_size = size / 2

        vertices = [
            (-half_size, -half_size, -half_size),
            (half_size, -half_size, -half_size),
            (half_size, half_size, -half_size),
            (-half_size, half_size, -half_size),
            (-half_size, -half_size, half_size),
            (half_size, -half_size, half_size),
            (half_size, half_size, half_size),
            (-half_size, half_size, half_size),
        ]

        indices = [
            (0, 1, 2),
            (0, 2, 3),  # front
            (4, 5, 6),
            (4, 6, 7),  # back
            (0, 1, 5),
            (0, 5, 4),  # bottom
            (2, 3, 7),
            (2, 7, 6),  # top
            (1, 2, 6),
            (1, 6, 5),  # right
            (0, 3, 7),
            (0, 7, 4),  # left
        ]

        # Create vertex data for the box

        vdata = GeomVertexData(
            "box", GeomVertexFormat.get_v3(), GeomVertexData.UHStatic
        )

        vertex_writer = GeomVertexWriter(vdata, "vertex")

        for vertex in vertices:
            vertex_writer.add_data3f(*vertex)

        # Create geometry (tris)

        geom = Geom(vdata)

        for index in indices:
            triangle = GeomTriangles(Geom.UHStatic)

            triangle.add_vertices(*index)

            geom.add_primitive(triangle)

        # Create geom node

        geom_node = GeomNode("box")

        geom_node.add_geom(geom)

        return NodePath(geom_node)

    def create_cone(self, size):
        """Procedurally creates a cone."""

        vertices = [(0, 0, size)]  # Tip of the cone

        segments = 16

        angle_step = 2 * math.pi / segments

        # Create vertices for the base of the cone

        for i in range(segments):
            angle = i * angle_step

            x = size * math.cos(angle)

            y = size * math.sin(angle)

            z = 0

            vertices.append((x, y, z))

        # Create triangles

        indices = []

        for i in range(segments):
            next_i = (i + 1) % segments

            indices.append((0, i + 1, next_i + 1))

        # Create vertex data for the cone

        format = GeomVertexFormat.get_v3n3c4t2()  # You can adjust this to your needs

        vdata = GeomVertexData("cone", format, GeomVertexData.UHStatic)

        vertex_writer = GeomVertexWriter(vdata, "vertex")

        for vertex in vertices:
            vertex_writer.add_data3f(*vertex)

        # Create geometry (tris)

        geom = Geom(vdata)

        for index in indices:
            triangle = GeomTriangles(Geom.UHStatic)

            triangle.add_vertices(*index)

            geom.add_primitive(triangle)

        # Create geom node

        geom_node = GeomNode("cone")

        geom_node.add_geom(geom)

        return NodePath(geom_node)

    def wandering(self, task):
        """Handles monster movement to random points."""

        if self.is_attacking:
            return Task.cont

        # Move towards the target position

        self.move_towards_target()

        # If we reached the target, set a new wandering target

        if (self.get_pos() - self.target_pos).length() < 0.1:
            self.set_new_wandering_target()

        return Task.cont

    def move_towards_target(self):
        """Moves the monster towards the target position."""

        direction = (self.target_pos - self.get_pos()).normalized()

        speed = 1

        self.set_pos(self.get_pos() + direction * speed)

    def set_new_wandering_target(self):
        """Set a new random target position within a defined area."""

        # Random position within a 10x10 unit square area (change this range as needed)

        x = random.uniform(-5, 5)

        y = random.uniform(-5, 5)

        z = 0  # Keeping the monster on the ground

        self.target_pos = Vec3(x, y, z)

    def weapon_swinging(self, task):
        """Periodically swing the weapon."""

        if self.is_moving or self.is_attacking:
            return Task.cont

        # Random interval for weapon swing (e.g., every 2-5 seconds)

        swing_interval = random.uniform(2, 5)

        if task.time > swing_interval:
            self.start_attack()  # Trigger attack animation or weapon swing

            task.time = 0  # Reset the timer

        return Task.cont

    def idle_animation(self, task):
        """Idle animation: oscillating or bobbing."""

        if self.is_moving or self.is_attacking:
            return Task.cont

        # Simulate some idle behavior here, like a slight bobbing motion

        self.set_h(self.get_h() + 1)  # Rotate around the Y-axis for visual effect

        return Task.cont

    def set_orientation(self, orientation):
        """Set the orientation (heading) of the monster."""

        self.set_h(orientation)

    def set_position(self, position):
        """Sets the position of the monster."""

        self.set_pos(position)  # Directly use NodePath's set_pos method

    def stop_idle(self):
        """Stop idle motion."""

        self.is_moving = False

        self.is_attacking = False

    def start_move(self):
        """Trigger a movement animation."""

        self.is_moving = True

    def stop_move(self):
        """Stop movement animation."""

        self.is_moving = False