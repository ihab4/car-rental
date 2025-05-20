from django import forms
from .models import Rental, Brand


class CarFilterForm(forms.Form):
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        label="Select a brand",
        empty_label="Select brand",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'brand-select',
        })
    )



class BookingForm(forms.ModelForm):
    brand = forms.ChoiceField
    brand = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "first name", "class": "form-control"}), label="")
    model = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "last_name", "class": "form-control"}), label="")
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "email", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "phone", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "country", "class": "form-control"}), label="")
    cin = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "city", "class": "form-control"}), label="")
    permis = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Expiration date", "class": "form-control"}), label="")

    class Meta:
        model = Rental
        exclude = ("user",)

