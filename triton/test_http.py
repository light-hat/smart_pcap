"""
Скрипт для тестирования инференса.
"""

import numpy as np
import tritonclient.http as httpclient
from transformers import DistilBertTokenizer

TRITON_SERVER_URL = "127.0.0.1:8000"
MODEL_NAME = "distilbert_classifier"


def prepare_input(text):
    """
    Токенизация входных данных.
    """
    tokenizer = DistilBertTokenizer.from_pretrained(
        "rdpahalavan/bert-network-packet-flow-header-payload"
    )
    inputs = tokenizer(
        text, return_tensors="np", padding="max_length", truncation=True, max_length=512
    )
    return inputs["input_ids"], inputs["attention_mask"]


def softmax(logits):
    """
    Интерпретация результатов инференса модели.
    """
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def main():
    """
    Основная логика скрипта.
    """

    try:
        id2label = {
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

        client = httpclient.InferenceServerClient(url=TRITON_SERVER_URL)

        if not client.is_model_ready(MODEL_NAME):
            raise Exception(f"Model {MODEL_NAME} is not ready on the server")

        text = "0 0 141 -1 80 63713 2960 2920 64 0 5 0 -1 119 10 32 32 32 32 32 32 32 32 60 47 100 105 118 62 10 32 32 32 32 32 32 32 32 60 100 105 118 32 99 108 97 115 115 61 34 99 111 110 116 101 110 116 95 115 101 99 116 105 111 110 95 116 101 120 116 34 62 10 32 32 32 32 32 32 32 32 32 32 60 112 62 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 85 98 117 110 116 117 39 115 32 65 112 97 99 104 101 50 32 100 101 102 97 117 108 116 32 99 111 110 102 105 103 117 114 97 116 105 111 110 32 105 115 32 100 105 102 102 101 114 101 110 116 32 102 114 111 109 32 116 104 101 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 117 112 115 116 114 101 97 109 32 100 101 102 97 117 108 116 32 99 111 110 102 105 103 117 114 97 116 105 111 110 44 32 97 110 100 32 115 112 108 105 116 32 105 110 116 111 32 115 101 118 101 114 97 108 32 102 105 108 101 115 32 111 112 116 105 109 105 122 101 100 32 102 111 114 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 105 110 116 101 114 97 99 116 105 111 110 32 119 105 116 104 32 85 98 117 110 116 117 32 116 111 111 108 115 46 32 84 104 101 32 99 111 110 102 105 103 117 114 97 116 105 111 110 32 115 121 115 116 101 109 32 105 115 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 60 98 62 102 117 108 108 121 32 100 111 99 117 109 101 110 116 101 100 32 105 110 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 47 117 115 114 47 115 104 97 114 101 47 100 111 99 47 97 112 97 99 104 101 50 47 82 69 65 68 77 69 46 68 101 98 105 97 110 46 103 122 60 47 98 62 46 32 82 101 102 101 114 32 116 111 32 116 104 105 115 32 102 111 114 32 116 104 101 32 102 117 108 108 10 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 100 111 99 117 109 101 110 116 97 116 105 111 110 46 32 68 111 99 117 109 101 110 116 97 116 105 111 110 32 102 111 114 32 116 104 101 32 119 101 98"  # pylint: disable=line-too-long

        input_ids, attention_mask = prepare_input(text)

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
        predicted_label = id2label[predicted_class]
        print("Predicted label:", predicted_label)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
