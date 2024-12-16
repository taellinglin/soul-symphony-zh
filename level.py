import os

from audio3d import audio3d

from npc import npc

from letters import Letters

from math import sin, floor
from doormanager import DoorManager
from random import choice, randint, uniform

from monsterman import MonsterManager

from monsterman import YinYangMonster

import random

from player import player

from panda3d.bullet import BulletWorld

from panda3d.bullet import BulletRigidBodyNode

from panda3d.bullet import BulletDebugNode

from panda3d.bullet import BulletTriangleMesh

from panda3d.bullet import BulletTriangleMeshShape

from panda3d.core import Vec3, Vec4

from panda3d.core import BitMask32

from panda3d.core import TextNode

from panda3d.core import NodePath

from panda3d.core import Material

from panda3d.core import CullFaceAttrib

from panda3d.core import (
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionRay,
    Point3,
    CollisionNode,
    CollisionPolygon,
    GeomVertexReader,
    GeomNode,
)


DEBUG = False



    
class Level:
    def __init__(self, player=None, lvl=None, arcade_lvl=None):
        # Add cleanup of existing physics/collision objects if they exist     
        # Convert lvl to int if it's a string and assign to self.lvl
        self.lvl = lvl
        self.arcade_lvl = arcade_lvl
        print(f"level: ", self.lvl)
        self.audio = audio3d()
        
        self.npcs = []
        self.npc_mounts = []
        self.portals = []
        self.player = player
        self.doors = []
        self.levels = base.levels
        self.arcade_levels = []
        self.current_arcade = arcade_lvl
        self.floortextures = self.load_textures_from_directory(
            "./graphics/patterns/floor"
        )

        self.walltextures = self.load_textures_from_directory(
            "./graphics/patterns/wall"
        )

        self.ceiltextures = self.load_textures_from_directory(
            "./graphics/patterns/ceiling"
        )

        # Define colors for cycling

        self.colors = [
            Vec4(1, 0, 0, 1),  # Red
            Vec4(1, 0.5, 0, 1),  # Orange
            Vec4(1, 1, 0, 1),  # Yellow
            Vec4(0, 1, 0, 1),  # Green
            Vec4(0, 0, 1, 1),  # Blue
            Vec4(0.29, 0, 0.51, 1),  # Indigo
            Vec4(0.56, 0, 1, 1),  # Violet
        ]

        
        self.portal_template = base.loader.loadModel("components/portal00.bam")

        self.letterlist = Letters()
        
        self.monster_manager = MonsterManager(base.render)

        self.monsters = self.monster_manager.place_monsters([], num_monsters=10)
        

        self.cTrav = CollisionTraverser()

        self.handler = CollisionHandlerQueue()
        self.clock = 0

        self.clock2 = 0
        
        self.color_cycle_task = None
        self.current_color_index = 0
        # Remove duplicate player creation
        # self.player = player()  # <- Remove this line
        
        # Add the update task to Panda3D's task manager to continually update monsters
        taskMgr.add(self.update, 'update')
        # base.taskMgr.add(self.monster_manager.update_monsters)  # Add to task manager to continuously update monsters

    def load_textures_from_directory(self, directory):
        texture_files = sorted(
            [
                f
                for f in os.listdir(directory)
                if f.endswith(".png") or f.endswith(".jpg")
            ]
        )

        textures = [
            base.loader.loadTexture(os.path.join(directory, texture))
            for texture in texture_files
        ]

        return textures
    

    def create_yin_yang(self):
    
        # Create and return a Yin-Yang monster


        return YinYangMonster(parent_node=self.render)

    def setup_npcs(self, npc_mounts):
        """
        Create and place NPCs dynamically based on the number of mounts.
        """
        self.npcs = []

        for mount in npc_mounts:
            # Create and load a new NPC
            npc_obj = npc().load_npc()
            self.npcs.append(npc_obj)

            # Get NPC attributes
            name = npc_obj.get("name")
            face = npc_obj.get("face")
            emblem = npc_obj.get("emblem")

            # Create and attach name tag
            name_node = TextNode(f"npcName_{name}")
            name_node.text = str(name)
            name_node.align = TextNode.A_center
            name_node.font = choice(base.fonts)
            npc_obj.get("nametag").attach_new_node(name_node)

            # Attach face and emblem if available
            if face:
                npc_obj.get("model").attach_new_node(face.get_node(0))
            if emblem:
                npc_obj.get("model").attach_new_node(emblem.get_node(0))

            # Attach NPC model to the mount
            npc_obj.get("model").instance_to(mount)

        print(f"Successfully created and placed {len(npc_mounts)} NPCs.")


    def update_task(self, task):

        dt = globalClock.get_dt()  # Get the delta time for this frame
    
        
        self.monster_manager.update_monsters(dt)

        return task.cont

    def update_colors(self, task):
        """Update colors for various game elements"""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        current_color = self.colors[self.current_color_index]
    def start_color_cycling(self):
        """Start the color cycling task if not already running"""
        if self.color_cycle_task is None:
            self.color_cycle_task = taskMgr.add(self.update_colors, "color_cycle_task")

    def stop_color_cycling(self):
        """Stop the color cycling task if running"""
        if self.color_cycle_task is not None:
            taskMgr.remove(self.color_cycle_task)
            self.color_cycle_task = None
    def load_world(self):
        # World


        self.worldNP = render.attachNewNode("World")

        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode("Debug"))

        self.debugNP.show()

        self.debugNP.node().showWireframe(DEBUG)

        self.debugNP.node().showConstraints(DEBUG)

        self.debugNP.node().showBoundingBoxes(DEBUG)

        self.debugNP.node().showNormals(DEBUG)

        # self.debugNP.showTightBounds()

    
        # self.debugNP.showBounds()

        self.world = BulletWorld()

        self.world.setGravity(Vec3(0, 0, -9.81 * 8))

        self.world.setDebugNode(self.debugNP.node())


    def load_ground(self, lvl, arcade_lvl=None):
        """Load the ground model for the specified level"""
        floorCol = None
        wallCol = None
        ceilCol = None
        try:
            level_index = int(lvl)
        except (ValueError, TypeError):
            print(f"Warning: Invalid level value '{lvl}'. Using level 0.")
            level_index = 0
        
        # Ensure level_index is within bounds
        if level_index < 0 or level_index >= len(self.levels):
            print(f"Warning: Level index {level_index} out of range. Using level 0.")
            level_index = 0
        
        print(f"Loading ground for level: {level_index}")
         # List all children of the current ground node

        self.ground = base.loader.loadModel(self.levels[level_index])
        print(self.ground)
        if self.ground.findAllMatches("**/npc**") > 0:
            self.npc_mounts = self.ground.findAllMatches("**/npc**")
            self.setup_npcs(self.npc_mounts)
        if self.ground.findAllMatches("**/levelFloor") > 0:
            self.floor = self.ground.findAllMatches("**/levelFloor").getPath(0)

        if self.ground.findAllMatches("**/levelWall") > 0:
            self.walls = self.ground.findAllMatches("**/levelWall").getPath(0)

        if self.ground.findAllMatches("**/levelCeil") > 0:
            self.ceil = self.ground.findAllMatches("**/levelCeil").getPath(0)
        if self.ground.findAllMatches("**/levelFloor") > 0:
            for stage in self.floor.find_all_texture_stages():
                self.floor.set_texture(stage, choice(self.floortextures), 1)
        if self.ground.findAllMatches("**/levelWall") > 0:
            for stage in self.walls.find_all_texture_stages():
                self.walls.set_texture(stage, choice(self.walltextures), 1)
        if self.ground.findAllMatches("**/levelCeil") > 0:
            for stage in self.ceil.find_all_texture_stages():
                self.ceil.set_texture(stage, choice(self.ceiltextures), 1)
        #if self.ground.findAllMatches("**/playerStart") > 0:

        if self.ground.findAllMatches("**/floorCol") > 0:
            floorCol = (
                self.ground.findAllMatches("**/floorCol").getPath(0).node().getGeom(0)
            )

        if self.ground.findAllMatches("**/wallCol") > 0:
            wallCol = self.ground.findAllMatches("**/wallCol").getPath(0).node().getGeom(0)

        if self.ground.findAllMatches("**/ceilCol") > 0:
            ceilCol = self.ground.findAllMatches("**/ceilCol").getPath(0).node().getGeom(0)
        
        if self.ground.findAllMatches("**/portal**") > 0:
            self.portals = self.ground.findAllMatches("**/portal**")
        if self.ground.findAllMatches("**/playerStart**") > 0:
            self.player_start = self.ground.findAllMatches("**/playerStart**")

        
        # Add safety check for spawn points
        if not self.portals:
            print("Warning: No portals or playerStart nodes found in level. Adding default spawn point.")
            # Create a default spawn point if no spawn positions exist
            default_spawn = NodePath("default_portal")
            default_spawn.setPos(0, 0, 5)  # Set a reasonable default position
            default_spawn.reparentTo(self.ground)
            if len(self.portals) > 0:
                self.portals.append(default_spawn)
        if self.ground.findAllMatches("**/door**") > 0:
            self.doors = self.ground.findAllMatches("**/door**")

        # Load the textures

        self.base_texture = base.loader.loadTexture(
            "portals/base00.png"
        )  # Base texture

        self.flower_texture = base.loader.loadTexture(
            "portals/effect01.png"
        )  # Flower texture
        
        # Check if textures are loaded correctly

        if not self.base_texture or not self.flower_texture:
            print("Error: Textures failed to load.")

        else:
            print("Textures loaded successfully.")

        if len(self.portals):
            for p, portal in enumerate(self.portals):
                # Play the portal sound effect
                self.audio.playSfx("portal_loop", portal, True)

                # Create portal instance
                portal_instance = self.portal_template.instanceTo(portal)
                
                # Only proceed with node setup if instance was created successfully
                if portal_instance:
                    portal.setPos(portal.getPos().x, portal.getPos().y, portal.getPos().z)

                    # Find the base and flower nodes
                    base_node = portal_instance.find("**/base")
                    flower_node = portal_instance.find("**/flower")

                    # Only apply textures if both nodes were found
                    if base_node and flower_node:
                        for stage in base_node.find_all_texture_stages():
                            base_node.set_texture(stage, self.base_texture, 1)

                        for stage in flower_node.find_all_texture_stages():
                            flower_node.set_texture(stage, self.flower_texture, 1)
                    else:
                        print(f"Warning: Could not find required nodes for portal {p}")
                else:
                    print(f"Warning: Failed to create portal instance {p}")
        
        # Assuming 'self.letterlist' is properly initialized and contains 'letter_nodes' as a list of NodePaths
        if self.ground.findAllMatches("**/letter**") > 0:
            self.letterlist.letter_mounts = self.ground.findAllMatches("**/letter**")
        if self.ground.findAllMatches("**/door**") > 0:
            if not hasattr(self, 'door_manager'):
                self.door_manager = DoorManager(self, "doors.json")
            self.door_manager.set_player(self.player)
            self.door_manager.replace_door_nodes()
            self.doors = self.door_manager.get_doors()
            for door_model in self.doors:  # Assuming self.doors contains your door models
                self.door_manager.start_color_cycle(door_model)
            # OR if you want to start color cycling for all doors at once, modify the DoorManager class
        # self.door_manager.start_color_cycle_all()  # Create this new method if needed



        self.letterlist.letter_mounts = self.ground.findAllMatches("**/letter**")

        # A helper function to check if a node is already in the parent-child chain

        def is_in_parent_chain(node, parent):

            current_parent = node.getParent()

            while current_parent:
                if current_parent == parent:
                    return True

                current_parent = current_parent.getParent()

            return False

        if len(self.letterlist.letter_mounts):
            for l, letter in enumerate(self.letterlist.letter_mounts):
                # Create a new node (could be a copy or a fresh new node) to add to the scene

                letter_node = letter.attachNewNode("letter_node")

                # Choose a random letter node to attach

                random_letter_node = choice(self.letterlist.letter_nodes)

                # Ensure that the random_letter_node is not part of the current letter node's parent-child chain

                if not is_in_parent_chain(random_letter_node, letter_node):
                    random_letter_node.reparentTo(letter)

                else:
                    print(
                        f"Cycle detected: Cannot reparent {random_letter_node} to {letter}"
                    )

        else:
            print("Error: No letter nodes found on the ground.")

        print(f"Current letter nodes: {self.letterlist.letter_nodes}")



        def setup_rigid_body(mesh, geom, body_name, restitution, parent_node, world):
            if not geom:
                return None

            # Create BulletTriangleMesh and add geometry
            mesh.addGeom(geom)
            shape = BulletTriangleMeshShape(mesh, dynamic=True)

            # Create and configure the rigid body
            body = BulletRigidBodyNode(body_name)
            body.setRestitution(restitution)
            bodyNP = parent_node.attachNewNode(body)
            bodyNP.node().addShape(shape)
            bodyNP.node().setRestitution(restitution)
            bodyNP.node().setCollisionResponse(True)
            bodyNP.setPos(0, 0, 0)
            bodyNP.setCollideMask(BitMask32.allOn())

            # Attach to physics world
            world.attachRigidBody(bodyNP.node())

            # Visualize the rigid body (optional)
            bodyNP.show()

            return bodyNP

        # Create meshes
        mesh_floor = BulletTriangleMesh()
        mesh_walls = BulletTriangleMesh()
        mesh_ceil = BulletTriangleMesh()

        # Set up rigid bodies for floor, walls, and ceiling
        self.floorNP = setup_rigid_body(mesh_floor, floorCol, "Floor", 0.75, self.worldNP, self.world)
        self.wallsNP = setup_rigid_body(mesh_walls, wallCol, "Walls", 0.75, self.worldNP, self.world)
        self.ceilNP = setup_rigid_body(mesh_ceil, ceilCol, "Ceil", 0.75, self.worldNP, self.world)

        # Reparent models to rigid bodies
        if self.floorNP:
            self.floor.reparentTo(self.floorNP)
        if self.wallsNP:
            self.walls.reparentTo(self.wallsNP)
        if self.ceilNP:
            self.ceil.reparentTo(self.ceilNP)

        # Reparent ground node to render
        self.ground.reparentTo(render)

        # Additional configurations
        spawn_count = 100


        for i in range(spawn_count):
            random_x = uniform(-500, 500)  # Random X coordinate within bounds

            random_y = uniform(-500, 500)  # Random Y coordinate within bounds

            # Ray now casts upwards (0, 0, 1) to detect collisions with objects above

            ray = CollisionRay(random_x, random_y, 50, 0, 0, -1)  # Upward ray

            ray_node = CollisionNode(f"ray_{i}")

            ray_node.addSolid(ray)

            ray_node.setFromCollideMask(BitMask32.allOn())

            ray_np = self.worldNP.attachNewNode(ray_node)

            # Add collider and handler

            self.cTrav.addCollider(ray_np, self.handler)

            # Perform collision traversal

            self.cTrav.traverse(self.worldNP)

            if self.handler.getNumEntries() > 0:
                self.handler.sortEntries()

                entry = self.handler.getEntry(0)  # Closest collision

                collision_point = entry.getSurfacePoint(self.worldNP)

                print(f"Spawn {i}: Placing monster at {collision_point}")

                # Adjust the Z value of the collision point to move the monster 0.25 units above the floor

                new_collision_point = Point3(
                    collision_point.x, collision_point.y, collision_point.z + 0.25
                )

                # Use the collision point to place a monster

                monster = self.monster_manager.create_monster(i)

                monster.setPos(new_collision_point)

                monster.reparentTo(self.worldNP)

            # Cleanup ray node

            ray_np.removeNode()
          # Index to get the first node
        self.player_start = self.ground.findAllMatches("**/playerStart").getPath(0).getPos()
        print(self.player_start)
        self.player.set_player_pos(self.player_start + (0, 0, 3))
    def spawn_on_floor(self, num_monsters=10):
        """Spawn a specified number of monsters on the floor using the existing floor collision geometry."""

        # Step 1: Get the existing floor collision geometry

        floor_col_geom = self.ground.find("**/floorCol")

        if not floor_col_geom:
            print("Error: No floor collision geometry found!")

            return

        print(
            floor_col_geom.ls()
        )  # Debug: Print floor collision details for validation

        # Check if it's a GeomNode

        if isinstance(floor_col_geom.node(), GeomNode):
            # Create a BulletTriangleMesh from the Geom

            mesh = BulletTriangleMesh()

            for geom in range(floor_col_geom.node().getNumGeoms()):
                mesh.addGeom(floor_col_geom.node().getGeom(geom))

            # Create a BulletTriangleMeshShape

            shape = BulletTriangleMeshShape(mesh, dynamic=False)

            # Create a rigid body for the floor

            body = BulletRigidBodyNode("FloorCollision")

            body.addShape(shape)

            # Attach the rigid body to the scene

            body_np = self.worldNP.attachNewNode(body)

            body_np.setPos(floor_col_geom.getPos(render))

            body_np.setCollideMask(BitMask32.bit(1))

            self.world.attachRigidBody(body)

            print("Generated collision geometry from floorCol.")

        else:
            print("Error: floorCol is not a GeomNode.")

            return

        # Step 2: Get the bounding box of the collision shape

        floor_bounds = body_np.getTightBounds()

        if not floor_bounds:
            print("Error: Unable to compute bounds for the floor collision geometry.")

            return

        min_x, min_y, min_z = floor_bounds[0].x, floor_bounds[0].y, floor_bounds[0].z

        max_x, max_y, max_z = floor_bounds[1].x, floor_bounds[1].y, floor_bounds[1].z

        # Debug bounding box

        if self.debugNP:
            print(
                f"Floor Bounds: Min({min_x}, {min_y}, {min_z}) Max({max_x}, {max_y}, {max_z})"
            )

        # Step 3: Spawn monsters at random positions on the floor

        for i in range(num_monsters):
            random_x = random.uniform(min_x, max_x)

            random_y = random.uniform(min_y, max_y)

            # Step 4: Cast a ray downwards to determine the Z position on the floor

            ray_start = Point3(random_x, random_y, max_z + 10)  # Start above the floor

            ray_end = Point3(random_x, random_y, min_z - 10)  # End below the floor

            # Perform the ray test

            ray_result = self.world.rayTestAll(
                ray_start, ray_end
            )  # Use rayTestAll for multiple hits

            if ray_result.getNumHits() > 0:  # Check for hits
                closest_hit = ray_result.getHit(0)

                hit_pos = closest_hit.getHitPos()

                # Offset the monster slightly above the floor

                spawn_pos = Point3(hit_pos.x, hit_pos.y, hit_pos.z + 0.25)

                # Step 5: Create and spawn the monster

                monster = self.monster_manager.create_yin_yang()

                monster.setPos(spawn_pos)

                monster.setH(random.uniform(0, 360))  # Randomize rotation

                monster.setCollideMask(
                    BitMask32.bit(1)
                )  # Ensure correct collision mask

                # Parent the monster to the appropriate node and add to the list

                monster.reparentTo(self.level.monsters_node)

                self.monsters.append(monster)

                print(f"Spawned monster at: {spawn_pos}")
    

            else:
                print(
                    f"No collision detected for monster {i} at position ({random_x}, {random_y})."
                )

                if self.debugNP:
                    print(f"Ray start: {ray_start}, Ray end: {ray_end}")

    def place_letters(self):
        for l, letter_node in enumerate(self.letterlist.letter_nodes):
            print("letter: " + letter_node.node().getText())  # Display the letter text

            # Create a new NodePath for the letter

            letter_path = NodePath("letter_" + letter_node.node().getText())

            # Enable anti-aliasing

            # Reparent the letter_node to the new path

            letter_node.reparentTo(letter_path)

            # Set the position and other transformations

            letter_path.setPos(self.letter_mounts.pop())

            letter_path.setSy(1)

            # Apply material with solid shading

            material = Material()

            material.setShadingModel(Material.SMH_solid)

            material.setColor(1, 1, 1, 1)  # Ensure fully opaque white

            letter_node.setMaterial(material, 1)

            # Set RenderMode to Filled (ensures it's not wireframe)

            letter_path.setRenderModeFilled()

            # Ensure two-sided rendering

    
            letter_path.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))

            letter_path.setTwoSided(True)

            # Debugging info

            print(f"Position: {letter_path.getPos()}")

            print(f"Two-sided: {letter_path.getTwoSided()}")
            
        self.floor = self.ground.find("**/floor")
        self.walls = self.ground.find("**/walls")
        self.ceil = self.ground.find("**/ceil")

    def get_current_arcade(self):
        return self.current_arcade
    
    def set_current_arcade(self, current_arcade):
        self.current_arcade = current_arcade
        
    def update(self, task):
        self.audio.update(task)

        self.clock += 0.001

        self.clock2 += 0.1

        # Calculate current color index with a slower cycle for clear transitions

        num_colors = len(self.colors)

        color_index = int(
            (self.clock * 0.3) % num_colors
        )  # Slower cycle for distinct color steps

        current_color = self.colors[
            color_index
        ]  # Directly use the color at current index

        # Apply color cycling to floor, walls, and ceiling
        if hasattr(self, 'floor'):
            
            for stage in self.floor.find_all_texture_stages():
                self.floor.setTexOffset(
                    stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6)
                )

                self.floor.setTexScale(
                    stage, 0.05 * sin(self.clock) + 2.5, 0.05 * sin(self.clock) + 2.5, 1
                )

                self.floor.set_color(current_color)

        # Update wall texture scale to simulate 512x1024 ratio

        wall_tex_scale_u = (
            0.5 * sin(self.clock) + 1.0
        )  # Adjust U scale to match 512x1024 ratio

        wall_tex_scale_v = (
            0.25 * sin(self.clock) + 0.5
        )  # Adjust V scale to match 512x1024 ratio
        if hasattr(self, 'walls'):
            for stage in self.walls.find_all_texture_stages():
                self.walls.setTexOffset(
                    stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6)
                )

                self.walls.setTexScale(stage, wall_tex_scale_u, wall_tex_scale_v)

                self.walls.set_color(current_color)

        if hasattr(self, 'ceil'):
            for stage in self.ceil.find_all_texture_stages():
                self.ceil.setTexOffset(
                    stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6)
                )

            self.ceil.setTexScale(
                stage, 0.05 * sin(self.clock) + 2.5, 0.05 * sin(self.clock) + 2.5, 1
            )

            self.ceil.set_color(current_color)

        return task.cont
    def cleanup(self):
        """Clean up physics world and other resources"""
        if hasattr(self, 'player'):
            self.player.ball_roll.stop()
            self.player.cleanup()
        
        if hasattr(self, 'door_manager'):
            self.door_manager.cleanup()  # Add this line
        if hasattr(self, 'floor'):
            self.floor.removeNode()
        if hasattr(self, 'walls'):
            self.walls.removeNode()
        if hasattr(self, 'ceil'):
            self.ceil.removeNode()
        if len(self.portals):
            for portal in self.portals:
                portal.removeNode()
        if len(self.letterlist.letter_nodes):
            for letter in self.letterlist.letter_nodes:
                letter.removeNode()
        if hasattr(self, 'npc_mounts'):
            for mount in self.npc_mounts:
                mount.removeNode()
            self.npcs = []
            self.npc_mounts = []
        # Cleanup monster manager if it exists
        if len(self.monsters):
            for monster in self.monsters:
                monster.removeNode()
        if len(self.doors):
            for door in self.doors:
                door.removeNode()
        if hasattr(self, 'monster_manager'):
            self.monster_manager.cleanup()
        if hasattr(self, 'ground'):
            self.ground = None
        # Cleanup audio
        if hasattr(self, 'audio'):
            self.audio.cleanup()
            # Remove any remaining tasks
            #base.task_mgr.remove('level_update')
