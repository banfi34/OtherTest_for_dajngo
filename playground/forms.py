from django import forms
from django.forms import ModelForm
from .models import Info, InfoReview


class InfoForm(ModelForm):
    class Meta:
        model = Info
        fields = ('name', 'publisher_name', 'info')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name your information'}),
            'publisher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Information'})
        }


class ReviewAdd(forms.ModelForm):
    class Meta:
        model = InfoReview
        fields = ('review_text', 'review_rating')


class InfoSecondForm(ModelForm):
    class Meta:
        model = Info
        fields = '__all__'
