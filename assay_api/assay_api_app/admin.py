from django.contrib import admin
from assay_api_app.models import ModelClono, ModelClonoLabelFree, ModelCountFluo, ModelCountLabelFree, ModelDormancy, ModelMigration, \
 ModelDormancyLabelFree

admin.site.register(ModelCountFluo)
admin.site.register(ModelCountLabelFree)
admin.site.register(ModelClono)
admin.site.register(ModelClonoLabelFree)
admin.site.register(ModelMigration)
admin.site.register(ModelDormancy)
admin.site.register(ModelDormancyLabelFree)