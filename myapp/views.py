from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import PostForm, RegisterForm
from .models import Post


def index_view(request):
    posts = Post.objects.prefetch_related("comments", "rates").all()
    context = {"posts": posts}
    return render(request, "home/index.html", context)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next")
            if not next_url:
                next_url = request.GET.get("next")
            if not next_url:
                next_url = "index"
            return redirect(next_url)
        else:
            error_message = "Nieprawidłowe dane!"
    return render(request, "accounts/login.html", {"error": error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")
    else:
        return redirect("index")


@login_required
def home_view(request):
    return render(request, "home/index.html")


class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "home/index.html")


@login_required
def add_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()

    return render(request, "home/add_post.html", {"form": form})
