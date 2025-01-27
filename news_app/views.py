from django.shortcuts import render
from django.views.generic import ListView
from news_app.models import Category, Post, Tag
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm
class HomePageView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["trending_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-views_count")[:3]

        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )
        context["featured_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at", "-views_count")[1:4]

        from datetime import timedelta
        from django.utils import timezone

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:7]

        context["recent_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:7]

        context['tags'] = Tag.objects.all()[:10]
        context['categories'] = Category.objects.all()[:3]
        return context

class ContactView(FormView):
    template_name = 'aznews/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact') 
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)

class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
