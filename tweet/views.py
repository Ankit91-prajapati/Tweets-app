

# Create your views here.
from collections import UserDict
from django.shortcuts import render
from django.contrib import messages
from .models import Tweet
from .forms import TweetForm ,UserRegisterationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login



# Create your views here.



def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweet_list.html", {"tweets": tweets})


@login_required(login_url="/register/")
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm()
    return render(request, "tweet_form.html", {"form": form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)
    return render(request, "tweet_form.html", {"form": form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("/account/login")
    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})




def register(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect("/account/login")
    else:
        form = UserRegisterationForm()
    
    return render(request, "registration/register.html", {"form": form})

def search(request):
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(text__icontains=query)
    else:
        tweets = Tweet.objects.all()
    return render(request, 'search.html', {'tweets': tweets})

