import pdb
import cv2
import numpy as np
import matplotlib.pyplot as plt

from .utils import *
from .settings import well_area, well_width, cell_area
from .preprocess import get_thresh_range, preprocess_binary_mask, custom_threshold
from .find_wells import fill_contours

# takes list containing number of cells and returns total singlecells, dublets, cluster, colony

def align_wells(w1_well_locs, w2_well_locs):
    indices = []
    for i, (w1_x, w1_y) in enumerate(w1_well_locs):
        for j, (w2_x, w2_y) in enumerate(w2_well_locs):
            dist = np.sqrt(np.square(w1_x-w2_x) + np.square(w1_y-w2_y))

            # if corresponding well found
            if dist < 30:
                indices.append((i, j))
                break
    return indices

def get_clonogenic_analysis(clono_input):

    w1_well_locs, w1_cell_count, w2_well_locs, w2_cell_count = clono_input
    died = 0
    remained_single = 0
    formed_clusters = 0
    formed_colonies = 0

    # corresponding well indices
    corr_w_idxs = align_wells(w1_well_locs, w2_well_locs)
    for i, j in corr_w_idxs:
        w1_count = w1_cell_count[i]
        w2_count = w2_cell_count[j]

        # started with cells
        if w1_count > 0 and w2_count == 0:
            died += 1
        # started with single cell
        elif w1_count == 1:
            if w2_count == 1:
                remained_single += 1
            elif 1 < w2_count <= 5:
                formed_clusters += 1
            else:
                formed_colonies += 1

    return [died, remained_single, formed_clusters, formed_colonies]


def get_cell_locs(img_8bit, mag, bgrnd):

    cnt_areas = []
    rect_ar = []
    filt_areas = []
    filt_locs = []
    filt_contours = []

    if bgrnd:
        th_start, _ = get_thresh_range(img_8bit, 3)
    else:
        th_start, _ = get_thresh_range(img_8bit, 2)

    bin_mask = preprocess_binary_mask(custom_threshold(img_8bit, th_start-30, 255))
    # contours
    contours, hierarchy = cv2.findContours(bin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw_contours(img_8bit, contours)
    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]
        cnt_area = cv2.contourArea(cnt)
        cnt_areas.append(cnt_area)
        (x, y),(w, h), _ = cv2.minAreaRect(cnt)
        aspect_ratio = w/h
        rect_ar.append(aspect_ratio)

        # if external contour and reasonable area
        if (cell_area[mag][0]*0.85 < cnt_area < 1.15*well_area[mag][1]) and (hier[3] == -1):
            x, y = int(x), int(y)
            filt_locs.append((x, y))
            filt_contours.append(cnt)
            filt_areas.append(cnt_area)

    repeated_idxs = perform_nonmax_suppression(filt_locs, cells=True)
    if len(repeated_idxs) > 0:
        for i, idx in enumerate(repeated_idxs):
            filt_locs.pop(idx - i)
            filt_contours.pop(idx - i)
            filt_areas.pop(idx - i)

    mask = fill_contours(filt_contours, img_8bit.shape)
    return filt_locs, filt_contours, mask


def count_cells(img, well_locs, cell_locs, cell_contours, mag):
    num_cells = np.zeros(well_locs.shape[0], dtype=int)
    total_areas = np.zeros(well_locs.shape[0], dtype=float)
    cnt_areas = []
    rect_ars = []

    draw_points(img, well_locs, cell_locs)

    # for each cell location
    for i, (c_x, c_y)  in enumerate(cell_locs):
        # get the coresponding well location
        all_dist = np.linalg.norm(well_locs - np.repeat(np.array([[c_x, c_y]]), well_locs.shape[0], axis = 0), axis=1)
        m = np.argmin(all_dist)
        min_dist = all_dist[m]

        # if cell inside well(dist lower than half the diagonal length)
        if min_dist < (well_width[mag][1]*1.41/2):
            cnt_area = cv2.contourArea(cell_contours[i])
            cnt_areas.append(cnt_area)
            (x, y), (w, h), _ = cv2.minAreaRect(cell_contours[i])
            aspect_ratio = h / w
            rect_ars.append(aspect_ratio)

            if  cell_area[mag][0] <= cnt_area <= cell_area[mag][1]: # single cell
                num_cells[m] += 1
            else:
                num_cells[m] += round(cnt_area/cell_area[mag][1])
            total_areas[m] += cnt_area
    return num_cells, total_areas


def get_well_data(input_args):
    mag = '10'
    bgrnd = True
    img, well_locs = input_args
    cell_mask = np.zeros(img.shape, dtype = np.uint8)
    if len(well_locs) > 0:
        cell_locs_i, cell_contours_i, cell_mask = get_cell_locs(img, mag, bgrnd)
        cell_counts_i, total_areas_i = count_cells(img, np.array(well_locs), cell_locs_i,
                                                   cell_contours_i, mag)
        return cell_counts_i.tolist(), total_areas_i.tolist(), cell_mask
    else:
        return [], [], []
        