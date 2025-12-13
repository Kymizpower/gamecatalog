from django.shortcuts import render, get_object_or_404
from .models import Game

def index(request):
    games = Game.objects.all()[:8]
    return render(request, 'catalog/index.html', {'games': games})

def game_list(request):
    games = Game.objects.all()
    return render(request, 'catalog/game_list.html', {'games': games})

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, 'catalog/game_detail.html', {'game': game})