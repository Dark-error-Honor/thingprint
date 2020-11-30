from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=64, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        label='', max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='',
                                       max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'confirm_password', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
