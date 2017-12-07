from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    address_line1 = forms.CharField(
        label='Address Line 1',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    address_line2 = forms.CharField(
        label='Address Line 2',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    city = forms.CharField(
        label='City',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    state = forms.CharField(
        label='State',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    country = forms.CharField(
        label='Country',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    zipcode = forms.CharField(
        label='Zipcode',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Address
        fields = [
            'address_line1',
            'address_line2',
            'city',
            'state',
            'country',
            'zipcode'
        ]
