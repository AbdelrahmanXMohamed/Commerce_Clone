from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Auctions,Category,Watchlist,Bids,Comments
from .forms import LoginForm,RegisterForm
from django.db.models import Max
def index(request):
    allAuction=Auctions.objects.all()
    try:
        user=request.user
        Watchlists=Watchlist.objects.filter(user=user)
        watched=[ i.auction.id for i in Watchlists]        

        return render(request, "auctions/index.html",{"allAuction":allAuction,"WatchLists":watched,"currentUser":user})
    except:
        return render(request, "auctions/index.html",{"allAuction":allAuction})

def login_view(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        # Attempt to sign user in
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])      
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "form":form
            })
    else:
        return render(request, "auctions/login.html",{"form":LoginForm()})


def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ensure password matches confirmation
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                return render(request, "auctions/register.html", {
                    "message": "Passwords must match.",
                    "form":form
                })
            email = form.cleaned_data["email"]
            username=form.cleaned_data["username"]
          # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "auctions/register.html", {
                    "message": "Username already taken.",
                    "form":form
                })
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{"form":RegisterForm()})


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
            bidsHistoty=Bids.objects.filter(auction=retrieveData).order_by("-price")[:10]
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
        try:
            user=request.user
            Watchlists=Watchlist.objects.filter(user=user)
            watched=[ i.auction.id for i in Watchlists]        
            return render(request, "auctions/category_Items.html",
            {"allAuction":AllAuctionItem,
            "WatchLists":watched,
            "currentUser":user,
            "category":category})
        except:
            return render(request, "auctions/category_Items.html",{"allAuction":AllAuctionItem,"category":category})

@login_required(login_url="/login")
def add_comment(request,id):
    if request.method == "POST":
        current_user=request.user
        auction=Auctions.objects.get(pk=id)
        comment=request.POST["Comments"]
        Comments.objects.create(user=current_user,auction=auction,comments=comment)
        return HttpResponseRedirect(reverse("details",args=[id]))


@login_required(login_url="/login")
def bid(request,id):
    if request.method == "POST":
        current_user=request.user
        auction=Auctions.objects.get(pk=id)
        price=request.POST["price"]
        Bids.objects.create(winner=current_user,auction=auction,price=price)
        currentAuction=Auctions.objects.get(pk=id)
        currentAuction.current_price=price
        if not currentAuction.have_bids:
            currentAuction.have_bids=True
        currentAuction.save()
        
        return HttpResponseRedirect(reverse("details",args=[id]))


@login_required(login_url="/login")
def close_bid(request,id):
    if request.method == "POST":
        currentAuction=Auctions.objects.get(pk=id)
        currentAuction.state=False
        currentAuction.save()
        return HttpResponseRedirect(reverse("details",args=[id]))