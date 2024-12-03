from django.urls import path
from .views import All_posts, Add_post, post_details, comment_new, Edit_post, post_delete

urlpatterns = [
    path('', All_posts, name='all_post'),
    path('post/add/', Add_post, name='add_post'),
    path('post/<int:pid>/', post_details, name='post_details'),
    path('post/<int:pid>/edit', Edit_post, name='edit_post'),
    path('post/<int:pid>/addcomment', comment_new, name='comment_new'),
    path('post/<int:pid>/delete', post_delete, name='post_delete')
]
