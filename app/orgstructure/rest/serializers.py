from rest_framework import serializers
from app.orgstructure.models import OrganizationalUnit


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalUnit
        fields = ["id", "name", "team", "parent"]
