"""
Модуль, описывающий базу данных сервиса.
"""

import uuid

from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    details = models.TextField(verbose_name="Дополнительная информация")
    created = models.DateTimeField(verbose_name="Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Дамп"
        verbose_name_plural = "Дампы"
        ordering = ["-created"]

    def __str__(self):
        return self.id


class Packet(models.Model):
    """
    Модель, описывающая сетевой пакет.
    TODO: Доработать и продумать метаданные.
    """

    ATTACK_LABELS = (
        ("0", "Analysis"),
        ("1", "Backdoor"),
        ("2", "Bot"),
        ("3", "DDoS"),
        ("4", "DoS"),
        ("5", "DoS GoldenEye"),
        ("6", "DoS Hulk"),
        ("7", "DoS SlowHTTPTest"),
        ("8", "DoS Slowloris"),
        ("9", "Exploits"),
        ("10", "FTP Patator"),
        ("11", "Fuzzers"),
        ("12", "Generic"),
        ("13", "Heartbleed"),
        ("14", "Infiltration"),
        ("15", "Normal"),
        ("16", "Port Scan"),
        ("17", "Reconnaissance"),
        ("18", "SSH Patator"),
        ("19", "Shellcode"),
        ("20", "Web Attack - Brute Force"),
        ("21", "Web Attack - SQL Injection"),
        ("22", "Web Attack - XSS"),
        ("23", "Worms"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dump = models.ForeignKey(Dump, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    label = models.CharField(
        verbose_name="Метка", max_length=100, choices=ATTACK_LABELS, default="0"
    )

    class Meta:
        verbose_name = "Сетевой пакет"
        verbose_name_plural = "Сетевые пакеты"
        ordering = ["-created"]

    def __str__(self):
        return self.id
