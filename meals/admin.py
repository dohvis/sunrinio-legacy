from django.contrib import admin

from meals.models import (
    Meal,
    Review,
)

admin.site.register(Meal)
admin.site.register(Review)
