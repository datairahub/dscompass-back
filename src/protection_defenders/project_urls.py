from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated
from rest_framework.routers import SimpleRouter, DefaultRouter

from .defenders_app.rest.urls import DefendersAPIRouter
from .defenders_auth import jwt
from .defenders_auth.rest.views import user_views, login_views, token_views

router = DefendersAPIRouter().register_router()
user_router = SimpleRouter()
user_router.register(r'users', user_views.UserViewSet)
router.registry.extend(user_router.registry)

login_router = DefaultRouter()
login_router.register(r'', login_views.LoginViewSet)

urlpatterns = [
    path('opensesame/', admin.site.urls),
    path('token/access/', jwt.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', jwt.TokenLogoutView, name='token_logout'),
    path('api/', include((router.urls, 'defenders'), namespace='defender_urls')),
    path('login/', include((login_router.urls, 'login'), namespace='login')),
    path('login/sign', token_views.AuthTokenObtainPairView.as_view(), name='auth_token')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is True:
    urlpatterns += [path(r'api-docs/',
                         include_docs_urls(title='Protect Defenders API',
                                           patterns=urlpatterns,
                                           authentication_classes=[BasicAuthentication, SessionAuthentication],
                                           permission_classes=[IsAuthenticated]))]
