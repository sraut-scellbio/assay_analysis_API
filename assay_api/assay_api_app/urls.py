from django.urls import path, re_path
from assay_api_app import views

# template tagging
app_name = 'assay_api_app'

urlpatterns = [
    re_path(r"^$", views.landing, name="scellbio_landing_page"),
    re_path(r"^scellbio_landing_page", views.landing, name="scellbio_landing_page"),
    re_path(r"^cell_count_fluo", views.cell_count_fluo, name="cell_count_fluo"),
    re_path(r"^cell_count_labelfree", views.cell_count_labelfree, name="cell_count_labelfree"),
    re_path(r"^clono_assay_labelfree", views.clono_assay_labelfree, name="clono_assay_labelfree"),
    re_path(r"^clono_assay", views.clono_assay, name="clono_assay"),
    re_path(r"^upload_success", views.upload_success, name="upload_success"),
]
