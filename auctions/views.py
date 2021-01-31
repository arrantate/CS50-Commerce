from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Category, WishList
from django.db.models import Max
from django.contrib import messages


def index(request):
    listings = Listing.objects.filter(is_sold=False)

    # gets highest bids and formats them to either NoneType or str with 2 decimal places
    highest_bids = [listing.bids.aggregate(Max('amount')).get('amount__max') for listing in listings]
    highest_bids = ["{:.2f}".format(bid) if bid is not None else bid for bid in highest_bids]

    context = {
        'title': 'COMMERCE',
        'listings': zip(listings, highest_bids),
        'categories': Category.objects.all(),
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    context = {
        'title': 'Login',
        'categories': Category.objects.all(),
    }

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
            messages.warning(request, 'Invalid username and/or password.')
            return render(request, "auctions/login.html", context)
    else:
        return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    context = {
        'title': 'Register',
        'categories': Category.objects.all(),
    }

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, 'Passwords must match.')
            return render(request, "auctions/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, 'Username already taken.')
            return render(request, "auctions/register.html", context)
        login(request, user)
        messages.success(request, 'User Created')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", context)


def listing(request, listing_pk):
    listing = Listing.objects.get(pk=listing_pk)
    
    context = {
        'title': listing.title,
        'listing': listing,
        'categories': Category.objects.all(),
    }

    return render(request, "auctions/listing.html", context)


def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('index')

    print(user.wish_list.all())

    context = {
        'title': f"{user.username}'s Wishlist",
        'wishlist': user.wish_list.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'auctions/wishlist.html', context)


def wishlist_add(request, listing_pk):
    listing = Listing.objects.get(pk=listing_pk)

    wishlist_entry = WishList(user=request.user, item=listing)
    wishlist_entry.save()

    messages.success(request, f'{listing.title} added to wishlist.')
    return redirect('listing', listing_pk=listing_pk)


def category(request, category_name):
    category = Category.objects.get(name=category_name)
    listings = Listing.objects.filter(is_sold=False, category=category)

    # gets highest bids and formats them to either NoneType or str with 2 decimal places
    highest_bids = [listing.bids.aggregate(Max('amount')).get('amount__max') for listing in listings]
    highest_bids = ["{:.2f}".format(bid) if bid is not None else bid for bid in highest_bids]

    context = {
        'title': 'COMMERCE',
        'listings': zip(listings, highest_bids),
        'categories': Category.objects.all(),
    }
    return render(request, "auctions/index.html", context)