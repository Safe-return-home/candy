from django.contrib.auth import get_user_model

class MyBackend:
    def authenticate(self, request, kakaoId=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(kakaoId=kakaoId)
        except UserModel.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None