import django_filters
from .models import Film

class GenreFilter(django_filters.FilterSet):

    class Meta:
        model = Film
        fields = ['genres']