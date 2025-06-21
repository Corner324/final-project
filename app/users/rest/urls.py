from rest_framework.routers import DefaultRouter
from app.users.rest.views import AppUserViewSet

router = DefaultRouter()
router.register(r"users", AppUserViewSet, basename="user")

urlpatterns = router.urls
