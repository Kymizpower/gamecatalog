from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator

def news_list(request):
    news_list = News.objects.filter(is_published=True)
    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    return render(request, 'news/news_detail.html', {'news_item': news_item})