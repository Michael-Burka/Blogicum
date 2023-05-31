from django.shortcuts import get_object_or_404, render
from django.http import Http404
from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    num_posts_to_display = 5
    post_list = (
        Post.objects.published()
        .order_by('-pub_date')[:num_posts_to_display]
    )
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.published(), pk=pk)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404
    post_list = Post.objects.published().filter(category=category)
    context = {
        'post_list': post_list,
        'category': category,
       }
    return render(request, template, context)
