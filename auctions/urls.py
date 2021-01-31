from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:listing_pk>", views.listing, name="listing"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add/<int:listing_pk>", views.wishlist_add, name="wishlist_add"),
    path("category/<str:category_name>", views.category, name="category"),
]
