"""
Файл для управления индексами OpenSearch.
"""

from .opensearch_client import opensearch_client

# Название индекса для HandledPacket
HANDLED_PACKET_INDEX = "handled_packets"


def create_handled_packet_index():
    """
    Создает индекс для модели HandledPacket.
    """
    index_body = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "dump_id": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "source_ip": {"type": "ip"},
                "destination_ip": {"type": "ip"},
                "source_port": {"type": "integer"},
                "destination_port": {"type": "integer"},
                "ip_length": {"type": "integer"},
                "ip_ttl": {"type": "integer"},
                "ip_tos": {"type": "integer"},
                "tcp_flags": {"type": "keyword"},
                "label": {"type": "text"},
            }
        },
    }

    if not opensearch_client.indices.exists(index=HANDLED_PACKET_INDEX):
        opensearch_client.indices.create(index=HANDLED_PACKET_INDEX, body=index_body)
        print(f"Индекс {HANDLED_PACKET_INDEX} создан.")
    else:
        print(f"Индекс {HANDLED_PACKET_INDEX} уже существует.")
