from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView

from .models import User
import requests

uri = "http://127.0.0.1:8000"

# 로그인 템플릿
def oauth_login(request):
    return render(request, './user/login.html', {})

# 인가 코드 요청
class Kakao(View):
    def get(self, request):
        kakao_api="https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri=f"{uri}/users/oauth/callback"
        client_id="1301c1e0e19f2a3c5b9ee4a72d7b83ef"
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

# 토큰 발급 및 회원가입
class KakaoCallback(View):
    def get(self, request):
        data = {
            "grant_type":"authorization_code",
            "client_id":"1301c1e0e19f2a3c5b9ee4a72d7b83ef",
            "redirection_uri":f"{uri}/users/oauth",
            "code":request.GET["code"]
        }
        kakao_token_api="https://kauth.kakao.com/oauth/token"
        access_token = requests.post(kakao_token_api, data=data).json().get("access_token")
        if access_token==None:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        #카카오 사용자 정보 요청
        kakao_user_api="https://kapi.kakao.com/v2/user/me"
        print(access_token)
        user_info=requests.get(kakao_user_api, headers={"Authorization":f"Bearer ${access_token}"}).json()
        print(user_info)
        if not User.objects.filter(kakaoId=user_info['id']).exists():
            User.objects.create(
                kakaoId=user_info['id'],
                userName=user_info['properties']['nickname'],
                last_login=timezone.now(),
                password="1234",
            )
        # 로그인
        user = User.objects.get(kakaoId=user_info['id'])
        login(request, user, 'user.auth.MyBackend')
        return redirect(f'{uri}/')