"""
Модуль конфигурации админ-панели для сервиса.
"""

from django.contrib import admin

from .models import Dump, Packet

admin.site.site_title = "Smart IDS"
admin.site.site_header = "Smart IDS admin"
admin.site.index_title = "Admin"


@admin.register(Dump)
class DumpAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Dump.
    """

    list_display = ("id", "user", "state", "created")
    list_display_links = ("id",)
    list_filter = ("state",)


@admin.register(Packet)
class PacketAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Packet.
    """

    list_display = ("id", "dump", "label", "created")
    list_display_links = ("id",)
    list_filter = ("label",)
