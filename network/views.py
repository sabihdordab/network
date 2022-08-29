from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator


def index(request):
    user = request.user
    posts = Post.objects.all().order_by('id').reverse() 
    # page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    if user.is_authenticated:
        return render(request, "network/index.html" , {
            'page_object' : page_object ,
            'user_likes_post' : [ like.post for like in Like.objects.filter(user=user).all() ]
        })
    else:
        return render(request, "network/index.html" , {
            'page_object' : page_object
        })



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

def create_post(request):
    if request.method == "POST":
        post = Post(user = request.user ,title = request.POST['post-title'] , content = request.POST['post-content'] , date = datetime.datetime.now())
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse(status=405)

@csrf_exempt
def edit_post(request,id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        title = json.loads(request.body).get('editedTitle')
        content = json.loads(request.body).get('editedContent')
        post.title = title
        post.content = content
        post.save()
        return JsonResponse({"message": "success", "content": content , "title" : title })
    else:
        return HttpResponse(status=405)


@csrf_exempt
def like_post(request,id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'message':'failed'})

        post=Post.objects.get(id=id)
        is_liked = False

        try:
            #unlike
            like = Like.objects.get(user=request.user,post=post)
            like.delete()
        except:
            #like
           like = Like(user=request.user,post=post)
           like.save()
           is_liked = True
           

        return JsonResponse({'message':'success', 'likes':len(post.likes.all()), 'is_liked': is_liked })

    return HttpResponse(status=405)

def user_profile(request,username):
    try:
        user = User.objects.get(username=username)
    except:
        #user does'nt exist
        return HttpResponse(status=404)

    try:
        following = Following.objects.get(user=request.user,user_followed=user)
        is_followed = True
    except:
        is_followed = False
        
    posts = user.posts.all().order_by('id').reverse()
    # page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'network/user_profile.html',{
            'page_object' : page_object ,
            'profile_user' : user ,
            'is_followed' : is_followed ,
            'user_likes_post' : [ like.post for like in Like.objects.filter(user=request.user).all() ]
        })
    else:
        return render(request, 'network/user_profile.html',{
            'page_object' : page_object ,
            'profile_user' : user
        })

def follow_unfollow(request,username):

    user = request.user
    if user.id is None :
        return HttpResponse(status=405)

    
    try:
        user_followed = User.objects.get(username=username)
    except:
        #user does'nt exist
        return HttpResponse(status=404)

    if user != user_followed :
        try:
            #unFollow
            following = Following.objects.get(user=request.user,user_followed=user_followed)
            following.delete()
        except:
            #follow
            following = Following(user=request.user,user_followed=user_followed)
            following.save()

    return HttpResponseRedirect(reverse("profile",args=(username,)))
    

def following(request): 
    user = request.user 
    if not user.is_authenticated:
        return HttpResponse(status=405)

    user = User.objects.get(id=user.id)
    user_following = [following.user_followed for following in user.following.all()]
    posts = Post.objects.filter(user__in=user_following).order_by('id').reverse()

    #page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_object' : page_object,
        'user_likes_post' : [ like.post for like in Like.objects.filter(user=user).all() ]
    })

    

    
    
