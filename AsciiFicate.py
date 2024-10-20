# AsciiFicate.py
import subprocess
import os
from PIL import Image
from time import sleep

def image_to_ascii(image_path, width, invert_colors=False):
    # Open the image
    img = Image.open(image_path)

    # Check if the image has an alpha channel (transparent)
    has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)

    # Convert palette images to RGBA
    if img.mode == 'P':
        img = img.convert('RGBA')

    # Calculate the new height to maintain the aspect ratio
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width / 2)  # Divided by 2 to better fit ASCII

    # Resize the image
    img = img.resize((width, height))

    # Convert to grayscale
    img = img.convert("LA")  # "LA" to maintain the alpha channel
    grayscale_img = img.convert("L")  # Convert to grayscale

    # Define ASCII characters based on opacity
    ascii_chars = '@%#*+=-:. '

    # Convert each pixel to an ASCII character
    ascii_str = ''
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))

            # If there is an alpha channel and it is transparent, add a space
            if has_alpha and pixel[1] == 0:  # pixel[1] is the opacity
                ascii_str += ' '  # Space for transparent pixels
            else:
                brightness = grayscale_img.getpixel((x, y))  # Get brightness
                if invert_colors:
                    brightness = 255 - brightness  # Invert brightness

                # Map the pixel brightness to the length of the ASCII characters
                brightness_index = brightness * (len(ascii_chars) - 1) // 255  # Normalize to the length of ASCII characters
                ascii_str += ascii_chars[brightness_index]  # Add corresponding character
        ascii_str += '\n'

    return ascii_str

def main():
    while True:  # Loop to repeat the process if the user desires
        print("Image to ASCII Converter")

        # List images in the folder
        images = [f for f in os.listdir('Images') if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not images:
            print("There are no images in the 'Images' folder.")
            input('-Restart-')
            subprocess.run("./AsciiFicate.py")
            return

        print("Available images:")
        for i, filename in enumerate(images):
            print(f"{i + 1}: {filename}")

        # Ask the user to select an image
        try:
            choice = int(input("Select the number of the image you want to convert: ")) - 1
            if choice < 0 or choice >= len(images):
                raise ValueError("Invalid selection.")
            image_path = os.path.join('Images', images[choice])
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Ask for size and opacity
        try:
            width = int(input("Enter the output width in characters: "))
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Ask if the user wants to invert colors
        invert_colors = input("Do you want to invert the colors? (y/n): ").strip().lower() == 'y'

        print(f"\nConverting: {images[choice]}")
        ascii_art = image_to_ascii(image_path, width, invert_colors=invert_colors)
        
        # Print the ASCII art in the console
        print(ascii_art)

        # Ask if the user wants to use it in a print
        use_in_print = input("Do you want to use this in a print? (y/n): ").strip().lower()
        if use_in_print in ['y']:
            print_string = ascii_art.replace('\n', '\\n')  # Escape new lines
            print("You can use the following string in your program:\n")
            print(f'print("{print_string}")\n')
            input("Reset")
            print("...\n")
            sleep(1)
        else:
            input("Reset")
            print("...\n")
            sleep(1)

if __name__ == "__main__":
    main()
# AsciiFicate
# Ver: 1.0
# [ROMA]software 
