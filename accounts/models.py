from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    business = models.ForeignKey(
        "business.Business",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    phone = models.CharField(max_length=20, blank=True)

    profile_image = models.ImageField(
        upload_to="users/profile/",
        blank=True,
        null=True,
    )

    is_owner = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.get_full_name() or self.username