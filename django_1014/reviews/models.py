from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# title : 리뷰 제목
# content : 리뷰 내용
# item_name : 리뷰 대상 인테리어 아이템
# grade : 평가 점수
# created_at : 리뷰 생성시간 / DateTime / auto_now_add = True
# updated_at : 리뷰 수정시간 / DateTime / auto_now = True

class Review(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    item_name = models.CharField(max_length=30)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)