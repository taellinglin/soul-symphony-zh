import os
import subprocess


def remove_null_bytes_and_format(directory):
    """
    Scans the current directory and its subdirectories for Python files,
    removes null bytes, and formats them using black.

    Args:
        directory (str): The directory to scan.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Remove null bytes from the file
                    with open(file_path, "rb") as f:
                        content = f.read()

                    if b"\x00" in content:
                        print(f"Null bytes found in {file_path}. Cleaning...")
                        cleaned_content = content.replace(b"\x00", b"")
                        with open(file_path, "wb") as f:
                            f.write(cleaned_content)
                        print(f"Null bytes removed from {file_path}.")

                    # Format Python file using black
                    print(f"Formatting {file_path} with black...")
                    subprocess.run(["black", file_path], check=True)
                    print(f"Formatted {file_path}.")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    # Start from the current working directory (CWD)
    cwd = os.getcwd()
    remove_null_bytes_and_format(cwd)
