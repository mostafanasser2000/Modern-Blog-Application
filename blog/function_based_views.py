from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q


### Function based views
def home(request):
    """get all posts in the blog"""
    posts = Post.published.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_list(request, tag_slug=None):
    """list all published posts by all users"""
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post_list.html", {"posts": posts, "tag": tag})


def post_detail(request, year: int, month: int, day: int, post):
    """retrieve a single post by year, month and day and post"""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=Post,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
    )
    comments = post.comments.filter(active=True)

    form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@login_required
def post_create(request):
    """Create a  single post"""
    if request.method == "GET":
        context = {"form": PostForm()}
        return render(request, "blog/post_form.html", context)

    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "The Post has been create successfully")
            return redirect("forum")
        else:
            messages.error(request, "Please correct the following errors")
            return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_update(request, post_id):
    """Update a single post"""

    post = get_object_or_404(Post, pk=post_id, author=request.user)
    url = reverse("post_detail", kwargs={"pk": post_id})

    if request.method == "GET":
        context = {"form": PostForm(instance=post), "post": post}
        return render(request, "blog/post_form.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully")
            return redirect(url)
        else:
            messages.error(request, "Pleases correct the following errors")
            return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_delete(request, post_id):
    """Delete a single Post"""

    post = get_object_or_404(Post, pk=post_id, author=request.user)
    context = {"post": post}
    if request.method == "GET":
        return render(request, "blog/post_confirm_delete.html", context)
    elif request.method == "POST":
        post.delete()
        messages.success(request, "The post has been deleted successfully")
        return redirect("forum")


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


def search(request):
    query = None
    results = Post.published.all()
    if query in request.GET:
        query = request.GET["query"]
        results = Post.published.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-published_at")
    return render(request, "blog/search.html", {"results": results, "query": query})


# advanced search
def post_search(request):
    query = None
    results = Post.published.all()
    if query in request.GET:
        query = request.GET["query"]
        search_vector = SearchVector("title", weight="A") + SearchVector(
            "content", weight="B"
        )
        search_query = SearchQuery(query)

        results = (
            Post.published.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(rank__gte="0.3")
            .order_by("-rank")
        )
    return render(request, "blog/search.html", {"results": results, "query": query})


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


def handle_tags(request, post):
    # set tags that are exist
    tags = request.POST.getlist("tags")
    tag_objects = Tag.objects.filter(slug__in=tags)
    post.tags.set(tag_objects)
    # set additional tags that not exist
    other_tags = request.POST.get("other_tags").split(",")
    # clean tag names from spaces
    other_tags_names = list(map(lambda x: x.strip(), other_tags))
    # filter empty tag names
    other_tags_names = list(filter(lambda x: x, other_tags_names))
    for tag_name in other_tags_names:
        new_tag, created = Tag.objects.get_or_create(name=tag_name)
        post.tags.add(new_tag)
