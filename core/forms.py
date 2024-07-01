from django import forms
from .models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'category': forms.Select(attrs={'class':'form-control' ,'placeholder': 'Select the category'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'product_available_count': forms.NumberInput(attrs={'class':'form-control' ,'placeholder': 'Enter product count'}),
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }





class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder' : '123 Main st',
    }))

    appartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Appartment or suite'

    }))
    country = CountryField(blank_label='(Select Country)').formfield(widget=CountrySelectWidget,attrs={
        'class': 'custom-select d-block w-100'
    })

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
