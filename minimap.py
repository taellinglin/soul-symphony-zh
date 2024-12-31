from math import sin, pi
from panda3d.core import DirectionalLight, Point3
from panda3d.core import NodePath, Material, TransparencyAttrib, Texture
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec4 
import random
from panda3d.core import CullFaceAttrib

class MiniMap(DirectObject):

    def __init__(self, base, level_model_path, texture_path=None, size=0.35, transparency=0.25):
        """
        Initializes the minimap with a single level model and optional texture.
        :param base: The Panda3D base instance.
        :param level_model_path: Path to the 3D model of the level.
        :param texture_path: Path to the texture to apply to the model (optional).
        :param size: Scale factor for the minimap size.
        :param transparency: Transparency level of the minimap (0.0 to 1.0).
        """
        self.base = base
        self.size = size
        self.transparency = transparency
        self.colors = [
            (1, 0, 0, self.transparency),  # Red
            (1, 0.5, 0, self.transparency),  # Orange
            (1, 1, 0, self.transparency),  # Yellow
            (0, 1, 0, self.transparency),  # Green
            (0, 0, 1, self.transparency),  # Blue
            (0.5, 0, 1, self.transparency),  # Indigo
            (1, 0, 1, self.transparency),  # Violet
        ]

        self.color_idx = -1
        # Load the level model
        self.level_model = self.base.loader.loadModel(level_model_path)
        self.level_model.setTransparency(TransparencyAttrib.MAlpha)
        self.level_model.setColor(1, 1, 1, self.transparency)  # Apply transparency
        self.level_model.reparentTo(self.base.render)

        # Apply texture if provided
        if texture_path:
            texture = self.base.loader.loadTexture(texture_path)
            self.level_model.setTexture(texture)

        # Attach the level model to the minimap root node
        self.minimap_root = self.base.aspect2d.attachNewNode("MinimapRoot")
        self.minimap_root.setTransparency(TransparencyAttrib.MAlpha)
        self.minimap_root.setScale(self.size)
        self.minimap_root.setPos(1.0 - self.size, 0, 0.2)  # Bottom-right corner

        self.level_model.reparentTo(self.minimap_root)
        self._adjust_minimap_level_model()

        # Player dot
        self.player_dot = self._create_player_dot()

    def _adjust_minimap_level_model(self):
        """Resizes and repositions the level model relative to the camera."""
        bounds_min, bounds_max = self.level_model.getTightBounds()
        size = bounds_max - bounds_min
        center = (bounds_min + bounds_max) / 2

        if size.x == 0 or size.z == 0:
            print("Error: Invalid size for the level model.")
            return

        scale = 2.0 / max(size.x, size.z)  # Normalize size to fit in the minimap
        self.level_model.setScale(scale)
        self.level_model.setPos(-center.x * scale, 0, -center.z * scale)
        self.level_model.setHpr(0, 45, 0)  # Top-down view

    def update(self, player_position, player_hpr):
        """Updates the 3D minimap with player position, correctly scaled."""

        # Get level bounds and calculate scaling
        bounds_min, bounds_max = self.level_model.getTightBounds()
        size = bounds_max - bounds_min
        center = (bounds_min + bounds_max) / 2
        level_scale = 1.0 / max(size.x, size.z)  # Scale to fit minimap bounds

        # Convert player position to minimap space
        minimap_player_pos = (player_position - center) * level_scale

        # Update player dot position relative to its parent
        self.player_dot.setPos(self.level_model, minimap_player_pos)

        # Update player dot orientation
        self.player_dot.setHpr(player_hpr)

        # Height representation (using color)
        min_height = bounds_min.y
        max_height = bounds_max.y
        height_range = max_height - min_height
        normalized_height = (player_position.y - min_height) / height_range if height_range != 0 else 0
        red = normalized_height
        blue = 1 - normalized_height
        green = 0
        self.player_dot.setColor(random.choice(self.colors))

        self.level_model.setColor(random.choice(self.colors))


    def _adjust_minimap_level_model(self):
        """Resizes and repositions the level model."""
        bounds_min, bounds_max = self.level_model.getTightBounds()
        size = bounds_max - bounds_min
        center = (bounds_min + bounds_max) / 2

        if size.x == 0 or size.z == 0:
            print("Error: Invalid size for the level model.")
            return

        scale = 1.0 / max(size.x, size.z)  # Normalize size
        print(f"Level Model Initial Scale: {scale}") #Print this value
        self.level_model.setScale(scale)
        self.level_model.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        self.level_model.setPos(-center.x * scale, -center.y * scale, -center.z * scale) #Adjust all axis
        self.level_model.setHpr(0,45, 0)  # Top-down view
    def _create_player_dot(self):
        """Creates a player dot with textures, scaling proportionally."""
        dot = self.base.loader.loadModel("models/orb.bam")
        if not dot:
            print("Error: Could not load orb.bam!")
            return None  # Handle loading failure

        # Clear any render states and ensure textures are enabled
        dot.clearTexture()  # Clear old textures if any
        dot.setColor(1, 1, 1, 1)  # Reset to ensure no tint
        dot.setTransparency(False)  # Ensure transparency doesn't interfere

        bounds_min, bounds_max = self.level_model.getTightBounds()
        size = bounds_max - bounds_min
        if size.x == 0 or size.z == 0:
            print("Error: Invalid level model size. Cannot scale dot.")
            return dot  # Return the dot even if it is not scaled

        scale = 0.010 * max(size.x, size.z) / self.size
        dot.setScale(scale)

        dot.reparentTo(self.minimap_root)
        
        # Debug: Confirm if the texture is applied
        print(f"Dot has texture: {dot.hasTexture()}")
        print(dot)
        return dot


    def update_minimap_position(self, padding=5):
        """
        Dynamically updates the minimap position to stay in the bottom-right corner
        with a specified padding. Also updates the player marker and circle to match
        the same position and rotation as the minimap.
        :param padding: Padding from the edges of the screen (in pixels).
        """
        window_width, window_height = self.base.win.getSize()

        # Calculate the position based on window size, minimap size, and padding
        norm_x = (window_width - self.size * 100 - padding) / window_width
        norm_y = -((window_height - self.size * 100 - padding) / window_height)  # Flip the Y axis

        # Set the minimap position
        self.minimap_root.setPos(norm_x, norm_y,0)

        # Apply the same position to the player marker and circle
        #self.player_dot.setPos(self.minimap_root.getPos())
        #self.player_dot.setH(self.minimap_root.getH())  # Same rotation as minimap




    def color_cycle(self, cycle_duration=3):
        """
        Cycles through colors (like a rainbow) for the level model.
        :param cycle_duration: Duration of the color cycle in seconds.
        """
        # Define the colors to cycle through (using Vec4 for RGBA colors)
        colors = [
            Vec4(1, 0, 0, 1),  # Red
            Vec4(1, 1, 0, 1),  # Yellow
            Vec4(0, 1, 0, 1),  # Green
            Vec4(0, 1, 1, 1),  # Cyan
            Vec4(0, 0, 1, 1),  # Blue
            Vec4(1, 0, 1, 1),  # Magenta
            Vec4(1, 0, 0, 1),  # Red (back to start)
        ]

        # Create a loop to cycle through the colors continuously
        self.color_task = self.base.taskMgr.add(self._color_cycle_task, "color_cycle_task", extraArgs=[cycle_duration, colors])

    def _color_cycle_task(self, cycle_duration, colors, task):
        """
        Task to update the color cycling over time.
        :param cycle_duration: Duration of one full color cycle.
        :param colors: List of colors to cycle through.
        :param task: The task parameter.
        """
        t = self.base.globalClock.getFrameTime()  # Current time in seconds
        
        # Calculate the index of the current color based on time
        color_index = int((t / cycle_duration) * len(colors)) % len(colors)
        
        # Set the color of the level model
        self.level_model.setColor(colors[color_index])

        return task.cont  # Continue the task

