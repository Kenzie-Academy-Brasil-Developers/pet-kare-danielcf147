from django.db import models


class SexOptions(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Default = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        choices=SexOptions.choices, max_length=20, default=SexOptions.Default
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        related_name="pets",
        null=False,
    )

    def __repr__(self) -> str:
        return f"<Group ({self.id} - {self.name})>"
