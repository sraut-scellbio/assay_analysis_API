from django.shortcuts import render, redirect
from assay_api_app import forms

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
            return redirect('assay_api_app:upload_success')
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
            return redirect('assay_api_app:upload_success')
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
