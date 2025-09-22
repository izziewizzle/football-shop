from django.contrib import admin
from .models import Product

# Register your models here.
# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "is_featured")
    search_fields = ("name", "description")
    list_filter = ("is_featured",)