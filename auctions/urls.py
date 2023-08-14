from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.CreateListing, name="create"),
    path("seeCategory", views.seeCategory, name="seeCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("addbid/<int:id>", views.addbid, name="addbid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),

    
]
