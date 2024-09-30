from django.contrib import admin
from .models import User, Organisation, Member, Role

# Register your models here.

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Member)
admin.site.register(Role)
