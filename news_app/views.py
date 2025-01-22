from django.shortcuts import render
from django.views.generic import ListView

from news_app.models import Post

class HomePageView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    # queryset = Post.objects.filter(
    #     published_at_isnull=False, status="active"
    # ).order_by("-publised_at")[:5]

