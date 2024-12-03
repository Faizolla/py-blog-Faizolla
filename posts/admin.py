from django.contrib import admin
from .models import Post, Post_Attachments, Comment
from modeltranslation.admin import TranslationAdmin
# Register your models here.
# admin.site.register(Post)
class CustomPostAdmin(TranslationAdmin):
    list_display = (
        'author',
        'title_ru',
        'title_kk',
        'title_en',
        'content_ru',
        'content_kk',
        'content_en',
        'date',
        'edited',
    )
@admin.register(Post)
class PostAdmin(TranslationAdmin):
    pass
admin.site.register(Post_Attachments)
admin.site.register(Comment)