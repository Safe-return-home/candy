from django.db import models

class Marker(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE) # 유저 매핑
    address = models.CharField(max_length=100) # 도로명주소
    latitude = models.FloatField() # 위도
    longitude = models.FloatField() # 경도
    street_lamp = models.CharField(max_length=10) # 가로등 수
    population = models.CharField(max_length=10) # 유동인구 수
    rating = models.IntegerField() # 안전캔디 점수
    body = models.CharField(max_length = 200) # 내용
    image = models.ImageField(upload_to='', blank=False) # 이미지
    regTime = models.DateTimeField(auto_now_add=True) # 작성시간

class Comment(models.Model):
    marker = models.ForeignKey('marker.Marker', on_delete=models.CASCADE, related_name="comments") # 마커 매핑
    user = models.ForeignKey('user.User', on_delete=models.CASCADE) # 유저 매핑
    body = models.CharField(max_length=200) # 내용
    regTime = models.DateTimeField(auto_now_add=True) # 작성시간