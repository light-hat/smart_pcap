"""
Инициализация клиента OpenSearch.
"""

from django.conf import settings
from opensearchpy import OpenSearch

opensearch_client = OpenSearch(
    hosts=[{"host": "opensearch", "port": 9200, "scheme": "https"}],
    http_auth=("admin", settings.OPENSEARCH_ADMIN_PASS),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)
