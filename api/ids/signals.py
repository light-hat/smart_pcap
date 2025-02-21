"""
Сигналы.
Здесь они реализованы для автоматической индексации создаваемых объектов пакетов дампа.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import HandledPacket
from .opensearch_client import opensearch_client
from .search_indexes import HANDLED_PACKET_INDEX


@receiver(post_save, sender=HandledPacket)
def index_handled_packet(sender, instance, **kwargs):
    """
    Индексирует объект HandledPacket в OpenSearch при сохранении.
    """
    document = {
        "dump_id": str(instance.dump.id),
        "timestamp": instance.timestamp.isoformat(),
        "source_ip": instance.source_ip,
        "destination_ip": instance.destination_ip,
        "source_port": instance.source_port,
        "destination_port": instance.destination_port,
        "ip_length": instance.ip_length,
        "ip_ttl": instance.ip_ttl,
        "ip_tos": instance.ip_tos,
        "tcp_flags": instance.tcp_flags,
        "label": instance.label,
    }
    opensearch_client.index(
        index=HANDLED_PACKET_INDEX, id=str(instance.id), body=document
    )


@receiver(post_delete, sender=HandledPacket)
def delete_handled_packet(sender, instance, **kwargs):
    """
    Удаляет объект HandledPacket из OpenSearch при удалении.
    """
    opensearch_client.delete(index=HANDLED_PACKET_INDEX, id=str(instance.id))
