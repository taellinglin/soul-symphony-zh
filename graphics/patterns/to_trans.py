import os
from PIL import Image
import glob

def create_alpha_mask(input_image_path):
    """Convert a grayscale image to an alpha mask where darker pixels are more transparent."""
    # Open the grayscale image
    grayscale_image = Image.open(input_image_path).convert('L')  # Convert to grayscale ('L')
    
    # Create a new RGBA image (adding an alpha channel)
    rgba_image = grayscale_image.convert('RGBA')
    
    # Load pixel data
    pixels = rgba_image.load()
    
    # Iterate over all pixels to set the alpha based on grayscale value
    for y in range(rgba_image.height):
        for x in range(rgba_image.width):
            gray_value = pixels[x, y][0]  # In grayscale, all channels have the same value
            
            # Calculate alpha as the inverse of gray_value (0 -> fully transparent, 255 -> fully opaque)
            alpha = gray_value
            pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2], alpha)
    
    # Overwrite the original image with the updated alpha mask
    rgba_image.save(input_image_path, 'PNG')
    print(f"Alpha mask applied and saved to {input_image_path}")

def process_images_in_directory(root_dir):
    """Process all grayscale images in the directory and subdirectories."""
    # Recursively find all images with .png extension in the directory and subdirectories
    for image_path in glob.iglob(os.path.join(root_dir, '**', '*.png'), recursive=True):
        create_alpha_mask(image_path)

# Run the script on the current working directory
if __name__ == "__main__":
    cwd = os.getcwd()  # Get the current working directory
    process_images_in_directory(cwd)
