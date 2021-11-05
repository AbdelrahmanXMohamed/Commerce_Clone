from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Auctions,Category,Watchlist,Bids,Comments

def index(request):
    allAuction=Auctions.objects.all()
    try:
        user=request.user
        Watchlists=Watchlist.objects.filter(user=user)
        watched=[ i.auction.id for i in Watchlists]
        print(watched)
        
        return render(request, "auctions/index.html",{"allAuction":allAuction,"WatchLists":watched,"currentUser":user})
    except:
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
        user = request.user
        name=request.POST["name"]
        description=request.POST["description"]
        imageURL=request.POST["imageURL"]
        category=Category.objects.get(name=request.POST["category"])
        price=request.POST["price"]
        if category:
            Auctions.objects.create(user=user,name=name,description=description,imageURL=imageURL,category=category,start_price=price)
        return HttpResponseRedirect(reverse("index"))
    allCategory=Category.objects.all()
    return render(request,"auctions/create.html",{
        "allCategory":allCategory
    })

def details(request,product):
    if request.method=="GET":
        retrieveData=Auctions.objects.get(pk=product)
        try:
            bidsHistoty=Bids.objects.filter(auction=retrieveData).order_by("-price")
        except :
            bidsHistoty=[]
        try:
            comments=Comments.objects.filter(auction=retrieveData).order_by("-time")
        except:
            comments=[]

        return render(request,"auctions/details.html",{"data":retrieveData,"bidsHistoty":bidsHistoty,"comments":comments})

@login_required(login_url="/login")
def functions_WatchList(request,id):

    if request.method == "POST":
        user=request.user
        getAuction=Auctions.objects.get(id=id)
        try:
            data=Watchlist.objects.get(user=user,auction=getAuction)
            if data:
                data.delete()
                return HttpResponseRedirect(reverse("index"))
        except :
            Watchlist.objects.create(user=user,auction=getAuction)
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def WatchList_remove(request,id):
    if request.method == "POST":
        user=request.user
        getAuction=Auctions.objects.get(id=id)
        data=Watchlist.objects.get(user=user,auction=getAuction)
        data.delete()
        return HttpResponseRedirect(reverse("mywatchlist"))

@login_required(login_url="/login")
def WatchListPage(request):
    user=request.user
    mywatchinglist=Watchlist.objects.filter(user=user)
    return render(request,"auctions/watchlist.html",{"mywatchinglist":mywatchinglist})

def CategoryPage(request):
    AllCategory=Category.objects.all()
    return render(request,"auctions/category.html",{"AllCategory":AllCategory})
    
def Categoryitems(request,id):
    if request.method=="GET":
        category=Category.objects.get(pk=id)
        AllAuctionItem=Auctions.objects.filter(category=category)
        return render(request,"auctions/category_Items.html",{"AllAuctionItem":AllAuctionItem})

@login_required(login_url="/login")
def add_comment(request,id):
    if request.method == "POST":
        current_user=request.user
        auction=Auctions.objects.get(pk=id)
        comment=request.post["Comments"]
        Comments.objects.create(user=current_user,auction=auction,comment=comment)
        return HttpResponseRedirect(reverse("details ",args=[id]))


@login_required(login_url="/login")
def bid(request,id):
    if request.method == "POST":
        current_user=request.user
        auction=Auctions.objects.get(pk=id)
        price=request.post["price"]
        Bids.objects.create(winner=current_user,auction=auction,price=price)
        return HttpResponseRedirect(reverse("details ",args=[id]))