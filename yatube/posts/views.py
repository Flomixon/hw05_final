from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow


def pagin(object, request, page):
    paginator = Paginator(object, page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@cache_page(20, key_prefix='index_page')
def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.select_related('author').\
        select_related('group').all()
    page_obj = pagin(post_list, request, 10)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    group = Group.objects.get(slug=slug)
    post_list = group.posts.all()
    page_obj = pagin(post_list, request, 10)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    post_list = author.post_user.all()
    page_obj = pagin(post_list, request, 10)
    user = request.user
    following = False
    if user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author.id
        ).exists()
    context = {
        'user': user,
        'author': author,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author'),
        id=post_id)
    template = 'posts/post_detail.html'
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'user': request.user,
        'comments': post.comments.prefetch_related('post').all(),
        'form': form
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    author = request.user
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = author
        form.save()
        return redirect('posts:profile', author)
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    template = 'posts/create_post.html'
    is_edit = True
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(
        request,
        template,
        {'form': form, 'post': post, 'is_edit': is_edit}
    )


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    authors = get_object_or_404(User, username=request.user)
    authors = set(authors.follower.values_list('author'))
    post_list = Post.objects.select_related('author').\
        select_related('group').filter(author__in=authors).all()
    page_obj = pagin(post_list, request, 10)
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user.get_username() != username:
        Follow.objects.select_related('author').get_or_create(
            user=request.user,
            author=author
        )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        user=request.user,
        author=User.objects.get(username=username)
    ).delete()
    return redirect('posts:profile', username)
