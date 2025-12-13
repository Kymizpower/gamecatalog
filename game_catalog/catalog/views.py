from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Game

def index(request):
    """Главная страница с 8 последними играми"""
    games = Game.objects.filter(is_available=True).order_by('-created')[:8]
    return render(request, 'catalog/index.html', {'games': games})

def game_list(request):
    """Список всех игр с фильтрами и сортировкой"""
    # Получаем параметры фильтрации из GET-запроса
    genre = request.GET.get('genre', '')
    platform = request.GET.get('platform', '')
    sort_by = request.GET.get('sort', '-created')
    search_query = request.GET.get('search', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    available_only = request.GET.get('available', '')
    
    # Начинаем с всех игр
    games = Game.objects.all()
    
    # Фильтр по жанру
    if genre:
        games = games.filter(genre=genre)
    
    # Фильтр по платформе
    if platform:
        # Ищем игры, у которых в поле platform содержится выбранная платформа
        games = games.filter(platform__icontains=platform)
    
    # Фильтр по цене (от и до)
    if price_min:
        try:
            price_min_value = float(price_min)
            games = games.filter(price__gte=price_min_value)
        except ValueError:
            pass
    
    if price_max:
        try:
            price_max_value = float(price_max)
            games = games.filter(price__lte=price_max_value)
        except ValueError:
            pass
    
    # Фильтр по доступности
    if available_only:
        games = games.filter(is_available=True)
    
    # Поиск по названию или разработчику
    if search_query:
        games = games.filter(
            Q(title__icontains=search_query) | 
            Q(developer__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_options = {
        'newest': '-created',           # Сначала новые
        'oldest': 'created',            # Сначала старые
        'price_asc': 'price',           # По цене (дешевые)
        'price_desc': '-price',         # По цене (дорогие)
        'name_asc': 'title',            # По названию (А-Я)
        'name_desc': '-title',          # По названию (Я-А)
        'rating_desc': '-metacritic_score',  # По рейтингу
    }
    
    if sort_by in sort_options:
        games = games.order_by(sort_options[sort_by])
    else:
        games = games.order_by('-created')  # По умолчанию новые сначала
    
    # Получаем уникальные жанры для фильтра
    all_genres = Game.objects.values_list('genre', flat=True).distinct()
    unique_genres = []
    seen = set()
    for genre_val in all_genres:
        if genre_val and genre_val not in seen:
            seen.add(genre_val)
            unique_genres.append(genre_val)
    
    # Получаем уникальные платформы
    all_platforms = []
    for game in Game.objects.all():
        if game.platform:
            # Разделяем платформы по запятой и добавляем в список
            platforms = [p.strip() for p in str(game.platform).split(',') if p.strip()]
            all_platforms.extend(platforms)
    unique_platforms = sorted(set(all_platforms))
    
    context = {
        'games': games,
        'genres': unique_genres,
        'platforms': unique_platforms,
        'selected_genre': genre,
        'selected_platform': platform,
        'selected_sort': sort_by,
        'search_query': search_query,
        'price_min': price_min,
        'price_max': price_max,
        'available_only': available_only,
        'total_games': games.count(),
    }
    
    return render(request, 'catalog/game_list.html', context)

def game_detail(request, slug):
    """Детальная страница игры"""
    game = get_object_or_404(Game, slug=slug)
    
    # Похожие игры (по жанру)
    similar_games = Game.objects.filter(
        genre=game.genre
    ).exclude(
        id=game.id
    ).order_by('-created')[:4]
    
    context = {
        'game': game,
        'similar_games': similar_games,
    }
    
    return render(request, 'catalog/game_detail.html', context)