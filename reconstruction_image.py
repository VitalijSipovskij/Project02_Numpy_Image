import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def display_images(images, titles, num_rows, num_cols, figsize=(10, 12)):
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)

    for i, ax in enumerate(axes.flat):
        if i < len(images):  # Ensure we don't access out-of-range indices
            print("Index:", i)
            ax.imshow(images[i])
            ax.set_title(titles[i])
            ax.axis('off')
        else:
            ax.axis('off')  # Turn off extra subplots if there are more subplots than images

    # Adjust individual subplot sizes
    for ax in axes.flat:
        ax.set_aspect('auto')  # Ensure images are not distorted
        ax.figure.tight_layout(pad=1.0)

    plt.subplots_adjust(wspace=0.2, hspace=0.1)
    plt.show()


def horizontal_shred(image, num_shreds_hor, rotation=0):
    height, width, _ = image.shape
    shred_height = height // num_shreds_hor
    shreds_strip = []
    for i in range(num_shreds_hor):
        shred = image[i * shred_height:(i + 1) * shred_height, :, :]
        if rotation != 0:
            shred = np.rot90(shred, rotation)
        shreds_strip.append(shred)
    return shreds_strip


def vertical_shred(image, num_shreds_ver, rotation=0):
    height, width, _ = image.shape
    shred_width = width // num_shreds_ver
    shreds_strip = []
    for i in range(num_shreds_ver):
        shred = image[:, i * shred_width:(i + 1) * shred_width, :]
        if rotation != 0:
            shred = np.rot90(shred, rotation)
        shreds_strip.append(shred)
    return shreds_strip


# Load the image
img_path = 'cat.jpg'
original_image = np.array(Image.open(img_path))

# Shred the image vertically num_shreds only effects reconstructed_new_image_1_2 and reconstructed_new_image_1_2_3_4
num_shreds = 100
shreds = [
    original_image[:, i * (original_image.shape[1] // num_shreds): (i + 1) * (original_image.shape[1] // num_shreds), :]
    for i in range(num_shreds)]

# Specify the order for reconstructing images
reconstruct_order_1 = [2 * i + 1 for i in range(num_shreds // 2)]
reconstruct_order_2 = [i for i in range(1, num_shreds + 1) if i not in reconstruct_order_1]

# Reconstruct images from shreds
reconstructed_image_1 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1], axis=1)
reconstructed_image_2 = np.concatenate([shreds[i - 1] for i in reconstruct_order_2], axis=1)

# Merge both images
reconstructed_new_image_1_2 = np.concatenate((reconstructed_image_1, reconstructed_image_2), axis=1)

# Define the reconstruction order for 1st, 2nd, 3rd, and 4th images
reconstruct_order_1_1 = [i for i in range(num_shreds) if i % 4 == 0]
reconstruct_order_1_2 = [i for i in range(num_shreds) if i % 4 == 1]
reconstruct_order_1_3 = [i for i in range(num_shreds) if i % 4 == 2]
reconstruct_order_1_4 = [i for i in range(num_shreds) if i % 4 == 3]

# Reconstruct images from shreds using the specified orders
reconstructed_image_1_1 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_1], axis=1)
reconstructed_image_1_2 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_2], axis=1)
reconstructed_image_1_3 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_3], axis=1)
reconstructed_image_1_4 = np.concatenate([shreds[i - 1] for i in reconstruct_order_1_4], axis=1)

# Merge  all 4 images into 1 reconstructed image
reconstructed_image_1_2_3_4 = np.concatenate((reconstructed_image_1_1, reconstructed_image_1_2,
                                              reconstructed_image_1_3, reconstructed_image_1_4), axis=1)

# Resize reconstructed images to match the width of the original image
reconstructed_new_image_1_2_resized = reconstructed_new_image_1_2[:, :original_image.shape[1], :]
reconstructed_image_1_2_3_4_resized = reconstructed_image_1_2_3_4[:, :original_image.shape[1], :]

# Resize original image to match the width of reconstructed images
original_image_resized = original_image[:, :reconstructed_new_image_1_2_resized.shape[1], :]

# Shred the reconstructed image horizontally with rotation
num_shreds_horizontal = 1  # Number of horizontal shreds
rotation_angle = 90  # Angle of rotation for shreds
shreds_horizontal = horizontal_shred(reconstructed_new_image_1_2_resized, num_shreds_horizontal)
shreds_horizontal_rotated = horizontal_shred(reconstructed_new_image_1_2_resized, num_shreds_horizontal,
                                             rotation=rotation_angle)

# Define the reconstruction orders for the reconstructed images horizontally
reconstruct_order_1_horizontal = [2 * i for i in range(num_shreds_horizontal // 2)]  # 1st, 3rd, 5th, 7th, 9th bits
reconstruct_order_2_horizontal = [2 * i + 1 for i in range(num_shreds_horizontal // 2)]  # 2nd, 4th, 6th, 8th, 10th bits

# Reconstruct images from horizontally shredded portions using the specified orders
reconstructed_image_horizontal_1 = np.concatenate([shreds_horizontal[i] for i in
                                                   reconstruct_order_1_horizontal], axis=0)
reconstructed_image_horizontal_2 = np.concatenate([shreds_horizontal[i] for i in
                                                   reconstruct_order_2_horizontal], axis=0)

# Reconstruct images from horizontally shredded portions using the specified orders ROTATED
reconstructed_image_horizontal_1_rotated = np.concatenate([shreds_horizontal_rotated[i] for i in
                                                           reconstruct_order_1_horizontal], axis=0)
reconstructed_image_horizontal_2_rotated = np.concatenate([shreds_horizontal_rotated[i] for i in
                                                           reconstruct_order_2_horizontal], axis=0)

# Merge the reconstructed images for the horizontally shredded image
reconstructed_new_image_horizontal = np.concatenate((reconstructed_image_horizontal_1,
                                                     reconstructed_image_horizontal_2), axis=0)

# Merge the reconstructed images for the horizontally shredded image ROTATED
reconstructed_new_image_horizontal_rotated = np.concatenate((reconstructed_image_horizontal_1_rotated,
                                                             reconstructed_image_horizontal_2_rotated), axis=0)

# Resize the new reconstructed image to match the size of the original image
reconstructed_new_image_resized_horizontal = reconstructed_new_image_horizontal[
                                             :original_image.shape[0], :original_image.shape[1]]

# Resize the new reconstructed image to match the size of the original image ROTATED
reconstructed_new_image_resized_horizontal_rotated = reconstructed_new_image_horizontal_rotated[
                                                     :original_image.shape[0], :original_image.shape[1]]

# Shred the reconstructed image vertically with rotation
num_shreds_vertical = 100  # Number of vertical shreds
rotation_angle_vertical = 90  # Angle of rotation for vertical shreds
shreds_vertical_rotated = vertical_shred(reconstructed_new_image_1_2_resized, num_shreds_vertical,
                                         rotation=rotation_angle_vertical)

# Define the reconstruction orders for the new images
reconstruct_order_1_vertical = [2 * i for i in range(num_shreds_vertical // 2)]  # 1st, 3rd, 5th, 7th, 9th bits
reconstruct_order_2_vertical = [2 * i + 1 for i in range(num_shreds_vertical // 2)]  # 2nd, 4th, 6th, 8th, 10th bits

# Reconstruct images from vertically shredded portions using the specified orders
reconstructed_image_vertical_1 = np.concatenate([shreds_vertical_rotated[i] for i in reconstruct_order_1_vertical],
                                                axis=1)
reconstructed_image_vertical_2 = np.concatenate([shreds_vertical_rotated[i] for i in reconstruct_order_2_vertical],
                                                axis=1)

# Merge the reconstructed images for the vertically shredded image
reconstructed_new_image_vertical = np.concatenate((reconstructed_image_vertical_1,
                                                   reconstructed_image_vertical_2), axis=1)

# Resize the new reconstructed image to match the size of the original image
reconstructed_new_image_resized_vertical_rotated = reconstructed_new_image_vertical[
                                                   :original_image.shape[0], :original_image.shape[1]]

# Shred the reconstructed image vertically with rotation
shreds_vertical_rotated_test = [
    original_image[:,
    i * (original_image.shape[1] // num_shreds_vertical): (i + 1) * (original_image.shape[1] // num_shreds_vertical), :]
    if rotation_angle_vertical == 0 else
    original_image[:,
    -((i + 1) * (original_image.shape[1] // num_shreds_vertical)): -i * (original_image.shape[1] // num_shreds_vertical), :]
    if rotation_angle_vertical == 90 else
    original_image[:,
    i * (original_image.shape[1] // num_shreds_vertical): (i + 1) * (original_image.shape[1] // num_shreds_vertical), :]
    if rotation_angle_vertical == 180 else
    original_image[:,
    -((i + 1) * (original_image.shape[1] // num_shreds_vertical)): -i * (original_image.shape[1] // num_shreds_vertical), :]
    if rotation_angle_vertical == 270 else
    original_image[:,
    -((i + 1) * (original_image.shape[1] // num_shreds_vertical)): -i * (original_image.shape[1] // num_shreds_vertical), :]
    for i in range(num_shreds_vertical)]

# Define the reconstruction order for 1st, 2nd, 3rd, and 4th images
reconstruct_order_1_1_test = [i for i in range(num_shreds_vertical) if i % 4 == 0]
reconstruct_order_1_2_test = [i for i in range(num_shreds_vertical) if i % 4 == 1]
reconstruct_order_1_3_test = [i for i in range(num_shreds_vertical) if i % 4 == 2]
reconstruct_order_1_4_test = [i for i in range(num_shreds_vertical) if i % 4 == 3]

# Reconstruct images from shreds using the specified orders
reconstructed_image_1_1_test = np.concatenate([shreds_vertical_rotated_test[i - 1] for i in reconstruct_order_1_1_test],
                                              axis=1)
reconstructed_image_1_2_test = np.concatenate([shreds_vertical_rotated_test[i - 1] for i in reconstruct_order_1_2_test],
                                              axis=1)
reconstructed_image_1_3_test = np.concatenate([shreds_vertical_rotated_test[i - 1] for i in reconstruct_order_1_3_test],
                                              axis=1)
reconstructed_image_1_4_test = np.concatenate([shreds_vertical_rotated_test[i - 1] for i in reconstruct_order_1_4_test],
                                              axis=1)

# Merge  all 4 images into 1 reconstructed image
reconstructed_image_1_2_3_4_vertical_test = np.concatenate((reconstructed_image_1_1_test, reconstructed_image_1_2_test,
                                                            reconstructed_image_1_3_test, reconstructed_image_1_4_test),
                                                           axis=1)

# Resize reconstructed images to match the width of the original image
reconstructed_image_1_2_3_4_vertical_test_resized = reconstructed_image_1_2_3_4_vertical_test[
                                                    :, :original_image.shape[1], :]

# Display images in 4 rows and 2 columns
display_images([original_image_resized, reconstructed_new_image_1_2_resized, reconstructed_image_1_2_3_4_resized,
                reconstructed_new_image_resized_horizontal, reconstructed_new_image_resized_vertical_rotated,
                reconstructed_new_image_resized_horizontal_rotated, reconstructed_image_1_2_3_4_vertical_test_resized],
               ['Original Image', 'Reconstructed 2 Images From Original Image',
                'Reconstructed 4 Images From Original Image', 'Reconstructed Image Horizontally',
                'Reconstructed Image Vertically Rotated', 'Reconstructed Image Horizontal Rotated',
                'Reconstructed Image Vertically Rotated v2'], 4, 2)
