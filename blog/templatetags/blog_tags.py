from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from blog.models import Tag


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.all().order_by("-published_at")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag(name="top_rated_post")
def top_rated_posts(count=5):
    return Post.published.annotate(total_likes=Count('likes')).order_by("-total_likes")[:count]


@register.simple_tag
def get_tags():
    tags = Tag.objects.all()
    return tags
