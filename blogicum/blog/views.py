from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
)
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse, reverse_lazy

from blog.models import Post, Category


User = get_user_model()


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    ordering = ['-pub_date']
    paginate_by = 10
    queryset = model.objects.published()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = model.objects.published()


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        if not category.is_published:
            raise Http404
        return Post.objects.published().filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    ordering = '-pub_date'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return (Post.objects.filter(author=user)
                .select_related('author')
                .order_by(self.ordering))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = get_object_or_404(User, username=username)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        context['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
