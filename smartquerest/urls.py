from rest_framework.routers import DefaultRouter

from .views import CabinetViewSet


router = DefaultRouter()
router.register(r'smartquerest', CabinetViewSet, basename='user')

urlpatterns = router.urls