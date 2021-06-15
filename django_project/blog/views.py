from django.urls import reverse_lazy
from .models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import \
    (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class HomeListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    extra_context = {'title': 'Home Django project'}
    ordering = ["-post_created"]
    template_name = 'blog/homepage.html'
    paginate_by = 3


class PostDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    extra_context = {'title': 'View Post'}

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_form.html'
    extra_context = {'button_name': 'create',
                     'title': 'Create Post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_form.html'
    extra_context = {'button_name': 'update',
                     'title': 'Update Post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog-homepage')
    template_name = 'blog/blog_confirm_delete.html'
    context_object_name = 'object'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False



class AboutTemplateView(TemplateView):
    extra_context = {'title': 'About Django project'}
    template_name = 'blog/about.html'


