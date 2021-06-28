from django.contrib import admin
from .models import Profile, Districts, Amphures, Provinces, Geographies, Address

admin.site.register(Profile)
admin.site.register(Address)


admin.site.register(Geographies)
admin.site.register(Provinces)
admin.site.register(Amphures)
admin.site.register(Districts)

# Register your models here.
