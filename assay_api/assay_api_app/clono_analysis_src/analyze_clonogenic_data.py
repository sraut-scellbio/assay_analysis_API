import os
import cv2
import pdb
import json
import torch
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
import multiprocessing
from cellpose import models
import matplotlib.pyplot as plt
from readlif.reader import LifFile

from .preprocess import get_normalized_8bit_stack
from .utils import save_swarm_data, get_class_count, get_normalized_arr
from .analyze_well_data import get_well_data, get_clonogenic_analysis

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_images_as_array(fld_path):
    images = []
    for root, _, files in os.walk(fld_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Attempt to open the file as an image
                with Image.open(file_path) as img:
                    # Convert image to numpy array and add to list
                    img_array = np.array(img)
                    images.append(img_array)
            except IOError:
                # If file is not an image, skip it
                print(f"Skipping non-image file: {file_path}")

    images_arr = np.array(images)
    return images_arr


def save_results(results_dict, save_path):
    # Ensure save_path exists
    os.makedirs(save_path, exist_ok=True)

    for key, value in results_dict.items():
        if isinstance(value, dict):
            # Save dictionary values as JSON files
            json_file_path = os.path.join(save_path, f"{key}.json")
            with open(json_file_path, 'w') as f:
                json.dump(value, f, indent=4)

        elif isinstance(value, list):
            # Create and save swarm plot for list values
            ser = pd.Series(value, name=key)
            filt_ser = ser[ser != 0]  # Remove zero values for plotting
            filt_ser.to_csv(os.path.join(save_path, f"{key}.csv"), index=False)
            plt.figure(figsize=(5, 7))
            plt.title(ser.name)
            sns.swarmplot(data=filt_ser, size=1)
            plt.yticks(np.arange(0, filt_ser.max() + 150, 150))
            plt.ylabel(key)
            plt.tight_layout()
            plt.grid()
            plt.savefig(os.path.join(save_path, f"{key}_swarmplot.pdf"), dpi=150)
            plt.close()  # Close the plot to free up memory

        else:
            print(f"Skipping key '{key}': Unsupported value type.")


def singleday_analysis(path_lf, path_fluo):

    swarm_data_area = []

    data_well = {
        'num_wells_identified': 0,
        'empty_wells': 0,
        'single_cells': 0,
        'dublets': 0,
        'triplets': 0,
        'clusters': 0,
        'colonies': 0
    }


    lf_stack = get_images_as_array(path_lf)
    fluo_stack = get_images_as_array(path_fluo)

    # get normlized stack
    lf_stack_norm = get_normalized_8bit_stack(lf_stack)
    fluo_stack_norm = get_normalized_8bit_stack(fluo_stack)

    lf_list_8bit = [lf_stack_norm [i, :, :] for i in range(lf_stack_norm.shape[0])]
    fluo_list_8bit = [fluo_stack_norm[i, :, :] for i in range(fluo_stack_norm.shape[0])]

    model = models.Cellpose(gpu=torch.cuda.is_available(), model_type='cyto2')
    cellpose_masks = model.eval(lf_list_8bit, diameter=40, channels=[0, 0], do_3D=False)[0]

    with multiprocessing.Pool() as pool:
        well_locations, cell_counts, total_cell_areas = zip(*pool.map(get_well_data, list(zip(cellpose_masks, fluo_list_8bit))))


    # remove empty items
    well_locations = [ele for ele in well_locations if ele != []]
    cell_counts = [ele for ele in cell_counts if ele != []]
    total_cell_areas = [ele for ele in total_cell_areas if ele != []]

    with multiprocessing.Pool() as pool:
        count_res_arr = np.array(pool.map(get_class_count, cell_counts))

    for j, key in enumerate(data_well.keys()):
        data_well[key] = int(np.sum(count_res_arr[:, j]))

    for i in range(len(well_locations)):
        if len(well_locations[i]) > 0 :
            swarm_data_area.extend(total_cell_areas[i])

    return data_well, swarm_data_area

def multiday_analysis(path_lf_d1, path_fluo_d1, path_lf_dn, path_fluo_dn):

    swarm_data_area_d1 = []
    swarm_data_area_dn = []

    data_well_d1 = {
        'num_wells_identified': 0,
        'empty_wells': 0,
        'single_cells': 0,
        'dublets': 0,
        'triplets': 0,
        'clusters': 0,
        'colonies': 0
    }

    data_well_dn = {
        'num_wells_identified': 0,
        'empty_wells': 0,
        'single_cells': 0,
        'dublets': 0,
        'triplets': 0,
        'clusters': 0,
        'colonies': 0
    }

    data_clonogenic = {
        'died': 0,
        'remained_single': 0,
        'formed_clusters': 0,
        'formed_colonies': 0
    }

    lf_stack_d1 = get_images_as_array(path_lf_d1)
    fluo_stack_d1 = get_images_as_array(path_fluo_d1)
    lf_stack_dn = get_images_as_array(path_lf_dn)
    fluo_stack_dn = get_images_as_array(path_fluo_dn)

    # get normlized stack
    lf_stack_norm_d1 = get_normalized_8bit_stack(lf_stack_d1)
    fluo_stack_norm_d1 = get_normalized_8bit_stack(fluo_stack_d1)
    lf_stack_norm_dn = get_normalized_8bit_stack(lf_stack_dn)
    fluo_stack_norm_dn = get_normalized_8bit_stack(fluo_stack_dn)

    lf_list_8bit_d1 = [lf_stack_norm_d1[i, :, :] for i in range(lf_stack_norm_d1.shape[0])]
    fluo_list_8bit_d1 = [fluo_stack_norm_d1[i, :, :] for i in range(fluo_stack_norm_d1.shape[0])]
    lf_list_8bit_dn = [lf_stack_norm_dn[i, :, :] for i in range(lf_stack_norm_dn.shape[0])]
    fluo_list_8bit_dn = [fluo_stack_norm_dn[i, :, :] for i in range(fluo_stack_norm_dn.shape[0])]

    model = models.Cellpose(gpu=torch.cuda.is_available(), model_type='cyto2')
    cellpose_masks_d1 = model.eval(lf_list_8bit_d1, diameter=40, channels=[0, 0], do_3D=False)[0]

    with multiprocessing.Pool() as pool:
        well_locations_d1, cell_counts_d1, total_cell_areas_d1 = zip(
            *pool.map(get_well_data, list(zip(cellpose_masks_d1, fluo_list_8bit_d1))))

    # remove empty items
    well_locations_d1 = [ele for ele in well_locations_d1 if ele != []]
    cell_counts_d1 = [ele for ele in cell_counts_d1 if ele != []]
    total_cell_areas_d1 = [ele for ele in total_cell_areas_d1 if ele != []]

    cellpose_masks_dn = model.eval(lf_list_8bit_dn, diameter=40, channels=[0, 0], do_3D=False)[0]

    pdb.set_trace()
    with multiprocessing.Pool() as pool:
        well_locations_dn, cell_counts_dn, total_cell_areas_dn = zip(
            *pool.map(get_well_data, list(zip(cellpose_masks_dn, fluo_list_8bit_dn))))

    # remove empty items
    well_locations_dn = [ele for ele in well_locations_dn if ele != []]
    cell_counts_dn = [ele for ele in cell_counts_dn if ele != []]
    total_cell_areas_dn = [ele for ele in total_cell_areas_dn if ele != []]

    with multiprocessing.Pool() as pool:
        count_res_arr_d1 = np.array(pool.map(get_class_count, cell_counts_d1))
        count_res_arr_dn = np.array(pool.map(get_class_count, cell_counts_dn))

    # arrange data for clonogenic analysis
    clono_input = [(well_locations_d1[i], cell_counts_d1[i], well_locations_dn[i], cell_counts_dn[i]) for i in
                   range(len(well_locations_d1))]
    with multiprocessing.Pool() as pool:
        clonogenic_analysis = np.array(pool.map(get_clonogenic_analysis, clono_input))

    for j, (key_d1, key_dn) in enumerate(zip(data_well_d1.keys(), data_well_dn.keys())):
        data_well_d1[key_d1] = int(np.sum(count_res_arr_d1[:, j]))
        data_well_dn[key_dn] = int(np.sum(count_res_arr_dn[:, j]))

    # update clonogenic analysis results for frame
    for j, key in enumerate(data_clonogenic.keys()):
        data_clonogenic[key] = int(np.sum(clonogenic_analysis[:, j]))

    for i in range(len(well_locations_d1)):
        if len(well_locations_d1[i]) > 0 and len(well_locations_dn[i]) > 0:
            swarm_data_area_d1.extend(total_cell_areas_d1[i])
            swarm_data_area_dn.extend(total_cell_areas_dn[i])

    return data_clonogenic, data_well_d1, data_well_dn, swarm_data_area_d1, swarm_data_area_dn
