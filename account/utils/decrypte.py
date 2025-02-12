from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from ..models import User

def decrypte_token(uid,token):
    pk = urlsafe_base64_decode(force_bytes(uid))
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return None
    if not default_token_generator.check_token(user,token):
        return None
    return user
