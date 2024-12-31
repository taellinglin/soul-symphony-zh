import bpy
import os
import json

# Path to the directory containing .blend files
BLEND_DIR = "./blend"
# Path to save the processed dataset
OUTPUT_FILE = "dataset.json"

# Function to extract data from the current Blender file
def extract_data():
    data = {
        "objects": [],
        "materials": [],
    }

    # Extract geometry and UVs
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            mesh_data = {
                "name": obj.name,
                "vertices": [list(vert.co) for vert in obj.data.vertices],
                "faces": [list(face.vertices) for face in obj.data.polygons],
                "uvs": []
            }

            # Extract UV coordinates
            if obj.data.uv_layers:
                uv_layer = obj.data.uv_layers.active.data
                mesh_data["uvs"] = [list(uv.uv) for uv in uv_layer]

            data["objects"].append(mesh_data)

    # Extract materials and shader nodes
    for material in bpy.data.materials:
        if material.use_nodes:
            nodes = [
                {
                    "name": node.name,
                    "type": node.type
                }
                for node in material.node_tree.nodes
            ]
            data["materials"].append({"name": material.name, "nodes": nodes})

    return data

# Main function to process all .blend files in the directory
def process_blend_files():
    dataset = []

    # Ensure the directory exists
    if not os.path.exists(BLEND_DIR):
        print(f"Directory {BLEND_DIR} does not exist.")
        return

    # Iterate through all .blend files
    for file_name in os.listdir(BLEND_DIR):
        if file_name.endswith(".blend"):
            blend_path = os.path.join(BLEND_DIR, file_name)

            try:
                # Open the blend file
                bpy.ops.wm.open_mainfile(filepath=blend_path)
                
                # Extract data and append to the dataset
                data = extract_data()
                data["file_name"] = file_name
                dataset.append(data)
                print(f"Processed {file_name}")

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    # Save the dataset to a JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(dataset, f, indent=4)
    print(f"Dataset saved to {OUTPUT_FILE}")

# Run the script
if __name__ == "__main__":
    process_blend_files()
