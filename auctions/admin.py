from django.contrib import admin
from .models import User, Category, Listing, WatchList, Bid, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(WatchList)


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'price', 'status')

admin.site.register(Listing, ListingAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'username', 'active')

admin.site.register(Comment, CommentAdmin)


class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'username', 'bidprice', 'bidstatus', 'completed')

admin.site.register(Bid, BidAdmin)
