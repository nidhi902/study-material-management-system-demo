from django.contrib import admin
from .models import Studymaterial
from .models import profile

# Register your models here.
admin.site.register(Studymaterial)


admin.site.register(profile)
class profileAdmin(admin.ModelAdmin):
    list_display=('user', 'role', 'accessbox')


    
