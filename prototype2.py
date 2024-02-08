import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def display_images(images, titles):
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(18, 12))

    for i in range(num_images):
        axes[i].imshow(images[i])
        axes[i].set_title(titles[i])
        axes[i].axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()


# Load the image
img_path = 'cat.jpg'
original_image = np.array(Image.open(img_path))

# Define the number of rows and columns for the square bits
num_rows = 8
num_cols = 8

# Calculate the height and width of each square bit
bit_height = original_image.shape[0] // num_rows
bit_width = original_image.shape[1] // num_cols

# Cut the original image into square bits
square_bits = np.array([original_image[i * bit_height: (i + 1) * bit_height, j * bit_width: (j + 1) * bit_width]
                        for i in range(num_rows) for j in range(num_cols)])

# Define the reconstruction order for Reconstructed Image 1
reconstruct_order_1 = [[0, 2, 4, 6], [8, 10, 12, 14], [16, 18, 20, 22], [24, 26, 28, 30],
                       [32, 34, 36, 38], [40, 42, 44, 46], [48, 50, 52, 54], [56, 58, 60, 62]]

# Define the reconstruction order for Reconstructed Image 2
reconstruct_order_2 = [[1, 3, 5, 7], [9, 11, 13, 15], [17, 19, 21, 23], [25, 27, 29, 31],
                       [33, 35, 37, 39], [41, 43, 45, 47], [49, 51, 53, 55], [57, 59, 61, 63]]

# Reconstruct images from square bits using the specified orders
reconstructed_image_1 = np.concatenate([np.concatenate([square_bits[i] for i in row], axis=0) for row in reconstruct_order_1], axis=1)
reconstructed_image_2 = np.concatenate([np.concatenate([square_bits[i] for i in row], axis=0) for row in reconstruct_order_2], axis=1)

# Display images
display_images([original_image, reconstructed_image_1, reconstructed_image_2],
               ['Original Image', 'Reconstructed Image 1', 'Reconstructed Image 2'])
