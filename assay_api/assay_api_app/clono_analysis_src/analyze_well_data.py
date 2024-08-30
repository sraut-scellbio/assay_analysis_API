import pdb
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from settings import avg_well_area, avg_cell_area, well_dist_thresh
from preprocess import conv_to_8bit, preprocess_dic_mask, \
    otsu_threshold, custom_threshold, preprocess_flo_mask, get_thresh_range


# takes list containing number of cells and returns total singlecells, dublets, cluster, colony

def disp_img(img):
    plt.imshow(img, cmap='gray')
    plt.show()

def get_well_mask(image_size, well_locations, avg_width):
    well_mask = np.zeros(image_size, dtype=np.uint8)

    avg_width = avg_width - 9
    # Loop through each square location and draw squares
    for col, row in well_locations:
        # Define the boundaries of the square
        start_row = max(0, row - avg_width // 2)
        end_row = min(image_size[0], row + avg_width // 2)
        start_col = max(0, col - avg_width // 2)
        end_col = min(image_size[1], col + avg_width // 2)

        # Set the square area to 255
        well_mask[start_row:end_row, start_col:end_col] = 255

    return well_mask

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

def get_well_contours(mask, perform_watershed=False):
    if perform_watershed:
        # perform watershed segmentation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        sure_bg = cv2.dilate(mask, kernel, iterations=1)

        # get sure foreground
        img_er = cv2.erode(mask, kernel, iterations=1)
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        img_open = cv2.morphologyEx(img_er, cv2.MORPH_OPEN, kernel_open, iterations=2)
        dist_trans = cv2.distanceTransform(img_open, cv2.DIST_L2, 3)
        ret, sure_fg = cv2.threshold(dist_trans, 0.50 * dist_trans.max(), 255, cv2.THRESH_BINARY)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        img_clr = np.uint8(cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB))
        w_markers = cv2.watershed(img_clr, markers)

        # merge external boundary with background
        w_markers[w_markers == -1] = 1
        contours, hierarchy = cv2.findContours(w_markers, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    else:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def get_well_locs(img_8bit, est_avg_gap):
    filt_locs = []
    filt_contours = []
    filt_hier = []

    sum_area = 0
    sum_width = 0

    # get well segmentation
    bin_mask = preprocess_dic_mask(img_8bit, img_8bit.shape)

    # get contours
    contours, hierarchy = get_well_contours(bin_mask, perform_watershed=True)

    # if contours were found
    if len(contours) > 0:
        outliers_idx = get_outliers_idx(contours)
        for i, cnt in enumerate(contours):
            if i not in outliers_idx:
                hier = hierarchy[0, i, :]
                # if area is large enough ti a well and contour in external
                if hier[3] == -1:
                    if len(cnt) >= 4:

                        x1, y1, w, h = cv2.boundingRect(cnt)
                        x2 = x1 + w
                        y2 = y1 + h

                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)

                        area = cv2.contourArea(cnt)
                        sum_area += area
                        sum_width += w
                        filt_locs.append((center_x, center_y))
                        filt_contours.append(cnt)
                        filt_hier.append(hier)

        if len(filt_locs) > 0:
            # save average area and width info for filtered contours
            avg_area = int(sum_area/len(filt_locs))
            avg_width = int(sum_width/len(filt_locs))

            # remove repeated indices
            repeated_idxs = perform_nonmax_suppression(filt_locs, cells=False)
            if repeated_idxs:
                for i, idx in enumerate(repeated_idxs):
                    filt_locs.pop(idx - i)
                    filt_contours.pop(idx - i)
                    filt_hier.pop(idx - i)

            # estimate positions for missing wells
            avg_gap = round(get_avg_gap(filt_locs, avg_width, est_avg_gap))

            est_well_locs = estimate_well_locations(bin_mask.shape, avg_width, avg_gap)

            # find points for applying affine transformation
            true_pts, est_pts = find_corresponding_points(filt_locs, est_well_locs, avg_width,
                                                          avg_gap, bin_mask.shape)

            true_well_locs = get_affine_transformed_points(true_pts, est_pts, est_well_locs)

            well_mask = get_well_mask(img_8bit.shape, true_well_locs, avg_width)
            return true_well_locs, avg_area, avg_width, well_mask

    return [], [], -1, []

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
        ret, sure_fg = cv2.threshold(dist_trans, 0.025 * dist_trans.max(), 255, cv2.THRESH_BINARY)
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

def get_cell_locs(img_8bit, well_mask):

    filt_areas = []
    filt_locs = []
    filt_contours = []

    th_mu, _ = get_thresh_range(img_8bit)
    bin_mask = custom_threshold(img_8bit, th_mu - (0.40*th_mu), 255)
    bin_mask = preprocess_flo_mask(bin_mask)

    final_mask = np.bitwise_and(bin_mask, well_mask)

    # contours
    contours, hierarchy = get_cell_contours(final_mask, perform_watershed=True)
    for i, cnt in enumerate(contours):
        hier = hierarchy[0, i, :]
        cnt_area = cv2.contourArea(cnt)

        # if external contour and reasonable area
        if (0.5*avg_cell_area < cnt_area < 1.15*avg_well_area) and (hier[3] == -1):
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

    return filt_locs, filt_contours

def count_cells(well_locs, cell_locs, cell_contours, avg_warea, avg_width):
    num_cells = np.zeros(well_locs.shape[0], dtype=int)
    total_areas = np.zeros(well_locs.shape[0], dtype=float)

    # for each cell location
    for i, (c_x, c_y, r)  in enumerate(cell_locs):
        # get the coresponding well location
        all_dist = np.linalg.norm(well_locs - np.repeat(np.array([[c_x, c_y]]), well_locs.shape[0], axis = 0), axis=1)
        m = np.argmin(all_dist)
        min_dist = all_dist[m]

        # if cell inside well(dist lower than half the diagonal length)
        if min_dist < (avg_width*1.41/2):
            cnt_area = cv2.contourArea(cell_contours[i])
            if cnt_area < avg_cell_area*1.15: # single cell
                num_cells[m] += 1
            else:
                num_cells[m] += round(cnt_area/avg_cell_area)
            total_areas[m] += cnt_area

    return num_cells, total_areas


def get_well_data(input_frame):
    dic_img8, flo_img8 = input_frame
    est_avg_gap = 17
    well_locs, avg_warea, avg_width, well_mask = get_well_locs(dic_img8, est_avg_gap)

    # if any wells were identified
    if len(well_locs) > 0:
        cell_locs, cell_contours = get_cell_locs(flo_img8, well_mask)
        cell_counts, total_area= count_cells(well_locs, cell_locs, cell_contours,
                                              avg_warea, avg_width)
        return well_locs.tolist(), cell_counts.tolist(), total_area.tolist()
    else:
        return [], [], []