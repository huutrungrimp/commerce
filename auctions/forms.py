from django.forms import ModelForm
from .models import Listing, Bid, Comment


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'username', 'description', 'price', 'listing_pics', 'slug', 'status']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'