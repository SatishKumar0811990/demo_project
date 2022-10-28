from django.contrib import admin

# Register your models here.
from .models import User,Course,Teacher


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',  'created_at']


admin.site.register(User, UserAdmin)






admin.site.register(Course)
admin,admin.site.register(Teacher)
