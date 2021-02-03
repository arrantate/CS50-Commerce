from django import forms

from .models import Listing, Category


class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64, label="Item name")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5}), label="Item description")
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, label="Starting Price")
    image_url = forms.CharField(max_length=500, required=False, label="Image URL (optional)")
    category = forms.ChoiceField(choices=[('NO CATEGORY', 'NO CATEGORY')]+[(category.name, category.name) for category in Category.objects.all()], 
                                        required=False, 
                                        label="Category")
