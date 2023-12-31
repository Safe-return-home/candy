from django.urls import path
from .views import oauth_login, Kakao, KakaoCallback

app_name = "user"

urlpatterns = [
    path("", oauth_login, name='login'),
    path("oauth/", Kakao.as_view(), name='oauth'),
    path("oauth/callback/", KakaoCallback.as_view()),
]