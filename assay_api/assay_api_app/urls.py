from django.urls import path, re_path
from assay_api_app import views
from django.conf import settings
from django.conf.urls.static import static

# template tagging
app_name = 'assay_api_app'

urlpatterns = [
    re_path(r"^$", views.landing, name="scellbio_landing_page"),
    re_path(r"^scellbio_landing_page", views.landing, name="scellbio_landing_page"),
    re_path(r"^cell_count_fluo", views.cell_count_fluo, name="cell_count_fluo"),
    re_path(r"^cell_count_labelfree", views.cell_count_labelfree, name="cell_count_labelfree"),
    re_path(r"^clono_assay_labelfree", views.clono_assay_labelfree, name="clono_assay_labelfree"),
    re_path(r"^clono_assay", views.clono_assay, name="clono_assay"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
