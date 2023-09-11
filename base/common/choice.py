from django.db import models


class ChoiceBoolean(models.TextChoices):
    """
    Y, N
    """

    YES = "Y", "예"
    NO = "N", "아니오"