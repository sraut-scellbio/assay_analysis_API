import os
import cv2
import pdb
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from .preprocess import get_normalized_8bit_list
from .utils import get_images_lists, draw_contours
from .analyze_cell_data import count_migrating_cells


def get_data(folder_path):

    
    total_count = 0
    cell_outlines = []
    imgs_list, img_fnames = get_images_lists(folder_path)
    imgs_nlist = get_normalized_8bit_list(imgs_list)

    for i, img in enumerate(imgs_nlist):
        n_cells, cnts = count_migrating_cells(img)
        outlines = draw_contours(img, cnts)
        cell_outlines.append(outlines)
        total_count += n_cells

    return total_count, cell_outlines, img_fnames

