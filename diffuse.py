from panda3d.core import Point3, Vec3, TransparencyAttrib
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, MouseWatcher, Camera, PointLight,LVecBase3f, LVecBase4f, CollisionNode, CollisionSphere, BitMask32, CollisionHandlerEvent, CollisionTraverser, AudioSound, CollisionBox, LVecBase3, LVector3, Vec4
from panda3d.core import TransformState
from panda3d.physics import LinearVectorForce
from panda3d.bullet import BulletWorld, BulletBoxShape
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletBoxShape, BulletSphereShape
from panda3d.core import CollisionNode, LVecBase3, BitMask32, NodePath, CollisionBox 
from panda3d.core import CollisionSphere
from panda3d.core import CollisionHandlerQueue, CollisionNode, CollisionSphere, BitMask32
import numpy as np
import random
import math
from math import sin
from math import pi
import pyaudio

class DiffusionVoxels(ShowBase):
    def __init__(self):
        super().__init__()
        p = pyaudio.PyAudio()
        self.time_step = 0
        # Initialize Bullet Physics world (if not already done in your code)
        if not hasattr(self, 'physics_world'):
            self.physics_world = BulletWorld()
            self.physics_world.setGravity(0, 0, 0) 
        self.setBackgroundColor(0, 0, 0)
        self.current_color_index = 0
        # Disable the default camera control and enable trackball controls
        self.disableMouse()
        self.useTrackball()
        self.world = BulletWorld()# Standard gravity
        # Initialize CollisionTraverser and Handler
        # Collision system initialization
        self.collision_traverser = CollisionTraverser()
        self.collision_handler = CollisionHandlerQueue()
        # Create a collider (example: a sphere)
        collider_node = CollisionNode('sphere_collider')
        collider_node.addSolid(CollisionSphere(0, 0, 0, 1))  # Example collider
        collider_node.setFromCollideMask(BitMask32.bit(1))  # Set "from" mask
        collider_node.setIntoCollideMask(BitMask32.bit(2))  # Set "into" mask
        collider_np = self.render.attachNewNode(collider_node)

        # Add collider to traverser and handler
        self.collision_traverser.addCollider(collider_np, self.collision_handler)
        # Grid size: 16x16x16
        self.grid_size = 8
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size), dtype=bool)  # Track cell state (alive or dead)
        self.transparency = np.ones((self.grid_size, self.grid_size, self.grid_size))  # Array to hold transparency values
        self.cycle_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    cube = self.create_cube_with_bullet(x, y, z, color=self.cycle_colors[self.current_color_index])
                    if self.current_color_index > len(self.cycle_colors):
                        self.current_color_index += 1
                    else:
                        self.current_color_index = 0
                    self.grid[(x, y, z)] = cube  # Ensure that this is a NodePath

                    # Store the initial position in the NumPy array
                    self.positions = np.array([x, y, z], dtype=np.float32)

        self.cubes = {}
        self.bells = {}
        self.voxels = []
        
        self.oscillation_speed = 1
        self.dimension_shift_speed = 1
        # Set the background color to black
        self.chime_sound = self.loader.loadSfx("./audio/chime_box.wav")
          # Set the grid size (can be adjusted as needed)
        

        # Oscillation settings
        self.oscillation_speed = 2  # Controls speed of oscillation
        self.dimension_shift_speed = 1
        # Set the background color to black
        if not self.chime_sound:
            print("Error: Could not load chime sound.")
            return

        self.chime_sound.setLoop(False)  # Ensure the sound doesn't loop automatically
        self.chime_sound.setVolume(1.0)  # Adjust volume as needed

        # Attach the sound to a moving NodePath
        self.sound_node = self.render.attachNewNode("BellSound")
          # Initial position for the sound
        

        # Set camera as the audio listener
        self.listener = self.camera



        self.cube_pivot = NodePath("CubePivot")
        self.cube_pivot.setPos(0.5,0.5,0.5)
        self.sound_node.setPos(0.5, 0.5, 0.5)
        self.cube_pivot.setHpr(0,0,0)
        self.cube_pivot.reparentTo(base.render)
        self.create_default_camera()
        self.create_grid()

        # Create a perpetual diffusion pattern
        self.create_perpetual_pattern()
        self.pivot = render.attachNewNode("Pivot")
        self.pivot.setPos(self.grid_size // 2, self.grid_size // 2, self.grid_size // 2)
        self.pivot.setHpr(0,0,0)
        self.pivot.reparentTo(base.render)
        
        base.cam.reparentTo(self.pivot)
        # Task manager to update cubes
        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.update_cubes, "update_cubes")
        self.taskMgr.add(self.check_voxel_bounce, "check_voxel_bounce")
        self.taskMgr.add(self.update_spheres, "update_spheres")
        self.pentatonic_frequencies = [523.25, 587.33, 659.25, 784.00, 880.00]  # C5, D5, E5, G5, A5

        # PyAudio setup
        self.p = pyaudio.PyAudio()

    def generate_sine_wave(self, frequency, duration=0.1, sample_rate=44100):
        """Generate a sine wave for a given frequency and duration."""
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = np.sin(2 * np.pi * frequency * t)
        return sine_wave.astype(np.float32)

    def play_sine_wave(self, frequency, duration=0.1):
        """Play a sine wave of the given frequency."""
        sine_wave = self.generate_sine_wave(frequency, duration)
        stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        stream.write(sine_wave.tobytes())
        stream.stop_stream()
        stream.close()
                            
    def play_chime_sound(self, pos):
        """Play the chime sound."""
        if self.chime_sound.status() != self.chime_sound.PLAYING:
            self.chime_sound.set3dAttributes(self.sound_node, pos)
            self.chime_sound.play()
    
    def create_default_camera(self):
        """
        Create and configure a default camera for the scene.
        """
        self.camera = base.cam
        self.cam.node().getLens().setFov(90)

        self.camera.reparentTo(base.render)
        self.camera.setPos(0, -10, 0)  # Position the camera
        self.camera.setHpr(0,0,0)
        self.camera.lookAt(self.cube_pivot)  # Make the camera look at the center

    def create_grid(self):
        """
        Create the 16x16x16 grid of cubes, assigning them random colors and initial states.
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    color = random.choice(self.cycle_colors)  # Random color
                    cube = self.create_cube_with_bullet(x, y, z, color)
                    bell = self.create_sphere_with_bullet(x, y, z, color)
                    self.grid[x, y, z] = random.choice([True, False])  # Random initial state (alive or dead)
                    self.cubes[(x, y, z)] = cube
                    self.bells[(x, y, z)] = bell

    def create_cube_with_bullet(self, x, y, z, color):
        # Create the cube model
        cube = self.loader.loadModel("models/box")
        cube.setTransparency(TransparencyAttrib.MAlpha)
        cube.setTextureOff(1)
        cube.setScale(1)
        cube.setPos(x, y, z)
        if ((self.grid), False):  # If the cell is "alive"
            color = self.cycle_colors[(x + y + z) % len(self.cycle_colors)]
            cube.setColorScale(self.get_color_from_name(color))  # Apply cycling color
        else:  # If the cube is "dead"
            cube.setColorScale(self.get_color_from_name('transparent'))  # Make transparent

        cube.reparentTo(self.render)

        # Create Bullet collision shape for the cube
        box_size = 1  # Size of the cube
        box_shape = BulletBoxShape(LVecBase3(box_size, box_size, box_size))

        # Create the Bullet rigid body node for the cube
        cube_rb_node = BulletRigidBodyNode(f"cube_{x}_{y}_{z}")
        cube_rb_node.addShape(box_shape)

        # Attach the rigid body to the scene graph
        cube_collision = self.render.attachNewNode(cube_rb_node)
        cube_collision.setPos(x, y, z)

        # Add the cube to the Bullet world
        self.world.attachRigidBody(cube_rb_node)

        # Check if the cube is alive or dead and update the color accordingly
        
        # Return the cube model and its rigid body
        return cube, cube_collision

    def create_sphere_with_bullet(self, x, y, z, color):
        # Create the sphere model
        sphere = self.loader.loadModel("models/orb.bam")
        sphere.setTransparency(TransparencyAttrib.MAlpha)
        sphere.setTextureOff(1)
        sphere.setScale(0.05)  # Set the desired scale of the sphere
        sphere.setPos(x, y, z)
        if ((self.grid), False):  # If the cell is "alive"
            color = self.cycle_colors[(x + y + z) % len(self.cycle_colors)]
            sphere.setColor(self.get_color_from_name(color))  # Apply cycling color
        else:  # If the cube is "dead"
            sphere.setColor(self.get_color_from_name('transparent'))  # Make transparent

        sphere.reparentTo(self.render)
        
        # Set the color of the sphere using the provided color name
        sphere = self.get_color_from_name(color)  # Apply color to the sphere

        # Create Bullet collision shape for the sphere
        sphere_radius = 0.05  # Radius of the sphere
        sphere_shape = BulletSphereShape(sphere_radius)

        # Create the Bullet rigid body node for the sphere
        sphere_rb_node = BulletRigidBodyNode(f"sphere_{x}_{y}_{z}")
        sphere_rb_node.addShape(sphere_shape)

        # Attach the rigid body to the scene graph
        sphere_collision = self.render.attachNewNode(sphere_rb_node)
        sphere_collision.setPos(x-1, y-1, z-1)

        # Add the sphere to the Bullet world
        self.world.attachRigidBody(sphere_rb_node)

        # Return the sphere model and its rigid body
        return sphere, sphere_collision

    def play_chime_sound(self, position):
        """Play the chime sound at the specified position."""
        if not self.chime_sound.status() == self.chime_sound.PLAYING:
            self.chime_sound.setVolume(1)  # Set the volume
            self.chime_sound.setPlayRate(1)  # Set the play rate
            self.chime_sound.setPos(position)  # Set position of the sound
            self.chime_sound.play()



    def setup_physics(self):
        """Setup the physics engine."""
        self.physics_world = NodePath(ForceNode("root"))  # Root of the physics world
        self.physics_world.reparentTo(self.render)
                
    def play_chime_sound_at_collision(self, entry):
        """Play the chime sound at the collision location."""
        # Get the positions of the colliding objects
        from_node = entry.getFromNodePath()
        into_node = entry.getIntoNodePath()

        # Determine the collision point
        collision_point = entry.getSurfacePoint(self.render)

        # Set the sound position to the collision point
        if self.chime_sound:
            self.chime_sound.set3dAttributes(
                (collision_point.x, collision_point.y, collision_point.z),
                velocity=(0, 0, 0)
            )
            self.chime_sound.play()

    def diffusion_pattern(self, t):
        """Generate a diffusion pattern to control transparency."""
        # Example: Oscillation pattern for transparency
        pattern = np.sin(np.pi * t + np.indices((self.grid_size, self.grid_size, self.grid_size)).sum(axis=0) * 0.1)
        # Normalize to [0, 1] range for transparency
        return (pattern + 1) / 2

    def update_transparency(self, t):
        """Update the transparency of cubes based on the diffusion pattern."""
        # Get the new transparency pattern based on time
        new_transparency = self.diffusion_pattern(t)

        # Apply the new transparency to the cubes
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    transparency_value = new_transparency[x, y, z]
                    cube = self.cubes.get((x, y, z))
                    if isinstance(cube, NodePath):
                        # Set transparency using the pattern value (modulate the transparency)
                        cube.setTransparency(True)
                        cube.setColorScale(1, 1, 1, transparency_value)  # R, G, B, A (transparency)
                    else:
                        print(f"Error: Cube at {(x, y, z)} is of type {type(cube)}, expected NodePath.")
    
    def update_cubes(self, task):
        """Update the cube positions and transparency."""
        t = globalClock.getFrameTime()

        # Apply dimensional oscillation shifts and updates
        oscillation_x = self.grid_size * math.sin(self.oscillation_speed * t)
        oscillation_y = self.grid_size * math.cos(self.oscillation_speed * t)
        oscillation_z = self.grid_size * math.sin(self.oscillation_speed * t + math.pi / 2)

        dimension_shift_x = self.grid_size * math.sin(self.dimension_shift_speed * t + math.pi / 4)
        dimension_shift_y = self.grid_size * math.cos(self.dimension_shift_speed * t)
        dimension_shift_z = self.grid_size * math.sin(self.dimension_shift_speed * t + math.pi)

        # Loop through the grid and shift positions in 3D space
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    cube = self.cubes.get((x, y, z))  # Fetch cube NodePath

                    if isinstance(cube, NodePath):  # Ensure that cube is a valid NodePath
                        # Compute new positions based on oscillation and dimension shift
                        new_pos = LVector3(
                            (x + oscillation_x + dimension_shift_x),
                            (y + oscillation_y + dimension_shift_y),
                            (z + oscillation_z + dimension_shift_z)
                        )

                        # Move the cube to the new position
                        cube.setPos(new_pos)

                        # Map the position to a note in the pentatonic scale
                        # You can modify this to assign notes based on position
                        note_index = (x + y + z) % len(self.pentatonic_frequencies)
                        frequency = self.pentatonic_frequencies[note_index]
                        self.play_sine_wave(frequency)

        # Update transparency with the diffusion pattern (not included in this snippet)
        self.update_transparency(t)

        return task.cont
    

    def generate_sine_wave(frequency, duration=0.1, sample_rate=44100):
        """Generate a sine wave for a given frequency and duration."""
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = np.sin(2 * np.pi * frequency * t)
        return sine_wave.astype(np.float32)

    def play_sine_wave(frequency, duration=0.1):
        """Play a sine wave of the given frequency."""
        sine_wave = generate_sine_wave(frequency, duration)
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        stream.write(sine_wave.tobytes())
        stream.stop_stream()
        stream.close()
    def play_3d_audio(self, audio_file, position):
        """Play 3D audio at a given position."""
        audio_manager = AudioManager()
        sound = audio_manager.loadSound(audio_file)
        sound.setLoop(False)  # Non-looping for now
        sound.setVolume(1.0)  # Adjust as necessary
        sound.play()

        # Set position of sound
        sound.setPosition(position)
        return sound

    def map_harmonics_to_pentatonic_scale(self, frequency):
        """Map frequency to the nearest note in the pentatonic scale."""
        pentatonic_frequencies = [261.63, 293.66, 329.63, 392.00, 440.00]  # C, D, E, G, A
        closest_freq = min(pentatonic_frequencies, key=lambda x: abs(x - frequency))
        return closest_freq

    def diffusion_pattern(self, t):
            """Generate a diffusion pattern to control transparency."""
            # Example: Oscillation pattern for transparency
            pattern = np.sin(np.pi * t + np.indices((self.grid_size, self.grid_size, self.grid_size)).sum(axis=0) * 0.1)
            # Normalize to [0, 1] range for transparency
            return (pattern + 1) / 2

    def update_transparency(self, t):
        """Update the transparency of cubes based on their alive/dead state."""
        # Get the new transparency pattern based on time
        new_transparency = self.diffusion_pattern(t)

        # Apply the new transparency to the cubes
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    transparency_value = 1.0 if self.grid[x, y, z] else 0.0  # Alive cubes are opaque, dead ones are transparent
                    cube = self.cubes.get((x, y, z))
                    if isinstance(cube, NodePath):
                        # Set transparency based on the cube's state (alive/dead)
                        cube.setTransparency(True)
                        cube.setColorScale(0, 0, 0, transparency_value)  # R, G, B, A (transparency)
                    else:
                        print(f"Error: Cube at {(x, y, z)} is of type {type(cube)}, expected NodePath.")
    
    def update_cubes(self, task):
        """Update the cube positions and transparency."""
        t = globalClock.getFrameTime()

        # Apply dimensional oscillation shifts and updates
        oscillation_x = self.grid_size * math.sin(self.oscillation_speed * t)
        oscillation_y = self.grid_size * math.cos(self.oscillation_speed * t)
        oscillation_z = self.grid_size * math.sin(self.oscillation_speed * t + math.pi / 2)

        dimension_shift_x = self.grid_size * math.sin(self.dimension_shift_speed * t + math.pi / 4)
        dimension_shift_y = self.grid_size * math.cos(self.dimension_shift_speed * t)
        dimension_shift_z = self.grid_size * math.sin(self.dimension_shift_speed * t + math.pi)

        # Loop through the grid and shift positions in 3D space
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    cube = self.cubes.get((x, y, z))  # Fetch cube NodePath

                    if isinstance(cube, NodePath):  # Ensure that cube is a valid NodePath
                        # Compute new positions based on oscillation and dimension shift
                        new_pos = LVector3(
                            (x + oscillation_x + dimension_shift_x),
                            (y + oscillation_y + dimension_shift_y),
                            (z + oscillation_z + dimension_shift_z)
                        )

                        # Move the cube to the new position
                        cube.setPos(new_pos)
                        self.positions[(x, y, z)] = new_pos

        # Update transparency with the diffusion pattern and cube state
        self.update_transparency(t)

        return task.cont

    def update_spheres(self, task):
        dx, dy, dz = 0.5, 0.5, -0.05  # Movement vector

        for sphere in self.bells.values():
            if isinstance(sphere, NodePath):
                pos = sphere.getPos()
                sphere.setPos(pos + LVector3(dx, dy, dz))

                # Perform collision detection
                self.collision_traverser.traverse(self.render)

                # Handle collisions
                if self.collision_handler.getNumEntries() > 0:
                    self.collision_handler.sortEntries()  # Sort collisions by distance
                    for entry in self.collision_handler.entries:
                        print(f"Collision between {sphere.getFromNodePath()} and {cube.getIntoNodePath()}")
                        collision_point = entry.getSurfacePoint(self.render)
                        self.play_3d_audio("audio/chime_box.wav", collision_point)

                return task.cont



    def play_3d_audio(self, file_path, position):
        """Play 3D audio at the given position."""
        sound = self.loader.loadSfx(file_path)
        if sound:
            sound.set3dAttributes(position.x, position.y, position.z, 0, 0, 0)
            sound.setLoop(False)  # Ensure the sound doesn't loop
            sound.play()
        else:
            print(f"Error: Could not load sound file at {file_path}")


    def update(self, task):
        """Update the grid and cycle transparency and diffusion."""
        new_grid = np.zeros_like(self.grid)
        
        # Harmonic transparency effect (oscillating effect over time)
        harmonic_transparency = self.calculate_harmonic_transparency(self.time_step)

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    alive_neighbors = self.count_alive_neighbors(x, y, z)
                    is_alive = self.grid[x, y, z]

                    # Basic Game of Life rules (diffusion)
                    if is_alive and (alive_neighbors == 2 or alive_neighbors == 3):
                        new_grid[x, y, z] = True
                    elif not is_alive and alive_neighbors == 3:
                        new_grid[x, y, z] = True
                    else:
                        new_grid[x, y, z] = False
                    
                    # Apply transparency based on harmonic function
                    self.update_cube_visual(x, y, z, harmonic_transparency)
        self.pivot.setH(self.pivot.getH()+1)
        self.pivot.setP(self.pivot.getP()+1)
        self.pivot.setR(self.pivot.getR()+1)
        self.grid = new_grid
        self.time_step += 1  # Increment time step for oscillation
        return task.cont

    def calculate_harmonic_transparency(self, time_step):
        """Calculate a harmonic transparency value using a sine function."""
        # Use sine wave for a smooth oscillation between 0 and 1
        # Adjust the frequency (e.g., 0.1) and amplitude (e.g., 1) to control the speed and intensity of oscillation
        transparency = (sin(2 * pi * 0.1 * time_step) + 1) / 2  # This will oscillate between 0 and 1
        return transparency

    def update_cube_visual(self, x, y, z, transparency):
        """Update the visual appearance of a cube with harmonic transparency."""
        if self.grid[x, y, z]:  # If the cube is alive
            color = Vec4(1, 1, 1, transparency)  # White with oscillating transparency
        else:
            color = Vec4(0, 0, 0, 0)  # Transparent if not alive

        # You could set the transparency/appearance for a cube here based on its position in the grid
        # Assuming you have a method or some 3D object representing each cube
        cube = self.get_cube_at(x, y, z)
        if cube:
            cube.setColor(color)

    def get_cube_at(self, x, y, z):
        """Get or create a cube at the given grid coordinates."""
        # You would implement this method to return a 3D cube object at the grid position
        pass


    def get_color_from_name(self, color_name):
        """Convert color names to RGBA color values."""
        color_map = {
            'red': (1, 0, 0, 0.1),
            'orange': (1, 0.647, 0, 0.1),
            'yellow': (1, 1, 0, 0.1),
            'green': (0, 1, 0, 0.1),
            'blue': (0, 0, 1, 0.1),
            'indigo': (0.294, 0, 0.510, 0.1),
            'violet': (0.933, 0.509, 0.933, 0.1),
        }
        return color_map.get(color_name, (0, 0, 0, 0.0))  
    def get_color_from_name(self, color_name):
        """
        Convert color names to RGBA color values.
        """
        color_map = {
            'red': (1, 0, 0, 0.1),  # Adding alpha to make it semi-transparent
            'orange': (1, 0.647, 0, 0.1),
            'yellow': (1, 1, 0, 0.1),
            'green': (0, 1, 0, 0.1),
            'blue': (0, 0, 1, 0.1),
            'indigo': (0.294, 0, 0.510, 0.1),
            'violet': (0.933, 0.509, 0.933, 0.1),
        }
        return color_map.get(color_name, (0, 0, 0, 0))  # Default to white with transparency if color is unknown

    def create_perpetual_pattern(self):
        """
        Create a small initial perpetual pattern that keeps evolving, with tessellated gliders
        coming from all corners of the grid.
        """
        # Define the basic glider pattern (you can modify this for other gliders or structures)
        pattern = [
            (0, 0, 0), (1, 0, 0), (2, 0, 0),
            (0, 1, 0), (1, 1, 0), (2, 1, 0),
            (1, 2, 0),
            (0, 0, 1), (1, 0, 1), (2, 0, 1),
            (0, 1, 1), (1, 1, 1), (2, 1, 1),
            (1, 2, 1)
        ]

        # Apply tessellation and symmetry by placing gliders at all corners and mirrored across the grid
        offsets = [
            (0, 0, 0),  # Top-left-front corner
            (self.grid_size-1, 0, 0),  # Top-right-front corner
            (0, self.grid_size-1, 0),  # Top-left-back corner
            (0, 0, self.grid_size-1),  # Bottom-left-front corner
            (self.grid_size-1, self.grid_size-1, 0),  # Top-right-back corner
            (self.grid_size-1, 0, self.grid_size-1),  # Bottom-right-front corner
            (0, self.grid_size-1, self.grid_size-1),  # Bottom-left-back corner
            (self.grid_size-1, self.grid_size-1, self.grid_size-1),  # Bottom-right-back corner
        ]

        # Iterate through each corner, applying the mirrored tessellating glider pattern
        for offset in offsets:
            ox, oy, oz = offset
            for x, y, z in pattern:
                # Place the pattern at various mirrored positions, based on corner offset
                self.grid[(ox + x) % self.grid_size, (oy + y) % self.grid_size, (oz + z) % self.grid_size] = True

        # Create a symmetrical pattern in the grid
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    # Add additional mirrored or tessellated patterns to the opposite sides
                    self.grid[x, self.grid_size - 1 - y, z] = self.grid[x, y, z]
                    self.grid[x, y, self.grid_size - 1 - z] = self.grid[x, y, z]
                    self.grid[self.grid_size - 1 - x, y, z] = self.grid[x, y, z]



    def count_alive_neighbors(self, x, y, z):
        """
        Count how many neighboring cubes are "alive" (True).
        """
        neighbors = [
            (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        alive_count = 0

        for dx, dy, dz in neighbors:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 0 <= nz < self.grid_size:
                if self.grid[nx, ny, nz]:
                    alive_count += 1
        return alive_count

    def check_voxel_bounce(self, task):
        """
        Check if a voxel has stopped moving and either bounce it or teleport it to a random location.
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if not self.grid[x, y, z]:
                        # If the voxel is dead, randomly teleport it or bounce it to a random position
                        if random.random() < 0.1:  # 10% chance to teleport to a random voxel
                            new_x, new_y, new_z = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
                            self.grid[new_x, new_y, new_z] = True
                            cube, _ = self.cubes[(new_x, new_y, new_z)]
                            cube.setColorScale(self.get_color_from_name(random.choice(self.cycle_colors)))
                        else:
                            # Bounce the voxel back to a neighboring position
                            dx, dy, dz = random.choice([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
                            new_x, new_y, new_z = (x + dx) % self.grid_size, (y + dy) % self.grid_size, (z + dz) % self.grid_size
                            self.grid[new_x, new_y, new_z] = True
                            # Unpack the cube and collision node correctly
                            cube, _ = self.cubes[(new_x, new_y, new_z)]

                            # Set the color for the cube
                            cube.setColorScale(self.get_color_from_name(random.choice(self.cycle_colors)))
                            return task.cont  # Continue the task


app = DiffusionVoxels()
app.run()
