import redis
from django.conf import settings

class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None
        )
        self.cache_prefix = "article_read_count:"
        self.hit_count = 0
        self.miss_count = 0
        
    def get_cache_key(self, article_id):
        return f"{self.cache_prefix}{article_id}"
        
    def get_read_count(self, article_id):
        key = self.get_cache_key(article_id)
        try:
            count = self.client.get(key)
            if count is not None:
                self.hit_count += 1
                return int(count)
            else:
                self.miss_count += 1
                return None
        except redis.RedisError as e:
            print(f"Redis异常: {str(e)}")
            return None
            
    def increment_read_count(self, article_id):
        key = self.get_cache_key(article_id)
        try:
            return self.client.incr(key)
        except redis.RedisError as e:
            print(f"Redis异常: {str(e)}")
            return None
            
    def set_read_count(self, article_id, count):
        key = self.get_cache_key(article_id)
        try:
            return self.client.setex(key, 1800, count)
        except redis.RedisError as e:
            print(f"Redis异常: {str(e)}")
            return None
            
    def get_hit_rate(self):
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0
        return self.hit_count / total * 100
        
    def reset_hit_rate_stats(self):
        self.hit_count = 0
        self.miss_count = 0