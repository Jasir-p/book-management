from django.urls import path,include
from .views import UserManagementView,RegisterView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserManagementView, basename='users')
urlpatterns = router.urls
urlpatterns += [
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("user/register/",RegisterView.as_view(), name="register"),
]




