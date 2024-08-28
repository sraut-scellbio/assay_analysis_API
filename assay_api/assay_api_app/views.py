from django.shortcuts import render
from assay_api_app import forms

def landing(request):
    return render(request, "assay_api_app/scellbio_landing_page.html")

# create form object for each site and add here
def cell_count_fluo(request):
    form = forms.FormCountFluo()
    if request.method == 'POST':
        form = forms.FormCountFluo(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data['image']

            save_path = os.path.join(os.cwd(), "downloads", image.name)
            with open(save_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

    return render(request, "assay_api_app/cell_count_fluo.html", {'form': form })

def cell_count_labelfree(request):
    form = forms.FormCountLabelfree()
    if request.method == 'POST':
        form = forms.FormCountLabelfree(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data['image']

            save_path = os.path.join(os.cwd(), "downloads", image.name)
            with open(save_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

    return render(request, "assay_api_app/cell_count_labelfree.html", {'form': form })

def clono_assay(request):
    form = forms.FormClono()
    if request.method == "POST":
        form = forms.FormClono(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            cell_line = form.cleaned_data['cell_line']
            num_wells = form.cleaned_data['num_wells']
            analysis_type = form.cleaned_data['analysis_type']
            saving_folder_name = form.cleaned_data['saving_folder_name']

            w1_d1_lf_folder = form.cleaned_data['w1_d1_lf']
            w1_d1_fluo_folder = form.cleaned_data['w1_d1_fluo']
            w2_d1_lf_folder = form.cleaned_data['w2_d1_lf']
            w2_d1_fluo_folder = form.cleaned_data['w2_d1_fluo']
            w3_d1_lf_folder = form.cleaned_data['w3_d1_lf']
            w3_d1_fluo_folder = form.cleaned_data['w3_d1_fluo']
            w4_d1_lf_folder = form.cleaned_data['w4_d1_lf']
            w4_d1_fluo_folder = form.cleaned_data['w4_d1_fluo']

            w1_dn_lf_folder = form.cleaned_data['w1_dn_lf']
            w1_dn_fluo_folder = form.cleaned_data['w1_dn_fluo']
            w2_dn_lf_folder = form.cleaned_data['w2_dn_lf']
            w2_dn_fluo_folder = form.cleaned_data['w2_dn_fluo']
            w3_dn_lf_folder = form.cleaned_data['w3_dn_lf']
            w3_dn_fluo_folder = form.cleaned_data['w3_dn_fluo']
            w4_dn_lf_folder = form.cleaned_data['w4_dn_lf']
            w4_dn_fluo_folder = form.cleaned_data['w4_dn_fluo']

            # save FILES

            # call python program for analysis
            # it should take the downloaded file paths as input
            # write the results as outputs to a location as a .zip file
            # take the user to a page that allows them to download the results
             
    return render(request, "assay_api_app/clono_assay.html", { 'form': form })

def clono_assay_labelfree(request):
    form = forms.FormClonoLabelfree()
    if request.method == "POST":
        form = forms.FormClonoLabelfree(request.POST, request.FILES)

        if form.is_valid():
            w1_d1_lf_folder = form.cleaned_data['w1_d1_lf']
            w2_d1_lf_folder = form.cleaned_data['w2_d1_lf']
            w3_d1_lf_folder = form.cleaned_data['w3_d1_lf']
            w4_d1_lf_folder = form.cleaned_data['w4_d1_lf']

            w1_dn_lf_folder = form.cleaned_data['w1_dn_lf']
            w2_dn_lf_folder = form.cleaned_data['w2_dn_lf']
            w3_dn_lf_folder = form.cleaned_data['w3_dn_lf']
            w4_dn_lf_folder = form.cleaned_data['w4_dn_lf']

    return render(request, "assay_api_app/clono_assay_labelfree.html", { 'form': form })
