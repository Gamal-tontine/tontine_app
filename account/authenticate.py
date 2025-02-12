from django.contrib.auth.backends import ModelBackend
from .models import User
class CustomAuthenticate(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email = username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            request.user = user
            return user
        return None