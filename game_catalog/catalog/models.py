from django.db import models
from django.urls import reverse

class Game(models.Model):
    GENRES = [
        ('RPG', 'Ролевые'),
        ('ACTION', 'Экшен'),
        ('STRATEGY', 'Стратегии'),
        ('ADVENTURE', 'Приключения'),
        ('SIMULATION', 'Симуляторы'),
        ('SPORT', 'Спортивные'),
        ('INDIE', 'Инди'),
        ('HORROR', 'Хоррор'),
    ]
    
    title = models.CharField('Название игры', max_length=200)
    slug = models.SlugField('URL-адрес', max_length=200, unique=True)
    description = models.TextField('Полное описание')
    short_description = models.CharField('Краткое описание', max_length=300)
    image = models.ImageField('Обложка игры', upload_to='games/%Y/%m/%d/')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    release_date = models.DateField('Дата выхода', blank=True, null=True)
    developer = models.CharField('Разработчик', max_length=100)
    publisher = models.CharField('Издатель', max_length=100, blank=True)
    genre = models.CharField('Жанр', max_length=20, choices=GENRES)
    platform = models.CharField('Платформа', max_length=100, default='PC')
    metacritic_score = models.IntegerField('Оценка Metacritic', blank=True, null=True)
    is_available = models.BooleanField('Доступно для покупки', default=True)
    created = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['genre']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'slug': self.slug})