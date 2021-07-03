from django.contrib import admin
from .models import Vacation, Itinerary, Packing, Photo

# Register your models here.
admin.site.register(Vacation)
admin.site.register(Itinerary)
admin.site.register(Packing)
admin.site.register(Photo)
