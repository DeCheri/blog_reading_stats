from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Article
from .services.read_count_service import ReadCountService

# 数据库
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    read_count_service = ReadCountService()
    
    try:
        read_count_service.increment_read_count(article_id)
    except Exception as e:
        print(f"阅读量统计异常: {str(e)}")
    
    try:
        count = read_count_service.get_read_count(article_id)
    except Exception as e:
        print(f"获取阅读量异常: {str(e)}")
        count = 0
        
    context = {
        'article': article,
        'read_count': count,
    }
    
    return render(request, 'reading_stats/article_detail.html', context)

def cache_hit_rate(request):
    read_count_service = ReadCountService()
    hit_rate = read_count_service.get_cache_hit_rate()
    
    return JsonResponse({
        'cache_hit_rate': f"{hit_rate:.2f}%",
        'status': 'success'
    })