from direct.particles.ParticleEffect import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup  # Correct import for ForceGroup
from direct.particles import ParticleManagerGlobal
from direct.particles import Particles
from panda3d.physics import RectangleEmitter
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
import glob
from panda3d.core import Filename, LVector3, LVector4, LPoint3, LPoint3f
import random
class SoulParticles:
    def __init__(self, texture_directory, parent_node):
        self.texture_directory = texture_directory
        self.parent_node = parent_node
        self.effect = None
        self.p = ParticleEffect()
        self.colors = [
            LVector4(1.0, 0.0, 0.0, 1.0),  # Red
            LVector4(1.0, 0.5, 0.0, 1.0),  # Orange
            LVector4(1.0, 1.0, 0.0, 1.0),  # Yellow
            LVector4(0.0, 1.0, 0.0, 1.0),  # Green
            LVector4(0.0, 0.0, 1.0, 1.0),  # Blue
            LVector4(0.29, 0.0, 0.51, 1.0),  # Indigo
            LVector4(0.93, 0.51, 0.93, 1.0)  # Violet
        ]
        self.color_index = 0
        self.time_since_last_change = 0.0
        self.color_change_interval = 0.5  # Change color every 0.5 seconds
        self.dt = globalClock.get_dt()
        
    def load_textures(self, directory):
        """Load all textures from the specified directory."""
        print(f"Loading textures from directory: {directory}")
        texture_files = glob.glob(f"{directory}/*.png")
        textures = []
        for file in texture_files:
            texture = loader.loadTexture(Filename.fromOsSpecific(file))
            if texture:
                textures.append(texture)
                print(f"Loaded texture: {file}")
            else:
                print(f"Failed to load texture: {file}")
        print(f"Total textures loaded: {len(textures)}")
        return textures

    def create_matrix_effect(self, t):
        print("Creating matrix effect...")
        self.p.cleanup()
        self.p = ParticleEffect()
         # Reset the effect and set scale
        self.p.reset()
        self.p.setScale(1, 1, 1)

        # Create a new particle system
        self.p0 = Particles.Particles('particles-1')

        # Particles parameters
        self.p0.setFactory("PointParticleFactory")
        self.p0.setRenderer("SpriteParticleRenderer")
        self.p0.setEmitter("BoxEmitter")
        self.p0.setPoolSize(4096)  # Number of particles
        self.p0.setBirthRate(0.00002)  # Rate of particle creation
        self.p0.setLitterSize(256)  # Number of particles per burst
        self.p0.setLitterSpread(128)  # Spread of particles within each burst
        self.p0.setSystemLifespan(20)  # Lifespan of the entire particle system (in seconds)
        self.p0.setLocalVelocityFlag(1)  # Local velocity flag
        self.p0.setSystemGrowsOlderFlag(0)  # Particles should not grow older

        # Factory parameters (control particle behavior)
        self.p0.factory.setLifespanBase(1)  # Base lifespan of each particle
        self.p0.factory.setLifespanSpread(5)  # Spread in particle lifespan
        self.p0.factory.setMassBase(10.0)  # Mass of each particle
        self.p0.factory.setMassSpread(9)  # Variation in particle mass
        self.p0.factory.setTerminalVelocityBase(1000.0)  # Terminal velocity of particles
        self.p0.factory.setTerminalVelocitySpread(500)  # Spread in terminal velocity

        # Renderer parameters (control appearance)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(0.5)  # Full opacity
        self.p0.renderer.setTexture(base.loader.loadTexture('stars/00041-2773312458.png'))  # Texture for particles
        self.p0.renderer.setColor(LVector4(1.0, 1.0, 1.0, 1.0))  # White color (RGBA)
        self.p0.renderer.setXScaleFlag(True)  # Disable scaling along X-axis
        self.p0.renderer.setYScaleFlag(True)  # Disable scaling along Y-axis
        self.p0.renderer.setAnimAngleFlag(False)  # No animation on particle angle
        self.p0.renderer.setInitialXScale(0.025)  # Initial size of particles (X)
        self.p0.renderer.setFinalXScale(0.0025)  # Final size of particles (X)
        self.p0.renderer.setInitialYScale(0.025)  # Initial size of particles (Y)
        self.p0.renderer.setFinalYScale(0.0025)  # Final size of particles (Y)
        self.p0.renderer.setNonanimatedTheta(360.0)  # No rotation on the particles
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)  # Linear blend for transparency
        self.p0.renderer.setAlphaDisable(False)  # Keep alpha blending enabled

        # Emitter parameters (control emission behavior)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)  # Emit particles in a radiating pattern
        self.p0.emitter.setAmplitude(100.0)  # No amplitude (adjust if you need more force)
        self.p0.emitter.setAmplitudeSpread(100.0)  # No spread in amplitude
        self.p0.emitter.setOffsetForce(LVector3(0.0, 0.0, -90.2))  # Apply a slight downward force
        self.p0.emitter.setExplicitLaunchVector(LVector3(0.0, 0.0, -90.0))  # Emit particles downward
        self.p0.emitter.setRadiateOrigin(LPoint3(0.0, 0.0, 0.0))  # Emit from the origin (0,0,0)
        self.p0.emitter.setMinBound(LPoint3(-1000, -1000, -1000))  # Minimum bounds of the emitter area
        self.p0.emitter.setMaxBound(LPoint3f(1000, 1000, 1000))  # Maximum bounds of the emitter area

        # Add the particles to the effect
        self.p.addParticles(self.p0)

        # Apply force groups (e.g., gravity or other forces)
        f0 = ForceGroup.ForceGroup('default')
        self.p.addForceGroup(f0)


    


        # Load and add textures
        textures = self.load_textures(self.texture_directory)
        if not textures:
            raise FileNotFoundError(f"No textures found in directory: {self.texture_directory}")

        for texture in textures:
            self.p0.renderer.addTexture(texture)
        print(f"Added {len(textures)} textures to renderer.")
        self.t = t
        self.p.reparentTo(self.t)

        print("Starting particle effect...")
        
        base.taskMgr.add(self.update, 'star_update')
        self.p.start(self.t)
        
    def loadParticleConfig(self, filename):
            # Start of the code from steam.ptf
            self.p.cleanup()
            self.p = ParticleEffect()
            self.p.loadConfig(Filename(filename))
            # Sets particles to birth relative to the teapot, but to render at
            # toplevel
            self.p.start(self.t)
            self.p.setPos(0, 0.000, 0)
    def load_font_glyphs(self, font_path):
        """Loads glyphs from the font and returns them as textures."""
        print(f"Loading glyphs from font: {font_path}")
        glyph_textures = []

        text_node = TextNode('glyph')
        text_node.setFont(loader.loadFont(font_path))
        text_node.setTextColor(1, 1, 1, 1)
        text_node.setAlign(TextNode.A_center)

        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            text_node.setText(char)
            texture = self.create_texture_from_text(text_node)
            if texture:
                glyph_textures.append(texture)
                print(f"Created texture for glyph: {char}")
            else:
                print(f"Failed to create texture for glyph: {char}")

        print(f"Total glyph textures created: {len(glyph_textures)}")
        return glyph_textures

    def create_texture_from_text(self, text_node):
        """Creates a texture from the rendered text node."""
        print(f"Creating texture from text node with text: {text_node.getText()}")

        cm = CardMaker("text_card")
        card = base.render.attachNewNode(cm.generate())
        text_node_path = card.attachNewNode(text_node)
        text_node_path.setScale(1)  # Ensure proper scaling for the render

        # Capture image from the text node
        img = PNMImage()
        card.node().setIntoCollideMask(0)  # Avoid interference with collision
        base.graphicsEngine.renderFrame()
        base.win.getScreenshot(img)

        texture = Texture()
        texture.load(img)

        card.removeNode()  # Clean up the temporary card
        print("Texture created successfully.")
        return texture
    
    def update(self, task):
        """
        Update the particle system with a color cycle.
        :param task: The task object, which provides information about the elapsed time.
        """
        self.randomize_color()  # Randomize color in every frame
        dt = task.dt  # Access the elapsed time from the task
        self.time_since_last_change += dt
        
        if self.time_since_last_change >= self.color_change_interval:
            # Cycle to the next color in the ROYGBIV array
            self.color_index = (self.color_index + 1) % len(self.colors)
            
            if self.p0 and self.p0.renderer:  # Check if self.p0 and its renderer are valid
                self.p0.renderer.setColor(self.colors[self.color_index])
                #print(f"Cycled to color: {self.colors[self.color_index]}")
            else:
                #print("Error: self.p0 or self.p0.renderer is None during color cycling.")
            
                self.time_since_last_change = 0.0  # Reset the timer
            
        return task.cont  # Continue the task

    def randomize_color(self):
        """
        Set the particle color to a random color from the ROYGBIV list.
        """
        if self.p0 and self.p0.renderer:  # Check if self.p0 and its renderer are valid
            random_color = random.choice(self.colors)
            self.p0.renderer.setColor(random_color)
            #print(f"Randomized color: {random_color}")
        else:
            #print("Error: self.p0 or self.p0.renderer is None during random color update.")
            pass

    def cleanup(self):
        """Clean up the particle system and associated resources."""
        print("Cleaning up particle effect...")
        
        # Stop the particle effect
        if self.p:
            self.p.cleanup()  # Clean up the particle effect resources
            self.p = None  # Set the particle effect reference to None to release it
        
        # Reset any textures or other resources
        self.p0 = None  # Remove the particle system (optional, as cleanup is already done)
        
        # Optional: Reset color cycling state
        self.color_index = 0
        self.time_since_last_change = 0.0
        
        # Optional: Remove any additional tasks if needed
        if 'star_update' in base.taskMgr.getTasks():
            base.taskMgr.remove('star_update')
        
        print("Cleanup completed.")
