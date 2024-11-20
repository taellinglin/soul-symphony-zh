from panda3d.core import NodePath, Vec3, Point3, CollisionNode, CollisionBox, LVector4, GeomVertexData, GeomVertexWriter, Geom, GeomTriangles, GeomNode
from direct.task import Task
import math


class ProceduralWeaponSwinger(NodePath):
    def __init__(self, parent=None, weapon_type='sword'):
        super().__init__("ProceduralWeaponSwinger")
        self.reparent_to(parent if parent else base.render)
        self.weapon_type = weapon_type
        self.sword = None
        self.swinging = False

        # Generate the weapon
        self.generate_weapon()

        # Set up the swinging task
        self.swing_angle = 0
        self.swing_speed = 30  # Degrees per second
        self.swing_duration = 1  # Swing duration in seconds
        self.swinging_start_time = 0

        # Add a task for the swinging animation
        taskMgr.add(self.swing_weapon, "SwingWeaponTask")

        # Add a task for the color cycling
        self.color_cycle_duration = 5  # Duration for one full cycle (in seconds)
        taskMgr.add(self.color_cycle, "ColorCycleTask")

    def generate_weapon(self):
        """Generates a procedural weapon."""
        if self.weapon_type == 'sword':
            self.sword = self.create_sword()
        elif self.weapon_type == 'axe':
            self.sword = self.create_axe()
        elif self.weapon_type == 'hammer':
            self.sword = self.create_hammer()

        self.sword.reparent_to(self)

    def create_sword(self):
        """Generates a sword weapon."""
        blade_length = 1.0
        handle_length = 0.3
        width = 0.05

        sword = NodePath("Sword")

        # Create blade (long part of sword)
        blade = self.create_box(blade_length, width, width)
        blade.set_pos(0, 0, blade_length / 2)
        blade.set_color(0.8, 0.8, 0.8, 1)  # Gray color for blade
        blade.reparent_to(sword)

        # Create handle (short part of sword)
        handle = self.create_box(handle_length, width * 1.5, width * 1.5)
        handle.set_pos(0, 0, -handle_length / 2)
        handle.set_color(0.6, 0.4, 0.2, 1)  # Brown color for handle
        handle.reparent_to(sword)

        return sword

    def create_axe(self):
        """Generates an axe weapon."""
        blade_width = 0.3
        blade_length = 0.7
        handle_length = 0.8
        handle_width = 0.1

        axe = NodePath("Axe")

        # Create blade (large flat part)
        blade = self.create_box(blade_length, blade_width, 0.05)
        blade.set_pos(0, 0, blade_length / 2)
        blade.set_color(0.7, 0.7, 0.7, 1)  # Metal color for blade
        blade.reparent_to(axe)

        # Create handle
        handle = self.create_box(handle_length, handle_width, handle_width)
        handle.set_pos(0, 0, -handle_length / 2)
        handle.set_color(0.6, 0.4, 0.2, 1)  # Wood color for handle
        handle.reparent_to(axe)

        return axe

    def create_hammer(self):
        """Generates a hammer weapon."""
        head_width = 0.4
        head_height = 0.2
        head_depth = 0.4
        handle_length = 1.2
        handle_width = 0.1

        hammer = NodePath("Hammer")

        # Create hammerhead (rectangular block)
        head = self.create_box(head_height, head_width, head_depth)
        head.set_pos(0, 0, head_height / 2)
        head.set_color(0.5, 0.5, 0.5, 1)  # Gray color for head
        head.reparent_to(hammer)

        # Create handle
        handle = self.create_box(handle_length, handle_width, handle_width)
        handle.set_pos(0, 0, -handle_length / 2)
        handle.set_color(0.6, 0.4, 0.2, 1)  # Wood color for handle
        handle.reparent_to(hammer)

        return hammer

    def create_box(self, length, width, height):
        """Generates a basic rectangular box."""
        vertices = [
            (-length / 2, -width / 2, -height / 2),
            (length / 2, -width / 2, -height / 2),
            (length / 2, width / 2, -height / 2),
            (-length / 2, width / 2, -height / 2),
            (-length / 2, -width / 2, height / 2),
            (length / 2, -width / 2, height / 2),
            (length / 2, width / 2, height / 2),
            (-length / 2, width / 2, height / 2),
        ]
        indices = [
            (0, 1, 2), (0, 2, 3),  # front
            (4, 5, 6), (4, 6, 7),  # back
            (0, 1, 5), (0, 5, 4),  # bottom
            (2, 3, 7), (2, 7, 6),  # top
            (1, 2, 6), (1, 6, 5),  # right
            (0, 3, 7), (0, 7, 4)   # left
        ]

        # Create vertex data for the box
        vdata = GeomVertexData("box", GeomVertexFormat.get_v3(), GeomVertexData.UHStatic)
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

    def swing_weapon(self, task):
        """Handles the swinging animation of the weapon."""
        if self.swinging:
            # Calculate the angle of swing (swinging back and forth)
            elapsed_time = globalClock.get_frame_time() - self.swinging_start_time
            swing_progress = (elapsed_time % self.swing_duration) / self.swing_duration
            angle = math.sin(swing_progress * 2 * math.pi) * 60  # Swinging from -60 to +60 degrees

            # Apply the rotation to the weapon
            self.sword.set_h(angle)
        return Task.cont

    def color_cycle(self, task):
        """Handles the color cycling of the weapon in ROYGBIV sequence."""
        elapsed_time = globalClock.get_frame_time()
        
        # Define the ROYGBIV colors (Red, Orange, Yellow, Green, Blue, Indigo, Violet)
        colors = [
            (1.0, 0.0, 0.0),  # Red
            (1.0, 0.5, 0.0),  # Orange
            (1.0, 1.0, 0.0),  # Yellow
            (0.0, 1.0, 0.0),  # Green
            (0.0, 0.0, 1.0),  # Blue
            (0.3, 0.0, 0.5),  # Indigo
            (0.5, 0.0, 1.0),  # Violet
        ]
        
        # Calculate the total number of colors in the ROYGBIV spectrum
        num_colors = len(colors)
        
        # Use the elapsed time to determine which color to display
        color_progress = (elapsed_time / self.color_cycle_duration) % 1  # Value between 0 and 1
        
        # Determine which color in the spectrum should be displayed
        color_index = int(color_progress * num_colors)
        current_color = colors[color_index]
        
        # Apply the color to the weapon
        self.sword.set_color(LVector4(current_color[0], current_color[1], current_color[2], 1))
        
        return Task.cont

    def start_swing(self):
        """Start the swinging action."""
        if not self.swinging:
            self.swinging = True
            self.swinging_start_time = globalClock.get_frame_time()

    def stop_swing(self):
        """Stop the swinging action."""
        if self.swinging:
            self.swinging = False
            self.sword.set_h(0)  # Reset the weapon to its neutral position

