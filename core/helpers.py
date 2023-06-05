from graphql import GraphQLError
import base64
from django.contrib.auth import get_user_model


def requires_authentication(func):
    def wrapper(self, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Authentication required.')
        return func(self, info, *args, **kwargs)
    return wrapper


def get_decoded_user_id(id):
    # Decode the ID
    decoded_id = base64.b64decode(id).decode('utf-8')
    # Extract the user ID
    user_id = decoded_id.split(':')[1]
    return user_id


def get_user(id):
    CustomUser = get_user_model()
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        raise GraphQLError("Invalid user.")

    return user
