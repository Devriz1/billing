from django.db import models


class BaseModel(models.Model):
    """
    Base model inherited by all models in the project.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True