from panda3d.core import CardMaker, NodePath


class MotionBlur:
    _instance = None  # Class-level attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        # Check if an instance already exists
        if cls._instance is None:
            # Create a new instance if none exists
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            # Prevent re-initialization of an existing instance
            return
        self._initialized = True

        # Disable clearing the color buffer for the window for blending effect
        base.win.set_clear_color_active(False)

        # Create a full-screen quad for the motion blur effect
        cardmaker = CardMaker("motion_blur_quad")
        cardmaker.set_frame_fullscreen_quad()

        # Attach the quad to a render-to-texture camera, not the main camera
        self.motion_quad = NodePath(cardmaker.generate())
        self.motion_quad.reparent_to(base.render2d)

        # Use a lower alpha value to prevent excessive blending and performance hit
        self.motion_quad.set_color(0, 0, 0, 0.025)
        self.motion_quad.set_transparency(True)

        # Adjust Z order to render the quad above the background
        self.motion_quad.set_bin("background", 0)
        self.motion_quad.set_depth_test(False)
        self.motion_quad.set_depth_write(False)

    def cleanup(self):
        if self.motion_quad is None or self.motion_quad.is_empty():
            return
        # Proceed with cleanup if motion_quad is valid
        self.motion_quad.removeNode()
        self.motion_quad = None
        MotionBlur._instance = None  # Allow new instance creation after cleanup
