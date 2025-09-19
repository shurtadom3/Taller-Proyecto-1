from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np

class Command(BaseCommand):
    help = 'Muestra el embedding de una película seleccionada al azar.'

    def handle(self, *args, **kwargs):
        movie = Movie.objects.order_by('?').first()
        if not movie:
            self.stdout.write(self.style.ERROR('No hay películas en la base de datos.'))
            return
        embedding = np.frombuffer(movie.emb, dtype=np.float32)
        self.stdout.write(self.style.SUCCESS(f'Título: {movie.title}'))
        self.stdout.write(f'Embedding (primeros 10 valores): {embedding[:10]}')
