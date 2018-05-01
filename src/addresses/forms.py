from django import forms
from .models import Address, ADDRESS_TYPES


class AddressForm(forms.ModelForm):

    nickname = forms.CharField(
        label='Nickname',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    address_type = forms.ChoiceField(
        choices=ADDRESS_TYPES,
        label='Address Type',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'},
        )
    )
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
            attrs={'class': 'form-control mb-3'}
        )
    )

    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            'address_type',
            'address_line1',
            'address_line2',
            'city',
            'country',
            'state',
            'zipcode'
        ]


class AddressCheckoutForm(forms.ModelForm):

    nickname = forms.CharField(
        label='Nickname',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    address_type = forms.ChoiceField(
        label='Address Type',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
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
            'nickname',
            'name',
            'address_line1',
            'address_line2',
            'city',
            'country',
            'state',
            'zipcode'
        ]
