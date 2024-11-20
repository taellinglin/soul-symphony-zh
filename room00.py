from math import pi
from math import sin
from math import cos
import random
import sys

from direct.showbase.PythonUtil import randFloat
from stageflow.core import Stage
from random import  choice
from random import  randint
from stageflow import Stage
from level import level
from player import player
from npc import npc
from dialog import dialog
from panda3d.core import LVecBase4f

from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import InputDevice
from panda3d.core import TextureStage
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.core import TextNode
from panda3d.core import Material
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBodyNode
from panda3d.core import ClipPlaneAttrib, Plane, LVecBase3
from direct.interval.IntervalGlobal import Sequence, Wait, Parallel
from panda3d.core import TransparencyAttrib, CardMaker, NodePath, Vec4, Vec3, Point3, LVector3, ColorWriteAttrib
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.LerpInterval import LerpColorInterval, LerpScaleInterval
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval
import os
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import math
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import KeyboardButton
from healthbar import HealthBar

class room00(Stage):
    def __init__(self, exit_stage="main_menu", lvl=None, audio_amplitude=None):
            super().__init__()  # Initialize the ShowBase
            if lvl is None:
                self.lvl = 0
            else:
                self.lvl = lvl
                
            self.exit_stage = exit_stage
            self.globalClock = globalClock
            self.rotation_speed = 60 # Degrees per second
            # Initialize colors (ROYGBIV)
            # Assuming player health is already initialized
            
            self.colors = []
            phase_frags = 6
            # Keep track of jump state
            self.on_ground = False
            self.jump_count = 0  # Tracks how many jumps have been performed
            # Define the ROYGBIV color pattern
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((1, sin(phase), 0, 1))  # Red to Orange
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((1 - sin(phase), 1, 0, 1))  # Orange to Yellow
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((0, 1, sin(phase), 1))  # Yellow to Green
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((0, 1 - sin(phase), 1, 1))  # Green to Cyan
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((sin(phase), 0, 1, 1))  # Cyan to Blue
            for phase in [0.5 * pi * (i / float(phase_frags)) for i in range(phase_frags)]:
                self.colors.append((1, 0, 1 - sin(phase), 1))  # Blue to Violet
                
            # Maintain a base colors list for cycling
            self.base_colors = [
                (1, 0, 0, 1),  # Red
                (1, 0.5, 0, 1),  # Orange
                (1, 1, 0, 1),  # Yellow
                (0, 1, 0, 1),  # Green
                (0, 0, 1, 1),  # Blue
                (0.5, 0, 1, 1),  # Indigo
                (1, 0, 1, 1)   # Violet
            ]
                        # Define a range of colors to choose from
            self.color_choices = [
                (1, 0, 0),     # Red
                (1, 0.5, 0),   # Orange
                (1, 1, 0),     # Yellow
                (0, 1, 0),     # Green
                (0, 0, 1),     # Blue
                (0.5, 0, 1),   # Indigo
                (1, 0, 1),     # Violet
            ]
            self.color_idx = -1
            self.clock = 0
            self.npcs = []
            self.audio_amplitude = audio_amplitude  # Amplitude array to sync transparency
            self.current_amplitude_idx = 0  # Index for amplitude tracking
            self.transparency = 0.15
            self.base_transparency = 0  # Base transparency value
            self.fs = 192000  # Sampling frequency
            self.buffer_size = 64  # Size of audio buffer
            self.audio_data = np.array([])  # Initialize as an empty array
            # Start audio stream
            self.stream = sd.InputStream(samplerate=self.fs, channels=2, blocksize=self.buffer_size, callback=self.audio_callback)
            self.stream.start()
                    # Initialize color intervals for cycling through colors
            base.disableMouse()  # Disable mouse control
            
    def star(self):

        # Load the star image
        self.star_node = NodePath('star_node')
        self.star_card = CardMaker('star_card')
        self.star_card.set_frame(0, 0, 1, 1)
        self.imageObject2 = OnscreenImage(image='graphics/star.png', pos=(0.0, 0.0, 0.0), scale=(1, 1, 1))
        self.imageObject2.setTransparency(TransparencyAttrib.MAlpha)
        self.imageObject3 = OnscreenImage(image='graphics/star2.png', pos=(0.0, 0.0, 0.0), scale=(1, 1, 1))
        self.imageObject3.setTransparency(TransparencyAttrib.MAlpha)

        # Correctly attach the generated node
        self.star_spinner = self.star_node.attach_new_node(self.star_card.generate())
        self.star_spinner.setPos(0, 0, 0)  # Center it at the origin
        
        self.star_decal = self.centerPivot(self.star_spinner)
        self.star_decal.setScale(1.0, 1.0, 1.0)

        


        
        # Call the method to create the pulsing effect for the star
        self.create_star_pulse()
        
        # Initialize a task to continuously rotate the star
        self.rotate_task = base.taskMgr.add(self.rotate_star, 'rotate_star')
    def create_star_pulse(self):
        # Star 1 pulsing effect
        self.star_pulse = Sequence(
            LerpScaleInterval(self.imageObject2, 1, scale=(0, 0, 0), startScale=(4, 4, 4)),  # Scale up
            Wait(0.5),  # Wait for half a second
            LerpScaleInterval(self.imageObject2, 1, scale=(4, 4, 4), startScale=(0, 0, 0)),  # Scale down
            Wait(0.5)  # Wait for half a second before looping
        )
        self.star_pulse.loop()

        # Star 2 pulsing effect
        self.star_pulse2 = Sequence(
            LerpScaleInterval(self.imageObject3, 1, scale=(4, 4, 4), startScale=(0, 0, 0)),  # Scale up
            Wait(0.5),  # Wait for half a second
            LerpScaleInterval(self.imageObject3, 1, scale=(0, 0, 0), startScale=(4, 4, 4)),  # Scale down
            Wait(0.5)  # Wait for half a second before looping
        )
        self.star_pulse2.loop()
    def rotate_star(self, task):
        dt = self.globalClock.get_dt()
        new_hpr = self.imageObject2.getHpr() + LVector3(0, 0, self.rotation_speed * dt)
        new_hpr2 = self.imageObject3.getHpr() + LVector3(0, 0, -self.rotation_speed * dt)
        self.imageObject2.setHpr(new_hpr)  # Set the new HPR
        self.imageObject3.setHpr(new_hpr2)

        return task.cont  # Continue the task
    def centerPivot(self, NP):
        pivot = NP.getBounds().getCenter()
        parent = NP.getParent()
        newNP = parent.attachNewNode('StarSpinner')
        newNP.setPos(pivot)
        NP.wrtReparentTo(newNP)
        #print(f"New parent position: {newNP.getPos()}")
        return newNP
    def audio_callback(self, indata, frames, time, status):
        if status:
            #print(status)
            pass
        self.audio_data = indata.flatten()  # Flatten the audio buffer

    def enter(self, lvl = None):
        if lvl == None:
            lvl = self.lvl
        self.lvl = lvl
        self.star()
        self.healthbar = HealthBar(parent=base.aspect2d)  # Create the health bar
        self.healthbar.max_health = 100  # Directly setting the max health
        self.healthbar.update_health(self.healthbar.max_health) # Set the initial health value
        
        self.star_color_cycle = Sequence(
            # ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(self.imageObject2, 0.04, Vec4(1, 0, 0, self.transparency), startColor=Vec4(1, 0.5, 0, 0), blendType='easeInOut'),  # Red to Orange
            LerpColorInterval(self.imageObject2, 0.05, Vec4(1, 1, 0, self.transparency), startColor=Vec4(1, 0, 0, 0), blendType='easeInOut'),    # Orange to Yellow
            LerpColorInterval(self.imageObject2, 0.06, Vec4(0, 1, 0, self.transparency), startColor=Vec4(1, 1, 0, 0), blendType='easeInOut'),    # Yellow to Green
            LerpColorInterval(self.imageObject2, 0.07, Vec4(0, 0, 1, self.transparency), startColor=Vec4(0, 1, 0, 0), blendType='easeInOut'),    # Green to Blue
            LerpColorInterval(self.imageObject2, 0.08, Vec4(0.29, 0, 0.51, self.transparency), startColor=Vec4(0, 0, 1, 0), blendType='easeInOut'),  # Blue to Indigo
            LerpColorInterval(self.imageObject2, 0.09, Vec4(0.56, 0, 1, self.transparency), startColor=Vec4(0.29, 0, 0.51, 0), blendType='easeInOut'),  # Indigo to Violet
            LerpColorInterval(self.imageObject2, 0.1, Vec4(1, 0, 0, self.transparency), startColor=Vec4(0.56, 0, 1, 0), blendType='easeInOut')  # Violet to Red (loop)
        )



        # Initialize color intervals for cycling through colors for star3
        self.star_color_cycle2 = Sequence(
            # Mirrored ROYGBIV Color Interpolation with staggered time for interference pattern
            LerpColorInterval(self.imageObject3, 0.1, Vec4(0.56, 0, 1, self.transparency), startColor=Vec4(1, 0, 0, 0), blendType='easeInOut'),  # Red to Violet
            LerpColorInterval(self.imageObject3, 0.09, Vec4(0.29, 0, 0.51, self.transparency), startColor=Vec4(0.56, 0, 1, 0), blendType='easeInOut'),  # Violet to Indigo
            LerpColorInterval(self.imageObject3, 0.08, Vec4(0, 0, 1, self.transparency), startColor=Vec4(0.29, 0, 0.51, 0), blendType='easeInOut'),  # Indigo to Blue
            LerpColorInterval(self.imageObject3, 0.07, Vec4(0, 1, 0, self.transparency), startColor=Vec4(0, 0, 1, 0), blendType='easeInOut'),    # Blue to Green
            LerpColorInterval(self.imageObject3, 0.06, Vec4(1, 1, 0, self.transparency), startColor=Vec4(0, 1, 0, 0), blendType='easeInOut'),    # Green to Yellow
            LerpColorInterval(self.imageObject3, 0.05, Vec4(1, 0.5, 0, self.transparency), startColor=Vec4(1, 1, 0, 0), blendType='easeInOut'),  # Yellow to Orange
            LerpColorInterval(self.imageObject3, 0.04, Vec4(1, 0, 0, self.transparency), startColor=Vec4(1, 0.5, 0, 0), blendType='easeInOut')   # Orange to Red (loop)
        )
        # Loop the color sequence indefinitely
        self.star_color_cycle.loop()

        # Initialize color intervals for cycling through colors for star3
        self.star_color_cycle2.loop()

        #print("Roll Test Area Entered...")
        base.cam.set_z(24)
        base.bgm.playMusic(None, True, 0.8)
        base.task_mgr.add(self.update, 'update')
        base.accept('escape', sys.exit)
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')
        inputState.watchWithModifiers('jump', 'gamepad-face_a')
        inputState.watchWithModifiers('jump', 'space')
        inputState.watchWithModifiers('cam-right', ']')
        inputState.watchWithModifiers('cam-left', '[')
        inputState.watchWithModifiers('cam-right', 'gamepad-trigger_right')
        inputState.watchWithModifiers('cam-left', 'gamepad-trigger_left')
        
        print("level: "+str(self.lvl))
        self.level = level(self.lvl)
        self.level.get_npcs(21)
        self.level.place_npcs()
        self.player = player()
        self.player.ballNP.reparentTo(self.level.worldNP)
        self.level.world.attachRigidBody(self.player.ballNP.node())
        self.player.ballNP.setPos(choice(self.level.portals).getPos()+(0,0,3))
        self.dialog = dialog()
        self.dialog_card = TextNode('dialog_card')
        self.dialog_card.align = 2
        self.dialog_card.setWordwrap(40)
        self.dialog_card.setFont(choice(base.fonts))
        self.dialog_card_node = aspect2d.attach_new_node(self.dialog_card)
        self.dialog_card_node.setScale(0.08)
        base.scoreboard.show()
        self.level.audio.audio3d.attachListener(base.cam)

        base.accept("gamepad-face_a", self.actionA)
        base.accept("space", self.actionA)
        base.accept("gamepad-face_a-up", self.actionAUp)
        base.accept("space-up", self.actionAUp)
        base.accept("gamepad-face_b", self.actionB)
        base.accept("shift", self.actionB)
        base.accept("gamepad-face_b-up", self.actionBUp)
        base.accept("shift-up", self.actionBUp)
        
        

        
    def actionA(self):
            # Check if the player is touching the ground
            result = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.floorNP.node())
            if result.getNumContacts() > 0:
                self.on_ground = True
                self.jump_count = 0  # Reset the jump count when on the ground
            else:
                self.on_ground = False
            
            # If player is on the ground or has performed less than 2 jumps
            if self.jump_count < 2:
                # Apply a jump force when the action is triggered
                self.player.ballNP.node().applyCentralImpulse(Vec3(0, 0, 128 + 32))
                base.bgm.playSfx('ball-jump')

                # Increment the jump counter
                self.jump_count += 1

                # Perform extra actions if near NPC mounts
                if len(self.level.npc_mounts):
                    for n, npc_mount in enumerate(self.level.npc_mounts):
                        if ((npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                            self.dialog_card.text = self.level.npcs[n].get('dialog')
                            self.dialog_card.setFont(choice(base.fonts))
                            self.dialog_card_node.show()
                            base.bgm.playSfx('start-dialog')
                            self.player.force = Vec3(0, 0, 0)
                            self.player.torque = Vec3(0, 0, 0)
                            self.player.ballNP.node().setLinearDamping(1)
                
                # Perform actions if near portals
                if len(self.level.portals):
                    for p, portal in enumerate(self.level.portals):
                        if ((portal.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                            self.dialog_card.setFont(choice(base.fonts))
                            self.dialog_card.text = choice(["出发吧！", "快点！", "耶！前进！", "我们走了！", "逃离！", "让我们迷失吧！", "再见！", "逃跑！", "离开这里！"])
                            self.dialog_card_node.show()
                            self.player.force = Vec3(0, 0, 0)
                            self.player.torque = Vec3(0, 0, 0)
                            self.player.ballNP.node().setLinearDamping(1)
                    
                    

    def actionAUp(self):
        if(self.player.ballNP.node().getLinearDamping() == 1):
            self.player.ballNP.node().setLinearDamping(0)
        self.dialog_card_node.hide()
        for p, portal in enumerate(self.level.portals):
            if((portal.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5):
                self.dialog_card.text = choice(["Ok!", "Alright!", "Affirmative!", "Totally!"])
                self.dialog_card_node.hide()
                base.bgm.stopSfx()
                base.bgm.playSfx('warp')
                self.transition(choice(base.levels))
                return
        
    def actionB(self):
        self.player.ballNP.node().setAngularDamping(0.82)
        self.player.ballNP.node().setLinearDamping(0.82)
         
    def actionBUp(self):
        self.player.ballNP.node().setAngularDamping(0)
        self.player.ballNP.node().setLinearDamping(0)
        

    def processInput(self, dt):
        force = Vec3(0,0,0)
        torque = Vec3(0,0,0)
        if(not base.gamepad_input.gamepad == None):
            self.left_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_x)
            self.left_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_y)
            self.right_x = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_x)
            self.right_y = base.gamepad_input.gamepad.findAxis(InputDevice.Axis.right_y)
            self.leftAnalog = Vec3(self.left_x.value, self.left_y.value, 0)
            force = self.leftAnalog
            torque = Vec3(0,0,self.right_x.value)
        if inputState.isSet('cam-right'): base.cam.set_r(self.ballNP, 0.5)
        if inputState.isSet('cam-left'): base.cam.set_r(self.ballNP, -0.5)        
        if inputState.isSet('forward'): force.setY( 1.0)
        if inputState.isSet('reverse'): force.setY(-1.0)
        if inputState.isSet('left'):    force.setX(-1.0)
        if inputState.isSet('right'):   force.setX( 1.0)
        if inputState.isSet('turnLeft'):  torque.setZ( 1.0)
        if inputState.isSet('turnRight'): torque.setZ(-1.0)

        force *= 100.0
        torque *= 100.0
        
        #force = self.ballNP.getRelativeVector(Vec3(base.cam.get_h(), base, 0), force)
        #torque = base.cam.getRelativeVector(self.ballNP, torque)

        self.player.ballNP.node().setActive(True)
        self.player.ballNP.node().applyCentralForce(force)
        self.player.ballNP.node().applyTorque(torque)


        
    def update(self, task):
        # Get the linear velocity vector
        velocity = self.player.ballNP.get_node(0).getLinearVelocity()
        # Calculate the magnitude of the velocity vector
        velocity_magnitude = velocity.length()  # Get the length (magnitude) of the vector

        # Map the magnitude to a transparency value in the range [0.15, 1.0]
        max_velocity = 2000.0  # Define a maximum expected velocity (this may need tuning)
        min_transparency = 0.0  # Minimum opacity (more transparent)
        max_transparency = 0.125    # Maximum opacity (fully opaque)

        # Normalize the transparency based on the velocity magnitude
        if velocity_magnitude > 0:
            # Normalize the velocity to a range between 0 and 1
            normalized_velocity = min(1, velocity_magnitude / max_velocity)
            # Set transparency so that lower velocity means higher transparency
            self.transparency = min_transparency + (max_transparency - min_transparency) * (1 - normalized_velocity)
        else:
            # If the ball is stationary, set transparency to minimum (most transparent)
            self.transparency = max_transparency

        # Set the rotation speed based on the velocity
        self.rotation_speed = velocity_magnitude * 2
        # Initialize color intervals for cycling through colors
    
        # Update the listener's velocity based on the player's ball position
        self.level.audio.audio3d.setListenerVelocity(self.player.ballNP.get_node(0).getLinearVelocity())
        
        # Update the color index for cycling through colors
        self.color_idx = (self.color_idx + 1) % len(self.colors)
        
        # Update ball roll speed based on linear velocity
        self.player.ball_roll.setPlayRate(0.05 * (abs(self.player.ballNP.get_node(0).getLinearVelocity().getX()) +
                                                abs(self.player.ballNP.get_node(0).getLinearVelocity().getY()) +
                                                abs(self.player.ballNP.get_node(0).getLinearVelocity().getZ())))

        # Check proximity to NPC mounts and show/hide nametags
        for n, npc_mount in enumerate(self.level.npc_mounts):
            nametag = npc_mount.find('**/npcNametag')
            if (npc_mount.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 5:
                if nametag.isHidden():
                    nametag.show()
                    base.bgm.playSfx('hover')
            else:
                nametag.hide()
            
        # Check for contacts with the floor and walls
        result = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.floorNP.node())
        result2 = self.level.world.contactTestPair(self.player.ballNP.node(), self.level.wallsNP.node())

        # Handle bouncing sound when contacting the floor
        if result.getNumContacts() > 0:
            contact = result.getContacts()[0]
            if contact.getNode1() == self.level.floorNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact.getManifoldPoint()
                    volume = abs(mpoint.getDistance())
                    pitch = volume
                    base.bgm.playSfx(choice(self.player.boings), volume, 1)
        else:
            self.player.boing = False

        # Handle bouncing sound when contacting the walls
        if result2.getNumContacts() > 0:
            contact2 = result2.getContacts()[0]
            if contact2.getNode1() == self.level.wallsNP.node():
                if not self.player.boing:
                    self.player.boing = True
                    mpoint = contact2.getManifoldPoint()
                    volume = abs(mpoint.getDistance())
                    pitch = volume
                    base.bgm.playSfx(choice(self.player.boings), volume, 1)
        else:
            self.player.boing = False

        
        # Iterate through each monster in the scene
        for monster in self.level.monsters:
            # Retrieve the combined node for the monster
            yin_yang_np = monster.yin_yang_np  # This holds the whole symbol

            # Perform contact tests with the Yin (black) and Yang (white) parts
            result_yin = self.level.world.contactTestPair(self.player.ballNP.node(), monster.yin_np.node())  # Black part
            result_yang = self.level.world.contactTestPair(self.player.ballNP.node(), monster.yang_np.node())  # White part

            # Decrease player's health if colliding with the Yin (black part)
            if result_yin.getNumContacts() > 0:
                contact_yin = result_yin.getContacts()[0]
                if contact_yin.getNode1() == monster.yin_np.node():
                    # Decrease player's health by 10%
                    new_health = self.player.health - (self.player.max_health * 0.1)
                    self.update_health(new_health)  # Update health bar and health value
                    print(f"Player hit Yin (black part)! Health decreased: {self.player.health}")

            # Heal player's health if colliding with the Yang (white part)
            if result_yang.getNumContacts() > 0:
                contact_yang = result_yang.getContacts()[0]
                if contact_yang.getNode1() == monster.yang_np.node():
                    # Increase player's health by 10%, ensuring it doesn't exceed max
                    new_health = self.player.health + (self.player.max_health * 0.1)
                    self.player.health = min(self.player.max_health, new_health)
                    self.update_health(self.player.health)  # Update health bar and health value
                    print(f"Player hit Yang (white part)! Health increased: {self.player.health}")




        # Update scoreboard and player color
        base.scoreboard.score_node.setColor(choice(self.colors))
        self.player.ballNP.set_color(choice(self.colors))

        # Check for interactions with letters
        for l, letter in enumerate(render.findAllMatches('**/letter**')):
            letter.set_h(letter, 1)
            letter.set_color(choice(self.colors))
            if (letter.getPos().getXy() - self.player.ballNP.getPos().getXy()).length() < 3:
                base.bgm.playSfx('pickup', 1, randFloat(0.1, 2), False)
                letter.detachNode()
                letter.removeNode()
                base.scoreboard.addPoints(1)
                print("Score + 1!")

     

        if self.audio_data.size > 0:
            # Limit the number of samples processed to avoid overflow
            # Limit the number of samples processed to avoid overflow
            max_samples = 1024
            if len(self.audio_data) > max_samples:
                self.audio_data = self.audio_data[:max_samples]
            samples = np.array(self.audio_data)[:max_samples]
            
            # Proceed with your FFT and transparency updates
            spectrum = np.fft.fft(samples)
            freqs = np.fft.fftfreq(len(samples), 1 / self.fs)
            band_indices = np.array_split(np.argsort(freqs), 7)
            amplitudes = [np.abs(spectrum[indices]).mean() for indices in band_indices]
            transparencies = np.clip(amplitudes / np.max(amplitudes), 0, 0.5)




            # Update the ground, floor, walls, and ceiling colors based on transparency
            objects_to_update = {
                'floor': self.level.floor.get_children(),
                'walls': self.level.walls.get_children(),
                'ceil': self.level.ceil.get_children()
            }

            for i, (key, children) in enumerate(objects_to_update.items()):
                for obj in children:
                    if obj.isHidden():
                        obj.show()
                    color_choice = random.choice(self.color_choices)  # Randomly select a color
                    
                    # Ensure the index for transparencies does not exceed its length
                    transparency_value = transparencies[i] if i < len(transparencies) else 0.05  # Default to 1.0 if out of bounds
                    obj.set_color(*(color_choice + (transparency_value*0.5,)))  # Apply transparency
            for p, portal in enumerate(self.level.portals):
                # Find the base and flower nodes
                base_node = portal.find("**/base")
                flower_node = portal.find("**/flower")
                
                # Make flower rotate or adjust orientation based on time or clock
                flower_node.setHpr(self.clock * 30,self.clock * 30,self.clock * 30)
                flower_node.setScale(2*((sin(self.clock)+1)/2))
                base_node.setScale(sin(self.clock)*2)
                # Apply transparency if necessary
                flower_node.setTransparency(TransparencyAttrib.MAlpha)  # Make the part use alpha transparency

                # Set the color write to False using ColorWriteAttrib for the flower node
                flower_node.setDepthTest(True)
                base_node.setH(-self.clock)
                
                # Randomly choose a color from the color choices list
                color_choice = random.choice(self.color_choices)
                # Create the emissive color using the selected color_choice
                emission_color = LVecBase4f(color_choice[0], color_choice[1], color_choice[2], (sin(self.clock*0.06) + 1)/2 )  # Use RGB and set alpha to 1 for full opacity
                # Randomly choose a color from the color choices list
                color_choice = random.choice(self.color_choices)
                # Create the emissive color using the selected color_choice
                emission_color2 = LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 0.75)  # Use RGB and set alpha to 1 for full opacity

                flower_node.setColor(emission_color)
                base_node.setColor(emission_color2)
               
            for n, npc_node in enumerate(self.level.npc_mounts):
                emblem = npc_node.find('**/npcEmblem')
                face = npc_node.find('**/npcFace')
                
                # Set random colors for emblem and face
                color_choice = random.choice(self.color_choices)
                emblem.set_color(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 0.5))  # Emblem color with some transparency
                
                color_choice = random.choice(self.color_choices)
                face.set_color(LVecBase4f(color_choice[0], color_choice[1], color_choice[2], 1))  # Face color fully opaque

                # Get the current time
                time = globalClock.getFrameTime()

                # Calculate Z position with a sine wave
                amplitude = 0.05  # Amplitude of the oscillation
                period = 2.0  # Duration of one full oscillation (2 seconds)
                frequency = 2 * math.pi / period  # Frequency to complete one oscillation in 2 seconds

                # Calculate the new Z offset based on sine wave
                bobbing_height = amplitude * math.sin(frequency * time)

                # Get the original position of the NPC (should be stored when the bobbing starts)
                original_pos = npc_node.getPos()  # Get the current position (this should be the original position at start)

                # Apply the oscillation relative to the original position (only change the Z value)
                npc_node.setZ(original_pos.getZ() + bobbing_height)
                npc_node.setDepthTest(False)
                
            #    print(npc_node)
            #    print(color_choice)

        # Increment clock and get delta time
        self.clock += 1
        dt = globalClock.getDt()
        self.processInput(dt)

        # Camera positioning based on player's ball position
        base.cam.set_x(self.player.ballNP.get_x())
        base.cam.set_y(self.player.ballNP.get_y() - 48)
        base.cam.set_z(self.player.ballNP.get_z() + 16)
        base.cam.look_at(self.player.ballNP)
        
        # Perform physics update
        self.level.world.doPhysics(dt, 25, 2.0 / 360.0)
        
        return task.cont

    
    def transition(self, exit_stage, lvl = None):
        if exit_stage == None:
            self.exit_stage = 'main_menu'
        else:
            self.exit_stage = exit_stage    
        base.flow.transition(self.exit_stage)
        
    def exit(self, data):
        self.star_node.removeNode()
        self.star_decal.removeNode()
        self.imageObject2.removeNode()
        self.imageObject3.removeNode()
        base.taskMgr.remove('rotate_star')
        self.player.ball_roll.stop()
        self.level.world.removeRigidBody(self.level.floorNP.node())
        self.level.world.removeRigidBody(self.level.wallsNP.node())
        
        self.level.world.removeRigidBody(self.player.ballNP.node())
        #self.level.world = None
        self.level.audio.stopLoopingAudio()
        #self.debugNP = None
        self.level.debugNP.detachNode()
        self.level.debugNP.removeNode()
        self.level.groundNP = None
        #self.player.ballNP = None
        self.player.ballNP.detachNode()
        self.player.ballNP.removeNode()
        for n, npc in enumerate(self.level.npc_mounts):
            npc.detachNode()
            npc.removeNode()
        for p, portal in enumerate(self.level.portals):
            portal.detachNode()
            portal.removeNode()
        for l, letter in enumerate(render.findAllMatches('**/letter**')):
            letter.detachNode()
            letter.removeNode()
        self.level.worldNP.removeNode()
        base.ignore('enter')
        base.ignore("gamepad-face_a")
        base.ignore("space")
        base.ignore("gamepad-face_a-up")
        base.ignore("space-up")
        base.ignore("gamepad-face_b")
        base.ignore("shift")
        base.ignore("gamepad-face_b-up")
        base.ignore("shift-up")
        
        #self.ball.detachNode()
        base.bgm.stopMusic()
        base.cam.set_z(1)
        base.cam.set_x(0)
        base.cam.set_y(0)
        base.cam.set_hpr(0,0,0)
        base.taskMgr.remove('update')
        for n, node in enumerate(aspect2d.findAllMatches('**/dialog_card')):
            node.detachNode()
            node.removeNode()
        return data