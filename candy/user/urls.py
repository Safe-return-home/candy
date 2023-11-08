from django.urls import path
from .views import oauth_login, Kakao, KakaoCallback

app_name = "user"

urlpatterns = [
    path("login/", oauth_login, name='login'),
    path("oauth/", Kakao.as_view()),
    path("oauth/callback/", KakaoCallback.as_view()),
]