from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm, RegisterForm, CommentForm, RateForm
from .models import Post, Rate


def index_view(request):
    rate_form = RateForm()
    posts = Post.objects.prefetch_related("comments", "rates").all()
    context = {"posts": posts, "rate_form": rate_form}
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


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = PostForm(instance=post)
    return render(request, "home/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("index")
    return HttpResponseForbidden("Nie można usunąć posta metodą GET")


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            else:
                comment.author = None
                comment.author_name = form.cleaned_data["author_name"]
            comment.save()
            return redirect("index")
    else:
        form = CommentForm()
    return render(
        request,
        "home/add_comment.html",
        {"form": form, "post": post},
    )


def add_rate(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.post = post
            rate.user = request.user
            existing_rate = Rate.objects.filter(
                post=post,
                user=rate.user,
            ).first()
            if existing_rate:
                existing_rate.score = rate.score
                existing_rate.save()
            else:
                rate.save()

            return redirect("index")
    else:
        form = RateForm()

    return render(request, "home/add_rate.html", {"form": form, "post": post})
