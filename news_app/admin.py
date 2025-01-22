from django.contrib import admin

from news_app.models import Post, Tag, Category

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)