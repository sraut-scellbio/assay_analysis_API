import os
import cv2
import numpy as np
from PIL import Image

def get_images_lists(fld_path):
    images_list = []

    # Loop through all files in the folder
    img_fnames = []
    for filename in os.listdir(fld_path):
        img_name = filename.split('\\')[-1]
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.tif')):
            img_fnames.append(img_name)
            img_path = os.path.join(fld_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # For grayscale images

            images_list.append(img)
    return images_list, img_fnames


def draw_contours(img, contours):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    img_clr = np.uint8(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    cv2.drawContours(img_clr, contours, -1, (255, 0, 0), 1)
    return img_clr


def save_cell_outlines(imgs_list, out_dir, img_fnames):
    os.makedirs(out_dir, exist_ok=True)

    for i, img in enumerate(imgs_list):
        outlines_img = Image.fromarray(img)
        save_path = os.path.join(out_dir, img_fnames[i])
        outlines_img.save(save_path)