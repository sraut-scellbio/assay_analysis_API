from django.urls import path, re_path
from assay_api_app import views
from django.conf import settings
from django.conf.urls.static import static

# template tagging
app_name = 'assay_api_app'

urlpatterns = [
    re_path(r"^$", views.landing, name="scellbio_landing_page"),
    re_path(r"^scellbio_landing_page", views.landing, name="scellbio_landing_page"),
    re_path(r"^cell_count_options", views.cell_count_options, name="cell_count_options"),
    re_path(r"^clono_assay_options", views.clono_assay_options, name="clono_assay_options"),
    re_path(r"^dormancy_assay_options", views.dormancy_assay_options, name="dormancy_assay_options"),
    re_path(r"^cell_count_fluo", views.cell_count_fluo, name="cell_count_fluo"),
    re_path(r"^cell_count_labelfree", views.cell_count_labelfree, name="cell_count_labelfree"),
    re_path(r"^clono_assay_labelfree", views.clono_assay_labelfree, name="clono_assay_labelfree"),
    re_path(r"^clono_assay", views.clono_assay, name="clono_assay"),
    re_path(r"^migration_assay", views.migration_assay, name="migration_assay"),
    re_path(r"^dormancy_assay_labelfree", views.dormancy_assay_labelfree, name="dormancy_assay_labelfree"),
    re_path(r"^dormancy_assay", views.dormancy_assay, name="dormancy_assay")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
