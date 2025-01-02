from celery import shared_task
from ids.models import Dump
from scapy.all import *
import tritonclient.http as httpclient
import numpy as np
from transformers import DistilBertTokenizer
from typing import Union

TRITON_SERVER_URL = "triton:8000"

MODEL_NAME = "distilbert_classifier"

ID2LABEL = {
    0: "Analysis",
    1: "Backdoor",
    2: "Bot",
    3: "DDoS",
    4: "DoS",
    5: "DoS GoldenEye",
    6: "DoS Hulk",
    7: "DoS SlowHTTPTest",
    8: "DoS Slowloris",
    9: "Exploits",
    10: "FTP Patator",
    11: "Fuzzers",
    12: "Generic",
    13: "Heartbleed",
    14: "Infiltration",
    15: "Normal",
    16: "Port Scan",
    17: "Reconnaissance",
    18: "SSH Patator",
    19: "Shellcode",
    20: "Web Attack - Brute Force",
    21: "Web Attack - SQL Injection",
    22: "Web Attack - XSS",
    23: "Worms"
}

def processing_packet_conversion(packet: Union[scapy.packet.Packet, scapy.layers.l2.Ether]) -> str:
    """
    Преобразование сетевого пакета, который мы извлекли из
    дампа, в строковое представление.
    :param packet: Объект сетевого пакета, который нужно обработать.
    :return: Строка с извлеченными характеристиками сетевого пакета.
    """
    # Clone the packet for processing without modifying the original.
    packet_2 = packet

    while packet_2:
        # Extract and count protocol layers in the packet.
        layer = packet_2[0]
        if layer.name not in protocol_counts:
            protocol_counts[layer.name] = 0
        else:
            protocol_counts[layer.name] += 1
        protocols.append(layer.name)

        # Break if there are no more payload layers.
        if not layer.payload:
            break
        packet_2 = layer.payload

    # Extract relevant information for feature creation.
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_port = packet.sport
    dst_port = packet.dport
    ip_length = len(packet[IP])
    ip_ttl = packet[IP].ttl
    ip_tos = packet[IP].tos
    tcp_data_offset = packet[TCP].dataofs
    tcp_flags = packet[TCP].flags

    # Process payload content and create a feature string.
    payload_bytes = bytes(packet.payload)
    payload_length = len(payload_bytes)
    payload_content = payload_bytes.decode('utf-8', 'replace')
    payload_decimal = ' '.join(str(byte) for byte in payload_bytes)
    final_data = "0" + " " + "0" + " " + "195" + " " + "-1" + " " + str(src_port) + " " + str(dst_port) + " " + str(ip_length) + " " + str(payload_length) + " " + str(ip_ttl) + " " + str(ip_tos) + " " + str(tcp_data_offset) + " " + str(int(tcp_flags)) + " " + "-1" + " " + str(payload_decimal)
    return final_data

def prepare_input(text: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Токенизация пакета перед инференсом.
    :param text: Пакет, приведённый к строковому формату.
    :return: Токенизированное значение и attention mask.
    """
    tokenizer = DistilBertTokenizer.from_pretrained("rdpahalavan/bert-network-packet-flow-header-payload")
    inputs = tokenizer(
        text,
        return_tensors="np",
        padding="max_length",
        truncation=True,
        max_length=512
    )
    return inputs["input_ids"], inputs["attention_mask"]

def softmax(logits: np.ndarray) -> np.ndarray:
    """
    Интерпретация ответа от модели.
    :param logits: Значение, которое вернула модель.
    :return: Метка класса (числовая).
    """
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

@shared_task
def process_dump_file(dump_id: str) -> None:
    """
    Асинхронная задача для обработки PCAP-дампа сетевого трафика.
    :param dump_id: ID созданного в БД объекта дампа.
    """

    dump = Dump.objects.get(id=dump_id)

    try:
        dump.status = "processing"
        dump.save()

        # ...

        dump.status = "ready"
        dump.result = result
        dump.save()

    except Exception as e:
        dump.status = "error"
        dump.result = str(e)
        dump.save()






