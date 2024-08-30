import os
import cv2
import pdb
import json
import torch
import numpy as np
import pandas as pd
import multiprocessing
from cellpose import models
import matplotlib.pyplot as plt
from readlif.reader import LifFile
from preprocess import get_normalized_8bit_stack
from utils import save_swarm_data, get_class_count
from analyze_well_data import get_well_data, get_clonogenic_analysis

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_clonogenic_assay_summary(data_path, well1_name, well2_name):

    # read datafile
    lfile = LifFile(data_path)
    metadata = lfile.image_list

    flo_stack_idx_w1 = 4
    dic_stack_idx_w1 = 2
    flo_stack_idx_w2 = 4
    dic_stack_idx_w2 = 2

    swarm_data_w1 = {
        'w1_count': [],
        'w1_area': []
    }

    swarm_data_w2 = {
        'w2_count': [],
        'w2_area': []
    }

    data_well1 = {
        'num_wells_identified': 0,
        'empty_wells': 0,
        'single_cells': 0,
        'dublets': 0,
        'triplets': 0,
        'clusters': 0,
        'colonies': 0
    }

    data_well2 = {
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

    # get hyperstack
    flo_hstack_w1 = lfile.get_image(flo_stack_idx_w1)
    dic_hstack_w1 = lfile.get_image(dic_stack_idx_w1)
    flo_hstack_w2 = lfile.get_image(flo_stack_idx_w2)
    dic_hstack_w2 = lfile.get_image(dic_stack_idx_w2)

    # get number of frames and check if they correspond
    n_images_flo_w1 = metadata[flo_stack_idx_w1]['dims_n'][10]
    n_images_dic_w1 = metadata[dic_stack_idx_w1]['dims_n'][10]

    n_images_flo_w2 = metadata[flo_stack_idx_w2]['dims_n'][10]
    n_images_dic_w2 = metadata[dic_stack_idx_w2]['dims_n'][10]

    # asset if number of frames in well1 and 2 are the same
    assert (n_images_dic_w1 == n_images_flo_w1 == n_images_dic_w2 == n_images_flo_w2)

    # get normaled image stacks
    dic_hstack_8bit_w1 = get_normalized_8bit_stack(dic_hstack_w1, n_images_dic_w1)
    flo_hstack_8bit_w1 = get_normalized_8bit_stack(flo_hstack_w1, n_images_flo_w1)
    dic_hstack_8bit_w2 = get_normalized_8bit_stack(dic_hstack_w2, n_images_dic_w2)
    flo_hstack_8bit_w2 = get_normalized_8bit_stack(flo_hstack_w2, n_images_flo_w2)


    dic_list_8bit_w1 = [dic_hstack_8bit_w1[i, :, :] for i in range(n_images_dic_w1)]
    flo_list_8bit_w1 = [flo_hstack_8bit_w1[i, :, :] for i in range(n_images_flo_w1)]
    dic_list_8bit_w2 = [dic_hstack_8bit_w2[i, :, :] for i in range(n_images_dic_w2)]
    flo_list_8bit_w2 = [flo_hstack_8bit_w2[i, :, :] for i in range(n_images_flo_w2)]

    # create input lists for multiprocessing
    model = models.Cellpose(gpu=torch.cuda.is_available(), model_type='cyto2')
    cellpose_masks_w1 = model.eval(dic_list_8bit_w1, diameter=40, channels=[0, 0], do_3D=False)[0]
    cellpose_masks_w2 = model.eval(dic_list_8bit_w2, diameter=40, channels=[0, 0], do_3D=False)[0]

    with multiprocessing.Pool() as pool:
        w1_well_locations, w1_cell_counts, w1_total_cell_areas = zip(*pool.map(get_well_data, list(zip(cellpose_masks_w1, flo_list_8bit_w1))))

    # remove empty items
    w1_well_locations = [ele for ele in w1_well_locations if ele != []]
    w1_cell_counts = [ele for ele in w1_cell_counts if ele != []]
    w1_total_cell_areas = [ele for ele in w1_total_cell_areas if ele != []]

    with multiprocessing.Pool() as pool:
        w2_well_locations, w2_cell_counts, w2_total_cell_areas = zip(*pool.map(get_well_data, list(zip(cellpose_masks_w2, flo_list_8bit_w2))))

    # remove empty items
    w2_well_locations = [ele for ele in w2_well_locations if ele != []]
    w2_cell_counts = [ele for ele in w2_cell_counts if ele != []]
    w2_total_cell_areas = [ele for ele in w2_total_cell_areas if ele != []]

    with multiprocessing.Pool() as pool:
        count_res_w1_arr = np.array(pool.map(get_class_count, w1_cell_counts))
        count_res_w2_arr = np.array(pool.map(get_class_count, w2_cell_counts))

    # arrange data for clonogenic analysis
    clono_input = [(w1_well_locations[i], w1_cell_counts[i], w2_well_locations[i], w2_cell_counts[i]) for i in range(len(w1_well_locations))]
    with multiprocessing.Pool() as pool:
        clonogenic_analysis = np.array(pool.map(get_clonogenic_analysis, clono_input))

    for j, (key_w1, key_w2) in enumerate(zip(data_well1.keys(), data_well2.keys())):
        data_well1[key_w1] = int(np.sum(count_res_w1_arr[:, j]))
        data_well2[key_w2] = int(np.sum(count_res_w2_arr[:, j]))

    # update clonogenic analysis results for frame
    for j, key in enumerate(data_clonogenic.keys()):
        data_clonogenic[key] = int(np.sum(clonogenic_analysis[:, j]))

    for i in range(len(w1_well_locations)):
        if len(w1_well_locations[i]) > 0 and len(w2_well_locations[i]) > 0:
            swarm_data_w1['w1_count'].extend(w1_cell_counts[i])
            swarm_data_w1['w1_area'].extend(w1_total_cell_areas[i])
            swarm_data_w2['w2_count'].extend(w2_cell_counts[i])
            swarm_data_w2['w2_area'].extend(w2_total_cell_areas[i])

    return data_well1, data_well2, data_clonogenic, swarm_data_w1, swarm_data_w2


if __name__ == '__main__':
    file_name = 'mGBM_50um_day7_TMZ_IR_IMPDH2_Device1.lif'
    root_dir = 'C:\\Users\\ShiskaRaut\\Desktop\\Projects'
    data_path = os.path.join(root_dir, 'Data', file_name)
    well1_name = 'WellA1_cells_mgbm'
    well2_name = 'WellA2_cells_mgbm'

    data_well1, data_well2, data_clonogenic, swarm_data_w1, swarm_data_w2 = get_clonogenic_assay_summary(data_path, well1_name, well2_name)

    fname_ini = f"{well1_name}_and_{well2_name}"
    out_dir = os.path.join(os.getcwd(), 'output', fname_ini)
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, f"{well1_name}_results.json"), 'w') as f:
        json.dump(data_well1, f)

    with open(os.path.join(out_dir, f"{well2_name}_results.json"), 'w') as f:
        json.dump(data_well2, f, indent=4)

    with open(os.path.join(out_dir, f"clonogenic_results.json"), 'w') as f:
        json.dump(data_clonogenic, f, indent=4)

    save_swarm_data(swarm_data_w1, out_dir, well1_name)
    save_swarm_data(swarm_data_w2, out_dir, well2_name)

