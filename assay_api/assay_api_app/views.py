from django.shortcuts import render

def landing(request):
    return render(request, "assay_api_app/scellbio_landing_page.html")

def cell_count_fluo(request):
    return render(request, "assay_api_app/cell_count_fluo.html")

def cell_count_labelfree(request):
    return render(request, "assay_api_app/cell_count_labelfree.html")

def clono_assay(request):
    return render(request, "assay_api_app/clono_assay.html")

def clono_assay_labelfree(request):
    return render(request, "assay_api_app/clono_assay_labelfree.html")
