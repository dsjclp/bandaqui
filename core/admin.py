from django.contrib import admin

from .models import Photo
from .models import Video

admin.site.register(Photo)
admin.site.register(Video)