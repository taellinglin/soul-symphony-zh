import os
import ast
import subprocess


def clean_and_format_files(directory):
    """
    Scans the directory and its subdirectories for Python files,
    removes placeholder docstrings, fixes indentation, and formats them using black.

    Args:
        directory (str): The directory to scan.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Read the Python file content
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Remove placeholder docstrings
                    content = remove_placeholder_docstrings(content)

                    # Parse the file into an AST for indentation adjustments
                    tree = ast.parse(content)
                    lines = content.splitlines()
                    updated_lines = lines[:]
                    insertions = []

                    # Fix indentation and ensure docstrings are correctly placed
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) or isinstance(
                            node, ast.ClassDef
                        ):
                            if not ast.get_docstring(node):
                                # Check for missing docstring and insert the placeholder docstring
                                insert_line = (
                                    node.body[0].lineno - 1
                                    if node.body
                                    else node.lineno
                                )
                                indent = " " * node.col_offset
                                placeholder = f"{indent}"
                                insertions.append((insert_line, placeholder))

                    # Apply insertions in reverse order to avoid shifting lines
                    for lineno, placeholder in reversed(insertions):
                        updated_lines.insert(lineno, placeholder)

                    # Write updated content back to the file
                    updated_content = "\n".join(updated_lines)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)

                    # Format the file using black
                    print(f"Formatting {file_path} with black...")
                    subprocess.run(["black", file_path], check=True)
                    print(f"Formatted {file_path}.")

                except subprocess.CalledProcessError as e:
                    print(f"Error formatting {file_path} with black: {e}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


def remove_placeholder_docstrings(content):
    """
    Removes all placeholder docstrings (\"\"\"Generated docstring placeholder.\"\"\") from the content.

    Args:
        content (str): The content of the Python file.

    Returns:
        str: The content with placeholder docstrings removed.
    """
    return content.replace("", "")


if __name__ == "__main__":
    # Start from the current working directory (CWD)
    cwd = os.getcwd()
    clean_and_format_files(cwd)
