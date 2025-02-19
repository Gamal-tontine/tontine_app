from django.contrib import admin
from .models import Acquitement, Payment

@admin.register(Acquitement)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class AuthorAdmin(admin.ModelAdmin):
    pass