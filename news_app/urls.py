from django.urls import path

from news_app import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("about-us/", views.AboutPageView.as_view(), name="about-us"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),

]