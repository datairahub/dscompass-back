from django.conf import settings


class CookieJWTMiddleware:
    """
    CookieJWTMiddleware
    If a refresh token cookie is present on the request,
    add the token to request.refresh to handle it later
    """

    def __init__(self, get_response):
        self.cookie_name = settings.SIMPLE_JWT['COOKIE_REFRESH_KEY']
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'COOKIES') and request.COOKIES.get(self.cookie_name, None):
            request.refresh = request.COOKIES.get(self.cookie_name)

        return self.get_response(request)
