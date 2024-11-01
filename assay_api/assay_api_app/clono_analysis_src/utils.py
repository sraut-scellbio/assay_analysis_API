import os
import pdb
import cv2
import math
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

def fill_contours(cnts, img_size):
    canvas = np.zeros(img_size, np.uint8)
    cv2.drawContours(canvas, cnts, -1, (255, 255, 255), thickness=-1)
    return canvas

def draw_contours(img, contours):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    img_clr = np.uint8(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    cv2.drawContours(img_clr, contours, -1, (255, 0, 0), 1)
    return img_clr

def draw_rect(img, locs):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    for loc in locs:
        x, y, w, h = loc
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), -1)
    return img

def draw_points(image, well_locs=None, cell_locs=None):
    image_with_circles = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)

    if well_locs is not None:
        for i in range(well_locs.shape[0]):
            cv2.circle(image_with_circles, (well_locs[i][0], well_locs[i][1]), 4, (255, 0, 0), -1)

    if cell_locs is not None:
        for (x, y) in cell_locs:
            cv2.circle(image_with_circles, (x, y), 4, (0, 0, 255), -1)
    return image_with_circles



def save_swarm_data(dict_file, out_dir, well_name):
    for i, key in enumerate(dict_file.keys()):
        ser = pd.Series(dict_file[key], name=f"{well_name}_{key}")
        # fil
        filt_ser = ser.drop(ser[ser == 0].index)
        filt_ser.to_csv(os.path.join(out_dir, f"{well_name}_{key}.csv"), index=False)
        plt.figure(figsize=(5, 7))
        plt.title(ser.name)
        if 'count' in ser.name:
            sns.histplot(data=filt_ser)
            plt.ylabel(f"{key}")
            plt.tight_layout()
            plt.grid()
            plt.savefig(os.path.join(out_dir, f"histplot_{well_name}_{key}.pdf"), dpi=150)
        else:
            sns.swarmplot(data=filt_ser, size=1)
            plt.yticks(np.arange(0, filt_ser.max() + 150, 150))
            plt.ylabel(f"{key}")
            plt.tight_layout()
            plt.grid()
            plt.savefig(os.path.join(out_dir, f"swarm_{well_name}_{key}.pdf"), dpi=150)
    print(f"Results saved in {out_dir}.")


def create_and_save_combined_mask(well_masks, cell_masks, fnames, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(well_masks)):
        w_mask = well_masks[i]
        c_mask = cell_masks[i]
        b_mask = 255 - w_mask
        fname = fnames[i]
        save_path = os.path.join(output_dir, fname)
        clr_mask = np.zeros((w_mask.shape[0], w_mask.shape[1], 3), dtype=np.uint8)
        clr_mask[:, :, 1] = b_mask * 0.65
        clr_mask[:, :, 2] = b_mask * 0.65
        clr_mask[:, :, 2] = clr_mask[:, :, 2] + w_mask*0.25
        clr_mask[:, :, 0] = c_mask #R
        clr_mask = Image.fromarray(clr_mask)
        clr_mask.save(save_path)
        # print(f"Mask successfully saved as {save_path}.")

def get_class_count(cell_count_list):
    n_wells = len(cell_count_list)
    empty_wells = cell_count_list.count(0)
    single_cells = cell_count_list.count(1)
    dublets = cell_count_list.count(2)
    triplets = cell_count_list.count(3)
    clusters = len(list(filter(lambda x: 3 < x <= 8, cell_count_list)))
    colonies = len(list(filter(lambda x: 8 < x , cell_count_list)))
    return [n_wells, empty_wells, single_cells, dublets, triplets, clusters, colonies]


def perform_nonmax_suppression(locs, cells=True):
    repeated_idxs = []  # list to store index of repeated/close values
    if cells:
        for i in range(len(locs)-1):
            x_i, y_i = locs[i]
            for j in range(i+1, len(locs)):
                x_j, y_j = locs[j]
                dist = np.sqrt(np.square(x_i-x_j) + np.square(y_i-y_j))
                if dist <= 2:
                    repeated_idxs.append(i)
                    break
    else:
        for i in range(len(locs) - 1):
            x_i, y_i = locs[i]
            for j in range(i+1, len(locs)):
                x_j, y_j = locs[j]
                dist = np.sqrt(np.square(x_i - x_j) + np.square(y_i - y_j))
                if dist <= 5:
                    repeated_idxs.append(i)
                    break

    return repeated_idxs
