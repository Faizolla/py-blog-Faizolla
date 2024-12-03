from django.shortcuts import redirect, render
from .models import Post, Post_Attachments, Comment
from .form import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def All_posts(request):
    posts = Post.objects.order_by('id')
    for post in posts:
        att = Post_Attachments.objects.filter(post_id = post.pk)
        post.att = att
    return render(request, 'post/postlist.html', {'posts' : posts})

@login_required
def Add_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        att = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            #Добавить пользователя
            post.author = request.user
            post.save()
            for img in att:
                Post_Attachments.objects.create(post_id = post.pk, file = img)

        return redirect(to='post_details', pid = post.pk)
    return render(request, 'post/newpost.html', {'form': form})

@login_required
def Edit_post(request, pid):
    post = Post.objects.get(pk=pid)
    post_att = Post_Attachments.objects.filter(post_id = pid)
    if request.method != 'POST':
        form = PostForm(instance= post)
    else:
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit=False)
            att = request.FILES.getlist('images')
            for image in att:
                Post_Attachments.objects.create(
                    file = image,
                    post_id = pid
                )
            chosen = request.POST.getlist('attachments')
            for image_id in chosen:
                Post_Attachments.objects.get(pk = int(image_id)).delete()
            post.edited = True
            #Добавить пользователя
            post.save()
        return redirect(to='post_details', pid = post.pk)
    return render(request, 'post/post_edit.html', {'form': form, 'post_att': post_att})


def post_details(request, pid):
    post = Post.objects.get(pk=pid)
    att = Post_Attachments.objects.filter(post_id = pid)
    comments = Comment.objects.filter(post_id = pid)
    return render(request, 'post/postdetails.html', {'post' : post, 'images': att, 'comments' : comments})

@login_required
def comment_new(request, pid):
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pid
            comment.author = request.user
            comment.save()
            return redirect('post_details', pid = pid) # Первый pid - <int:pid>, второй pid - это id поста которому мы сейчас оставляем комментарий
    return render(request, 'post/comment_new.html', {'form' : form})


@login_required
def post_delete(request, pid):
    post = Post.objects.get(pk=pid)
    post.delete()
    return redirect(to='all_post')