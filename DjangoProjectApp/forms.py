from .models import Film, User, Genre
from typing import Any
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model
from django.forms import (
    CharField,
    ChoiceField,
    DateField,
    Field,
    ValidationError,
    ModelForm,
    Form,
    ModelMultipleChoiceField
)
from django.forms.widgets import DateInput, CheckboxSelectMultiple
from django.forms import TextInput

class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
        )
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            # "username",
        )
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
    
class AddFilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ["title", "description", "image", "year_created", "genres"]
        
    genres = ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple
    )
    
    def save(self, commit=True):
        film = super().save(commit=False)
        print(self.cleaned_data)
        for genre in self.cleaned_data["genres"]:
            print(genre)
        if commit:
            film.save()
            film.genres.add(*self.cleaned_data["genres"])
            
        return film
        