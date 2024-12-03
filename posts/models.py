from django.db import models
from users.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    date = models.DateTimeField(auto_now=timezone.now(), verbose_name='Дата создания')  
    edited = models.BooleanField(default=False, verbose_name='Редактирован')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return f'{self.author}: {self.title} ({self.date})'
    
class Post_Attachments(models.Model):
    file = models.FileField(upload_to='images/', verbose_name='Файл')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')

    class Meta:
        verbose_name = 'Изображение к посту'
        verbose_name_plural = 'Изображения к постам'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, verbose_name='Пост')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'