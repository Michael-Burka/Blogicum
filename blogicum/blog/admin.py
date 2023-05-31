from django.contrib import admin

from .models import Post, Location, Category

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )
    list_editable = (
        'is_published',
        'category',
        'location',
    )
    search_fields = ('title',)
    list_filter = ('is_published', 'pub_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
    )
    list_editable = (
        'is_published',
        'title',

    )
    search_fields = ('title',)
    list_filter = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_published',
    )
    list_editable = (
        'name',
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)


admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
