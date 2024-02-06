import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def distort(img, orientation='horizontal', func=np.sin, x_scale=0.05, y_scale=5):
    assert orientation[:3] in ['hor', 'ver'], "dist_orient should be 'horizontal'|'vertical'"
    assert func in [np.sin, np.cos], "supported functions are np.sin and np.cos"
    assert 0.00 <= x_scale <= 0.1, "x_scale should be in [0.0, 0.1]"
    assert 0 <= y_scale <= min(img.size[0], img.size[1]), "y_scale should be less than image size"
    img_dist = img.copy()

    def shift(x):
        return int(y_scale * func(np.pi * x * x_scale))

    img_array = np.array(img_dist)

    for c in range(3):
        for i in range(img_array.shape[1] if orientation.startswith('ver') else img_array.shape[0]):
            if orientation.startswith('ver'):
                img_array[:, i, c] = np.roll(img_array[:, i, c], shift(i))[:img_array.shape[0]]
            else:
                img_array[i, :, c] = np.roll(img_array[i, :, c], shift(i))[:img_array.shape[1]]

    return Image.fromarray(img_array.astype(np.uint8))


# Load the cat image using PIL
img_path = 'cat.jpg'
img = Image.open(img_path)


def plot_grid(images, rows, cols, figsize=(10, 10)):
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(images[i])
        ax.axis('off')
    plt.show()


imgs_distorted = []
for ori in ['ver', 'hor']:
    for x_param in [0.01, 0.02, 0.03, 0.04]:
        for y_param in [2, 10, 20, 30, 40]:
            imgs_distorted.append(distort(img, orientation=ori, x_scale=x_param, y_scale=y_param))

plot_grid(imgs_distorted, 2, 5, figsize=(20, 8))
