from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from auth_login.models import User


@database_sync_to_async
def get_user(scope):
    # Get the user from the token in the WebSocket scope
    try:
        token_key = parse_qs(scope["query_string"].decode("utf-8"))["token"][0]
        token = AccessToken(token_key)
        user_id = token.payload.get("user_id")

        if user_id:
            user = User.objects.get(id=user_id)
            return user
    except Exception as e:
        print(e)
        return AnonymousUser()

    return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Add the user to the scope based on the token
        scope["user"] = await get_user(scope)
        return await super().__call__(scope, receive, send)
