import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

def normalize_and_scale(img):
    img_scaled = (img - img.min()) / (img.max() - img.min()) * 255
    return img_scaled

def conv_to_8bit(img):
    img_scaled = normalize_and_scale(img)
    img_8bit = img_scaled.astype(np.uint8)
    return img_8bit

def standardize(img, mu, std):
    return (img - mu) / std

def get_normalized_8bit_stack(img_hstack, num_images):
    img_list = [np.array(img_hstack.get_frame(m=i)) for i in range(num_images)]
    img_arr = np.transpose(np.dstack(img_list), (2, 0, 1))
    mu = np.mean(img_arr)
    std = np.std(img_arr)
    norm_arr = (img_arr - mu)/std
    min_vals = norm_arr.min(axis=(1,2))[:, np.newaxis, np.newaxis]
    max_vals = norm_arr.max(axis=(1,2))[:, np.newaxis, np.newaxis]
    norm_arr_scaled = ((norm_arr - min_vals) / (max_vals - min_vals)) * 255
    img_stack_8bit = norm_arr_scaled.astype(np.uint8)
    return img_stack_8bit

def get_thresh_range(img, n_comp=2):
    gmm = GaussianMixture(n_components=n_comp)
    gmm.fit(img.reshape(-1, 1))
    means = gmm.means_
    std_devs = gmm.covariances_ ** 0.5
    mean = means[np.argmax(means), 0]
    std = std_devs[np.argmax(means), 0, 0]
    thresh_range = (math.ceil(mean - std), math.floor(mean + std))
    return mean, std

def otsu_threshold(img):
    ret, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = th.astype('uint8')
    return th

def custom_threshold(img, th1=100, th2=255, inv=False):
    if inv:
        _, th = cv2.threshold(img, th1, th2, cv2.THRESH_BINARY_INV)
    else:
        _, th = cv2.threshold(img, th1, th2, cv2.THRESH_BINARY)
    th = th.astype('uint8')
    return th

def preprocess_dic_stack(dic_stack):
    img_8bit = conv_to_8bit(dic_stack)
    med_blur = cv2.medianBlur(img_8bit, 7)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_eqc1 = clahe.apply(med_blur)
    img_blur = cv2.GaussianBlur(img_eqc1,(7,7),0)
    return img_blur

def preprocess_dic_mask(dic_mask, resize_dims):
    dic_mask[dic_mask > 0] = 255
    img_resized = cv2.resize(dic_mask, (resize_dims[1], resize_dims[0]), cv2.INTER_CUBIC)
    img_th = custom_threshold(img_resized, 5, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img_close = cv2.morphologyEx(img_th, cv2.MORPH_CLOSE, kernel, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    img_open = cv2.morphologyEx(img_close, cv2.MORPH_OPEN, kernel, iterations=4)
    return img_open

def preprocess_flo_stack(flo_stack):
    img_8bit = conv_to_8bit(flo_stack)
    return img_8bit

def preprocess_flo_mask(flo_mask):
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    img_open = cv2.morphologyEx(flo_mask, cv2.MORPH_OPEN, kernel_open, iterations=2)
    # kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # img_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    return img_open



