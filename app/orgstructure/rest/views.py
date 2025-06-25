from rest_framework import viewsets, permissions
from app.orgstructure.models import OrganizationalUnit
from app.orgstructure.rest.serializers import OrganizationalUnitSerializer


class OrganizationalUnitViewSet(viewsets.ModelViewSet):
    queryset = OrganizationalUnit.objects.all()
    serializer_class = OrganizationalUnitSerializer
    permission_classes = [permissions.IsAuthenticated]
