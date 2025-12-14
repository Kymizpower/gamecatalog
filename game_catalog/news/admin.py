from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'display_image',
        'title',
        'is_published',
        'published_date',
        'short_content_preview'
    ]
    
    list_filter = ['is_published', 'published_date']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title',
                'slug',
                'short_content',
                'content',
                'image',
                'display_image_preview',
            )
        }),
        ('Статус', {
            'fields': ('is_published',)
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)}
    
    readonly_fields = ['display_image_preview', 'published_date']
    
    # Метод для отображения изображения в списке
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 5px; object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    display_image.short_description = 'Изображение'
    
    # Метод для предпросмотра изображения в форме
    def display_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 10px; margin-top: 10px;" />',
                obj.image.url
            )
        return "Изображение не загружено"
    display_image_preview.short_description = 'Предпросмотр изображения'
    
    # Метод для отображения краткого содержания
    def short_content_preview(self, obj):
        return obj.short_content[:100] + "..." if len(obj.short_content) > 100 else obj.short_content
    short_content_preview.short_description = 'Краткое содержание'
    
    actions = ['publish_selected', 'unpublish_selected']
    
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "Выбранные новости опубликованы")
    publish_selected.short_description = "Опубликовать выбранные новости"
    
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "Выбранные новости сняты с публикации")
    unpublish_selected.short_description = "Снять с публикации"