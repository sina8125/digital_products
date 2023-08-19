from django.contrib import admin

from .models import Category, Product, File


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enable', 'created_time']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']


class FileInLineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file', 'file_type', 'is_enable']
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [FileInLineAdmin]
    list_display = ['title', 'is_enable', 'created_time']
    list_filter = ['is_enable']
    filter_horizontal = ['categories']
