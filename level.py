import os

from audio3d import audio3d

from npc import npc

from letters import Letters

from math import sin, floor

from random import choice, randint, uniform

from monsterman import MonsterManager

from monsterman import YinYangMonster

import random

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

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, Point3, CollisionNode, CollisionPolygon, GeomVertexReader, GeomNode





DEBUG = False

class level():



    def __init__(self, lvl):

        self.audio = audio3d()

        self.npcs = []

        self.levels = [

            base.loader.loadModel("levels/level00.bam"),

            base.loader.loadModel("levels/level01.bam"),

            base.loader.loadModel("levels/level02.bam"),

            base.loader.loadModel("levels/level03.bam"),

            base.loader.loadModel("levels/maze00.bam"),

            base.loader.loadModel("levels/maze02.bam")

        ]

        self.floortextures = self.load_textures_from_directory('./graphics/patterns/floor')

        self.walltextures = self.load_textures_from_directory('./graphics/patterns/wall')

        self.ceiltextures = self.load_textures_from_directory('./graphics/patterns/ceiling')

        if lvl == None:

            lvl = randint(0,len(self.levels))

        else:

            self.lvl = lvl

                # Define colors for cycling

        self.colors = [

            Vec4(1, 0, 0, 1),      # Red

            Vec4(1, 0.5, 0, 1),    # Orange

            Vec4(1, 1, 0, 1),      # Yellow

            Vec4(0, 1, 0, 1),      # Green

            Vec4(0, 0, 1, 1),      # Blue

            Vec4(0.29, 0, 0.51, 1),# Indigo

            Vec4(0.56, 0, 1, 1)    # Violet

        ]

        self.portals = []

        self.portal_template = base.loader.loadModel("components/portal00.bam")

        self.letterlist = Letters()

        self.load_world()

        # Example of how you'd use this:

        

        # Simulate the game loop where you update monsters' movement and "kick-off" behavior

        # This loop would typically be part of the Panda3D task manager



        self.monster_manager = MonsterManager(base.render)

        self.monsters = self.monster_manager.place_monsters([], num_monsters=10)

        self.cTrav = CollisionTraverser()

        self.handler = CollisionHandlerQueue()

        self.load_ground()

        

        

        # Add the update task to Panda3D's task manager to continually update monsters

        

        #base.taskMgr.add(self.monster_manager.update_monsters)  # Add to task manager to continuously update monsters

        self.clock = 0

        self.clock2 = 0

        

        

        #self.place_letters()

        base.task_mgr.add(self.update, 'level_update')



    def load_textures_from_directory(self, directory):

        texture_files = sorted([

            f for f in os.listdir(directory) 

            if f.endswith('.png') or f.endswith('.jpg')

        ])

        textures = [base.loader.loadTexture(os.path.join(directory, texture)) for texture in texture_files]

        return textures

    def create_yin_yang(self):

        # Create and return a Yin-Yang monster

        return YinYangMonster(parent_node=self.render)

    def get_npcs(self, num_npcs):

        for n in range(num_npcs):

            new_npc = npc()

            self.npcs.append(new_npc.load_npc())

        

    def place_npcs(self):

        if len(self.npc_mounts):

            for n, npc in enumerate(self.npc_mounts):

                npcObject = self.npcs[n]

                name = self.npcs[n].get('name')

                face = self.npcs[n].get('face')

                emblem = self.npcs[n].get('emblem')

                name_node = TextNode("npcName_"+str(name))

                name_node.text = str(name)

                name_node.align = 2

                name_node.font = choice(base.fonts)

                npcObject.get('nametag').attach_new_node(name_node)

                #frame.set_pos(npc,(0,0,5))

                npcObject.get('model').attach_new_node(face.get_node(0))

                npcObject.get('model').attach_new_node(emblem.get_node(0))

                

                npcObject.get('model').instance_to(self.npc_mounts[n])

    def update_task(self,task):

        dt = globalClock.get_dt()  # Get the delta time for this frame

        self.monster_manager.update_monsters(dt)

        return task.cont

    def load_world(self):

        # World

        self.worldNP = render.attachNewNode('World')

        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))

        self.debugNP.show()

        self.debugNP.node().showWireframe(DEBUG)

        self.debugNP.node().showConstraints(DEBUG)

        self.debugNP.node().showBoundingBoxes(DEBUG)

        self.debugNP.node().showNormals(DEBUG)



        #self.debugNP.showTightBounds()

        #self.debugNP.showBounds()



        self.world = BulletWorld()

        self.world.setGravity(Vec3(0, 0, -9.81*8))

        self.world.setDebugNode(self.debugNP.node())

        

            

    def load_ground(self):

        self.ground = self.levels[self.lvl]

        self.npc_mounts = self.ground.findAllMatches("**/npc**")  

        self.floor = self.ground.findAllMatches("**/levelFloor").getPath(0)

        self.walls = self.ground.findAllMatches("**/levelWall").getPath(0)

        self.ceil = self.ground.findAllMatches("**/levelCeil").getPath(0)


        for stage in self.floor.find_all_texture_stages():

            self.floor.set_texture(stage, choice(self.floortextures), 1)

        for stage in self.walls.find_all_texture_stages():

            self.walls.set_texture(stage, choice(self.walltextures), 1)

        for stage in self.ceil.find_all_texture_stages():

            self.ceil.set_texture(stage, choice(self.ceiltextures), 1)



        self.player_start = self.ground.findAllMatches("**/playerStart").getPath(0)

        self.portals = self.ground.findAllMatches("**/portal**")



        floorCol = self.ground.findAllMatches("**/floorCol").getPath(0).node().getGeom(0)

        wallCol = self.ground.findAllMatches("**/wallCol").getPath(0).node().getGeom(0)

        ceilCol = self.ground.findAllMatches("**/ceilCol").getPath(0).node().getGeom(0)

        

        self.player_start = self.ground.findAllMatches("**/playerStart").getPath(0)

        self.portals = self.ground.findAllMatches("**/portal**")

        # Load the textures

        self.base_texture = base.loader.loadTexture('portals/base00.png')  # Base texture

        self.flower_texture = base.loader.loadTexture('portals/effect01.png')  # Flower texture



        # Check if textures are loaded correctly

        if not self.base_texture or not self.flower_texture:

            print("Error: Textures failed to load.")

        else:

            print("Textures loaded successfully.")

            

        if len(self.portals):

            for p, portal in enumerate(self.portals):

                # Play the portal sound effect

                self.audio.playSfx('portal_loop', portal, True)



                # Instantiate the portal template

                portal_instance = self.portal_template.instanceTo(portal)

                portal.setPos(portal.getPos().x, portal.getPos().y, portal.getPos().z)

                # Debug: Check if portal_instance is valid

                if not portal_instance:

                    print(f"Error: Failed to instantiate portal {p}.")

                    continue



                # Print the portal's node hierarchy to see what's inside

                print(f"Portal {p} hierarchy:")

                portal_instance.ls()  # List the hierarchy of the portal instance



                # Check for the base and flower components in the portal hierarchy

                base_node = portal_instance.find("**/base")  # Searching for base node in the portal hierarchy

                flower_node = portal_instance.find("**/flower")  # Searching for flower node in the portal hierarchy



                for stage in base_node.find_all_texture_stages():

                    base_node.set_texture(stage, self.base_texture, 1)

                for stage in flower_node.find_all_texture_stages():

                    flower_node.set_texture(stage, self.flower_texture, 1)





        # Assuming 'self.letterlist' is properly initialized and contains 'letter_nodes' as a list of NodePaths

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

                letter_node = letter.attachNewNode('letter_node')

                

                # Choose a random letter node to attach

                random_letter_node = choice(self.letterlist.letter_nodes)



                # Ensure that the random_letter_node is not part of the current letter node's parent-child chain

                if not is_in_parent_chain(random_letter_node, letter_node):

                    random_letter_node.reparentTo(letter)

                else:

                    print(f"Cycle detected: Cannot reparent {random_letter_node} to {letter}")

        else:

            print("Error: No letter nodes found on the ground.")





        print(f"Current letter nodes: {self.letterlist.letter_nodes}")

        mesh = BulletTriangleMesh()

        mesh2 = BulletTriangleMesh()

        mesh3 = BulletTriangleMesh()

        mesh.addGeom(floorCol)

        mesh2.addGeom(wallCol)

        mesh2.addGeom(ceilCol)

        

        shape = BulletTriangleMeshShape(mesh, dynamic=True)

        shape2 = BulletTriangleMeshShape(mesh2, dynamic=True) 

        shape3 = BulletTriangleMeshShape(mesh3, dynamic=True) 

        

        body = BulletRigidBodyNode('Floor')

        body2 = BulletRigidBodyNode('Walls')

        body3 = BulletRigidBodyNode('Ceil')

        body.setRestitution(0.75)
        body2.setRestitution(0.75)
        body3.setRestitution(0.75)
        

        bodyNP = self.worldNP.attachNewNode(body)

        bodyNP2 = self.worldNP.attachNewNode(body2)

        bodyNP3 = self.worldNP.attachNewNode(body3)

        

        bodyNP.node().addShape(shape)

        bodyNP2.node().addShape(shape2)

        bodyNP3.node().addShape(shape3)

        

        bodyNP.node().setRestitution(0.75)

        bodyNP2.node().setRestitution(0.75)

        bodyNP3.node().setRestitution(0.75)

        

        bodyNP.node().setCollisionResponse(True)

        bodyNP2.node().setCollisionResponse(True)

        bodyNP3.node().setCollisionResponse(True)

        

        bodyNP.setPos(0, 0, 0)

        bodyNP2.setPos(0, 0, 0)

        bodyNP3.setPos(0, 0, 0)

        

        bodyNP.setCollideMask(BitMask32.allOn())

        bodyNP2.setCollideMask(BitMask32.allOn())

        bodyNP3.setCollideMask(BitMask32.allOn())

        

        self.world.attachRigidBody(bodyNP.node())

        self.world.attachRigidBody(bodyNP2.node())

        self.world.attachRigidBody(bodyNP3.node())

        

        bodyNP.show()

        bodyNP2.show()

        bodyNP3.show()

        

        self.floor.reparentTo(bodyNP)

        self.walls.reparentTo(bodyNP2)

        self.ceil.reparentTo(bodyNP3)

        

        self.floorNP = bodyNP

        self.wallsNP = bodyNP2

        self.ceilNP = bodyNP3

        

        self.ground.reparentTo(render)



        # Now we have a valid cTrav

        spawn_count = 100

        for i in range(spawn_count):

            random_x = uniform(-500, 500)  # Random X coordinate within bounds

            random_y = uniform(-500, 500)  # Random Y coordinate within bounds

            

            # Ray now casts upwards (0, 0, 1) to detect collisions with objects above

            ray = CollisionRay(random_x, random_y, 50, 0, 0, -1)  # Upward ray

            ray_node = CollisionNode(f'ray_{i}')

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

                new_collision_point = Point3(collision_point.x, collision_point.y, collision_point.z + 0.25)

        

                # Use the collision point to place a monster

                monster = self.monster_manager.create_monster(i)

                monster.setPos(new_collision_point)

                monster.reparentTo(self.worldNP)

            

            # Cleanup ray node

            ray_np.removeNode()

            base_node = portal_instance.find("**/base")  # Searching for base node in the portal hierarchy

            flower_node = portal_instance.find("**/flower")  # Searching for flower node in the portal hierarchy

        



            

    

    def spawn_on_floor(self, num_monsters=10):

        """Spawn a specified number of monsters on the floor using the existing floor collision geometry."""

    

        # Step 1: Get the existing floor collision geometry

        floor_col_geom = self.ground.find("**/floorCol")

        if not floor_col_geom:

            print("Error: No floor collision geometry found!")

            return



        print(floor_col_geom.ls())  # Debug: Print floor collision details for validation



        # Check if it's a GeomNode

        if isinstance(floor_col_geom.node(), GeomNode):

            # Create a BulletTriangleMesh from the Geom

            mesh = BulletTriangleMesh()

            for geom in range(floor_col_geom.node().getNumGeoms()):

                mesh.addGeom(floor_col_geom.node().getGeom(geom))

            

            # Create a BulletTriangleMeshShape

            shape = BulletTriangleMeshShape(mesh, dynamic=False)



            # Create a rigid body for the floor

            body = BulletRigidBodyNode('FloorCollision')

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

            print(f"Floor Bounds: Min({min_x}, {min_y}, {min_z}) Max({max_x}, {max_y}, {max_z})")



        # Step 3: Spawn monsters at random positions on the floor

        for i in range(num_monsters):

            random_x = random.uniform(min_x, max_x)

            random_y = random.uniform(min_y, max_y)



            # Step 4: Cast a ray downwards to determine the Z position on the floor

            ray_start = Point3(random_x, random_y, max_z + 10)  # Start above the floor

            ray_end = Point3(random_x, random_y, min_z - 10)    # End below the floor



            # Perform the ray test

            ray_result = self.world.rayTestAll(ray_start, ray_end)  # Use rayTestAll for multiple hits

            

            if ray_result.getNumHits() > 0:  # Check for hits

                closest_hit = ray_result.getHit(0)

                hit_pos = closest_hit.getHitPos()

                

                # Offset the monster slightly above the floor

                spawn_pos = Point3(hit_pos.x, hit_pos.y, hit_pos.z + 0.25)



                # Step 5: Create and spawn the monster

                monster = self.monster_manager.create_yin_yang()

                monster.setPos(spawn_pos)

                monster.setH(random.uniform(0, 360))  # Randomize rotation

                monster.setCollideMask(BitMask32.bit(1))  # Ensure correct collision mask



                # Parent the monster to the appropriate node and add to the list

                monster.reparentTo(self.level.monsters_node)

                self.monsters.append(monster)



                print(f"Spawned monster at: {spawn_pos}")

            else:

                print(f"No collision detected for monster {i} at position ({random_x}, {random_y}).")

                if self.debugNP:

                    print(f"Ray start: {ray_start}, Ray end: {ray_end}")













    def place_letters(self):

        for l, letter_node in enumerate(self.letterlist.letter_nodes):

            print("letter: " + letter_node.node().getText())  # Display the letter text

            

            # Create a new NodePath for the letter

            letter_path = NodePath('letter_' + letter_node.node().getText())

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







            

    def update(self, task):

        self.audio.update(task)

        self.clock += 0.001

        self.clock2 += 0.1



        # Calculate current color index with a slower cycle for clear transitions

        num_colors = len(self.colors)

        color_index = int((self.clock * 0.3) % num_colors)  # Slower cycle for distinct color steps

        current_color = self.colors[color_index]  # Directly use the color at current index



        # Apply color cycling to floor, walls, and ceiling

        for stage in self.floor.find_all_texture_stages():

            self.floor.setTexOffset(stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6))

            self.floor.setTexScale(stage, 0.05 * sin(self.clock) + 2.5, 0.05 * sin(self.clock) + 2.5, 1)

            self.floor.set_color(current_color)



        # Update wall texture scale to simulate 512x1024 ratio

        wall_tex_scale_u = 0.5 * sin(self.clock) + 1.0   # Adjust U scale to match 512x1024 ratio

        wall_tex_scale_v = 0.25 * sin(self.clock) + 0.5  # Adjust V scale to match 512x1024 ratio

        for stage in self.walls.find_all_texture_stages():

            self.walls.setTexOffset(stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6))

            self.walls.setTexScale(stage, wall_tex_scale_u, wall_tex_scale_v)

            self.walls.set_color(current_color)



        for stage in self.ceil.find_all_texture_stages():

            self.ceil.setTexOffset(stage, 0.5 * sin(self.clock / 6), 0.5 * sin(self.clock / 6))

            self.ceil.setTexScale(stage, 0.05 * sin(self.clock) + 2.5, 0.05 * sin(self.clock) + 2.5, 1)

            self.ceil.set_color(current_color)

        

        return task.cont