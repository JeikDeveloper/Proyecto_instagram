from django import forms
from django.contrib.auth.models import User
from users.models import Profile

class SignupForm(forms.Form):
    username = forms.CharField(min_length=4,max_length=20)
    password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput())
    password_confirmation = forms.CharField(
                                            min_length=8,
                                            max_length=20,
                                            widget=forms.PasswordInput())
    first_name = forms.CharField(min_length=2,max_length=50)
    last_name = forms.CharField(min_length=2,max_length=50)

    email = forms.CharField(min_length=10,max_length=80,widget=forms.EmailInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        filter_username = User.objects.filter(username=username).exists()
        if filter_username:
            raise forms.ValidationError('Username in use.')
        return username


    def clean(self):
        data = super().clean()
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Do not match passwords')
        
        return data


    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()


class ProfileForm(forms.Form):
    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=10, required=False)
    picture = forms.ImageField()