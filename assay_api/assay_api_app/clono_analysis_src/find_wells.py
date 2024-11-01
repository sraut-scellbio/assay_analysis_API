import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

from .settings import well_area
from .utils import draw_contours, draw_rect, draw_points, fill_contours
from .preprocess import preprocess_img

import pdb

device = "cuda"


def apply_thresholding(img):
    th_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return th_img

def draw_external_contours(img_shape, contours, hierarchy):
    canvas = np.zeros(img_shape, dtype=np.uint8)
    filt_contours = []
    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]
        # if contour is external
        if hier[3] == -1:
            filt_contours.append(contours[i])
    cv2.drawContours(canvas, filt_contours, -1, (255, 255, 255), thickness=2)
    return canvas

def get_external_edges(img):
    img_med = cv2.medianBlur(img, 7)
    med_can = cv2.Canny(cv2.medianBlur(img, 9), 0, 250, 5)
    gau_can = cv2.Canny(cv2.GaussianBlur(img_med, (7, 7), 0), 0, 255, 5)
    contours, hierarchy = cv2.findContours(gau_can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    edges = draw_external_contours(img.shape, contours, hierarchy)
    return edges


def add_white_boundary(img, boundary_thickness=5):

    # Create a white (255) border around the image
    bordered_image = cv2.copyMakeBorder(
        img,
        top=boundary_thickness,
        bottom=boundary_thickness,
        left=boundary_thickness,
        right=boundary_thickness,
        borderType=cv2.BORDER_CONSTANT,
        value=255  # White boundary (grayscale value 255)
    )

    bordered_image_resized = cv2.resize(bordered_image, (img.shape[1], img.shape[0]))
    return bordered_image_resized

def get_locations(mask, mag):

    locs = []
    aspect_ratios = []
    rect_areas = []
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        rect_aspect_ratio = h / w
        rect_area = h * w
        aspect_ratios.append(rect_aspect_ratio)
        rect_areas.append(rect_area)
        if (0.40 <= rect_aspect_ratio <= 3) and (well_area[mag][0]*0.45 <= rect_area <= well_area[mag][1]):
            locs.append((int(x+(w*0.5)), int(y+(h*0.5))))

    return locs

def best_enclosed_by_rect(cnt):
    # Minimum enclosing rectangle
    x, y, w, h = cv2.boundingRect(cnt)
    rect_area = h * w

    # Minimum enclosing circle
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    circle_area = np.pi * (radius ** 2)

    # Determine the better enclosing shape by comparing areas
    if rect_area < circle_area:
        return 1
    return 0


# filter contours based on shape and size
def find_squares(cnts, mag):
    filt_cnts = []
    aspect_ratios = []
    cnt_areas = []
    rect_areas = []
    cnt_rect_diff = []
    best_enclosing = []

    for i, cnt in enumerate(cnts):
        cnt_area = cv2.contourArea(cnt)
        cnt_areas.append(cnt_area)

        x, y, w, h = cv2.boundingRect(cnt)
        rect_aspect_ratio = h / w
        rect_area = h*w
        aspect_ratios.append(rect_aspect_ratio)
        rect_areas.append(rect_area)

        area_diff = abs(cnt_area - rect_area)/rect_area
        cnt_rect_diff.append(area_diff)
        best_enclosing.append(best_enclosed_by_rect(cnt))
        if (0.16 <= rect_aspect_ratio <= 5.6) and (well_area[mag][0]*0.1 <= rect_area <= well_area[mag][1]) and best_enclosed_by_rect(cnt) and area_diff <= 0.15:
            filt_cnts.append(cnt)

    return filt_cnts


def connect_edges(edge_image):

    # Create a horizontal kernel (e.g., 1x5 for horizontal connection)
    kernel5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # edges for mask
    img_dil = cv2.dilate(edge_image, kernel5, iterations=2)
    img_close = cv2.morphologyEx(img_dil, cv2.MORPH_CLOSE, kernel5, iterations=4)
    img_open = cv2.morphologyEx(img_close, cv2.MORPH_CLOSE, kernel5, iterations=1)
    img_erode = cv2.erode(img_open, kernel3, iterations=1)
    return img_erode

def get_well_locs(image_stack, mag, sam_checkpoint):

    masks_list = []
    well_locs = []
    num_images = image_stack.shape[0]
    img_shape = image_stack[0, :, :].shape

    model_type = "vit_h"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(sam)

    for i in range(num_images):
        img = image_stack[i, :, :]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img_blur = preprocess_img(img_rgb)

        masks = mask_generator.generate(img_blur)

        mask = np.zeros(img.shape, dtype='bool')
        for mask_dict in masks:
            if well_area[mag][0]*0.1 <= mask_dict['area'] <= well_area[mag][1]:
                mask = np.logical_or(mask, mask_dict['segmentation'])

        contours_msk, hierarchy_msk = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        final_cnts = find_squares(contours_msk, mag)
        final_mask = fill_contours(final_cnts, img_shape)

        final_locs = get_locations(final_mask, mag)
        masks_list.append(final_mask)

        well_locs.append(final_locs)

    return well_locs, np.array(masks_list)
