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
    path("posts/<int:pk>/<slug:slug>/update/", views.PostUpdate.as_view(), name="post_update"),
    path("posts/<int:pk>/<slug:slug>/delete/", views.PostDelete.as_view(), name="post_delete"),
    path("posts/<int:pk>/<slug:slug>/share/", views.post_share, name="post_share"),
    path("comment/", views.comment, name="post_comment"),
    path("tags/<slug:tag>/", views.PostList.as_view(), name="posts_by_tag"),
    path("search/", views.PostList.as_view(), name="post_search"),
    path("draft/", views.PostDraftedList.as_view(), name="post-draft"),
    path("like/", views.like, name="post_like"),
]
