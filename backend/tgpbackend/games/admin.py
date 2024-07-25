from django.contrib import admin
from django.contrib import admin
from django.apps import apps
from .models import *


class GameAdmin(admin.ModelAdmin):
    raw_id_fields = ('price',)


app = apps.get_app_config('games')

for model_name, model in app.models.items():
    if model_name == 'game':
        admin.site.register(model,GameAdmin)
    else:
        admin.site.register(model)


