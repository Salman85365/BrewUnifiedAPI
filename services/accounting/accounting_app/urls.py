from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView
from .views import CustomUserViewSet, TransactionViewSet, AccountViewSet, \
    CustomTokenVerifyView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(),
         name='token_verify'),
    path('', include(router.urls)),
]
