from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Post, Comment
from taggit.forms import TagWidget, TagField


class PostForm(ModelForm):
    title = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Post Title"})
    )
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={"placeholder": "Post Content"})
    )
    # extra_tags = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"placeholder": "Enter additional tags comma separated tag1, tag2..."}
    #     ),
    #     required=False,
    # )

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
