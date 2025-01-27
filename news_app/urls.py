from django.urls import path

from news_app import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path('contact.html', views.ContactView.as_view(), name='contact'),
    path ("post-list/", views.PostListView.as_view(), name="post-list"),
]