from django.shortcuts import render
from .models import Song

def home(request):
    songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs})

def search(request):
    query = request.GET.get('q', '')
    songs = Song.objects.filter(title__icontains=query)
    return render(request, 'home.html', {'songs': songs, 'query': query})
