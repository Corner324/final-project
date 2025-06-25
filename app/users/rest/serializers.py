from rest_framework import serializers

from app.users.models import AppUser, Team
from app.orgstructure.models import OrganizationalUnit


class AppUserPreviewSerializer(serializers.ModelSerializer):
    organizational_unit = serializers.StringRelatedField(read_only=True)
    manager = serializers.StringRelatedField(read_only=True)
    unit_role = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = AppUser
        fields = ("username", "organizational_unit", "manager", "unit_role", "status")


class AppUserRegisterSerializer(serializers.ModelSerializer):
    team_code = serializers.CharField(
        write_only=True, help_text="Код приглашения в команду"
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = AppUser
        fields = ("username", "password", "email", "team_code")

    def validate_team_code(self, value):
        if not Team.objects.filter(code=value).exists():
            raise serializers.ValidationError("Команда с таким кодом не найдена.")
        return value

    def create(self, validated_data):
        team_code = validated_data.pop("team_code")
        team = Team.objects.get(code=team_code)
        user = AppUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            team=team,
        )
        return user


class AppUserUpdateSerializer(serializers.ModelSerializer):
    organizational_unit = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationalUnit.objects.all(), required=False
    )
    manager = serializers.PrimaryKeyRelatedField(
        queryset=AppUser.objects.all(), required=False
    )
    unit_role = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = AppUser
        fields = ("email", "status", "organizational_unit", "manager", "unit_role")
        read_only_fields = ("status",)  # Только админ может менять статус


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("status",)


class UserUnitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("organizational_unit", "manager", "unit_role")
