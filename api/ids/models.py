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


class HandledPacket(models.Model):
    """
    Модель, описывающая сетевой пакет.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dump = models.ForeignKey(Dump, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    timestamp = models.DateTimeField(verbose_name="Дата и время передачи IP-пакета")
    source_ip = models.CharField(verbose_name="IP отправителя", max_length=15)
    destination_ip = models.CharField(verbose_name="IP получателя", max_length=15)
    source_port = models.IntegerField(verbose_name="Порт источника")
    destination_port = models.IntegerField(verbose_name="Порт назначения")
    ip_length = models.IntegerField(verbose_name="Длина IP-пакета")
    ip_ttl = models.IntegerField(verbose_name="Time to Live (TTL)")
    ip_tos = models.IntegerField(verbose_name=" Type of Service (ToS)")
    # payload = models.TextField(verbose_name="Полезная нагрузка")
    tcp_data_offset = models.IntegerField(verbose_name=" Смещение данных TCP")
    tcp_flags = models.CharField(verbose_name="Флаги TCP", max_length=15)
    inference_input = models.TextField(verbose_name="Данные для инференса")

    label = models.CharField(verbose_name="Метка", max_length=100)

    class Meta:
        verbose_name = "Сетевой пакет"
        verbose_name_plural = "Сетевые пакеты"
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)
