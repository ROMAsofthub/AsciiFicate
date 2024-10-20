# AsciiFicate.py
import subprocess
import os
from PIL import Image
from time import sleep

def image_to_ascii(image_path, width, invert_colors=False):
    # Abrir la imagen
    img = Image.open(image_path)

    # Verificar si la imagen tiene un canal alfa (transparente)
    has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)

    # Convertir imágenes en modo de paleta a RGBA
    if img.mode == 'P':
        img = img.convert('RGBA')

    # Calcular la nueva altura para mantener la relación de aspecto
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width / 2)  # Dividido por 2 para ajustar mejor a ASCII

    # Redimensionar la imagen
    img = img.resize((width, height))

    # Convertir a escala de grises
    img = img.convert("LA")  # "LA" para mantener el canal alfa
    grayscale_img = img.convert("L")  # Convertir a escala de grises

    # Definir caracteres ASCII en función de la opacidad
    ascii_chars = '@%#*+=-:. '

    # Convertir cada píxel a un carácter ASCII
    ascii_str = ''
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))

            # Si hay un canal alfa y es transparente, agregar un espacio
            if has_alpha and pixel[1] == 0:  # pixel[1] es la opacidad
                ascii_str += ' '  # Espacio para píxeles transparentes
            else:
                brightness = grayscale_img.getpixel((x, y))  # Obtener el brillo
                if invert_colors:
                    brightness = 255 - brightness  # Invertir brillo

                # Mapear el brillo del píxel a la longitud de los caracteres ASCII
                brightness_index = brightness * (len(ascii_chars) - 1) // 255  # Normalizar a la longitud de los caracteres ASCII
                ascii_str += ascii_chars[brightness_index]  # Agregar carácter correspondiente
        ascii_str += '\n'

    return ascii_str

def main():
    while True:  # Bucle para repetir el proceso si el usuario lo desea
        print("Transformador de imágenes a ASCII")

        # Listar imágenes en la carpeta
        images = [f for f in os.listdir('Images') if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not images:
            print("No hay imágenes en la carpeta 'Images'.")
            input('-Reiniciar-')
            subprocess.run("./AsciiFicate.py")
            return

        print("Imágenes disponibles:")
        for i, filename in enumerate(images):
            print(f"{i + 1}: {filename}")

        # Solicitar al usuario que seleccione una imagen
        try:
            choice = int(input("Selecciona el número de la imagen que deseas convertir: ")) - 1
            if choice < 0 or choice >= len(images):
                raise ValueError("Selección no válida.")
            image_path = os.path.join('Images', images[choice])
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Solicitar tamaño y opacidad
        try:
            width = int(input("Introduce el ancho de la salida en caracteres: "))
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Preguntar si se desea invertir colores
        invert_colors = input("¿Deseas invertir los colores? (y/n): ").strip().lower() == 'y'

        print(f"\nConvirtiendo: {images[choice]}")
        ascii_art = image_to_ascii(image_path, width, invert_colors=invert_colors)
        
        # Imprimir el arte ASCII en la consola
        print(ascii_art)

        # Preguntar si se desea usar en un print
        use_in_print = input("¿Deseas usar esto en un print? (y/n): ").strip().lower()
        if use_in_print in ['y']:
            print_string = ascii_art.replace('\n', '\\n')  # Escapar saltos de línea
            print("Puedes usar el siguiente string en tu programa:\n")
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
