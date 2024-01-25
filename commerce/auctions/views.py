from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Category, Comment, Listing, User


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(
        request,
        "auctions/index.html",
        {
            "listings": activeListings,
            "categories": allCategories,
        },
    )


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(
            request,
            "auctions/index.html",
            {
                "listings": activeListings,
                "categories": allCategories,
            },
        )


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST["newComment"]
    newComment = Comment(author=currentUser, listing=listingData, message=message)
    newComment.save()
    return HttpResponseRedirect(reverse("productlisting", args=(id,)))


def mylistings(request):
    currentUser = request.user
    listings = Listing.objects.filter(isActive=True, owner=currentUser)
    return render(
        request,
        "auctions/mylistings.html",
        {
            "listings": listings,
        },
    )


def productlisting(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    allComments = Comment.objects.filter(listing=listing)
    return render(
        request,
        "auctions/productlisting.html",
        {
            "listing": listing,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": allComments,
        },
    )


def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingwatchlist.all()
    return render(
        request,
        "auctions/watchlist.html",
        {
            "listings": listings,
        },
    )


def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("productlisting", args=(id,)))


def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("productlisting", args=(id,)))


def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(
            request,
            "auctions/create.html",
            {
                "categories": allCategories,
            },
        )
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.get(categoryName=category)
        bid = Bid(bid=float(price), user=currentUser)
        bid.save()
        newListing = Listing(
            title=title,
            description=description,
            imageURL=imageurl,
            price=bid,
            category=categoryData,
            owner=currentUser,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# would need a form that will post category, image, description, and price also title and time and date created
# Every user should see this and be able to make a bid on the item
# bid
# show number of people that have bid on it
# show if youre winning the bid
# show the owner of the item
# watchlist page
# shows items you have put a bid on
# create listings
# you should be able to add items
