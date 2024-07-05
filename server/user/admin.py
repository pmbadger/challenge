from django.contrib import admin
from .models import User, Profile
from .forms import UserAdminForm

admin.site.register(Profile)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
