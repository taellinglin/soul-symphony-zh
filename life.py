from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, LVector3
import numpy as np
import colorsys
from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase

class GameOfLife3D(ShowBase):
    def __init__(self):
        super().__init__()
        self.grid_size = 16  # Set grid size to 16x16x16
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size), dtype=int)
        self.color_grid = np.zeros((self.grid_size, self.grid_size, self.grid_size, 3), dtype=float)
        self.cubes = {}
        self.starting_pattern()
        self.create_grid()
        self.camera = self.create_default_camera().reparentTo(base.render)
        self.taskMgr.add(self.update, "update")

    def create_default_camera(self):
        # Create and position the camera
        self.camera_node = base.cam
        self.camera_node.set_pos(0, 0, 40)
        self.camera_node.look_at(Point3(self.grid_size // 2, self.grid_size // 2, self.grid_size // 2))
        return self.camera_node

    def rgb_to_hsv(self, r, g, b):
        """Convert RGB to HSV."""
        return colorsys.rgb_to_hsv(r, g, b)

    def hsv_to_rgb(self, h, s, v):
        """Convert HSV back to RGB."""
        return colorsys.hsv_to_rgb(h, s, v)

    def starting_pattern(self):
        """Initialize a recursive fractal-like pattern in 16x16x16 grid."""
        center = self.grid_size // 2
        self.recursive_fill(center, center, center, self.grid_size // 2)

    def recursive_fill(self, x, y, z, size):
        """Recursively fill the grid with a fractal-like structure."""
        if size <= 0:
            return
        # Set the current region to "alive" and color it
        self.grid[x - size:x + size, y - size:y + size, z - size:z + size] = 1
        self.color_grid[x - size:x + size, y - size:y + size, z - size:z + size] = [1, 0, 0]  # Initial red

        # Recursively apply the pattern to smaller regions (creating a fractal effect)
        self.recursive_fill(x - size // 2, y - size // 2, z - size // 2, size // 2)
        self.recursive_fill(x + size // 2, y - size // 2, z - size // 2, size // 2)
        self.recursive_fill(x - size // 2, y + size // 2, z - size // 2, size // 2)
        self.recursive_fill(x + size // 2, y + size // 2, z - size // 2, size // 2)
        self.recursive_fill(x - size // 2, y - size // 2, z + size // 2, size // 2)
        self.recursive_fill(x + size // 2, y - size // 2, z + size // 2, size // 2)
        self.recursive_fill(x - size // 2, y + size // 2, z + size // 2, size // 2)
        self.recursive_fill(x + size // 2, y + size // 2, z + size // 2, size // 2)

    def create_grid(self):
        # Create the grid's cubes in 3D space
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if self.grid[x, y, z] == 1:
                        self.add_cube(x, y, z)

    def add_cube(self, x, y, z):
        # Create a cube at a given position and add it to the scene
        pos = LVector3(x, y, z)
        cube = self.create_custom_cube()
        cube.setScale(1)
        cube.setPos(pos)
        cube.setColor(self.color_grid[x, y, z][0], self.color_grid[x, y, z][1], self.color_grid[x, y, z][2], 1)
        cube.reparentTo(self.render)
        self.cubes[(x, y, z)] = cube

    def create_custom_cube(self):
        """Create a flat-shaded cube."""
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData('cube', format, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, 'vertex')

        # Define vertices of a cube
        vertices = [
            (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)
        ]
        for v in vertices:
            vertex.addData3(*v)

        # Define cube faces with triangles
        triangles = [
            (0, 1, 2), (2, 3, 0), (4, 5, 6), (6, 7, 4), (0, 1, 5), (5, 4, 0),
            (2, 3, 7), (7, 6, 2), (0, 4, 7), (7, 3, 0), (1, 5, 6), (6, 2, 1)
        ]
        
        prim = GeomTriangles(Geom.UHDynamic)
        for t in triangles:
            prim.addVertices(*t)
        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)
        
        cube_node = GeomNode('cube')
        cube_node.addGeom(geom)
        return NodePath(cube_node)

    def update(self, task):
        # Update the grid, apply Game of Life rules, and update colors
        self.grid = self.apply_game_of_life(self.grid)
        self.update_cubes(self.grid)
        base.cam.lookAt(self.grid_size // 2, self.grid_size //2 , self.grid_size //2)
        return task.cont

    def apply_game_of_life(self, grid):
        """Apply the Game of Life rules to the grid."""
        new_grid = grid.copy()
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                for z in range(grid.shape[2]):
                    neighbors = self.count_neighbors(grid, x, y, z)
                    if grid[x, y, z] == 1:
                        if neighbors < 2 or neighbors > 3:
                            new_grid[x, y, z] = 0  # Cell dies
                    else:
                        if neighbors == 3:
                            new_grid[x, y, z] = 1  # Cell becomes alive
        return new_grid

    def count_neighbors(self, grid, x, y, z):
        """Count live neighbors of a cell."""
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if dx == dy == dz == 0:
                        continue
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and 0 <= nz < grid.shape[2]:
                        count += grid[nx, ny, nz]
        return count

    def update_cubes(self, new_grid):
        """Update cubes based on the new grid state."""
        for (x, y, z), cube in list(self.cubes.items()):
            if new_grid[x, y, z] == 0:
                cube.removeNode()
                del self.cubes[(x, y, z)]
            else:
                self.apply_color_rules(x, y, z, new_grid)

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if new_grid[x, y, z] == 1 and (x, y, z) not in self.cubes:
                        self.add_cube(x, y, z)

    def apply_color_rules(self, x, y, z, grid):
        """Update the cube color based on the grid state."""
        cube = self.cubes.get((x, y, z))
        if cube:
            hue = (x + y + z) % 7 / 7.0  # Color cycling over ROYGBIV
            r, g, b = self.hsv_to_rgb(hue, 1.0, 1.0)
            cube.setColor(r, g, b, 1)

app = GameOfLife3D()
app.run()
