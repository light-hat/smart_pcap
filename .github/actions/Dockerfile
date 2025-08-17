FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    make \
    graphviz \
    plantuml \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    sphinx \
    sphinx-rtd-theme \
    sphinx-copybutton \
    sphinxcontrib-mermaid \
    sphinxcontrib-plantuml \
    sphinxcontrib-httpdomain \
    sphinxcontrib-openapi \
    sphinx-autobuild \
    myst-parser \
    autodocsumm

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
