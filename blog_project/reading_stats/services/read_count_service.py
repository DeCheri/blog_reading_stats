from django.db import transaction
import threading
from .cache_service import CacheService
from .db_service import DBService

class ReadCountService:
    def __init__(self):
        self.cache_service = CacheService()
        self.db_service = DBService()
        self.lock = threading.Lock()
        
    def get_read_count(self, article_id):
        count = self.cache_service.get_read_count(article_id)
        
        if count is not None:
            return count
            
        try:
            with self.lock:
                count = self.cache_service.get_read_count(article_id)
                if count is not None:
                    return count
                    
                count = self.db_service.get_read_count(article_id)
                self.cache_service.set_read_count(article_id, count)
                
                return count
        except Exception as e:
            print(f"获取阅读量失败: {str(e)}")
            return 0
            
    def increment_read_count(self, article_id):
        new_count = self.cache_service.increment_read_count(article_id)
        
        if new_count is None:
            try:
                return self.db_service.increment_read_count(article_id)
            except Exception as e:
                print(f"增加阅读量失败: {str(e)}")
                return self.get_read_count(article_id)
                
        self._async_update_db(article_id)
        return new_count
        
    def _async_update_db(self, article_id):
        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=5)
        executor.submit(self._update_db_task, article_id)
        executor.shutdown(wait=False)
        
    def _update_db_task(self, article_id):
        try:
            cache_count = self.cache_service.get_read_count(article_id)
            if cache_count is not None:
                self.db_service.increment_read_count(article_id)
        except Exception as e:
            print(f"异步更新数据库失败: {str(e)}")
            
    def get_cache_hit_rate(self):
        return self.cache_service.get_hit_rate()