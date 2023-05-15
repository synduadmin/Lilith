from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

        
admin.site.register(Category, CategoryAdmin)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('display_featured_image', 'title', 'slug', 'status','created_on',  'display_categories')
    list_filter = ("status",)
    search_fields = ['title', 'content', 'categories__name']
    prepopulated_fields = {'slug': ('title',)}

    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="120" height="120" />', obj.featured_image)
        else:
            return "No Image"

    display_featured_image.short_description = 'Featured Image'

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    
    display_categories.short_description = 'Categories'

admin.site.register(Post, PostAdmin)
