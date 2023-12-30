from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def sign_in(request):
    """Loin existing user"""
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("blog:home")

        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                messages.success(
                    request,
                    f"Welcome back, {user.first_name}  {user.last_name}!",
                )
                return redirect("blog:home")

        messages.error(request, f"Invalid username or password")
        return render(request, "users/login.html", {"form": form})


def sign_up(request):
    """Register new users"""
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            messages.success(request, "You have been singed up successfully!")
            login(request, user)
            return redirect("blog:home")

        else:
            return render(request, "users/register.html", {"form": form})


# FIX: here I can't use my LoginForm with the Login View
class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"
    form_class = (
        LoginForm()
    )  # error is here as Login View has its own login form class

    def get_success_url(self) -> str:
        return reverse_lazy("blog:home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(FormView):
    """Register new users"""

    template_name = "users/register.html"
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Your account has been created successfully")
        return super(RegisterView, self).form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }

        return render(request, "users/profile_form.html", context=context)

    def post(self, request):
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect("blog:home")

        else:
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
            }

            messages.error(request, "Error updating your profile")
            return render(request, "users/profile_form.html", context=context)


@login_required()
def profile_view(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, "users/profile.html", {"profile": profile})


@require_POST
@login_required()
def follow(request):
    user_id, action = request.POST.get("id"), request.POST.get("action")
    print(user_id, action)
    if user_id and action:
        try:
            follower_profile = Profile.objects.get(user=request.user)
            following_profile = Profile.objects.get(user__id=user_id)
            if action == "follow":
                follower_profile.following.add(following_profile)
            else:
                follower_profile.following.remove(following_profile)

            return JsonResponse({"status": "ok"})

        except Profile.DoesNotExist:
            pass

        return JsonResponse({"status": "error"})



