
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html",{
        "listing": Auction.objects.all()
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

@login_required
def newListing(request):
    context = {}
    context['form'] = auctionForm()

    if request.method == 'POST':
        form = auctionForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
        
            return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/newListing.html", context)


def listing(request, listing_id):
    auction = Auction.objects.get(pk = listing_id)

    try:
        if auction.closed == True:
            
            highest_bid = Bids.objects.filter(auction=auction).order_by('-bid_price').first()
            highest_bidder = User.objects.get(id = highest_bid.user_id)

            context = {
                        "message": "Auction is now closed",
                        'Post': auction,
                        'highest_bid': 'Bought for: £' + str(highest_bid.bid_price),
                        'highest_bidder': 'Won by ' + str(highest_bidder),
                        
                        
                    }
            return render(request, "auctions/listing.html", context)

    except Exception:
        return render(request, "auctions/listing.html", {
        'Post': auction,
        'bid_form': BidForm(),
        'message': 'Author Closed Bidding with No Bidders'
    })

    comments = Comments.objects.filter(auction = auction)
    

    return render(request, "auctions/listing.html", {
        'Post': auction,
        'bid_form': BidForm(),
        'comment_form': commentsForm(),
        'comments': comments,
    })

@login_required
def watchlist(request):

    user = request.user 
    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def watchlist_add(request):
    if request.method=="POST":
        listing = Auction.objects.get(pk=request.POST["listingID"])

        try:
            user = request.user
            user = User.objects.get(pk=int(user.id))
            user.watchlist.add(listing)

        except Exception:
            return HttpResponseRedirect("/" + listing)

        return HttpResponseRedirect(reverse("watchlist"))

    
    return render(request, "auctions/watchlist.html")

@login_required
def watchlist_remove(request):
    if request.method=="POST":
        listing = Auction.objects.get(pk=request.POST["listingID"])

        try:
            user = request.user
            user = User.objects.get(pk=int(user.id))
            user.watchlist.remove(listing)

        except Exception:
            return HttpResponseRedirect(reverse("watchlist"))

        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html")


@login_required
def bid(request):

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_price = float(form.cleaned_data["bid_price"])
            auction_id = request.POST.get("auction_id")
           
            auction = Auction.objects.get(pk=auction_id)
            user = User.objects.get(id=request.user.id)

            
            if auction.user == user:
                context = {
                    "message": "Seller Cannot Bid",
                    'Post': auction,
                    'bid_form': BidForm()
                }
                return render(request, "auctions/listing.html", context)

            highest_bid = Bids.objects.filter(auction=auction).order_by('-bid_price').first()
            if highest_bid is None or bid_price > highest_bid.bid_price:
                try:
                    new_bid = Bids(auction=auction, user=user, bid_price=bid_price)
                    new_bid.save()
                except Exception:
                    return HttpResponseRedirect("/" + auction_id)


            if auction.price < bid_price:

                auction.price = bid_price
                auction.save()
                return HttpResponseRedirect("/" + auction_id)

            else:
                context = {
                    "message": "Your bid is too small",
                    'Post': auction,
                    'bid_form': BidForm()
                }
                return render(request, "auctions/listing.html", context)

                
@login_required          
def closeListing(request):
    if request.method == 'POST':

        auction = Auction.objects.get(pk=request.POST["listingID"])
        auction.closed = True
        auction.save()
    
        auction_id = request.POST["listingID"]

        return HttpResponseRedirect("/" + auction_id)

    return HttpResponseRedirect("/" + auction_id)

    
    

@login_required
def addComment(request):
    if request.method == "POST":
        form = commentsForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            auction_id = request.POST.get("auction_id")
           
            auction = Auction.objects.get(pk=auction_id)
            user = User.objects.get(id=request.user.id)

            try:
                new_comment = Comments(auction=auction, userComment=user, comment=comment)
                new_comment.save()
            except Exception:
                return HttpResponseRedirect("/" + auction_id)


        return HttpResponseRedirect("/" + auction_id)

  
def categories(request):

    listCategory = Auction.objects.values_list('category', flat=True)

    noDuplicates = []

    for i in listCategory:
        if i not in noDuplicates:
            noDuplicates.append(i)
    listCategory = noDuplicates

    return render(request, 'auctions/categories.html',{
        'listCategory': listCategory
    })

def categoryView(request, category):

    listing_category = Auction.objects.filter(category = category)
    work = category

    return render(request, 'auctions/categoryView.html',{
        'listing_category': listing_category,
        'category': work,
    })