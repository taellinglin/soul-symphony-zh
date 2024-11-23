import os
import subprocess

def normalize_ogg_files():
    input_directory = "./"  # Directory containing the original .ogg files
    output_directory = "./normalized"  # Directory for the normalized files

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get a list of all .ogg files in the input directory
    ogg_files = [f for f in os.listdir(input_directory) if f.endswith(".ogg")]

    print(f"Found {len(ogg_files)} .ogg files.")

    for ogg_file in ogg_files:
        input_file = os.path.join(input_directory, ogg_file)
        temp_file = os.path.join(output_directory, ogg_file)  # Output file path in 'normalized' directory
        
        print(f"Processing {input_file} -> {temp_file}")

        # Construct FFmpeg command to normalize the file
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ar", "96000",  # Set sample rate to 96000 Hz (you can adjust this if needed)
            "-c:a", "libvorbis",
            "-q:a", "0",  # Quality level (0-10), lower values are better quality
            "-vn",  # No video
            "-y",  # Overwrite output file if it exists
            temp_file
        ]

        try:
            # Run the FFmpeg command
            subprocess.run(command, check=True)

            print(f"Normalized file saved at: {temp_file}")

            print(f"Successfully normalized: {ogg_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error normalizing {ogg_file}: {e}")
        except PermissionError as e:
            print(f"Permission error with {ogg_file}: {e}")

if __name__ == "__main__":
    normalize_ogg_files()
