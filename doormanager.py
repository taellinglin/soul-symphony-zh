import json
from direct.showbase.DirectObject import DirectObject
from panda3d.core import (
    Vec3, 
    NodePath, 
    CollisionNode, 
    CollisionBox, 
    BitMask32, 
    CollisionHandlerEvent,
    GeomNode,
    CollisionTraverser,
    TransparencyAttrib,
    Point3
)
import random

class DoorManager(DirectObject):
    def __init__(self, level, config_file, player=None):
        print("Initializing DoorManager...")
        self.level = level
        self.player = player
        self.activation_radius = 5  # Adjust this value to change activation distance
        self.doors = []  # Store found doors
        self.a_pressed = False
    
        
        # Accept both press and release of 'A'
        self.accept('ActionA', self.on_a_press)
        self.accept('ActionAup', self.on_a_release)
        self.near_door = False
        
        self.color_cycle_tasks = []
        
        # Simplified rainbow colors
        self.colors = [
            (1, 0, 0, 1),      # Red
            (1, 0.5, 0, 1),    # Orange
            (1, 1, 0, 1),      # Yellow
            (0, 1, 0, 1),      # Green
            (0, 0, 1, 1),      # Blue
            (0.29, 0, 0.51, 1),# Indigo
            (0.93, 0.51, 0.93, 1),  # Violet
        ]
        self.current_color_index = 0

    def get_doors(self):
        """Return the list of door nodes"""
        return self.doors

    def replace_door_nodes(self):
        print("Searching for door nodes...")
        
        if hasattr(self.level, 'ground'):
            ground = self.level.ground
            door_nodes = ground.findAllMatches("**/door*")
            print(f"Found {door_nodes.getNumPaths()} door nodes")
            
            for node in door_nodes:
                # Get the original door ID (should match doors.json)
                door_id = node.getName()
                if door_id.startswith("door"):  # Only process nodes that start with "door"
                    print(f"Processing door: {door_id}")

                    try:
                        door_model = loader.loadModel("./components/door.bam")
                        if not door_model:
                            continue
                        
                        # Keep the original door ID
                        door_model.setName(door_id)
                        
                        door_model.reparentTo(self.level.ground)
                        door_model.setPos(node.getPos(render))
                        door_model.setHpr(node.getHpr(render))
                        
                        # Debug print to see node hierarchy
                        print(f"Door model hierarchy for {door_id}:")
                        door_model.ls()
                        
                        # Make frame invisible but keep collision
                        frame = door_model.find("**/frame")
                        if not frame.isEmpty():
                            print("Found frame, making invisible")
                            frame.setTransparency(TransparencyAttrib.MAlpha)
                            frame.setAlpha(0)
                            frame.setColor(1, 1, 1, 0)  # Fully transparent
                        else:
                            print("Warning: Frame not found!")
                        
                        # Make collision nodes invisible
                        frame_collision = door_model.find("**/frame_collision")
                        if not frame_collision.isEmpty():
                            print("Setting up frame collision")
                            frame_collision.hide()
                            
                            cnode = CollisionNode(f'frame_collision_{door_id}')
                            bounds = frame_collision.getBounds()
                            center = bounds.getCenter()
                            min_point = bounds.getMin()
                            max_point = bounds.getMax()
                            
                            cbox = CollisionBox(center, 
                                              (max_point.getX() - min_point.getX()) / 2,
                                              (max_point.getY() - min_point.getY()) / 2,
                                              (max_point.getZ() - min_point.getZ()) / 2)
                            cnode.addSolid(cbox)
                            collision_np = frame_collision.attachNewNode(cnode)
                            cnode.setFromCollideMask(BitMask32.bit(1))
                            cnode.setIntoCollideMask(BitMask32.bit(1))
                            collision_np.hide()
                        else:
                            print("Warning: Frame collision not found!")
                        
                        # Hide warp collision
                        warp_collision = door_model.find("**/warp_collision")
                        if not warp_collision.isEmpty():
                            warp_collision.hide()
                        
                        # Make sure cubes are visible and colorable
                        cubes = door_model.findAllMatches("**/Cube*")
                        print(f"Found {cubes.getNumPaths()} cubes")
                        for cube in cubes:
                            cube.setTransparency(TransparencyAttrib.MAlpha)
                            cube.setColor(1, 0, 0, 1)  # Set initial color to red
                            cube.clearMaterial()
                            cube.setTextureOff(1)
                            cube.show()
                        
                        # Add door to the list
                        self.doors.append(door_model)
                        print(f"Added door {door_id} to doors list")
                        
                        # Start color cycling for this door
                        self.start_color_cycle(door_model)
                        
                        # Remove the original node
                        node.removeNode()
                        
                    except Exception as e:
                        print(f"Error processing door {door_id}: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"Skipping non-door node: {door_id}")

    def start_color_cycle(self, door_model):
        """Start color cycling for a specific door"""
        if door_model not in self.doors:
            self.doors.append(door_model)
        
        # Start color cycle if not already running
        if not taskMgr.hasTaskNamed('colorCycle'):
            taskMgr.doMethodLater(0.02, self.update_colors, 'colorCycle')

    def update_colors(self, task):
        """Update the colors of all doors"""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        
        # Update each door's cubes and warp plane
        for door in self.doors:
            # Color the cubes
            cubes = door.findAllMatches("**/Cube*")
            for i, cube in enumerate(cubes):
                color_index = (self.current_color_index + i) % len(self.colors)
                cube.setTransparency(TransparencyAttrib.MAlpha)
                cube.setColor(self.colors[color_index])
            
            # Color the warp plane
            warp = door.find("**/warp")
            if not warp.isEmpty():
                warp.setTransparency(TransparencyAttrib.MAlpha)
                warp.clearMaterial()
                warp.setTextureOff(1)
                warp.setColor(self.colors[self.current_color_index])
                warp.show()
        
        return task.again

    def set_player(self, player):
        """Set the player reference"""
        self.player = player
        print("Player reference updated in DoorManager")

    def cleanup(self):
        """Clean up resources"""
        self.doors = []
        taskMgr.remove('colorCycle')


    def on_a_press(self):
        """Handle 'A' button press"""
        self.a_pressed = True
        
    def on_a_release(self):
        """Handle 'A' button release"""
        self.a_pressed = False

    def set_current_door(self, door):
        """Set the current active door"""
        self.current_door = door
        print(f"Current door set to: {door.getName() if door else 'None'}")