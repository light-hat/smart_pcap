import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "rdpahalavan/bert-network-packet-flow-header-payload"

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

dummy_input = {
    "input_ids": torch.randint(low=0, high=model.config.vocab_size, size=(1, 512)),
    "attention_mask": torch.ones((1, 512)),
}

torch.onnx.export(
    model,
    tuple(dummy_input.values()),
    "model.onnx",
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
    },
    opset_version=14,
)
