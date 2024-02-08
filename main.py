import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def display_images(images, titles, num_rows, num_cols, figsize=(6, 18)):
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)  # Adjust the figure size as needed

    for i in range(num_rows):
        axes[i].imshow(images[i])
        axes[i].set_title(titles[i])
        axes[i].axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)  # Adjust the horizontal and vertical spacing between subplots
    plt.show()


# Load the image
img_path = 'cat.jpg'
original_image = np.array(Image.open(img_path))

# Shred the image vertically
num_shreds = 100
shreds = [original_image[:, i * (original_image.shape[1] // num_shreds): (i + 1) * (original_image.shape[1] // num_shreds), :] for i in range(num_shreds)]

# Specify the order for reconstructing images
reconstruct_order_1 = [2 * i + 1 for i in range(num_shreds // 2)]  # 1st, 3rd, 5th, 7th, 9th bits
reconstruct_order_2 = [i for i in range(1, num_shreds + 1) if i not in reconstruct_order_1]  # Remaining bits

# Reconstruct images from shreds
reconstructed_image_1 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1], axis=1)
reconstructed_image_2 = np.concatenate([shreds[i - 1] for i in reconstruct_order_2], axis=1)

# Merge Reconstructed Image 1 and Reconstructed Image 2
reconstructed_new_image_1_2 = np.concatenate((reconstructed_image_1, reconstructed_image_2), axis=1)

# Define the reconstruction orders for the third row
reconstruct_order_1_1 = [i for i in range(num_shreds) if i % 4 == 0]  # 1st, 5th, 9th, ...
reconstruct_order_1_2 = [i for i in range(num_shreds) if i % 4 == 1]  # 2nd, 6th, 10th, ...
reconstruct_order_1_3 = [i for i in range(num_shreds) if i % 4 == 2]  # 3rd, 7th, 11th, ...
reconstruct_order_1_4 = [i for i in range(num_shreds) if i % 4 == 3]  # 4th, 8th, 12th, ...

# Reconstruct images from shreds using the specified orders
reconstructed_image_1_1 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_1], axis=1)
reconstructed_image_1_2 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_2], axis=1)
reconstructed_image_1_3 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_3], axis=1)
reconstructed_image_1_4 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_4], axis=1)

# Merge the reconstructed images for the third row horizontally
reconstructed_image_1_2_3_4 = np.concatenate((reconstructed_image_1_1, reconstructed_image_1_2, reconstructed_image_1_3, reconstructed_image_1_4), axis=1)

# Resize reconstructed images in the 2nd and 3rd rows to match the width of the original image
reconstructed_new_image_1_2_resized = reconstructed_new_image_1_2[:, :original_image.shape[1], :]
reconstructed_image_1_2_3_4_resized = reconstructed_image_1_2_3_4[:, :original_image.shape[1], :]

# Resize original image to match the width of reconstructed images in the 2nd and 3rd rows
original_image_resized = original_image[:, :reconstructed_new_image_1_2_resized.shape[1], :]

# Display images in three rows
display_images([original_image_resized, reconstructed_new_image_1_2_resized, reconstructed_image_1_2_3_4_resized],
               ['', '', ''], 3, 1)
