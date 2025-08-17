"""
Асинхронные Celery-таски для обработки дампов памяти.
"""

import os

from celery import shared_task
from django.conf import settings
from ids.models import Dump

@shared_task
def process_dump_file(dump_id: str) -> None:
    """
    Асинхронная задача для обработки PCAP-дампа сетевого трафика.
    :param dump_id: ID созданного в БД объекта дампа.
    """

    dump = Dump.objects.get(id=dump_id)

    try:

        dump_file = os.path.join(str(settings.MEDIA_ROOT), str(dump.source))

        # with PcapReader(dump_file) as pcap:
        #     for pkt in pcap:
        #         if IP in pkt and TCP in pkt:  # IPv4 and TCP
        #             packet_data = processing_packet_conversion(pkt)
        #             if packet_data:
        #                 packet_ml_label = infer_packet_data(packet_data["final_data"])
        #                 packet_object = HandledPacket.objects.create(
        #                     dump=dump,
        #                     timestamp=packet_data["timestamp"],
        #                     source_ip=packet_data["source_ip"],
        #                     destination_ip=packet_data["destination_ip"],
        #                     source_port=packet_data["source_port"],
        #                     destination_port=packet_data["destination_port"],
        #                     ip_length=packet_data["ip_length"],
        #                     ip_ttl=packet_data["ip_ttl"],
        #                     ip_tos=packet_data["ip_tos"],
        #                     # payload=packet_data["payload"],
        #                     tcp_data_offset=packet_data["tcp_data_offset"],
        #                     tcp_flags=packet_data["tcp_flags"],
        #                     inference_input=packet_data["final_data"],
        #                     label=packet_ml_label,
        #                 )
        #                 print(packet_object)

        dump.state = "ready"
        dump.save()

    except Exception as e:
        dump.state = "error"
        dump.details += "\n Error: " + str(e)
        dump.save()

        # print(f"Тип исключения: {type(e)}")
        # print(f"Сообщение исключения: {e}")
        # print(f"Информация об исключении: {repr(e)}")
        # print(
        #     f"Путь к файлу и строка, где произошло исключение: {e.__traceback__.tb_frame.f_code.co_filename}:{e.__traceback__.tb_lineno}"  # pylint: disable=line-too-long
        # )
