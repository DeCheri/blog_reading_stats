from django.db import transaction
from django.db.models import F
from ..models import ArticleReadCount

class DBService:
    def get_read_count(self, article_id):
        try:
            with transaction.atomic():
                read_count_obj = ArticleReadCount.objects.select_for_update().get(article=article_id)
                return read_count_obj.count
        except ArticleReadCount.DoesNotExist:
            # 如果阅读量记录不存在，创建一个新记录
            from ..models import Article  # 确保导入正确的Article模型
            article = Article.objects.get(id=article_id)
            read_count_obj = ArticleReadCount.objects.create(article=article, count=0)
            return 0
        except Exception as e:
            print(f"数据库查询异常: {str(e)}")
            raise
            
    def increment_read_count(self, article_id):
        try:
            with transaction.atomic():
                read_count_obj, created = ArticleReadCount.objects.get_or_create(
                    article_id=article_id,
                    defaults={'count': 0}
                )
                if not created:
                    read_count_obj.count = F('count') + 1
                    read_count_obj.save()
                return read_count_obj.count
        except Exception as e:
            print(f"数据库更新异常: {str(e)}")
            raise