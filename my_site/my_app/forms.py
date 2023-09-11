from django import forms
from my_app.models import Publisher


class UserForm(forms.Form):
    name = forms.CharField(label='User name', max_length=20)
    age = forms.IntegerField(label='User age')
    gender = forms.CharField(label='User gender', max_length=6)
    nationality = forms.CharField(label='User nationality', max_length=100)


class PublisherForm(forms.Form):
    name = forms.CharField(label='Publisher name', max_length=20)


class BookForm(forms.Form):
    name = forms.CharField(max_length=300, label='Title of the book')
    price = forms.IntegerField(label='Price of the book')
    # publisher = forms.ModelChoiceField(queryset=Publisher.objects.all())
    name_publisher = forms.CharField(label='Publisher name', max_length=20)
