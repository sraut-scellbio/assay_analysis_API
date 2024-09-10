import os
import cv2
import glob
import random
import string
import zipfile
import numpy as np
import seaborn as sns
from zipfile import ZipFile
import matplotlib.pyplot as plt

from django.conf import settings
from django.shortcuts import render, redirect

from assay_api_app import forms
from assay_api_app.cell_count_fluo_src import preprocess, utils, analyze_cell_data
from assay_api_app.cell_count_fluo_src.analyze_cell_data import count_cells_fluo, count_cells_labelfree


def landing(request):
    return render(request, "assay_api_app/scellbio_landing_page.html")

def upload_success(request):
    return render(request, "assay_api_app/upload_success.html")


def generate_unique_id(length=8):
    # Define the characters to use in the identifier
    characters = string.ascii_letters + string.digits
    # Randomly choose characters from the pool and join them to form the identifier
    unique_id = ''.join(random.choice(characters) for _ in range(length))
    return unique_id


def save_results(res_dict, swarm_data, save_path):
    # save count data
    with open(os.path.join(save_patj, f"count_results.json"), 'w') as f:
        json.dump(res_dict, f)

    # save plot
    for i, key in enumerate(swarm_data.keys()):
        ser = pd.Series(swarm_data[key], name=f"area")
        # fil
        filt_ser = ser.drop(ser[ser == 0].index)
        filt_ser.to_csv(os.path.join(out_dir, f"{key}_area.csv"), index=False)
        plt.figure(figsize=(5, 7))
        plt.title(ser.name)
        sns.swarmplot(data=filt_ser, size=1)
        plt.yticks(np.arange(0, filt_ser.max() + 150, 150))
        plt.ylabel(f"{key}_area")
        plt.tight_layout()
        plt.grid()
        plt.savefig(os.path.join(out_dir, f"swarmplot{key}_area.pdf"), dpi=150)

# create form object for each site and add here
def cell_count_fluo(request):
    if request.method == 'POST':
        form = forms.FormCountFluo(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            image_name = (form.cleaned_data.get('image')).name
            img_path = os.path.join(settings.MEDIA_ROOT,'count_fluo',image_name)
            print(img_path)
            if img_path is None:
                print("Image not found.")
            else:
                img_raw = cv2.imread(img_path)
                img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
                img_8bit = preprocess.conv_to_8bit(img_gray)

                num_cells, cell_locs, cell_contours = count_cells_fluo(img_8bit)

                # draw and display contours
                img_clr = utils.draw_contours(img_8bit, cell_contours)
                img_clr_name = f"processed_{image_name}"
                img_clr_path = os.path.join(settings.STATIC_DIR, 'images', img_clr_name)

                # Save the processed image
                cv2.imwrite(img_clr_path, img_clr)

                # Provide the path as a reference in the template
                # img_clr_url = os.path.join(settings.STATIC_URL, 'images', img_clr_name)

                return render(request, "assay_api_app/cell_count_fluo_results.html", {
                    'num_cells': num_cells,
                    'img_clr_name': img_clr_name
                })
        else:
            print("form invalid\n")
            print(form.errors)
    else:
        form = forms.FormCountFluo()
    return render(request, "assay_api_app/cell_count_fluo.html", {'form': form })


def cell_count_labelfree(request):
    if request.method == 'POST':
        form = forms.FormCountLabelFree(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_name = (form.cleaned_data.get('image')).name
            img_path = os.path.join(settings.MEDIA_ROOT,'count_labelfree',image_name)
            print(img_path)
            if img_path is None:
                print("Image not found.")
            else:
                img_raw = cv2.imread(img_path)
                img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
                img_8bit = preprocess.conv_to_8bit(img_gray)

                num_cells, cell_locs, cell_contours = count_cells_labelfree(img_8bit)

                # draw and display contours
                img_clr = utils.draw_contours(img_8bit, cell_contours)
                img_clr_name = f"processed_{image_name}"
                img_clr_path = os.path.join(settings.STATIC_DIR, 'images', img_clr_name)

                # Save the processed image
                cv2.imwrite(img_clr_path, img_clr)

                # Provide the path as a reference in the template
                # img_clr_url = os.path.join(settings.STATIC_URL, 'images', img_clr_name)

                return render(request, "assay_api_app/cell_count_labelfree_results.html", {
                    'num_cells': num_cells,
                    'img_clr_name': img_clr_name
                })
        else:
            print("form invalid\n")
            print(form.errors)
    else:
        form = forms.FormCountLabelFree()
    return render(request, "assay_api_app/cell_count_labelfree.html", {'form': form })


def clono_assay(request):
    file_fields = [
        'w1_d1_lf',
        'w1_d1_fluo',
        'w2_d1_lf',
        'w2_d1_fluo',
        'w3_d1_lf',
        'w3_d1_fluo',
        'w4_d1_lf',
        'w4_d1_fluo',
        'w1_dn_lf',
        'w1_dn_fluo',
        'w2_dn_lf',
        'w2_dn_fluo',
        'w3_dn_lf',
        'w3_dn_fluo',
        'w4_dn_lf',
        'w4_dn_fluo'
    ]

    if request.method == "POST":
        form = forms.FormClono(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            image_folders_d1 = dict()
            image_folders_dn = dict()

            uname = form.cleaned_data.get('name')
            cell_line = form.cleaned_data.get('cell_line')
            analysis_type = form.cleaned_data.get('analysis_type')
            num_wells = int(form.cleaned_data.get('num_wells'))

            f_uid = generate_unique_id()
            user_uid = f"{uname}_{cell_line}_{f_uid}"
            # save labelfree and fluorescent paths as tuple values
            for i in range(0, len(file_fields), 2):
                if (form.cleaned_data.get(file_fields[i])) is not None and (form.cleaned_data.get(file_fields[i+1]) is not None):
                    fname_lf = (form.cleaned_data.get(file_fields[i])).name
                    fname_fluo = (form.cleaned_data.get(file_fields[i+1])).name
                    folder_path_lf = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', fname_lf)
                    folder_path_fluo = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', fname_fluo)

                    folder_path_lf_exto = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', user_uid, file_fields[i])
                    folder_path_fluo_exto = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', user_uid, file_fields[i+1])
                    os.makedirs(folder_path_lf_exto, exist_ok=True)
                    os.makedirs(folder_path_fluo_exto, exist_ok=True)

                    # extract labelfree folder
                    with ZipFile(folder_path_lf, 'r') as zip_ref:
                        zip_ref.extractall(folder_path_lf_exto)

                    # extract fluorescent folder
                    with ZipFile(folder_path_fluo, 'r') as zip_ref:
                        zip_ref.extractall(folder_path_fluo_exto)

                    tokens = file_fields[i].split('_')
                    if tokens[1] == 'd1':
                        d1_lf = os.path.join(folder_path_lf_exto, fname_lf.split('.')[0])
                        d1_fluo = os.path.join(folder_path_fluo_exto, fname_fluo.split('.')[0])
                        image_folders_d1[tokens[0]] = (d1_lf, d1_fluo)
                    else:
                        dn_lf = os.path.join(folder_path_lf_exto, fname_lf.split('.')[0])
                        dn_fluo = os.path.join(folder_path_fluo_exto, fname_fluo.split('.')[0])
                        image_folders_dn[tokens[0]] = (dn_lf, dn_fluo)

            # remove zip files
            zip_files = glob.glob(os.path.join(settings.MEDIA_ROOT, 'clono_analysis', '*.zip'))
            for zip_file in zip_files:
                try:
                    os.remove(zip_file)
                    print(f"Removed file: {zip_file}")
                except Exception as e:
                    print(f"Error removing file {zip_file}: {e}")

            # create root results folder
            results_fld_name = f"results_{user_uid}"
            root_results_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', results_fld_name)
            os.makedirs(root_results_path, exist_ok=True)
            # check if the items uploaded correspond to the analysis model_type
            if (analysis_type == 'Single Day') and (len(image_folders_d1.values()) > 0):
                for well_id, (path_lf, path_fluo) in image_folders_d1.items():
                    # create results folder
                    well_fld_path = os.path.join(root_results_path, well_id)
                    os.makedirs(well_fld_path)
                    # res_dict, swarm_data_dict = singleday_analysis(path_lf, path_fluo)
                    # save_results(res_dict, swarm_data_dict, well_fld_path)

                    zip_fname = f"{results_fld_name}.zip"
                    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', zip_fname)
                    with ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for root, dirs, files in os.walk(root_results_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Add file to zip file with relative path
                                zip_file.write(file_path, os.path.relpath(file_path, root_results_path))

                return render(request, "assay_api_app/clono_assay_results.html", {
                'results_zipfile': f'{settings.MEDIA_URL}clono_analysis/{zip_fname}',
                })


            elif (analysis_type == 'Multi Day') and (set(image_folders_d1.keys()) == set(image_folders_dn.keys())) and (len(image_folders_d1.values()) > 0):
                for well_id in image_folders_d1.keys():
                    well_fld_path = os.path.join(root_results_path, well_id)
                    os.makedirs(well_fld_path)
                    path_lf_d1, path_fluo_d1 = image_folders_d1[well_id]
                    path_lf_dn, path_fluo_dn = image_folders_dn[well_id]
                    # res_dict, swarm_data_dict = multiday_analysis(path_lf_d1, path_fluo_d1, path_lf_dn, path_fluo_dn)
                    # save_results(res_dict, swarm_data_dict, well_fld_path)

                    zip_fname = f"{results_fld_name}.zip"
                    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis', zip_fname)
                    with ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for root, dirs, files in os.walk(root_results_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Add file to zip file with relative path
                                zip_file.write(file_path, os.path.relpath(file_path, root_results_path))

                return render(request, "assay_api_app/clono_assay_results.html", {
                'results_zipfile': f'{settings.MEDIA_URL}clono_analysis/{zip_fname}',
                })

            return render(request, "assay_api_app/clono_assay_results.html", {
            'results_zipfile': None,
            })

        else:
            print("form invalid\n")
            print(form.errors)
    else:
        form = forms.FormClono()
    return render(request, "assay_api_app/clono_assay.html", { 'form': form })


def clono_assay_labelfree(request):
    if request.method == "POST":
        form = forms.FormClonoLabelFree(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_folders_d1 = dict()
            image_folders_dn = dict()

            uname = form.cleaned_data.get('name')
            cell_line = form.cleaned_data.get('cell_line')
            analysis_type = form.cleaned_data.get('analysis_type')
            num_wells = int(form.cleaned_data.get('num_wells'))

            f_uid = generate_unique_id()
            user_uid = f"{uname}_{cell_line}_{f_uid}"
            # save labelfree and fluorescent paths as tuple values
            for i in range(0, len(file_fields)):
                if form.cleaned_data.get(file_fields[i]) is not None:
                    fname_lf = (form.cleaned_data.get(file_fields[i])).name
                    folder_path_lf = os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', fname_lf)

                    folder_path_lf_exto = os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', user_uid, file_fields[i])
                    os.makedirs(folder_path_lf_exto, exist_ok=True)

                    # extract labelfree folder
                    with ZipFile(folder_path_lf, 'r') as zip_ref:
                        zip_ref.extractall(folder_path_lf_exto)

                    tokens = file_fields[i].split('_')
                    if tokens[1] == 'd1':
                        d1_lf = os.path.join(folder_path_lf_exto, fname_lf.split('.')[0])
                        image_folders_d1[tokens[0]] = d1_lf
                    else:
                        dn_lf = os.path.join(folder_path_lf_exto, fname_lf.split('.')[0])
                        image_folders_dn[tokens[0]] = dn_lf

            # remove zip files
            zip_files = glob.glob(os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', '*.zip'))

            for zip_file in zip_files:
                try:
                    os.remove(zip_file)
                    print(f"Removed file: {zip_file}")
                except Exception as e:
                    print(f"Error removing file {zip_file}: {e}")

            # create root results folder
            results_fld_name = f"results_{user_uid}"
            root_results_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', results_fld_name)
            os.makedirs(root_results_path, exist_ok=True)
            # check if the items uploaded correspond to the analysis model_type
            if (analysis_type == 'Single Day') and (len(image_folders_d1.values()) > 0):
                for well_id, path_lf in image_folders_d1.items():
                    # create results folder
                    well_fld_path = os.path.join(root_results_path, well_id)
                    os.makedirs(well_fld_path)
                    # res_dict, swarm_data_dict = singleday_analysis(path_lf)
                    # save_results(res_dict, swarm_data_dict, well_fld_path)

                    zip_fname = f"{results_fld_name}.zip"
                    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', zip_fname)
                    with ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for root, dirs, files in os.walk(root_results_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Add file to zip file with relative path
                                zip_file.write(file_path, os.path.relpath(file_path, root_results_path))

                return render(request, "assay_api_app/clono_assay_results.html", {
                'results_zipfile': f'{settings.MEDIA_URL}clono_analysis_labelfree/{zip_fname}',
                })


            elif (analysis_type == 'Multi Day') and (set(image_folders_d1.keys()) == set(image_folders_dn.keys())) and (len(image_folders_d1.values()) > 0):
                for well_id in image_folders_d1.keys():
                    well_fld_path = os.path.join(root_results_path, well_id)
                    os.makedirs(well_fld_path)
                    path_lf_d1 = image_folders_d1[well_id]
                    path_lf_dn = image_folders_dn[well_id]
                    # res_dict, swarm_data_dict = multiday_analysis(path_lf_d1, path_lf_dn)
                    # save_results(res_dict, swarm_data_dict, well_fld_path)

                    zip_fname = f"{results_fld_name}.zip"
                    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'clono_analysis_labelfree', zip_fname)
                    with ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for root, dirs, files in os.walk(root_results_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Add file to zip file with relative path
                                zip_file.write(file_path, os.path.relpath(file_path, root_results_path))

                return render(request, "assay_api_app/clono_assay_results.html", {
                'results_zipfile': f'{settings.MEDIA_URL}clono_analysis_labelfree/{zip_fname}',
                })

            return render(request, "assay_api_app/clono_assay_results.html", {
            'results_zipfile': None,
            })
        else:
            print("form invalid\n")
            print(form.errors)
    else:
        form = forms.FormClonoLabelFree()
    return render(request, "assay_api_app/clono_assay_labelfree.html", { 'form': form })
