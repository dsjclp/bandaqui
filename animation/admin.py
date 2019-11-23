from django.contrib import admin

from .models import Location
from .models import Piece
from .models import Instrument
from .models import Event
from .models import Profile
from .models import Eventinstrument
from .models import Participation

from django.contrib.contenttypes.admin import GenericTabularInline


admin.site.register(Piece)
admin.site.register(Location)
admin.site.register(Instrument)
admin.site.register(Profile)
admin.site.register(Eventinstrument)
admin.site.register(Event)
admin.site.register(Participation)