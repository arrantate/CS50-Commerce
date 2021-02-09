from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Category, WatchList, Bid, Comment
from .forms import NewListingForm
from .decorators import user_is_authenticated
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


@user_is_authenticated
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
    user = request.user

    listing = Listing.objects.get(pk=listing_pk)
    if user.is_authenticated:
        listing_in_watch_list = WatchList.objects.filter(user=user, item=listing).exists()
    else:
        # This is to be assigned in the case that there is no user logged in
        listing_in_watch_list = None

    context = {
        'title': listing.title,
        'listing': listing,
        'listing_in_watch_list': listing_in_watch_list,
        'categories': Category.objects.all(),
        'comments': Comment.objects.filter(listing=listing).order_by('-date_created'),
    }

    if request.method == "POST":
        comment = request.POST.get('comment')
        new_comment = Comment(comment=comment, user=user, listing=listing)
        new_comment.save()

    return render(request, "auctions/listing.html", context)


@user_is_authenticated
def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('index')

    print(user.watch_list.all())

    context = {
        'title': f"{user.username}'s Watchlist",
        'watchlist': user.watch_list.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'auctions/watchlist.html', context)


@user_is_authenticated
def watchlist_add(request, listing_pk):
    user = request.user
    listing = Listing.objects.get(pk=listing_pk)

    if WatchList.objects.filter(user=user, item=listing).exists() == False:
        watchlist_entry = WatchList(user=user, item=listing)
        watchlist_entry.save()
        messages.success(request, f'{listing.title} added to watchlist.')
        
    return redirect('listing', listing_pk=listing_pk)


@user_is_authenticated
def watchlist_remove(request, listing_pk):
    user = request.user
    listing = Listing.objects.get(pk=listing_pk)

    if WatchList.objects.filter(user=user, item=listing).exists():
        WatchList.objects.filter(user=user, item=listing).delete()
        messages.success(request, f'{listing.title} removed from watchlist.')
        
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


@user_is_authenticated
def new_listing(request):
    user = request.user

    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['category'])
            category = Category.objects.get(name=form.cleaned_data['category'])
            new_listing = Listing(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                starting_bid = form.cleaned_data['starting_bid'],
                image = form.cleaned_data['image_url'],
                category = category,
                seller = user,
            )
            new_listing.save()

            return redirect('listing', listing_pk=new_listing.pk)

    else:
        form = NewListingForm()

    context = {
        'title': 'New Listing',
        'categories': Category.objects.all(),
        'form': form,
    }
    return render(request, "auctions/new_listing.html", context)