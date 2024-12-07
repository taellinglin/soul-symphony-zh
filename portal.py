
from direct.showbase.Loader import Loader

from audio3d import audio3d

from panda3d.core import NodePath



class Portal:
    def __init__(self):
    
        # Load the model for the portal

        self.model = base.loader.loadModel("components/portal00.bam")

        # Set up the portal audio using audio3d

        self.audio3d = audio3d()

        self.portal_loops = self.audio3d.sfx3d.get("portal_loop")

        # Load the textures

        self.texture1 = base.loader.loadTexture("/portal/portall00.png")  # Base texture

        self.texture2 = base.loader.loadTexture(
            "/portal/portall02.png"
        )  # Flower texture

        # Find the base square part of the portal and apply texture1

        base_part = self.model.find(
            "**/base"
        )  # Replace with actual name of the base node

        if not base_part.isEmpty():
            base_part.setTexture(self.texture1)

        # Find the flower object part of the portal and apply texture2

        flower_part = self.model.find(
            "**/flower"
        )  # Replace with actual name of the flower node

        if not flower_part.isEmpty():
            flower_part.setTexture(self.texture2)

        # Position the entire model in the scene

        self.model.reparentTo(base.render)

        self.model.setPos(0, 10, 0)  # Position it in the world (adjust as needed)

        # Optional: Scale the portal to a suitable size

    
        self.model.setScale(2)  # Adjust the scale of the portal

    
    def warp(self):
        pass

    def update(self, task):
        pass