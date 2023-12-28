from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("posts/", views.PostList.as_view(), name="post_list"),
    path("posts/<int:pk>/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path(
        "posts/author/<str:author_name>/",
        views.PostList.as_view(),
        name="posts_by_author",
    ),
    path("posts/create/", views.PostCreate.as_view(), name="post_create"),
    path("posts/<int:pk>/update/", views.PostUpdate.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", views.PostDelete.as_view(), name="post_delete"),
    path("posts/<int:post_id>/share/", views.post_share, name="post_share"),
    path("posts/<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("tags/<slug:tag>/", views.PostList.as_view(), name="posts_by_tag"),
    path("posts/search/", views.PostList.as_view(), name="post_search"),
    path("posts/draft/", views.PostDraftedList.as_view(), name="post-draft"),
    path("post/<int:pk>/like/", views.like_post, name="post_like"),
    path("post/<int:pk>/dislike/", views.dislike_post, name="post_dislike"),
]
