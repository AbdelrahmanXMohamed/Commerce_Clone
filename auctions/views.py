from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Auctions,Category


def index(request):
    allAuction=Auctions.objects.all()
    return render(request, "auctions/index.html",{"allAuction":allAuction})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method=="POST":
        print(request.user)
        user = request.user
        name=request.POST["name"]
        description=request.POST["description"]
        imageURL=request.POST["imageURL"]
        category=Category.objects.get(name=request.POST["category"])
        price=request.POST["price"]
        if category:
            Auctions.objects.create(user=user,name=name,description=description,imageURL=imageURL,category=category,price=price)
        return HttpResponseRedirect(reverse("index"))
    allCategory=Category.objects.all()
    return render(request,"auctions/create.html",{
        "allCategory":allCategory
    })

def details(request,product):
    if request.method=="GET":
        retrieveData=Auctions.objects.get(pk=product)
        print(retrieveData)
        return render(request,"auctions/details.html",{"data":retrieveData})

@login_required
def add_WatchList(request):
    pass


@login_required
def elements_from_watchList(request):
    pass

@login_required
def add_comment(request):
    pass

def bid(request):
    pass