
from panda3d.core import Vec3



    
class CameraController:

    def __init__(self, player, base_zoom=10, min_zoom=5, max_zoom=20, elasticity=0.1):

        self.player = player  # Ensure this is a NodePath
        self.base_zoom = base_zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.elasticity = elasticity

        self.target_zoom = base_zoom
        self.current_zoom = base_zoom
        self.previous_position = Vec3(0, 0, 0)

        # Add the update task
        taskMgr.add(self.update_camera, "update_camera_task")
    

    def update_camera(self, task):
        # Check if player NodePath is valid
        if not self.player:  # This will check if self.player is None or invalid
            print("Player object is invalid. Skipping camera update.")
            return task.cont

        # Compute speed
        current_position = self.player.get_pos()
        speed = (current_position - self.previous_position).length()
        self.previous_position = current_position

        # Calculate target zoom
        zoom_factor = speed * 2
        self.target_zoom = max(
            self.min_zoom, min(self.max_zoom, self.base_zoom + zoom_factor)
        )

        # Smooth zoom transition
        self.current_zoom += (self.target_zoom - self.current_zoom) * self.elasticity

        # Update camera position
        camera_position = current_position + Vec3(
            0, -self.current_zoom, self.current_zoom / 2
        )
        base.cam.set_pos(camera_position)

        # Make the camera look at the player
        base.cam.look_at(current_position)

        return task.cont
