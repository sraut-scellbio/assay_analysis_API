import pdb
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models
from .utils import *
from .settings import avg_well_area, cell_area_range, well_dist_thresh
from .preprocess import conv_to_8bit, preprocess_dic_mask, \
    otsu_threshold, custom_threshold, preprocess_flo_mask, get_thresh_range


# takes list containing number of cells and returns total singlecells, dublets, cluster, colony

def get_cell_contours(mask, perform_watershed=False):

    if perform_watershed:

        # perform watershed segmentation
        kernel_dil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        sure_bg = cv2.dilate(mask, kernel_dil, iterations=1)

        # get sure foreground
        # kernel_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # img_er = cv2.erode(mask, kernel_er, iterations=1)
        # kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # img_open = cv2.morphologyEx(img_er, cv2.MORPH_OPEN, kernel_open, iterations=6)
        # kernel_oper = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        # img_oper = cv2.erode(img_open, kernel_oper, iterations=1)

        # distance transform and foreground
        dist_trans = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_trans, 0.12 * dist_trans.max(), 255, cv2.THRESH_BINARY)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        img_clr= cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        w_markers = cv2.watershed(img_clr, markers)

        # merge external boundary with background
        w_markers[w_markers == -1] = 1
        contours, hierarchy = cv2.findContours(w_markers, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    else:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def count_cells_fluo(img_8bit):

    circ_areas = []
    cnt_areas = []
    filt_areas = []
    filt_locs = []
    filt_contours = []

    th_mu, _ = get_thresh_range(img_8bit)
    bin_mask = custom_threshold(img_8bit, th_mu+5, 255)
    bin_mask = preprocess_flo_mask(bin_mask)

    # contours
    contours, hierarchy = get_cell_contours(bin_mask, perform_watershed=True)
    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]

        cnt_area = cv2.contourArea(cnt)
        cnt_areas.append(cnt_area)

        # fit a circle and filter based on the area of the circle not the contour
        # this helps eliminate objects/noise with non-circular shape
        (_, _), radius = cv2.minEnclosingCircle(cnt)
        circ_area = np.pi*(radius**2)
        circ_areas.append(circ_area)

        # if external contour and reasonable area
        if (cell_area_range[0] < circ_area < cell_area_range[1]) and (hier[3] == -1):
            ((x, y), r) = cv2.minEnclosingCircle(cnt)
            x, y = int(x), int(y)
            filt_locs.append((x, y, r))
            filt_contours.append(cnt)
            filt_areas.append(cnt_area)

    repeated_idxs = perform_nonmax_suppression(filt_locs, cells=True)
    for i, idx in enumerate(repeated_idxs):
        filt_locs.pop(idx - i)
        filt_contours.pop(idx - i)
        filt_areas.pop(idx - i)

    return len(filt_locs), filt_locs, filt_contours

def count_cells_labelfree(img_8bit):
    circ_areas = []
    cnt_areas = []
    filt_areas = []
    filt_locs = []
    filt_contours = []

    model = models.Cellpose(gpu=torch.cuda.is_available(), model_type='cyto3')
    bin_mask = model.eval(img_8bit, diameter=20, channels=[0, 0], do_3D=False)[0]
    bin_mask = custom_threshold(bin_mask, 5, 255)
    bin_mask = preprocess_dic_mask(bin_mask, img_8bit.shape)

    # contours
    contours, hierarchy = get_cell_contours(bin_mask, perform_watershed=True)

    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]

        cnt_area = cv2.contourArea(cnt)
        cnt_areas.append(cnt_area)

        # fit a circle and filter based on the area of the circle not the contour
        # this helps eliminate objects/noise with non-circular shape
        (_, _), radius = cv2.minEnclosingCircle(cnt)
        circ_area = np.pi * (radius ** 2)
        circ_areas.append(circ_area)

        # if external contour and reasonable area
        if (cell_area_range[0] < circ_area < cell_area_range[1]) and (hier[3] == -1):
            ((x, y), r) = cv2.minEnclosingCircle(cnt)
            x, y = int(x), int(y)
            filt_locs.append((x, y, r))
            filt_contours.append(cnt)
            filt_areas.append(cnt_area)

    repeated_idxs = perform_nonmax_suppression(filt_locs, cells=True)
    for i, idx in enumerate(repeated_idxs):
        filt_locs.pop(idx - i)
        filt_contours.pop(idx - i)
        filt_areas.pop(idx - i)

    return len(filt_locs), filt_locs, filt_contours
