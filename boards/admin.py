from django.contrib import admin
from boards.models import (
    Board,
    Post,
    Comment,
)

admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Comment)
