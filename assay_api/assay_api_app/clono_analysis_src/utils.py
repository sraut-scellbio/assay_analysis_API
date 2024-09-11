import os
import pdb
import cv2
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from settings import well_dist_thresh


def get_normalized_arr(img_arr):
    # Convert the list of images to a numpy array (assuming all images have the same shape)
    images_array = np.array(img_arr)

    # Compute mean and standard deviation
    mean = np.mean(images_array)
    std = np.std(images_array)

    # Normalize images (subtract mean and divide by std)
    img_arr_norm = (images_array - mean) / std
    return img_arr_norm

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


# return both contours and hierarchy
def find_contours(img):
    results = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return results

def is_contour_closed(cnt):
    start_point = cnt[0][0]  # The first point
    end_point = cnt[-1][0]  # The last point
    return (np.linalg.norm(start_point - end_point)) < 10


def get_avg_contour_area(contours):
    n_items = 0
    total_area = 0
    for cnt in contours:
        if is_contour_closed(cnt):
            cnt_area = cv2.contourArea(cnt)
            total_area += cnt_area
            n_items += 1

    avg_area = total_area/n_items
    return avg_area

def compute_m(r, c, n_rows=10, n_cols=12):
    m = (r * n_cols) + c
    return m

def is_inside_well(w_pos, c_pos):
    w_x, w_y, w, h = w_pos
    c_x, c_y, r = c_pos

    if (abs(w_x - c_x) <= (w/2 + 1)) and (abs(w_y - c_y) <= (h/2 + 1)):
        return True
    else:
        return False

def draw_points(image, points):
    image_with_circles = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)

    # Draw each point as a circle
    for (x, y) in points:
        cv2.circle(image_with_circles, (x, y), 5, (255, 0, 0), 2)

    # Display the image
    plt.imshow(image_with_circles)
    plt.show()

def draw_contours(img, contours):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    img_clr = np.uint8(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    cv2.drawContours(img_clr, contours, -1, (255, 0, 0), 2)
    plt.imshow(img_clr)
    plt.show()

def visualize_well_locs(img_th, well_locs):
    img_clr = cv2.cvtColor(img_th, cv2.COLOR_GRAY2BGR)
    for i in range(well_locs.shape[0]):
        cv2.circle(img_clr, (well_locs[i][0], well_locs[i][1]), 5, (255, 0, 0), -1)

    plt.imshow(img_clr)
    plt.show()

def get_outliers_idx(contours, well=True):
    areas = []
    outliers_idx = []
    aspect_ratios = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areas.append(area)
        x, y, w, h = cv2.boundingRect(cnt)
        AR = max([w, h])/min([w, h])
        aspect_ratios.append(AR)

    area_p25 = np.percentile(areas, 25)
    area_p75 = np.percentile(areas, 75)

    if well:
        area_p75 = area_p75+500

    for i in range(len(areas)):
        if areas[i] < area_p25 or areas[i] > area_p75 or aspect_ratios[i] > 1.15:
            outliers_idx.append(i)

    return outliers_idx


def get_avg_gap(filt_locs, avg_width, est_avg_gap):
    sorted_locs = sorted(filt_locs, key=lambda x: (x[1], x[0]))
    gaps_total = 0
    count = 0
    for i in range(len(sorted_locs) - 1):
        x1, y1 = sorted_locs[i]
        for j in range(i+1, len(sorted_locs)):
            x2, y2 = sorted_locs[j]
            dist = np.sqrt(np.square(x1-x2) + np.square(y1-y2))
            # if wells are adjacent
            if dist < avg_width*1.35:
                gaps_total += dist - avg_width
                count += 1
                break # for every well we only need one adjacent well

    if count > 0:
        avg_gap = gaps_total/count
    else:
        avg_gap = est_avg_gap
    return avg_gap

def estimate_well_locations(img_size, width, gap):

    r, c = img_size
    max_well_r = int(r / (width + gap)) + 1
    max_well_c = int(c / (width + gap)) + 1

    # y values will be stored in dim 1 whereas x vals will be stored in dim 2
    est_locs = np.zeros(((max_well_r * max_well_c), 2), dtype=int)
    for i in range(max_well_r):
        for j in range(max_well_c):
            est_x = (j * (width + gap)) + (width / 2)
            est_y = (i * (width + gap)) + (width / 2)
            m = (i * max_well_c) + j
            est_locs[m][0] = est_x
            est_locs[m][1] = est_y

    return est_locs


def get_hash_key(width, gap, well_loc, max_well_c):
    x, y = well_loc
    i = int((y - width/1)/(width + gap)) + 1
    j = int((x - width/1)/(width + gap)) + 1
    m = (i * max_well_c) + j
    return m


def find_corresponding_points(true_well_locs, est_well_locs, width, gap, img_size):

    r, c = img_size
    max_well_r = int(r / (width + gap)) + 1
    max_well_c = int(c / (width + gap)) + 1

    # find the corresponding/closest estimated well locations for true locations
    corr_well_locs = []
    for well_loc in true_well_locs:
        m = get_hash_key(width, gap, well_loc, max_well_c)
        est_x = est_well_locs[m][0]
        est_y = est_well_locs[m][1]
        corr_well_locs.append((est_x, est_y))

    true_pts = np.array(true_well_locs)
    est_pts = np.array(corr_well_locs)
    return true_pts, est_pts


def get_quadrant(point):
    x, y = point
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 and y >= 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x >= 0 and y < 0:
        return 4
    else:
        return 0

# returns affine transformation matrix given original and transformed points
def get_affine_transformed_points(pts_B, pts_A, est_well_locs):

    points = pts_B-pts_A
    quadrants = np.array([get_quadrant(point) for point in points])

    # Count the number of points in each quadrant
    unique, counts = np.unique(quadrants, return_counts=True)
    quadrant_counts = dict(zip(unique, counts))

    # Identify the quadrant with the most points (excluding points on the axes)
    most_points_quadrant = max((q for q in quadrant_counts if q != 0), key=quadrant_counts.get)

    # Filter the points to include only those in the identified quadrant
    filt = quadrants == most_points_quadrant

    pts_A = pts_A[filt]
    pts_B = pts_B[filt]
    centroid_A = np.mean(pts_A, axis=0)
    centroid_B = np.mean(pts_B, axis=0)
    A_centered = pts_A - centroid_A
    B_centered = pts_B - centroid_B

    # Step 2: Compute the rotation matrix using SVD
    H = A_centered.T @ B_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Special case to handle reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # Step 3: Compute the translation vector
    trans_vec = centroid_B - R @ centroid_A

    # Create the transformation matrix
    transformation_matrix = np.eye(3)
    transformation_matrix[:2, :2] = R
    transformation_matrix[:2, 2] = trans_vec

    A_T = np.hstack((pts_A, np.ones((pts_A.shape[0], 1)))) @ transformation_matrix.T
    ones = np.ones((est_well_locs.shape[0], 1))
    est_well_pts_homo = np.hstack((est_well_locs, ones))
    true_well_pts_homo = est_well_pts_homo @ transformation_matrix.T
    true_well_locs = true_well_pts_homo[:, :2].astype(int)
    return true_well_locs

def get_class_count(cell_count_list):
    n_wells = len(cell_count_list)
    empty_wells = cell_count_list.count(0)
    single_cells = cell_count_list.count(1)
    dublets = cell_count_list.count(2)
    triplets = cell_count_list.count(3)
    clusters = len(list(filter(lambda x: 3 < x < 50, cell_count_list)))
    colonies = len(list(filter(lambda x: 50 <= x , cell_count_list)))
    return [n_wells, empty_wells, single_cells, dublets, triplets, clusters, colonies]


def perform_nonmax_suppression(locs, cells=True):
    repeated_idxs = []  # list to store index of repeated/close values
    if cells:
        for i in range(len(locs)-1):
            x_i, y_i, _ = locs[i]
            for j in range(i+1, len(locs)):
                x_j, y_j, _ = locs[j]
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
                if dist <= 2:
                    repeated_idxs.append(i)
                    break

    return repeated_idxs
