from typing import Any
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from flask import request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from DjangoProjectApp.filters import GenreFilter
from DjangoProjectApp.forms import AddFilmForm, LoginForm, SignupForm
from django.views.generic import View, ListView, FormView
from DjangoProjectApp.models.films import Film, Genre
from DjangoProjectApp.models.user import User, Like
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from functools import reduce
from django.http import JsonResponse
import operator

# def superuser_required():
#     def wrapper(wrapped):
#         class WrappedClass(UserPassesTestMixin, wrapped):
#             def test_func(self):
#                 return self.request.user.is_superuser

#         return WrappedClass
#     return wrapper




class SignupView(FormView):
    template_name = "DjangoProjectApp/signup.html"
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# class MainView(View):
class AuthenticationView(FormView):
    template_name = "DjangoProjectApp/login.html"
    model = User
    form_class = LoginForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)

def logout_page(request):
    logout(request)
    return redirect("main_page")

def main_page(request):
    genres = Genre.objects.all()
    genres_filter = request.GET.getlist("genres")
    films = Film.objects.all()
    min_year_created = request.GET.get('min_year')
    max_year_created = request.GET.get('max_year')

    if min_year_created and max_year_created:
        films = films.filter(year_created__gte=min_year_created, year_created__lte=max_year_created)
    
    if genres_filter:
        querysets = []
        for genre in genres_filter:
            querysets.append(films.filter(genres=genre))
        films = reduce(operator.and_, querysets)

    paginated = Paginator(films, 3)
    page_number = request.GET.get('page')
    
    page = paginated.get_page(page_number)
    # print(films)    
    # for film in films:
    #     print(film.title, film.genres.all())
    return render(request, "DjangoProjectApp/main_page.html", {'genres': genres, 'films': page.object_list, 'page': page})

@login_required(login_url="/login")
def profile_page(request):
    user = request.user
    liked_films = user.liked_films.all()

    return render(request, "DjangoProjectApp/profile_page.html", {'user': user, 'liked_films': liked_films})

class AddFilmView(FormView):
    # if request.user.is_superuser == False:
    #     messages.info(request, 'Вы не Администратор.')
    form_class = AddFilmForm
    model = Film
    template_name = "DjangoProjectApp/add_film.html"
    success_url = reverse_lazy('main_page') 

    def form_valid(self, form: Any) -> HttpResponse:

        if Film.objects.filter(title=form.cleaned_data['title']).exists():
            messages.error(self.request, 'Фильм с таким названием уже существует')
            return super().form_invalid(form)

        form.instance.user = self.request.user
        film = form.save(commit=False)
        film.save()
        form.save_m2m()
        return super().form_valid(form)
    
# class FilmDetailView(View):
#     model = Film
#     template_name = "DjangoProjectApp/film_detail.html"
    
def FilmDetail(request, slug):
    film = Film.objects.get(slug=slug)
    return render(request, 'DjangoProjectApp/film_detail.html', {'film': film})

@user_passes_test(lambda u: u.is_superuser, login_url="/")
def delete_film(request, slug):
    film = get_object_or_404(Film, slug=slug)
    film.delete()
    return redirect('/') 

@login_required
def like_film(request):
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
        film = Film.objects.get(id=film_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, film=film)

        if not created:
            like.delete()

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})