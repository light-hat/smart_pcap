"""
Асинхронные Celery-таски для обработки дампов памяти.
"""

import os
from datetime import datetime
from typing import Union

import numpy as np
import tritonclient.http as httpclient
from celery import shared_task
from django.conf import settings
from ids.models import Dump, HandledPacket
from scapy.all import *
from transformers import DistilBertTokenizer

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
    23: "Worms",
}


def processing_packet_conversion(
    packet: Union[scapy.packet.Packet, scapy.layers.l2.Ether]
) -> str:
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
    payload_content = payload_bytes.decode("utf-8", "replace")
    payload_decimal = " ".join(str(byte) for byte in payload_bytes)
    final_data = (
        "0"
        + " "
        + "0"
        + " "
        + "195"
        + " "
        + "-1"
        + " "
        + str(src_port)
        + " "
        + str(dst_port)
        + " "
        + str(ip_length)
        + " "
        + str(payload_length)
        + " "
        + str(ip_ttl)
        + " "
        + str(ip_tos)
        + " "
        + str(tcp_data_offset)
        + " "
        + str(int(tcp_flags))
        + " "
        + "-1"
        + " "
        + str(payload_decimal)
    )

    return {
        "timestamp": datetime.fromtimestamp(float(packet.time)),
        "source_ip": src_ip,
        "destination_ip": dst_ip,
        "source_port": src_port,
        "destination_port": dst_port,
        "ip_length": ip_length,
        "ip_ttl": ip_ttl,
        "ip_tos": ip_tos,
        "payload": str(payload_content),
        "tcp_data_offset": tcp_data_offset,
        "tcp_flags": str(tcp_flags),
        "final_data": final_data,
    }


def prepare_input(text: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Токенизация пакета перед инференсом.
    :param text: Пакет, приведённый к строковому формату.
    :return: Токенизированное значение и attention mask.
    """
    tokenizer = DistilBertTokenizer.from_pretrained(
        "rdpahalavan/bert-network-packet-flow-header-payload"
    )
    inputs = tokenizer(
        text, return_tensors="np", padding="max_length", truncation=True, max_length=512
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


def infer_packet_data(inference_input: str) -> str:
    """
    Выполняет инференс через Triton.
    :param inference_input: Входные данные пакета для инференса.
    :return: Метка класса.
    """

    try:

        client = httpclient.InferenceServerClient(url=TRITON_SERVER_URL)

        if not client.is_model_ready(MODEL_NAME):
            raise Exception(f"Model {MODEL_NAME} is not ready on the server")

        input_ids, attention_mask = prepare_input(inference_input)

        inputs = [
            httpclient.InferInput("input_ids", input_ids.shape, "INT64"),
            httpclient.InferInput("attention_mask", attention_mask.shape, "FP32"),
        ]

        inputs[0].set_data_from_numpy(input_ids.astype(np.int64))
        inputs[1].set_data_from_numpy(attention_mask.astype(np.float32))

        outputs = [httpclient.InferRequestedOutput("logits")]

        response = client.infer(model_name=MODEL_NAME, inputs=inputs, outputs=outputs)

        logits = response.as_numpy("logits")
        probabilities = softmax(logits)
        predicted_class = np.argmax(probabilities, axis=-1)[0]

        return ID2LABEL[predicted_class]

    except Exception as e:
        print("Inference error: ", str(e))
        return "Error"


@shared_task
def process_dump_file(dump_id: str) -> None:
    """
    Асинхронная задача для обработки PCAP-дампа сетевого трафика.
    :param dump_id: ID созданного в БД объекта дампа.
    """

    dump = Dump.objects.get(id=dump_id)

    try:

        dump_file = os.path.join(str(settings.MEDIA_ROOT), str(dump.source))

        with PcapReader(dump_file) as pcap:
            for pkt in pcap:
                if IP in pkt and TCP in pkt:  # IPv4 and TCP
                    packet_data = processing_packet_conversion(pkt)
                    if packet_data:
                        packet_ml_label = infer_packet_data(packet_data["final_data"])
                        packet_object = HandledPacket.objects.create(
                            dump=dump,
                            timestamp=packet_data["timestamp"],
                            source_ip=packet_data["source_ip"],
                            destination_ip=packet_data["destination_ip"],
                            source_port=packet_data["source_port"],
                            destination_port=packet_data["destination_port"],
                            ip_length=packet_data["ip_length"],
                            ip_ttl=packet_data["ip_ttl"],
                            ip_tos=packet_data["ip_tos"],
                            # payload=packet_data["payload"],
                            tcp_data_offset=packet_data["tcp_data_offset"],
                            tcp_flags=packet_data["tcp_flags"],
                            inference_input=packet_data["final_data"],
                            label=packet_ml_label,
                        )
                        print(packet_object)

        dump.state = "ready"
        dump.save()

    except Exception as e:
        dump.state = "error"
        dump.details += "\n Error: " + str(e)
        dump.save()

        print(f"Тип исключения: {type(e)}")
        print(f"Сообщение исключения: {e}")
        print(f"Информация об исключении: {repr(e)}")
        print(
            f"Путь к файлу и строка, где произошло исключение: {e.__traceback__.tb_frame.f_code.co_filename}:{e.__traceback__.tb_lineno}"  # pylint: disable=line-too-long
        )
