from django.db import models
from django.urls import reverse
from pytils.translit import slugify

class Film(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to="")
    year_created = models.IntegerField()
    genres = models.ManyToManyField("Genre", through="MovieGenre", through_fields=("film", "genre"), related_name="films")
    slug = models.SlugField(unique=True)
    prepopulated_fields = {"slug": ("title", )}

    def get_absolute_url(self):
        return reverse('film_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Film, self).save(*args, **kwargs)
        

class Genre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class MovieGenre(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="genre_set")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="film_set")