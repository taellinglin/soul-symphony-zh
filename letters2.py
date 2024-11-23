from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from panda3d.core import GeomNode, Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, TextNode, NodePath, Point3
from panda3d.core import InternalName
from panda3d.core import LPoint3f, LVector3f
import numpy as np
import math

class VertexPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.vertices = []

    def moveTo(self, p0):
        self.vertices.append((p0[0], p0[1]))

    def lineTo(self, p1):
        self.vertices.append((p1[0], p1[1]))

    def curveTo(self, p1, p2, p3):
        self.vertices.append((p1[0], p1[1]))
        self.vertices.append((p2[0], p2[1]))
        self.vertices.append((p3[0], p3[1]))

    def closePath(self):
        pass

class Letters():
    def __init__(self):
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.fonts = {
            'daemon': 'fonts/konnarian/Daemon.otf',
            'chesilin': 'fonts/konnarian/Chesilin.otf',
            'note': 'fonts/konnarian/Note.otf',
            'music': 'fonts/konnarian/Music.otf',
        }
        self.letter_nodes = []
        self.letter_mounts = []
        for font_name, font_path in self.fonts.items():
            if not font_path:
                print(f"Failed to load font: {font_name}")
        self.load_letters()

    def load_letters(self):
        for font_name in self.fonts:
            for letter in self.letters:
                letter_node = self.make_letter(letter, font_name, position=(0, 0, 0), depth=1)
                if letter_node:
                    self.letter_nodes.append(letter_node)

    def make_letter(self, letter, font, position, depth, scale_factor=1.0):
        #print(f"Making letter: {letter}, font: {font}, position: {position}, depth: {depth}")

        # Step 1: Create geometry for the letter
        shape = self.create_letter_shape(letter, font)
        
        if shape:
            print(f"Shape for letter {letter} created successfully.")
            
            # Step 2: Extract vertices from the shape and normalize
            vertices = self.get_vertices_from_shape(shape)
            #print(f"Extracted vertices for letter '{letter}': {vertices}")

            # Step 3: Normalize and scale the vertices (Proportional scaling)
            normalized_vertices = self.normalize_vertices(vertices)
            scaled_vertices = self.scale_vertices(normalized_vertices, scale_factor)
            #print(f"Normalized and scaled vertices for letter '{letter}': {scaled_vertices}")

            # Step 4: Extrude the vertices along the Z-axis, adjusting depth proportionally
            extruded_geometry = self.extrude_vertices(scaled_vertices, depth)
            #print(f"Extruded geometry for letter '{letter}' at depth {depth}: {extruded_geometry}")
            
            # Step 5: Create a GeomNode from the extruded geometry
            geom_node = self.create_geom_node_from_extrusion(extruded_geometry)
            if geom_node:
                #print(f"GeomNode created successfully for letter '{letter}'")

                # Step 6: Set position and reparent to render
                node_path = NodePath(geom_node)
                node_path.set_pos(position)
                node_path.set_scale(2, 2, 2)  # Scale for visual adjustments
                
                node_path.reparent_to(render)
                return node_path
                    
        return None


    def create_letter_shape(self, letter, font_name):
        font_path = self.fonts[font_name]
        font = TTFont(font_path)
        glyph_set = font.getGlyphSet()

        if letter not in glyph_set:
            #print(f"Letter '{letter}' not found in font!")
            return None

        glyph = glyph_set[letter]
        pen = VertexPen(glyph_set)
        glyph.draw(pen)
        return pen.vertices

    def get_vertices_from_shape(self, shape):
        normalized_vertices = self.normalize_vertices(shape)
        return normalized_vertices

    def extrude_vertices(self, vertices, depth):
        # Optionally adjust depth based on the aspect ratio
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        width = max_x - min_x
        scaled_depth = depth * width  # Scale depth based on width

        extruded_vertices = []
        for v in vertices:
            extruded_vertices.append((v[0], v[1], 0))  # Bottom layer
            extruded_vertices.append((v[0], v[1], scaled_depth))  # Top layer

        return extruded_vertices


    def create_geom_node_from_extrusion(self, extruded_vertices):
        rotated_vertices = self.rotate_vertices(extruded_vertices, -90)  # Rotate by 90 degrees
        #print(f"Rotated vertices: {rotated_vertices}")

        vertex_format = GeomVertexFormat.getV3n3cpt2()
        vertex_data = GeomVertexData('letter_vertices', vertex_format, Geom.UH_static)
        
        vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
        normal_writer = GeomVertexWriter(vertex_data, 'normal')
        color_writer = GeomVertexWriter(vertex_data, 'color')

        # Add vertices to the vertex writer
        for v in rotated_vertices:
            vertex_writer.addData3f(v[0], v[1], v[2])
            normal_writer.addData3f(0, 0, 1)  # Normals pointing outwards
            color_writer.addData4f(1, 1, 1, 1)  # White color

        geom = Geom(vertex_data)
        self.add_faces_to_geom(geom, rotated_vertices)
        geom_node = GeomNode('extruded_letter_geom')
        geom_node.addGeom(geom)

        return geom_node

    def add_faces_to_geom(self, geom, rotated_vertices):
        # Modifying vertex data and adding faces
        #print(f"Adding faces to geometry with {len(rotated_vertices)} vertices.")
        
        original_vertex_data = geom.getVertexData()
        vertex_data = GeomVertexData(original_vertex_data)
        vertex_data.setUsageHint(Geom.UHDynamic)
        
        array_data = vertex_data.modifyArray(0)  # Access vertex array
        vertex_writer = GeomVertexWriter(array_data, 0)  # Column for vertices

        # Write each vertex
        for vertex in rotated_vertices:
            vertex_writer.addData3f(vertex[0], vertex[1], vertex[2])

        # Calculate and write normals
        normals = self.calculate_normals(rotated_vertices)
        normal_writer = GeomVertexWriter(array_data, 1)  # Assuming column 1 for normals

        for normal in normals:
            normal_writer.addData3f(normal[0], normal[1], normal[2])

        geom.setVertexData(vertex_data)

        # Add faces (triangles) to the geometry
        self.add_faces_to_geom_from_vertices(geom, rotated_vertices)

    def add_faces_to_geom_from_vertices(self, geom, vertices):
        num_faces = len(vertices) // 4  # Each face consists of 4 vertices (not 3)
        geom_quads = GeomTriangles(Geom.UH_static)

        for i in range(num_faces):
            # Each quad is made of four vertices
            i0 = i * 4
            i1 = i0 + 1
            i2 = i0 + 2
            i3 = i0 + 3

            # Add the vertices to form a quad
            geom_quads.addVertices(i0, i1, i2)
            geom_quads.addVertices(i0, i2, i3)

        #print(f"Added {num_faces} quads to geometry.")
        geom.addPrimitive(geom_quads)


    def calculate_normals(self, vertices):
        normals = []
        for i in range(0, len(vertices) - 2, 3):
            v0 = LPoint3f(*vertices[i])
            v1 = LPoint3f(*vertices[i+1])
            v2 = LPoint3f(*vertices[i+2])
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = edge1.cross(edge2)
            normal.normalize()
            normals.extend([normal] * 3)
       #print(f"Calculated normals: {normals}")
        return normals
    
    def rotate_vertices(self, vertices, angle_degrees):
        # Convert angle to radians
        angle_radians = math.radians(angle_degrees)
        
        # Rotation matrix for rotation around Z-axis (2D rotation)
        cos_theta = math.cos(angle_radians)
        sin_theta = math.sin(angle_radians)
        
        rotated_vertices = []
        
        for v in vertices:
            x, y, z = v
            # Apply the 2D rotation to the x and y coordinates
            rotated_x = cos_theta * x - sin_theta * y
            rotated_y = sin_theta * x + cos_theta * y
            rotated_vertices.append((rotated_x, rotated_y, z))  # Keep z as is for now
        
        return rotated_vertices
    def normalize_vertices(self, shape):
        if isinstance(shape, list):
            # Find the min and max values for x, y, and z coordinates, handling missing z-values
            min_x = min(v[0] for v in shape)
            max_x = max(v[0] for v in shape)
            min_y = min(v[1] for v in shape)
            max_y = max(v[1] for v in shape)
            
            # For z, check if it exists in each vertex, otherwise assume it's 0
            min_z = min(v[2] if len(v) > 2 else 0 for v in shape)
            max_z = max(v[2] if len(v) > 2 else 0 for v in shape)

            normalized_vertices = []
            for v in shape:
                # Unpack x, y and add z if it's missing (assume z=0 for 2D vertices)
                x, y = v[0], v[1]
                z = v[2] if len(v) > 2 else 0  # Default z-value is 0 for 2D vertices

                # Normalize x, y, and z to the range [0, 1] based on the min/max values
                normalized_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0
                normalized_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0
                normalized_z = (z - min_z) / (max_z - min_z) if max_z != min_z else 0

                # Append the normalized (x, y, z) values
                normalized_vertices.append((normalized_x, normalized_y, normalized_z))

            return normalized_vertices
        else:
            #print(f"Shape is not a list: {shape}")
            return []





    def scale_vertices(self, vertices, scale_factor):
        scaled_vertices = []
        for v in vertices:
            # Apply scaling to each vertex
            scaled_vertices.append((v[0] * scale_factor, v[1] * scale_factor, v[2]))
        return scaled_vertices

    def update(self, task):
        return task.cont
