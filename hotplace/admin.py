from django.contrib import admin
from .models import (
    Place,
    Review,
)

admin.site.register(Place)
admin.site.register(Review)
