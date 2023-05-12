from django.contrib import admin

from api.models import CustomUserModel, Invate, Subscribe


admin.site.register(Invate)
admin.site.register(CustomUserModel)
admin.site.register(Subscribe)
