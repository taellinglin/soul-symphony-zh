import os


def remove_null_bytes_from_file(filepath):
    """Removes null bytes from the given Python file."""

    try:
        # Open the file in binary mode to handle all byte sequences

        with open(filepath, "rb") as file:
            content = file.read()

        # Remove null bytes

        content = content.replace(b"\x00", b"")

        # Reopen the file in write mode and save the cleaned content

        with open(filepath, "wb") as file:
            file.write(content)

        print(f"Null bytes removed from {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")


def remove_null_bytes_in_directory(directory):
    """Recursively removes null bytes from all .py files in the directory."""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                remove_null_bytes_from_file(filepath)


if __name__ == "__main__":
    # Get the current working directory

    cwd = os.getcwd()

    # Remove null bytes from all .py files in the current directory and subdirectories

    remove_null_bytes_in_directory(cwd)
