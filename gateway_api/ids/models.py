"""
Модуль, описывающий базу данных сервиса.
"""

import uuid

from django.core.validators import FileExtensionValidator
from django.db import models


class Dump(models.Model):
    """
    Модель, описывающая загруженный на обработку дамп трафика.
    """

    STATE_LABELS = (
        ("processing", "В обработке"),
        ("ready", "Готово"),
        ("error", "Ошибка анализа"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        verbose_name="Название дампа", max_length=100, null=True, blank=True
    )
    source = models.FileField(
        verbose_name="Дамп",
        upload_to="dumps/",
        validators=[FileExtensionValidator(allowed_extensions=["pcap"])],
    )
    state = models.CharField(
        verbose_name="Статус",
        max_length=100,
        choices=STATE_LABELS,
        default="processing",
    )
    details = models.TextField(
        verbose_name="Дополнительная информация", null=True, blank=True
    )
    created = models.DateTimeField(verbose_name="Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Дамп"
        verbose_name_plural = "Дампы"
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)
