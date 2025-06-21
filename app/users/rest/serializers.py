from rest_framework import serializers

from app.users.models import AppUser, Team


class AppUserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("username",)


class AppUserRegisterSerializer(serializers.ModelSerializer):
    team_code = serializers.CharField(write_only=True, help_text="Код приглашения в команду")
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
    class Meta:
        model = AppUser
        fields = ("email", "status")
        read_only_fields = ("status",)  # Только админ может менять статус
