from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from datetime import timedelta
from django.utils import timezone

from newspaper.models import Category, Comment, Contact, Post, Tag

class HomePageView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    # queryset = Post.objects.filter(
    #     published_at_isnull=False, status="active"
    # ).order_by("-publised_at")[:5]

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
    

class ContactPageView():
    model = Contact
    template_name = "aznews/contacts.html"
    context_object_name = "contacts"


class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
     
class AboutPageView(ListView):
    model = Post
    template_name = "aznews/about.html"
    context_object_name = "posts"
    # queryset = Post.objects.filter(
    #     published_at_isnull=False, status="active"
    # ).order_by("-publised_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    

        context["trending_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-views_count")[:3]


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.views_count += 1
        obj.save()

        context["previous_post"] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__lt=obj.id
            )
            .order_by("-id")
            .first()
        )
        context["next_post"] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__gt=obj.id
            )
            .order_by("id")
            .first()
        )
        context["comments"] = Comment.objects.filter(post=obj).order_by("-created_at")
        return context

    def post(self, request, *args, **kwargs):
        """Handle comment form submission."""
        obj = self.get_object()  
        comment_text = request.POST.get("comment")
        name = request.POST.get("name")
        email = request.POST.get("email")

        if comment_text and name and email:
            Comment.objects.create(
                post=obj,
                comment=comment_text,
                name=name,
                email=email
            )
            return redirect("post-detail", pk=obj.pk)
        context = self.get_context_data()
        context["error"] = "Please fill out all required fields."
        return self.render_to_response(context)