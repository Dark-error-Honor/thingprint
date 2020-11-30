from django import forms
from core.models import Thing


class ThingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    price = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'image-field'
    }))

    class Meta:
        model = Thing
        fields = [
            'title',
            'description',
            'price',
            'image',
        ]
