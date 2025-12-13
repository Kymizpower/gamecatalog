from django.db import models

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    content = models.TextField('Содержание')
    short_content = models.CharField('Краткое содержание', max_length=300)
    image = models.ImageField('Изображение', upload_to='news/')
    published_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.title