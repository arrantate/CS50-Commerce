from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:listing_pk>", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_pk>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/remove/<int:listing_pk>", views.watchlist_remove, name="watchlist_remove"),
    path("category/<str:category_name>", views.category, name="category"),
    path("new/", views.new_listing, name="new_listing"),
    path("bid/<int:listing_pk>", views.new_bid, name="new_bid")
]
