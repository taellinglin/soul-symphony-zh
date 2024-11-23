import os
import chardet

def convert_to_utf8(file_path):
    """
    Converts a file to UTF-8 encoding, removing invalid characters if necessary.
    """
    try:
        # Read file content and detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected_encoding = chardet.detect(raw_data)['encoding']

        if detected_encoding is None:
            print(f"Could not detect encoding for {file_path}. Skipping.")
            return

        # Decode content using detected encoding
        content = raw_data.decode(detected_encoding, errors='ignore')

        # Write content back as UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Converted {file_path} from {detected_encoding} to UTF-8.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    """
    Recursively processes all .py files in the directory, converting them to UTF-8.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                convert_to_utf8(file_path)

if __name__ == "__main__":
    # Process current working directory
    cwd = os.getcwd()
    print(f"Processing directory and subfolders: {cwd}")
    process_directory(cwd)
    print("Conversion complete.")
