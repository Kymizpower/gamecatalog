import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_catalog.settings')
django.setup()

from catalog.models import Game

test_games = [
    {
        'title': 'Cyberpunk 2077',
        'slug': 'cyberpunk-2077',
        'description': 'Cyberpunk 2077 — приключенческая ролевая игра, действие которой происходит в мегаполисе Найт-Сити, где власть, роскошь и модификации тела ценятся выше всего. Вы играете за V, наёмника в поисках уникального имплантата, который является ключом к бессмертию.',
        'short_description': 'Футуристическая RPG от создателей Ведьмака',
        'price': 2999.99,
        'developer': 'CD Projekt Red',
        'publisher': 'CD Projekt',
        'genre': 'RPG',
        'platform': 'PC, PlayStation, Xbox',
        'metacritic_score': 86,
        'release_date': date(2020, 12, 10)
    },
    {
        'title': 'Elden Ring',
        'slug': 'elden-ring',
        'description': 'Elden Ring — новая ролевая игра с фэнтезийным сеттингом, созданная в сотрудничестве Хидэтаки Миядзаки и Джорджа Р. Р. Мартина. Исследуйте мир Межземья, сражайтесь с могучими противниками и раскрывайте секреты древних богов.',
        'short_description': 'Эпическая dark fantasy RPG от FromSoftware',
        'price': 3499.99,
        'developer': 'FromSoftware',
        'publisher': 'Bandai Namco',
        'genre': 'RPG',
        'platform': 'PC, PlayStation, Xbox',
        'metacritic_score': 96,
        'release_date': date(2022, 2, 25)
    },
    {
        'title': 'Counter-Strike 2',
        'slug': 'counter-strike-2',
        'description': 'Counter-Strike 2 представляет собой крупнейший технологический скачок в истории серии, обеспечивая бесплатное обновление для всех игроков CS:GO.',
        'short_description': 'Легендарный тактический шутер',
        'price': 0,
        'developer': 'Valve',
        'publisher': 'Valve',
        'genre': 'ACTION',
        'platform': 'PC',
        'metacritic_score': 82,
        'release_date': date(2023, 9, 27)
    },
    {
        'title': 'Stardew Valley',
        'slug': 'stardew-valley',
        'description': 'Унаследовав старую ферму своего деда в долине Стардью, вы, вооружившись ветхими инструментами и небольшим количеством монет, решите начать новую жизнь.',
        'short_description': 'Расслабляющая фермерская симуляция',
        'price': 399.99,
        'developer': 'ConcernedApe',
        'publisher': 'ConcernedApe',
        'genre': 'SIMULATION',
        'platform': 'PC, PlayStation, Xbox, Switch',
        'metacritic_score': 89,
        'release_date': date(2016, 2, 26)
    }
]

for game_data in test_games:
    game, created = Game.objects.get_or_create(
        slug=game_data['slug'],
        defaults=game_data
    )
    if created:
        print(f'Добавлена игра: {game.title}')
    else:
        print(f'Игра уже существует: {game.title}')

print(f'Всего игр в базе: {Game.objects.count()}')