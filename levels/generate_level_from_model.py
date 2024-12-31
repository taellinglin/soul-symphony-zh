import bpy
import numpy as np
import tensorflow as tf
import os
import argparse

# Path to the trained model
MODEL_FILE = "enhanced_blend_model.h5"
# Output directory for generated files
OUTPUT_DIR = "./generated_dungeons"

# Number of dungeons to generate
NUM_DUNGEONS = 100

# Load the trained model
def load_model():
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(f"Model file {MODEL_FILE} not found.")
    return tf.keras.models.load_model(MODEL_FILE)

# Generate dungeon data using the model
def generate_dungeon(model, prompt):
    """
    Generate a dungeon using the trained model and a prompt.
    The prompt helps define the characteristics of the dungeon.
    """
    random_features = np.random.rand(1, 3).astype(np.float32)  # Generates a (1, 3) input
    prediction = model.predict(random_features)

    num_objects = max(1, int(prediction[0][0]))  # Ensure at least 1 object
    scale_avg = max(0.1, float(prediction[0][1]))  # Avoid zero or negative scales

    objects = []
    for i in range(num_objects):
        obj_data = {
            "name": f"Object_{i}",
            "vertices": [
                [0, 0, 0],  # Vertex 1
                [1, 0, 0],  # Vertex 2
                [1, 1, 0],  # Vertex 3
                [0, 1, 0],  # Vertex 4
            ],  # Square floor (will be extruded for room)
            "scale": [scale_avg, scale_avg, scale_avg],
            "location": [i * 2.0, 0.0, 0.0],  # Spaced out along X-axis
        }
        objects.append(obj_data)

    # Handle prompt and adjust level design accordingly
    if 'ramp' in prompt.lower():
        # Add ramp feature to the dungeon (same geometry as floor)
        objects.append({
            "name": "Ramp",
            "vertices": [
                [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]
            ],  # Flat base for the ramp
            "scale": [1.5, 1.5, 1],
            "location": [0, 0, 0],
        })

    dungeon_data = {
        "objects": objects
    }
    return dungeon_data

# Create floor as one whole geometry
def create_floor(location, scale):
    # Create a single mesh for the floor
    bpy.ops.mesh.primitive_plane_add(size=scale[0], location=location)
    floor = bpy.context.object
    floor.name = "levelFloor"
    return floor

# Create ramp as part of the floor geometry (same mesh)
def create_ramp(location, scale):
    # Create a plane for ramp base
    bpy.ops.mesh.primitive_plane_add(size=scale[0], location=location)
    ramp_base = bpy.context.object
    ramp_base.name = "ramp_base"

    # Select all faces to extrude
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, scale[2])})
    bpy.ops.object.mode_set(mode='OBJECT')

    # Rotate to form a ramp (45 degrees on X and Y axis)
    ramp_base.rotation_euler[0] = np.radians(45)
    ramp_base.rotation_euler[1] = np.radians(45)

    return ramp_base

# Create walls as separate geometry
def create_wall(location, scale):
    # Create wall (extrusion)
    bpy.ops.mesh.primitive_cube_add(size=scale[0], location=location)
    wall = bpy.context.object
    wall.name = "levelWall"
    return wall

# Create ceiling as separate geometry
def create_ceiling(location, scale):
    # Create ceiling (same as wall, but flipped or scaled)
    bpy.ops.mesh.primitive_cube_add(size=scale[0], location=location)
    ceiling = bpy.context.object
    ceiling.name = "levelCeil"
    return ceiling

# Save dungeon data to a .blend file
def save_to_blend(dungeon_data, file_path):
    # Clear existing objects
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Create main nodes (levelFloor, levelWall, levelCeil)
    level_floor_node = bpy.data.objects.new("levelFloor", None)
    level_wall_node = bpy.data.objects.new("levelWall", None)
    level_ceil_node = bpy.data.objects.new("levelCeil", None)

    # Link the nodes to the scene
    bpy.context.scene.collection.objects.link(level_floor_node)
    bpy.context.scene.collection.objects.link(level_wall_node)
    bpy.context.scene.collection.objects.link(level_ceil_node)

    # Create corresponding geometry for each node (floorCol, wallCol, ceilCol)
    floor_col = create_floor((0, 0, 0), (10, 10, 1))  # Floor geometry
    wall_col = create_wall((5, 5, 1), (2, 10, 3))  # Wall geometry
    ceil_col = create_ceiling((0, 0, 10), (10, 10, 1))  # Ceiling geometry

    # Link geometries to their respective nodes
    level_floor_node.location = (0, 0, 0)
    level_wall_node.location = (5, 5, 1)
    level_ceil_node.location = (0, 0, 10)

    # Save to .blend file
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

# Main function
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate a dungeon based on a prompt.")
    parser.add_argument('prompt', type=str, help='The prompt for generating the dungeon (e.g., "half pipes", "ramp", "labyrinth")')

    # Parse arguments
    args = parser.parse_args()

    # Load the trained model
    model = load_model()

    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Generate and save multiple dungeons based on the prompt
    for i in range(1, NUM_DUNGEONS + 1):
        dungeon_data = generate_dungeon(model, args.prompt)
        output_file_blend = os.path.join(OUTPUT_DIR, f"generated_dungeon_{i:03}.blend")
        save_to_blend(dungeon_data, output_file_blend)
        print(f"Generated dungeon {i} saved to {output_file_blend}")

# Run the script
if __name__ == "__main__":
    main()
