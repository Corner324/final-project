from django.db import models


class OrganizationalUnit(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(
        "users.Team", on_delete=models.CASCADE, related_name="units"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        unique_together = ("name", "team")

    def __str__(self):
        return f"{self.name} ({self.team.name})"
