from json.decoder import JSONDecodeError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import EmptyPage, Paginator

import json

from .models import User, Post

@ensure_csrf_cookie
def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def newpost(request): 
    # composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."})
    # get data and user. Also get body from data
    content = request.POST["body"]
    user = request.user
    # check post has data
    if len(content) < 1 or len(content) > 300:
        return JsonResponse({
            "error": "Posts must be between 1 and 300 characters"
        }, status=400)
    # post to database
    post = Post(
        author=user,
        body=content,
    )
    post.save()
    return JsonResponse({
        "message": "Post successful",
    }, status=201)


@login_required
def posts(request,username,page=1): 
    # check GET Request only
    if request.method != "GET":
        return JsonResponse({"error": "GET requests only."})
    
    if username == "following":
        posts = Post.objects.filter(author__in=request.user.following.all())
    elif username == "all":
        posts = Post.objects
    else:
        posts = Post.objects.filter(author__username=username)
    
    posts = posts.order_by('-timestamp').all()
    paginator = Paginator(posts, 10)
    maxPages = paginator.num_pages
    
    try: 
        postPage = paginator.page(page)
    except EmptyPage:
        postPage = paginator.page(1)
    pageOfPosts = postPage.object_list

    pageHasPrev = postPage.has_previous()
    pageHasNext = postPage.has_next()


    return JsonResponse({
        "posts" : [post.serialize(current_user=request.user) for post in pageOfPosts],
        "max_pages": [maxPages],
        "pageHasPrev": [pageHasPrev],
        "pageHasNext": [pageHasNext],
        },safe=False)


@login_required
def profile(request, username): 
    # get profile matching username
    user = User.objects.get(username = username)
    return JsonResponse({
        "username": user.username,
        "numOfFollowers": len(user.followers.all()),
        "numFollowing": len(user.following.all()),
        "following": user.followers.filter(pk=request.user.pk).exists() if request.user.is_authenticated else None})

@login_required
def getCurrentUser(request):
    if request.user.is_authenticated:
        username=request.user.username
        return JsonResponse(username, safe=False)

@login_required
def follow(request, username): 
    if request.method != "PUT":
        return JsonResponse({"error": "Request Method must be PUT"}, status=400)
    body = json.loads(request.body)
    if 'action' not in body:
        return JsonResponse({"error": "Request sent without an action call of 'follow' or 'unfollow'"}, status=400)
    action = json.loads(request.body)['action']
    profileUser = User.objects.get(username=username)
    if action == 'follow':
        request.user.following.add(profileUser)
    elif action == 'unfollow':
        request.user.following.remove(profileUser)

    return HttpResponse(status=204)

@login_required
def like(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Request Method must be PUT"}, status=400)
    body = json.loads(request.body)
    if 'action' not in body:
        return JsonResponse({"error": "Request sent without an action call of 'like' or 'unlike'"}, status=400)
    action = json.loads(request.body)['action']
    post = Post.objects.get(id=id)
    if action == 'like':
        request.user.liked.add(post)
    elif action == 'unlike':
        request.user.liked.remove(post)

    return HttpResponse(status=204)

@login_required
def editbody(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Request Method must be PUT"}, status=400)
    body = json.loads(request.body)
    if 'body' not in body:
        return JsonResponse({"error": "Request sent without content."}, status=400)
    bodyContent = json.loads(request.body)['body']
    post = Post.objects.get(id=id)
    if post.author.pk != request.user.pk:
        return JsonResponse({"error": "Only post owner can edit this post."}, status=400)
    
    post.body = bodyContent
    post.save()

    return HttpResponse(status=204)
