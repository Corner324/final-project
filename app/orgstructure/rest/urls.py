from rest_framework.routers import DefaultRouter
from app.orgstructure.rest.views import OrganizationalUnitViewSet

router = DefaultRouter()
router.register(r"units", OrganizationalUnitViewSet)

urlpatterns = router.urls
