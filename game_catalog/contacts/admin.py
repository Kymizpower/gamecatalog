from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'phone_display',
        'message_preview',
        'created',
        'is_processed'
    ]
    
    list_filter = ['created', 'is_processed']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_processed']
    readonly_fields = ['created', 'message_display']
    list_per_page = 20
    
    fieldsets = (
        ('Информация о отправителе', {
            'fields': (
                'name',
                'email',
                'phone',
                'created',
            )
        }),
        ('Сообщение', {
            'fields': (
                'message_display',
            )
        }),
        ('Статус обработки', {
            'fields': ('is_processed', 'processed_notes')
        }),
    )
    
    # Добавляем поля в модель (нужно добавить их в models.py)
    # is_processed = models.BooleanField('Обработано', default=False)
    # processed_notes = models.TextField('Заметки обработки', blank=True)
    
    def phone_display(self, obj):
        if obj.phone:
            return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)
        return "Не указан"
    phone_display.short_description = 'Телефон'
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Сообщение'
    
    def message_display(self, obj):
        return format_html('<div class="message-box" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;">{}</div>', obj.message)
    message_display.short_description = 'Текст сообщения'
    
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
        self.message_user(request, "Выбранные сообщения помечены как обработанные")
    mark_as_processed.short_description = "Пометить как обработанные"
    
    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)
        self.message_user(request, "Выбранные сообщения помечены как необработанные")
    mark_as_unprocessed.short_description = "Пометить как необработанные"