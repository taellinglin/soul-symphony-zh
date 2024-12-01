import os
from mutagen.oggvorbis import OggVorbis


def clean_titles_in_ogg_files():
    # Get the current working directory
    cwd = os.getcwd()

    # Loop through all files in the directory
    for filename in os.listdir(cwd):
        if filename.endswith(".ogg"):
            try:
                # Load the OGG file
                audio_file = OggVorbis(os.path.join(cwd, filename))

                # Extract the title from the metadata
                title = audio_file.get("TITLE", None)

                if title:
                    # Clean the title by removing unwanted characters like '[', ']', and any extra spaces
                    cleaned_title = title[0].strip("[]', ").strip()

                    # Generate the new filename
                    new_filename = f"灵林 - 灵魂交响乐 - {cleaned_title}.ogg"

                    # Create the full path for renaming
                    new_file_path = os.path.join(cwd, new_filename)

                    # Rename the file
                    os.rename(os.path.join(cwd, filename), new_file_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Title not found for '{filename}', skipping...")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    clean_titles_in_ogg_files()
