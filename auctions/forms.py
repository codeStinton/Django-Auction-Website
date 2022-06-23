from django import forms
from . import models

class auctionForm(forms.ModelForm):
    class Meta:
        model = models.Auction
        fields = ['title', 'description', 'price', 'image', 'category']
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = models.Bids
        fields = ['bid_price']
        widgets = {
            "bid_price": forms.NumberInput(attrs={
                "placeholder": "Bid",
                "min": 0.01,
                "max": 100000,
                "class": "form-control"
            })
        }

class commentsForm(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ['comment']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':100}),
        }
