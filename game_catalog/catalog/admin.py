from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке
    list_display = [
        'id',
        'display_image',
        'title',
        'genre',
        'price',
        'developer',
        'is_available',
        'release_date',
        'created'
    ]
    
    # Поля для поиска
    search_fields = ['title', 'developer', 'description']
    
    # Фильтры справа
    list_filter = ['genre', 'platform', 'is_available', 'release_date']
    
    # Редактируемые поля прямо в списке
    list_editable = ['price', 'is_available']
    
    # Пагинация
    list_per_page = 20
    
    # Поля в детальном просмотре
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title',
                'slug',
                'description',
                'short_description',
                'image',
                'display_image_preview',
            )
        }),
        ('Детали игры', {
            'fields': (
                'genre',
                'price',
                'release_date',
                'developer',
                'publisher',
                'platform',
                'metacritic_score',
            )
        }),
        ('Статус', {
            'fields': ('is_available',)
        }),
    )
    
    # Автозаполнение slug из title
    prepopulated_fields = {'slug': ('title',)}
    
    # Порядок полей в форме добавления
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'slug', 'description', 'image', 'price', 'genre'),
        }),
    )
    
    # Метод для отображения изображения в списке
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.image.url
            )
        return "Нет изображения"
    display_image.short_description = 'Обложка'
    
    # Метод для предпросмотра изображения в форме
    def display_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 10px; margin-top: 10px;" />',
                obj.image.url
            )
        return "Изображение не загружено"
    display_image_preview.short_description = 'Предпросмотр обложки'
    
    # Поля только для чтения при редактировании
    readonly_fields = ['display_image_preview', 'created', 'updated']
    
    # Действия в админке
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Выбранные игры теперь доступны для покупки")
    make_available.short_description = "Сделать доступными"
    
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Выбранные игры теперь недоступны")
    make_unavailable.short_description = "Сделать недоступными"