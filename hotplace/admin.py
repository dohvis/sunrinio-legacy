from django.contrib import admin
from .models import (
    Image,
    Place,
    Review,
)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'y', 'x']


admin.site.register(Place, PlaceAdmin)
admin.site.register(Review)
admin.site.register(Image)
