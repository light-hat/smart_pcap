"""
Модуль конфигурации админ-панели для сервиса.
"""

from django.contrib import admin

from ids.models import Dump, HandledPacket

admin.site.site_title = "Smart IDS"
admin.site.site_header = "Smart IDS admin"
admin.site.index_title = "Admin"


@admin.register(Dump)
class DumpAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Dump.
    """

    list_display = ("id", "state", "created")
    list_display_links = ("id",)
    list_filter = ("state",)


@admin.register(HandledPacket)
class PacketAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Packet.
    """

    list_display = (
        "id",
        "dump",
        "label",
        "timestamp",
        "source_ip",
        "destination_ip",
        "source_port",
        "destination_port",
        "ip_length",
        "ip_ttl",
        "ip_tos",
        "tcp_data_offset",
        "tcp_flags",
    )
    list_display_links = ("id",)
    list_filter = (
        "dump",
        "label",
    )
