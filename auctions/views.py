from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Listing, WatchList, Bid, Comment, Category
from .forms import ListingForm, BidForm, CommentForm
from django.contrib import messages
from django.db.models import Max, FloatField, F
from collections import defaultdict 


def view_listing(request):
    listings = Listing.objects.all()
    for listing in listings:
        bids = Bid.objects.filter(listing=listing)
        if bids.exists():
            max_bid = Bid.objects.filter(listing=listing).aggregate(finalbid=Max('bidprice'))            
            bid = Bid.objects.get(listing=listing, bidprice=max_bid['finalbid']) 
            myslug = bid.listing.slug
            for bidlisting in listings:
                if bidlisting.slug == myslug:
                    newlisting = Listing.objects.filter(slug=myslug)
                    updated_listing=newlisting.update(price=max_bid['finalbid'])                  
    context ={'listings': listings}
    return render(request, 'auctions/view_listing.html', context)


def active_listing(request):
    listings = Listing.objects.filter(status='ACTIVE')
    context = {'listings': listings}
    return render(request, 'auctions/active_listing.html', context ={'listings':listings})


def view_by_category(request, slug):    
    cat = get_object_or_404(Category, slug=slug)
    listings = Listing.objects.filter(category__slug=cat.slug)  
    context = {'listings':listings}
    return render(request, 'auctions/view_by_category.html', context)


def category_view(request):    
    categ = Category.objects.all()

    context = {'categ':categ}
    return render(request, 'auctions/category_view.html', context)


def close_listing(request, slug):
    listing = Listing.objects.get(slug=slug)
    bid_list = Bid.objects.filter(listing=listing)
    if bid_list.exists()== False:
        messages.info(request, 'The listing has not been bidden. You can delete the listing if you want to close it.')    
        return HttpResponseRedirect(reverse('active_listing'))
    else:  
        max_bid = Bid.objects.filter(listing=listing).aggregate(finalbid=Max('bidprice'))
        winning = Bid.objects.filter(bidprice=max_bid['finalbid'])[0]
        form = ListingForm(initial={
            'title':listing.title, 
            'username':winning.username,
            'description':listing.description,
            'price':winning.bidprice,
            'slug':listing.slug,
            'status':'CLOSE'
            })
        
        if request.method == 'POST':
            form = ListingForm(request.POST, instance=listing)
            if form.is_valid(): 
                bid_form = Bid.objects.filter(listing=listing, username=winning.username)
                update_bid = bid_form.update(bidstatus='WON', completed=True)
                bid_lost = Bid.objects.filter(listing=listing).exclude(username=winning.username)
                update_lost = bid_lost.update(bidstatus='LOST', completed=True)
                form.save()
                return HttpResponseRedirect(reverse("index"))
        context = {'form': form}
        return render(request, 'auctions/close_listing.html', context)


def mylisting(request, pk):
    username = User.objects.get(id=pk)
    dataset = username.listing_set.all()
    context ={'dataset': dataset, 'username': username} 
    return render(request, 'auctions/mylisting.html', context)


def delete_bidding(request, slug):    
    listing = get_object_or_404(Listing, slug=slug)
    bid_listing = Bid.objects.get(listing__slug=listing.slug, username=request.user)
    bid_listing.delete()
    return HttpResponseRedirect(reverse('active_listing'))


def bidding(request, slug):
    listing = Listing.objects.get(slug=slug)
    if listing.username != request.user:        
        if listing.status == 'ACTIVE':        
            form = BidForm(initial={'listing':listing, 'username':request.user, 'Complete': False})
            if Bid.objects.filter(listing=listing).exists():        
                if Bid.objects.filter(listing=listing, username=request.user).exists(): 
                    messages.info(request, 'Your bid was already placed')    
                    return HttpResponseRedirect(reverse('active_listing'))          
                elif request.method == 'POST':
                    form = BidForm(request.POST)
                    if form.is_valid():
                        input_bid = float(request.POST.get('bidprice'))
                        maxbid = Bid.objects.filter(listing=listing).aggregate(max_bid=Max('bidprice'))
                        if input_bid <= maxbid['max_bid']:
                            messages.info(request, 'Your bid must be greater than the other people price')    
                            return HttpResponseRedirect(reverse('active_listing'))
                        else:
                            bid = Bid.objects.create(listing=listing, username=request.user, bidprice=input_bid, bidstatus='PENDING')   
                            bid.save()
                        return HttpResponseRedirect(reverse('active_listing'))
                else: 
                    context = {'form': form}
                    return render(request, 'auctions/bidding_form.html', context)
            elif request.method == 'POST':
                    form = BidForm(request.POST)
                    if form.is_valid():
                        bidprice = float(request.POST.get('bidprice'))
                        current_price = float(listing.get_bidprice())
                        if bidprice < current_price:
                            messages.info(request, 'Your bid must be greater than or equal to the starting price')    
                            return HttpResponseRedirect(reverse('active_listing'))
                        else:
                            bid = Bid.objects.create(listing=listing, username=request.user, bidprice=bidprice, bidstatus='PENDING')   
                            bid.save()
                        return HttpResponseRedirect(reverse('active_listing'))
            else:
                context = {'form': form}
                return render(request, 'auctions/bidding_form.html', context)
        else:
            messages.info(request, 'The listing was closed')    
            return HttpResponseRedirect(reverse('active_listing')) 
    else:
        messages.info(request, 'You cannot bid your listing')    
        return HttpResponseRedirect(reverse('active_listing'))   
    

def listing_comment(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    form = CommentForm(initial={'listing':listing, 'username':request.user})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(listing=listing, username=request.user, content=content)
            comment.save()
            return HttpResponseRedirect(reverse('active_listing'))

    else:
        context = {'form': form}
    return render(request, 'auctions/listing_comment.html', context)


def bids_view(request, pk):
    username = User.objects.get(id=pk)
    dataset = username.bid_set.all()
    context ={'dataset': dataset, 'username': username} 
    return render(request, 'auctions/bids_view.html', context)


def watchlist(request, pk):
    username = User.objects.get(id=pk)
    dataset = username.watchlist_set.all()
    context ={'dataset': dataset, 'username': username} 
    return render(request, 'auctions/watchlist.html', context)


def remove_listing_from_watchlist(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    watch_listing = WatchList.objects.filter(
        listing=listing,
        username=request.user,
        active=False
    )
    watch_listing.delete()
    return HttpResponseRedirect(reverse('index'))


def add_to_watchlist(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    watch_listing = WatchList.objects.create(
        listing = listing,
        username = request.user,
        active = False
    )
    if watch_listing in WatchList.objects.all():
        pass
    else:
        watch_listing.save()
    return HttpResponseRedirect(reverse('active_listing'))


def create_listing(request):          
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm(initial={'username':request.user})
        context = {'form': form}
    return render(request, 'auctions/create_listing.html', context)


def delete_listing(request, slug):    
    listing = Listing.objects.get(slug=slug, username=request.user)
    listing.delete()
    return HttpResponseRedirect(reverse('active_listing'))


def detail_listing(request, slug):
    listing = Listing.objects.get(slug=slug)
    comments = Comment.objects.filter(listing=listing)
    context ={'listing':listing, 'comments': comments}     
    return render(request, 'auctions/detail_listing.html', context)


def index(request):
    return render(request, "auctions/index.html")


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
