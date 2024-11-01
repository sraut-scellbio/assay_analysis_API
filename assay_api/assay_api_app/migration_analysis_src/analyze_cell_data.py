import cv2
import numpy as np

from .preprocess import custom_threshold, get_thresh_range, preprocess_binary_mask


def count_migrating_cells(img_8bit):

    aspect_ratios = []
    cnt_areas = []
    filt_areas = []
    filt_locs = []
    filt_contours = []

    # pdb.set_trace()
    # img_8bit = preprocess_flo_img(img_8bit)
    # img_8bit = mask_saturated_pixels(img_8bit)
    th_mu, _ = get_thresh_range(img_8bit)
    bin_mask_th0 = preprocess_binary_mask(custom_threshold(img_8bit, 10, 255),
                                          perform_watershed=False)
    bin_mask_th1 = preprocess_binary_mask(custom_threshold(img_8bit, th_mu + 15, 255), perform_watershed=False)
    bin_mask = (np.logical_xor(bin_mask_th0, bin_mask_th1)).astype('uint8')

    # contours
    contours, hierarchy = cv2.findContours(bin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]

        cnt_area = cv2.contourArea(cnt)
        cnt_areas.append(cnt_area)

        x, y, w, h = cv2.boundingRect(cnt)
        rect_ar = h/w
        aspect_ratios.append(rect_ar)

        # filter based on aspect ratio
        # if external contour and reasonable area
        if (hier[2] == -1) and rect_ar > 1.35 and (20 < cnt_area < 350):
            x, y = int(x), int(y)
            filt_locs.append((x, y, w, h))
            filt_contours.append(cnt)
            filt_areas.append(cnt_area)

    return len(filt_locs), filt_contours

