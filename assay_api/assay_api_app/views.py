import os
import cv2
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from assay_api_app import forms
from assay_api_app.cell_count_fluo_src import preprocess, utils, analyze_cell_data
from assay_api_app.cell_count_fluo_src.analyze_cell_data import count_cells_fluo, count_cells_labelfree
from django.conf import settings

def landing(request):
    return render(request, "assay_api_app/scellbio_landing_page.html")

def upload_success(request):
    return render(request, "assay_api_app/upload_success.html")

# create form object for each site and add here
def cell_count_fluo(request):
    if request.method == 'POST':
        form = forms.FormCountFluo(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            image_name = (form.cleaned_data.get('image')).name
            img_path = os.path.join('downloads','count_fluo',image_name)
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
            img_path = os.path.join('downloads','count_labelfree',image_name)
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
    if request.method == "POST":
        form = forms.FormClono(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('assay_api_app:upload_success')
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
            return redirect('assay_api_app:upload_success')
        else:
            print("form invalid\n")
            print(form.errors)
    else:
        form = forms.FormClonoLabelFree()
    return render(request, "assay_api_app/clono_assay_labelfree.html", { 'form': form })
