from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    activeListing = Listing.objects.filter(isON=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : activeListing,
        "categories" :  allCategories,
    })

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    theowner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allcomments": allcomments,
        "theowner": theowner
    })

def watchlist(request):
    currentUser = request.user
    listings = currentUser.Watchlistitems.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def addcomment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newcomment']

    newcomment = Comment(
        author=currentUser,
        listing=listingData,
        message=message,
    )
    newcomment.save() 
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def seeCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(NameCategory=categoryFromForm)
        activeListing = Listing.objects.filter(isON=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListing,
            "categories":  allCategories,
        })

def CreateListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        urlimage = request.POST["urlimage"]
        price = request.POST["price"]
        category = request.POST["category"]
        actualUser = request.user

        #Data Collector from specific categ.
        categCollector = Category.objects.get(NameCategory=category)
        bid = Bid(bid=int(price), user=actualUser)
        bid.save()
        newListing = Listing(
            title=title,
            description=description,
            bildUrl=urlimage,
            price=bid,
            category=categCollector,
            owner=actualUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))

def addbid(request,id):
    newbid = request.POST['newbid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    theowner = request.user.username == listingData.owner.username
    if int(newbid) > listingData.price.bid:
        updatebid = Bid(user=request.user, bid=int(newbid))
        updatebid.save()
        listingData.price = updatebid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid updated",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "allcomments": allcomments,
            "theowner": theowner,

        })
    else:
        return render(request, "auctions/listing.html", {
            "listing" : listingData,
            "message": "Bid not updated, current price is higher or equal than your bid",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "allcomments": allcomments,
            "theowner": theowner,

        })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isON = False
    listingData.save()
    theowner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allcomments": allcomments,
        "theowner": theowner,
        "update": True,
        "message": "Your acution is closed."
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
