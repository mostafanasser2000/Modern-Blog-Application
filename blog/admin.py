from django.contrib import admin
from .models import Post, Comment, Tag

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_at", "status"]
    list_filter = ["status", "created_at", "published_at", "status"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "published_at"
    ordering = ["status", "published_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at", "active"]
    list_filter = ["active", "created_at", "updated_at"]
    search_fields = ["user", "body"]


admin.site.register(Tag)
