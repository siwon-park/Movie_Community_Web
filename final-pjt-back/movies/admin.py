from django.contrib import admin
from .models import Movie, Genre, Rate

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Rate)