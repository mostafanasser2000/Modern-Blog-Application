from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tag
from django.db.models import Count
from django.db.models import Q


@login_required
def post_share(request, post_id):
    """Share a post using email"""
    post = get_object_or_404(Post, pk=post_id)
    sent = False
    form = None
    user_email = request.user.email

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            valid_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{valid_data['title']} recommends you read f{post.title}"
            message = f"Read {post.title} at {post_url}\n\n{valid_data['title']}'s comments: {valid_data['comments']}"
            send_mail(subject, message, user_email, [valid_data["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post_share.html", {"form": form, "sent": sent, "post": post}
    )


@login_required
@require_POST
def post_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect(reverse_lazy("blog:post_detail", kwargs={"pk": post.id}))


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    return redirect("blog:post_detail", pk=post.pk)


@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post)
    like.delete()
    return redirect("blog:post_detail", pk=post.pk)


def get_extra_tags(request, post):
    extra_tags = []
    other_tags = request.POST.get("other_tags").split(",")
    # clean tag names from spaces
    other_tags_names = [tag.strip() for tag in other_tags if tag.strip()]
    for tag_name in other_tags_names:
        post.tags.add(Tag.objects.create(name=tag_name))


class PostList(ListView):
    """List all posts in the blog app"""

    context_object_name = "posts"
    paginate_by = 3
    queryset = Post.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        author_name = self.kwargs.get("author_name", "")
        query = self.request.GET.get("query", "")
        tag = self.kwargs.get("tag")

        if author_name:
            qs = qs.filter(author__username=author_name)
        if tag:
            tag = Tag.objects.get(slug=tag)
            qs = qs.filter(tags__in=[tag])
        if query:
            qs = qs.filter(Q(title__icontains=query) or Q(content__icontains=query))
        return qs


class PostDraftedList(LoginRequiredMixin, ListView):
    """List all drafted posts for a user in the blog app"""

    context_object_name = "posts"
    template_name = "post_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.drafted.filter(author=self.request.user)


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # get all related posts
        post_tags_ids = post.tags.values_list("id", flat=True)
        related_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
        related_posts = related_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-published_at"
        )[:4]
        # get all comments on that post
        comments = post.comments.filter(active=True)
        is_liked = False
        if self.request.user.is_authenticated:
            is_liked = post.likes.filter(user=self.request.user).exists()
        # form for users to comment
        form = CommentForm()
        context["comments"] = comments
        context["form"] = form
        context["related_posts"] = related_posts
        context["liked_post"] = is_liked
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    """Create a single post"""

    model = Post
    success_url = reverse_lazy("blog:post_list")
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        get_extra_tags(self.request, post)
        messages.success(self.request, "Post was created successfully")
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    """Update a specific post"""

    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        get_extra_tags(self.request, post)
        messages.info(self.request, "Post was updated successfully")
        return super(PostUpdate, self).form_valid(form)

    def get_queryset(self):
        base_qs = super(PostUpdate, self).get_queryset()
        return base_qs.filter(author=self.request.user)

    def get_permission_denied_message(self) -> str:
        return "Permission denied"


class PostDelete(LoginRequiredMixin, DeleteView):
    """Delete a specific post"""

    model = Post
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        messages.success(self.request, "Post was deleted successfully")
        return super(PostDelete, self).form_valid(form)

    # filter query set to ensure that only author of the post can delete it
    def get_queryset(self):
        base_qs = super(PostDelete, self).get_queryset()
        return base_qs.filter(author=self.request.user)
