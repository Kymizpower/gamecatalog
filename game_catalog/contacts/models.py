from django.db import models

class ContactMessage(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    message = models.TextField('Сообщение')
    created = models.DateTimeField('Дата отправки', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return f'{self.name} - {self.email}'