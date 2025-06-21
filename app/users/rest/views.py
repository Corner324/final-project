from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from app.users.models import AppUser
from app.users.rest.serializers import (
    AppUserPreviewSerializer,
    AppUserRegisterSerializer,
    AppUserUpdateSerializer,
)


class IsAdminOrSelf(permissions.BasePermission):
    """Разрешает пользователю редактировать только себя, а админу — всех."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj


class AppUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AppUser.objects.select_related("team").all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == "create":
            return AppUserRegisterSerializer
        elif self.action in ["update", "partial_update"]:
            return AppUserUpdateSerializer
        return AppUserPreviewSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.action == "destroy":
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
