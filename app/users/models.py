from django.db import models
from django.contrib.auth.models import AbstractUser

__all__ = ("AppUser", "Team")


class Team(models.Model):
    """
    Модель команды (компании), к которой может принадлежать пользователь.
    """

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Название команды",
        help_text="Уникальное название команды или компании.",
    )
    code = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Код приглашения",
        help_text="Уникальный код для присоединения к команде.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name


class AppUser(AbstractUser):
    """
    Кастомная модель пользователя с поддержкой статусов и привязки к команде.
    """

    STATUS_CHOICES = [
        ("member", "Участник"),
        ("admin", "Администратор"),
    ]
    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="Команда",
        help_text="Команда, к которой принадлежит пользователь.",
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="member",
        verbose_name="Статус доступа",
        help_text="Роль пользователя в команде (участник или администратор).",
    )
    organizational_unit = models.ForeignKey(
        "orgstructure.OrganizationalUnit",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
        verbose_name="Подразделение",
        help_text="Подразделение, к которому принадлежит пользователь.",
    )
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subordinates",
        verbose_name="Руководитель",
        help_text="Руководитель пользователя в оргструктуре.",
    )
    unit_role = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Роль в подразделении",
        help_text="Должность или роль пользователя в подразделении.",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
