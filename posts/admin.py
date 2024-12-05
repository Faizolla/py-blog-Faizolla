from django.contrib import admin
from .models import Post, Post_Attachments, Comment
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class CustomPostAdmin(TranslationAdmin):
    fieldsets = (
        (_('Автор'), {'fields': ('author',)}),
        (_('Пост на русском'), {'fields': ( 'title_ru', 'content_ru',)}),
        (_('Пост на казахском'), {'fields': ( 'title_kk', 'content_kk',)}),
        (_('Пост на английском'), {'fields': ( 'title_en', 'content_en',)}),
        (_('Дополнительная информация'), {'fields': ( 'edited',)}),
    )
    add_fieldsets = (
        (_('Автор'), {'fields': ('author',)}),
        (_('Пост на русском'), {'fields': ( 'title_ru', 'content_ru',)}),
        (_('Пост на казахском'), {'fields': ( 'title_kk', 'content_kk',)}),
        (_('Пост на английском'), {'fields': ( 'title_en', 'content_en',)}),   
    )
    list_display = (
        'title',
        'date',
        'edited',
    )
admin.site.register(Post_Attachments)
admin.site.register(Comment)