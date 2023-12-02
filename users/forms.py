from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        label="",
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        label="",
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        label="",
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
        label="",
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
        label="",
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        label="",
    )
    password1 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        label="",
    )

    password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={"placeholder": "Password Confirmation"}),
        label="",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )
    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        new_email = self.cleaned_data["email"]

        # remove updated user from queryset we will use
        # to insure that the new email never been used
        # this will be helpful when user not update it's email
        if User.objects.exclude(id=self.instance.id).filter(email=new_email):
            raise forms.ValidationError("Email already in use.")

        return new_email


class ProfileUpdateForm(forms.ModelForm):
    """Form for update user profile"""

    avatar = forms.ImageField(
        label="",
        widget=forms.FileInput(attrs={"placeholder": "Avatar"}),
        required=False,
    )
    about = forms.CharField(
        label="", widget=forms.Textarea(attrs={"placeholder": "About"}), required=False
    )
    twitter_bio = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={"placeholder": "Twitter Profile"}),
        required=False,
    )
    facebook_bio = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={"placeholder": "Facebook Profile"}),
        required=False,
    )
    youtube_bio = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={"placeholder": "Youtube Channel"}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ["about", "avatar", "twitter_bio", "facebook_bio", "youtube_bio"]
