from django.urls import path
from .views import article_detail, cache_hit_rate

urlpatterns = [
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    path('stats/cache-hit-rate/', cache_hit_rate, name='cache_hit_rate'),
]