from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    title = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Post Title"})
    )
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={"placeholder": "Post Content"})
    )

    class Meta:
        model = Post
        fields = ["title", "content", "status", "tags"]


class EmailPostForm(forms.Form):
    title = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Title"}), max_length=25
    )
    to = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    comments = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "message"}),
    )


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label="", widget=forms.Textarea(attrs=({"placeholder": "Write your comment"}))
    )

    class Meta:
        model = Comment
        fields = ["body"]
