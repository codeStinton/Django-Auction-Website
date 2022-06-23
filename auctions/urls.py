from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.newListing, name="newListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
    path("bid", views.bid, name="bid"),
    path("closeListing", views.closeListing, name="closeListing"),
    path("addComment", views.addComment, name="addComment"),
    path("categories", views.categories, name="categories"),
    path("categoryView<str:category>", views.categoryView, name="categoryView"),
]
