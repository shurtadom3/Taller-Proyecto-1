from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib,base64


from .models import Movie
# Create your views here.

def home(request):
   #return render(request, 'home.html', {'name': 'Sara Hurtado'})
  searchTerm = request.GET.get('searchMovie')
  if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
  else:
        movies = Movie.objects.all()
  return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})
       
   

def about(request):
   return render(request, 'about.html',{'name': 'Sara Hurtado'})

def statistics_view(request):
    matplotlib.use('Agg')

    # Películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.figure(figsize=(6,4))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='blue')
    plt.title('Number of Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.tight_layout()
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    image_png_year = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_png_year).decode('utf-8')

    # películas por género (considerando solo el primer género si hay varios)
    genre_counts = {}
    for movie in Movie.objects.all():
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1
        else:
            genre_counts['None'] = genre_counts.get('None', 0) + 1
    plt.figure(figsize=(6,4))
    plt.bar(genre_counts.keys(), genre_counts.values(), color='green')
    plt.title('Number of Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    # Renderizar la plantilla stadistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})