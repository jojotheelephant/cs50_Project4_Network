from django.contrib import admin
from .models import User, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'body', 'timestamp')

admin.site.register(Post, PostAdmin)
admin.site.register(User)

