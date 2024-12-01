import os
import shutil
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK


def tag_and_copy_files():
    input_directory = "./"  # Directory containing the .ogg files
    output_directory = "./tagged"  # Directory to copy tagged files to

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get a list of all .ogg files in the input directory
    ogg_files = [f for f in os.listdir(input_directory) if f.endswith(".ogg")]

    for idx, ogg_file in enumerate(ogg_files, start=1):
        input_file = os.path.join(input_directory, ogg_file)
        try:
            # Try loading the audio file with Mutagen's OggVorbis class
            audio_file = OggVorbis(input_file)

            # Set the tags for artist, album, and track number
            audio_file["TPE1"] = "灵林"  # Artist
            audio_file["TALB"] = "灵魂交响乐"  # Album
            audio_file["TRCK"] = str(idx)  # Track number
            audio_file.save()  # Save the tags

            # Construct the new filename with track number
            new_filename = f"灵林 - 灵魂交响乐 - {str(idx).zfill(2)}.ogg"
            output_file = os.path.join(output_directory, new_filename)

            # Copy the tagged file to the 'tagged' folder with the new name
            shutil.copy(input_file, output_file)

            print(f"Tags written and file copied for {ogg_file}:")
            print(f"Artist: 灵林")
            print(f"Album: 灵魂交响乐")
            print(f"Track: {str(idx).zfill(2)}")
            print(f"Copied to {output_file}")
            print("------------")

        except Exception as e:
            print(f"Error processing {ogg_file}: {e}")


if __name__ == "__main__":
    tag_and_copy_files()
