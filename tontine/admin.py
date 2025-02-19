from django.contrib import admin
from .models import TontineCollective
@admin.register(TontineCollective)
class AuthorAdmin(admin.ModelAdmin):
    pass
