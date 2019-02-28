from django.contrib import admin

from .models import Photo,Group

myModels = [Photo,Group]
admin.site.register(myModels)

