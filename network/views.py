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
from django.contrib.auth.decorators import login_required
from .forms import *

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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username,password=password)
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            except:
                pass
            
             
        return render(request,'network/login.html',{
                'form' : form,
                'message' : "invalid username / password ?"
            })

    else: #get method?
        return render(request,'network/login.html',{
            'form' : LoginForm
        })



@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm']:
                try:
                    user = form.save()
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                except:
                    return render(request,'network/register.html',{
                        'form' : form,
                        'message' : "idk!?"
                    })
            else: #password != confirm
                return render(request, "network/register.html", {
                "message": "Password and Confirm must match.",
                "form" : form
            })
        else: #not valid form
            return render(request,'network/register.html',{
                        'form' : form,
                        'message' : "username already taken or invalid inputs"
                    })

    else: #get method?
        return render(request,'network/register.html',{
            'form' : RegisterForm
        })


def create_post(request):
    if request.method == "POST":
        post = Post(user = request.user ,title = request.POST['post-title'] , content = request.POST['post-content'] , date = datetime.datetime.now())
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url="login")
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
@login_required(login_url="login")
def like_post(request,id):
    if request.method == 'POST':
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

@login_required(login_url="login")
def follow_unfollow(request,username):

    user = request.user
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
    
@login_required(login_url="login")
def following(request): 
    user = request.user
    posts = [following.get_user_followed_posts() for following in user.following.all()]

    #page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_object' : page_object,
        'user_likes_post' : [ like.post for like in Like.objects.filter(user=user).all() ]
    })

    

    
    
