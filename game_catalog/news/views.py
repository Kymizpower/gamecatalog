from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import News
from django.core.paginator import Paginator

def news_list(request):
    # Получаем параметры фильтрации
    filter_type = request.GET.get('filter', 'published')
    
    # Базовый запрос
    if filter_type == 'all':
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(is_published=True)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-published_date')
    if sort_by in ['published_date', '-published_date', 'title', '-title']:
        news_list = news_list.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(news_list, 6)  # 6 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'sort_by': sort_by,
        'total_news': news_list.count(),
    }
    
    return render(request, 'news/news_list.html', context)

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    
    # Получаем последние новости (кроме текущей)
    latest_news_list = News.objects.filter(
        is_published=True
    ).exclude(
        id=news_item.id
    ).order_by('-published_date')[:5]
    
    # Получаем архив новостей по месяцам
    archive_months = News.objects.filter(
        is_published=True
    ).annotate(
        month=TruncMonth('published_date')
    ).values(
        'month'
    ).annotate(
        count=Count('id')
    ).order_by('-month')[:6]
    
    # Получаем связанные новости (по заголовку)
    related_news = News.objects.filter(
        is_published=True
    ).exclude(
        id=news_item.id
    ).filter(
        title__icontains=news_item.title[:20]
    ).order_by('-published_date')[:3]
    
    context = {
        'news_item': news_item,
        'latest_news_list': latest_news_list,
        'archive_months': archive_months,
        'related_news': related_news,
    }
    
    return render(request, 'news/news_detail.html', context)