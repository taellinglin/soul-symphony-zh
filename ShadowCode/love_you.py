from direct.showbase.ShowBase import ShowBase
from panda3d.core import *  # For other Panda3D classes you're using
from math import sin, cos, pi

class CameraSetup(ShowBase):
    def __init__(self):
        super().__init__()
        print("Initializing CameraSetup...")

        # Position camera for top-down view
        self.camera.set_pos(0, 0, 100)  # Higher up for better top-down view
        self.camera.look_at(0, 0, 0)
        self.camLens.setFov(60)
        
        self.useTrackball()
        self.create_scene()

    def create_scene(self):
        print("\n=== Starting Scene Creation ===")
        self.setBackgroundColor(0, 0, 0)  # Pure black background
        self.create_orb()
        self.create_heart_curls()

    def create_orb(self):
        print("Creating orb pattern...")
        num_rings = 30
        points_per_ring = 360  # Increased for more detail
        max_radius = 25  # Base radius for torus
        
        for ring in range(num_rings):
            # Flatter scaling for torus shape
            ring_ratio = (ring / (num_rings - 1)) * 2 - 1  # -1 to 1
            ring_scale = 1 - (ring_ratio * ring_ratio) * 0.3  # Much flatter scaling
            height = ring - (num_rings / 2)
            
            for i in range(points_per_ring):
                angle = i * (2 * pi / points_per_ring)
                hue = angle / (2 * pi)  # Color based on angle for rainbow effect
                
                # More torus-like shape
                radius = max_radius * (1 - 0.1 * abs(height) / (num_rings / 2))  # Very slight radius variation
                x = radius * cos(angle)
                y = radius * sin(angle)
                z = height * 0.2  # Much flatter in z-direction
                
                cube = self.create_single_cube()
                cube.setPos(x, y, z)
                cube.setScale(0.1)  # Smaller cubes for finer detail
                
                color = self.hue_to_rgb(hue)
                material = Material()
                material.setEmission((*color, 1))
                cube.setMaterial(material)
                cube.reparentTo(self.render)

    def create_heart_curls(self):
        print("Creating heart curls...")
        num_rings = 80  # Doubled for more detail
        points_per_ring = 360  # Increased for smoother curves
        orb_radius = 25
        
        # Create two curls
        for curl in [-1, 1]:  # Left and right curls
            for ring in range(num_rings):
                ring_progress = ring / num_rings
                ring_scale = 1 - ring_progress * 0.95  # Slightly more gradual taper
                
                # Base height starts from center of orb
                base_height = ring * 0.3  # Reduced height increment for tighter spiral
                curl_angle = ring_progress * pi * 2.5  # Increased rotation for tighter curl
                
                for i in range(points_per_ring):
                    angle = i * (2 * pi / points_per_ring)
                    hue = (ring / num_rings + i / points_per_ring) % 1.0
                    
                    # Create curl shape
                    radius = 15 * ring_scale
                    base_x = radius * cos(angle) + (20 * curl * ring_scale)
                    
                    # Rotate curls to be perpendicular to ground plane
                    if curl > 0:
                        x = base_x * cos(curl_angle)
                        y = base_height + base_x * sin(curl_angle)
                        z = radius * sin(angle)
                    else:
                        x = base_x * cos(-curl_angle + pi)
                        y = base_height + base_x * sin(-curl_angle + pi)
                        z = radius * sin(angle)
                    
                    # Scale everything to fit inside orb
                    scale_factor = 0.8
                    x *= scale_factor
                    y *= scale_factor
                    z *= scale_factor
                    
                    cube = self.create_single_cube()
                    cube.setPos(x, y, z)
                    cube.setScale(0.1)  # Smaller cubes for finer detail
                    
                    color = self.hue_to_rgb(hue)
                    material = Material()
                    material.setEmission((*color, 1))
                    cube.setMaterial(material)
                    cube.reparentTo(self.render)

    def create_single_cube(self):
        format = GeomVertexFormat.get_v3()
        vdata = GeomVertexData('cube', format, Geom.UH_static)
        vertex_writer = GeomVertexWriter(vdata, 'vertex')

        # Define vertices for a cube
        vertices = [
            (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)
        ]
        for vertex in vertices:
            vertex_writer.addData3(*vertex)

        geom = Geom(vdata)
        prim = GeomTriangles(Geom.UH_static)
        
        indices = [
            (0, 1, 2), (2, 3, 0),  # Bottom
            (4, 5, 6), (6, 7, 4),  # Top
            (0, 1, 5), (5, 4, 0),  # Front
            (2, 3, 7), (7, 6, 2),  # Back
            (0, 3, 7), (7, 4, 0),  # Left
            (1, 2, 6), (6, 5, 1)   # Right
        ]
        
        for tri in indices:
            prim.addVertices(*tri)
        
        geom.addPrimitive(prim)
        geom_node = GeomNode('cube')
        geom_node.addGeom(geom)
        
        cube = NodePath(geom_node)
        cube.setTwoSided(True)
        return cube

    def hue_to_rgb(self, hue):
        import colorsys
        return colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    def add_lighting(self):
        # Empty method - we're using only emissive materials
        pass

if __name__ == "__main__":
    app = CameraSetup()
    app.run()
