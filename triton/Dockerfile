FROM python:3.11 AS exporter

WORKDIR /app

RUN pip install --no-cache-dir transformers onnx torch

COPY export_model.py ./

RUN python3 export_model.py

FROM nvcr.io/nvidia/tritonserver:23.01-py3 AS triton_server

COPY --from=exporter /app/model.onnx /models/distilbert_classifier/1/

COPY config.pbtxt /models/distilbert_classifier/config.pbtxt

CMD ["tritonserver", "--model-repository=/models", "--log-verbose=1"]
