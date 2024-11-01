import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

def preprocess_img(img):
    img_med = cv2.medianBlur(img, 7)
    gau = cv2.blur(img_med, (7, 7))
    return gau

def get_normalized_8bit_stack(img_arr):
    mu = np.mean(img_arr)
    std = np.std(img_arr)
    std_arr = (img_arr - mu)/std
    min_vals = std_arr.min(axis=(1, 2))[:, np.newaxis, np.newaxis]
    max_vals = std_arr.max(axis=(1, 2))[:, np.newaxis, np.newaxis]
    norm_arr_scaled = ((std_arr - min_vals) / (max_vals - min_vals)) * 255
    img_stack_8bit = norm_arr_scaled.astype(np.uint8)
    return img_stack_8bit

def get_thresh_range(img, n_comp=2):
    gmm = GaussianMixture(n_components=n_comp)
    gmm.fit(img.reshape(-1, 1))
    means = gmm.means_
    std_devs = gmm.covariances_ ** 0.5
    mean = means[np.argmax(means), 0]
    std = std_devs[np.argmax(means), 0, 0]
    return mean, std


def custom_threshold(img, th1=100, th2=255, inv=False):
    if inv:
        _, th = cv2.threshold(img, th1, th2, cv2.THRESH_BINARY_INV)
    else:
        _, th = cv2.threshold(img, th1, th2, cv2.THRESH_BINARY)
    th = th.astype('uint8')
    return th

def preprocess_binary_mask(mask, perform_watershed=False):

    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close, iterations=1)
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img_open = cv2.morphologyEx(img_close, cv2.MORPH_OPEN, kernel_open, iterations=2)

    if perform_watershed:
        # get sure foreground
        kernel_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        img_er = cv2.erode(img_open, kernel_er, iterations=1)
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        img_open = cv2.morphologyEx(img_er, cv2.MORPH_OPEN, kernel_open, iterations=5)
        kernel_oper = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        img_oper = cv2.erode(img_open, kernel_oper, iterations=1)

        # distance transform and foreground
        dist_trans = cv2.distanceTransform(img_oper, cv2.DIST_L2, 3)
        ret, sure_fg = cv2.threshold(dist_trans, 0.15 * dist_trans.max(), 255, cv2.THRESH_BINARY)
        final_mask = cv2.morphologyEx(sure_fg, cv2.MORPH_OPEN, kernel_open, iterations=3)
        intersection = np.count_nonzero(np.logical_and(mask, final_mask))

        # mask_area = np.count_nonzero(mask)  # I assume this is faster as mask1 == 1 is a bool array
        # final_mask_area = np.count_nonzero(final_mask)
        # iou_val = intersection / (mask_area + final_mask_area - intersection)

        # if iou_val > 0.2:
        return final_mask
    return img_open
