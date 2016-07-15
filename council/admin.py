from django.contrib import admin
from council.models import (
    Activity,
    Party,
    Promise,
)

admin.site.register(Activity)
admin.site.register(Party)
admin.site.register(Promise)
