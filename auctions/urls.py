from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activelisting/", views.active_listing, name="active_listing"),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('delete-listing/<slug>', views.delete_listing, name='delete_listing'),
    path('listing/', views.view_listing, name='view_listing'),
    path('listing/<slug>/', views.detail_listing, name='detail_listing'),
    path('add-to-watchlist/listing/<slug>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-listing-from-watchlist/<slug>/', views.remove_listing_from_watchlist, 
            name='remove_listing_from_watchlist'),
    path('watchlist/<pk>', views.watchlist, name='watchlist'),
    path('delete-bidding/<str:slug>/', views.delete_bidding, name='delete_bidding'),
    path('bids-view/<pk>', views.bids_view, name='bids_view'),
    path('comment/<slug:slug>/', views.listing_comment, name='listing_comment'),
    path('bidding/<slug:slug>/', views.bidding, name='bidding_form'),
    path('close_listing/<slug>/', views.close_listing, name='close_listing'),
    path('mylisting/<pk>', views.mylisting, name='mylisting'),
    path('category/', views.category_view, name='category_view'),
    path('category/<slug>', views.view_by_category, name='view_by_category'),
]
