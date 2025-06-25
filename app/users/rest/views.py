from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from app.users.models import AppUser
from app.users.rest.serializers import (
    AppUserPreviewSerializer,
    AppUserRegisterSerializer,
    AppUserUpdateSerializer,
    UserStatusSerializer,
    UserUnitInfoSerializer,
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

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_status(self, request, pk=None):
        user = self.get_object()
        serializer = UserStatusSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_unit_info(self, request, pk=None):
        user = self.get_object()
        serializer = UserUnitInfoSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def add_to_team(self, request, pk=None):
        user = self.get_object()
        team_id = request.data.get("team_id")
        if not team_id:
            return Response({"error": "team_id required"}, status=400)
        from app.users.models import Team

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"error": "team not found"}, status=404)
        user.team = team
        user.save()
        return Response({"result": "added to team"})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def remove_from_team(self, request, pk=None):
        user = self.get_object()
        user.team = None
        user.save()
        return Response({"result": "removed from team"})
