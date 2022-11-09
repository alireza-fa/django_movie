from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    token_info = RefreshToken.for_user(user)
    return {
        "refresh": str(token_info),
        "access_token": str(token_info.access_token)
    }
