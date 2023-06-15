from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def rle_encode(img, output_path):
    """
    Run length encoding.
    """
    pixels = np.array(img).flatten()
    runs = []
    run_length = 0
    current_pixel = pixels[0]

    for pixel in pixels:
        if pixel != current_pixel:
            runs.append((run_length, current_pixel))
            run_length = 0
            current_pixel = pixel
        run_length += 1

    runs.append((run_length, current_pixel))

    # Export pixels and runs to a text file
    with open(output_path, "w") as file:
        file.write("Input pixels:\n")
        for pixel in pixels:
            file.write(f"{pixel} ")
        file.write("\n\n")
        file.write("Runs:\n")
        for run in runs:
            file.write(f"{run}\n")

    return {"size": img.size, "runs": runs}


def rle_decode(rle_data):
    """
    Decode an RLE encoded image.
    """
    runs = rle_data["runs"]
    shape = rle_data["size"]
    result = np.zeros(np.prod(shape))
    index = 0

    for run in runs:
        result[index : index + run[0]] = run[1]
        index += run[0]

    return result.reshape(shape[::-1])


def sizeof_fmt(num, suffix="B"):
    """
    Convert bytes to human-readable file sizes.
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, "Yi", suffix)


def show_images(original, decoded, original_file, decoded_file):
    """
    Display the original and decoded images side by side.
    """
    fig, axs = plt.subplots(2, 2, figsize=(8, 5), gridspec_kw={"height_ratios": [5, 1]})

    axs[0, 0].imshow(original)
    axs[0, 0].set_title("Original Image")
    axs[0, 0].axis("off")

    axs[0, 1].imshow(decoded, cmap="binary")
    axs[0, 1].set_title("Decoded Image")
    axs[0, 1].axis("off")

    original_size = os.path.getsize(original_file)
    decoded_size = os.path.getsize(decoded_file)

    axs[1, 0].axis("off")
    axs[1, 0].text(
        0.5,
        0.5,
        f"Original Image Size: {sizeof_fmt(original_size)}",
        ha="center",
        va="center",
    )

    axs[1, 1].axis("off")
    axs[1, 1].text(
        0.5,
        0.5,
        f"Decoded Image Size: {sizeof_fmt(decoded_size)}",
        ha="center",
        va="center",
    )

    plt.tight_layout()
    plt.show()


def compare_file_sizes(original_file, decoded_file):
    """
    Compare the file sizes of the original and decoded images.
    """
    original_size = os.path.getsize(original_file)
    decoded_size = os.path.getsize(decoded_file)

    print(f"Original Image Size: {original_size} bytes")
    print(f"Decoded Image Size: {decoded_size} bytes")


def select_image():
    """
    Open a file dialog to select an image file.
    """
    image_path = filedialog.askopenfilename(
        filetypes=(("Image files", "*.bmp*"), ("All files", "*.*"))
    )
    if image_path:
        process_image(image_path)


def process_image(image_path):
    """
    Process the selected image.
    """
    try:
        img = Image.open(image_path)

        output_file = "encoding_data.txt"

        encoded = rle_encode(img.convert("L"), output_file)

        print(f"RLE: {encoded}")

        decoded_img_data = rle_decode(encoded)

        original_img_data = np.array(img)

        decoded_img = Image.fromarray(np.uint8(decoded_img_data * 255))
        decoded_file = "decoded.bmp"
        decoded_img.save(decoded_file)
        print(f"Saved decoded image as {decoded_file}")

        show_images(original_img_data, decoded_img_data, image_path, decoded_file)

    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The selected file could not be found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def create_gui():
    """
    Create the graphical user interface.
    """
    root = tk.Tk()
    root.title("Fax Coding Demo")

    root.geometry("150x150")

    btn_select = tk.Button(root, text="Select Image", command=select_image)

    window_width = 150
    window_height = 150
    button_width = btn_select.winfo_reqwidth()
    button_height = btn_select.winfo_reqheight()
    position_top = int(window_height / 2 - button_height / 2)
    position_right = int(window_width / 2 - button_width / 2)

    btn_select.place(x=position_right, y=position_top)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
