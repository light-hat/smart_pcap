<h1 align="center"> Smart IDS </h1>

<p align="center">
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Unit test status" src="https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pylint status" src="https://github.com/light-hat/smart_ids/workflows/Pylint/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Bandit SAST status" src="https://github.com/light-hat/smart_ids/workflows/SAST/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

<p align="center">
Веб-сервис, который выявляет сетевые атаки методами ML. В проекте реализуется инференс с аппаратным ускорением на GPU, асинхронная обработка PCAP-дампов сетевого трафика, гибкий поиск по результатам обработки, мониторинг веб-сервиса и интеграцию с SIEM-системами (в будущем).
</p>

<p align="center">
<i>Read this in other languages: </i> 
<a href="https://github.com/light-hat/smart_ids/blob/master/Readme.md">English</a>,
Русский.
</p>

<h2 align="center"> Стек </h2>

<p align="center">

<img src="https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white">
<img src="https://img.shields.io/badge/cuda-000000.svg?style=for-the-badge&logo=nVIDIA&logoColor=green">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
<img src="https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4">
<img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white">
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white">
<img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white">
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">

</p>

## Содержание

<!-- TOC -->
  * [Содержание](#содержание)
  * [Пару слов о модели](#пару-слов-о-модели)
  * [Требования](#требования)
    * [Аппаратное окружение](#аппаратное-окружение)
    * [Программное окружение](#программное-окружение)
  * [Развёртывание](#развёртывание)
    * [Подготовка сервера](#подготовка-сервера)
    * [Конфигурирование](#конфигурирование)
    * [Запуск проекта](#запуск-проекта)
  * [Эксплуатация](#эксплуатация)
    * [Документация API](#документация-api)
    * [Административная панель](#административная-панель)
<!-- TOC -->

## Пару слов о модели

Для инференса взята модель [rdpahalavan/bert-network-packet-flow-header-payload](https://huggingface.co/rdpahalavan/bert-network-packet-flow-header-payload) на Hugging Face.

Ноутбук с подробностями о модели можно найти [здесь](https://github.com/TPs-ESIR-S9/PcapFileAnalysis/blob/main/NetworkPcapAnalysis.ipynb).

Модель классифицирует пакеты на 24 класса:

```python
['Analysis',
 'Backdoor',
 'Bot',
 'DDoS',
 'DoS',
 'DoS GoldenEye',
 'DoS Hulk',
 'DoS SlowHTTPTest',
 'DoS Slowloris',
 'Exploits',
 'FTP Patator',
 'Fuzzers',
 'Generic',
 'Heartbleed',
 'Infiltration',
 'Normal',
 'Port Scan',
 'Reconnaissance',
 'SSH Patator',
 'Shellcode',
 'Web Attack - Brute Force',
 'Web Attack - SQL Injection',
 'Web Attack - XSS',
 'Worms']
```

## Требования

| Зависимость | Значение     |
|-------------|--------------|
| CPU         | `4 ядра`     |
| RAM         | `32 Гб`      |
| Disk        | `150 Гб`     |
| GPU         | `16 Гб VRAM` |

## Развёртывание

> [!NOTE]
> Тестирование проводилось на сервере с Ubuntu 22.04 с GPU Tesla T4.

### Подготовка сервера

> [!TIP]
> Для начала стоит установить Docker и Docker Compose на ваш сервер по этой [инструкции](https://docs.docker.com/engine/install/ubuntu/) с официального сайта Docker.

Когда установлен `Docker`, проверьте драйвера видеокарты:

```shell
nvidia-smi
```

<details>
  <summary>👀 Что примерно должно быть в ответе</summary>

<hr />

```
Sat Jan  4 01:37:28 2025       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.183.01             Driver Version: 535.183.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       Off | 00000000:00:06.0 Off |                  Off |
| N/A   49C    P0              28W /  70W |    783MiB / 16384MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

<hr />

</details>

<details>
  <summary>👀 Как поставить драйвера на GPU</summary>

<hr />

Устанавливаем инструменты для компиляции драйверов и заголовки ядра:

```shell
sudo apt update
sudo apt-get install build-essential linux-headers-$(uname -r)
```

Ищем доступные версии драйвера:

```shell
ubuntu-drivers devices
```

Находим в выводе похожую строчку:

```text
...
driver   : nvidia-driver-535 - distro non-free recommended
...
```

Это версия драйвера, которую вам нужно установить. Делаем это:

```shell
sudo apt-get install nvidia-driver-535
```

Затем перезапускаем сервер:

```shell
sudo reboot
```

После перезагрузки снова проверяем драйвера GPU:

```shell
nvidia-smi
```

<hr />

</details>

После этого проверьте, установлен ли на сервере `NVIDIA Container Toolkit`:

```shell
dpkg -l | grep nvidia-container-toolkit
```

<details>
  <summary>👀 Что примерно должно быть в ответе</summary>

<hr />

```
ii  nvidia-container-toolkit          1.17.3-1          amd64     NVIDIA Container toolkit
ii  nvidia-container-toolkit-base     1.17.3-1          amd64     NVIDIA Container Toolkit Base

```

<hr />

</details>

> [!TIP]
> Если в этом ответе пусто, вот [мануал](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) c официального сайта как установить NVIDIA Container Toolkit.

### Конфигурирование

Для начала клонируйте репозиторий:

```shell
git clone https://github.com/light-hat/smart_ids
cd smart_ids
```

В корне репозитория создайте `.env` файл со следующим содержимым:

```
API_URL=127.0.0.1
API_PORT=80
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=shop_database
GF_SECURITY_ADMIN_PASSWORD=admin
GF_SECURITY_ADMIN_USER=admin
```

Переменные окружения в конфигурации:

- `API_URL`: адрес, на котором будет развёрнут сервис;

- `API_PORT`: порт, на котором будет принимать запросы сервис;

- `POSTGRES_HOST`: хост базы данных (имя сервиса в стеке приложений);

- `POSTGRES_PORT`: порт базы данных;

- `POSTGRES_USER`: пользователь базы данных;

- `POSTGRES_PASSWORD`: пароль от базы данных;

- `POSTGRES_DB`: имя базы данных, используемой сервисом;

- `GF_SECURITY_ADMIN_PASSWORD`: имя пользователя для авторизации в Grafana;

- `GF_SECURITY_ADMIN_USER`: пароль для авторизации в Grafana.

Можете сделать это автоматически через скрипт:

```shell
./configure.sh
```

### Запуск проекта

Запустите стек приложений на Docker следующей командой:

```shell
docker-compose up -d --build
```

<details>
  <summary>👀 Как выглядит здоровый лог при запуске</summary>

<hr />

Лог инференса:

```shell
sudo docker compose logs triton
```

```text
triton-1  | 
triton-1  | =============================
triton-1  | == Triton Inference Server ==
triton-1  | =============================
triton-1  | 
triton-1  | NVIDIA Release 23.01 (build 52277748)
triton-1  | Triton Server Version 2.30.0
triton-1  | 
triton-1  | Copyright (c) 2018-2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
triton-1  | 
triton-1  | Various files include modifications (c) NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
triton-1  | 
triton-1  | This container image and its contents are governed by the NVIDIA Deep Learning Container License.
triton-1  | By pulling and using the container, you accept the terms and conditions of this license:
triton-1  | https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
triton-1  | 
triton-1  | I0104 00:22:29.587736 1 pinned_memory_manager.cc:240] Pinned memory pool is created at '0x7f438a000000' with size 268435456
triton-1  | I0104 00:22:29.591405 1 cuda_memory_manager.cc:105] CUDA memory pool is created on device 0 with size 67108864
triton-1  | I0104 00:22:29.596887 1 model_lifecycle.cc:459] loading: distilbert_classifier:1
triton-1  | I0104 00:22:29.599877 1 onnxruntime.cc:2459] TRITONBACKEND_Initialize: onnxruntime
triton-1  | I0104 00:22:29.599965 1 onnxruntime.cc:2469] Triton TRITONBACKEND API version: 1.11
triton-1  | I0104 00:22:29.600015 1 onnxruntime.cc:2475] 'onnxruntime' TRITONBACKEND API version: 1.11
triton-1  | I0104 00:22:29.600051 1 onnxruntime.cc:2505] backend configuration:
triton-1  | {"cmdline":{"auto-complete-config":"true","min-compute-capability":"6.000000","backend-directory":"/opt/tritonserver/backends","default-max-batch-size":"4"}}
triton-1  | I0104 00:22:29.622589 1 onnxruntime.cc:2563] TRITONBACKEND_ModelInitialize: distilbert_classifier (version 1)
triton-1  | I0104 00:22:29.623700 1 onnxruntime.cc:666] skipping model configuration auto-complete for 'distilbert_classifier': inputs and outputs already specified
triton-1  | I0104 00:22:29.624518 1 onnxruntime.cc:2606] TRITONBACKEND_ModelInstanceInitialize: distilbert_classifier (GPU device 0)
triton-1  | 2025-01-04 00:22:30.303281404 [W:onnxruntime:, session_state.cc:1030 VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
triton-1  | 2025-01-04 00:22:30.303326346 [W:onnxruntime:, session_state.cc:1032 VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
triton-1  | I0104 00:22:30.591136 1 model_lifecycle.cc:694] successfully loaded 'distilbert_classifier' version 1
triton-1  | I0104 00:22:30.591333 1 server.cc:563] 
triton-1  | +------------------+------+
triton-1  | | Repository Agent | Path |
triton-1  | +------------------+------+
triton-1  | +------------------+------+
triton-1  | 
triton-1  | I0104 00:22:30.591412 1 server.cc:590] 
triton-1  | +-------------+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | | Backend     | Path                                                            | Config                                                                                                                                                        |
triton-1  | +-------------+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | | onnxruntime | /opt/tritonserver/backends/onnxruntime/libtriton_onnxruntime.so | {"cmdline":{"auto-complete-config":"true","min-compute-capability":"6.000000","backend-directory":"/opt/tritonserver/backends","default-max-batch-size":"4"}} |
triton-1  | +-------------+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | 
triton-1  | I0104 00:22:30.591520 1 server.cc:633] 
triton-1  | +-----------------------+---------+--------+
triton-1  | | Model                 | Version | Status |
triton-1  | +-----------------------+---------+--------+
triton-1  | | distilbert_classifier | 1       | READY  |
triton-1  | +-----------------------+---------+--------+
triton-1  | 
triton-1  | I0104 00:22:30.668177 1 metrics.cc:864] Collecting metrics for GPU 0: Tesla T4
triton-1  | I0104 00:22:30.669197 1 metrics.cc:757] Collecting CPU metrics
triton-1  | I0104 00:22:30.669509 1 tritonserver.cc:2264] 
triton-1  | +----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | | Option                           | Value                                                                                                                                                                                                |
triton-1  | +----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | | server_id                        | triton                                                                                                                                                                                               |
triton-1  | | server_version                   | 2.30.0                                                                                                                                                                                               |
triton-1  | | server_extensions                | classification sequence model_repository model_repository(unload_dependents) schedule_policy model_configuration system_shared_memory cuda_shared_memory binary_tensor_data statistics trace logging |
triton-1  | | model_repository_path[0]         | /models/                                                                                                                                                                                             |
triton-1  | | model_control_mode               | MODE_NONE                                                                                                                                                                                            |
triton-1  | | strict_model_config              | 0                                                                                                                                                                                                    |
triton-1  | | rate_limit                       | OFF                                                                                                                                                                                                  |
triton-1  | | pinned_memory_pool_byte_size     | 268435456                                                                                                                                                                                            |
triton-1  | | cuda_memory_pool_byte_size{0}    | 67108864                                                                                                                                                                                             |
triton-1  | | response_cache_byte_size         | 0                                                                                                                                                                                                    |
triton-1  | | min_supported_compute_capability | 6.0                                                                                                                                                                                                  |
triton-1  | | strict_readiness                 | 1                                                                                                                                                                                                    |
triton-1  | | exit_timeout                     | 30                                                                                                                                                                                                   |
triton-1  | +----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
triton-1  | 
triton-1  | I0104 00:22:30.673629 1 grpc_server.cc:4819] Started GRPCInferenceService at 0.0.0.0:8001
triton-1  | I0104 00:22:30.674047 1 http_server.cc:3477] Started HTTPService at 0.0.0.0:8000
triton-1  | I0104 00:22:30.715444 1 http_server.cc:184] Started Metrics Service at 0.0.0.0:8002
```

Лог API:

```shell
sudo docker compose logs api
```

```text
api-1  | DB not yet run...
api-1  | DB did run.
api-1  | Migrations for 'ids':
api-1  |   ids/migrations/0001_initial.py
api-1  |     + Create model Dump
api-1  |     + Create model HandledPacket
api-1  | Operations to perform:
api-1  |   Apply all migrations: admin, auth, contenttypes, ids, sessions
api-1  | Running migrations:
api-1  |   Applying contenttypes.0001_initial... OK
api-1  |   Applying auth.0001_initial... OK
api-1  |   Applying admin.0001_initial... OK
api-1  |   Applying admin.0002_logentry_remove_auto_add... OK
api-1  |   Applying admin.0003_logentry_add_action_flag_choices... OK
api-1  |   Applying contenttypes.0002_remove_content_type_name... OK
api-1  |   Applying auth.0002_alter_permission_name_max_length... OK
api-1  |   Applying auth.0003_alter_user_email_max_length... OK
api-1  |   Applying auth.0004_alter_user_username_opts... OK
api-1  |   Applying auth.0005_alter_user_last_login_null... OK
api-1  |   Applying auth.0006_require_contenttypes_0002... OK
api-1  |   Applying auth.0007_alter_validators_add_error_messages... OK
api-1  |   Applying auth.0008_alter_user_username_max_length... OK
api-1  |   Applying auth.0009_alter_user_last_name_max_length... OK
api-1  |   Applying auth.0010_alter_group_name_max_length... OK
api-1  |   Applying auth.0011_update_proxy_permissions... OK
api-1  |   Applying auth.0012_alter_user_first_name_max_length... OK
api-1  |   Applying ids.0001_initial... OK
api-1  |   Applying sessions.0001_initial... OK
api-1  | [2025-01-04 00:22:48 +0000] [76] [INFO] Starting gunicorn 23.0.0
api-1  | [2025-01-04 00:22:48 +0000] [76] [INFO] Listening at: http://0.0.0.0:8000 (76)
api-1  | [2025-01-04 00:22:48 +0000] [76] [INFO] Using worker: sync
api-1  | [2025-01-04 00:22:48 +0000] [77] [INFO] Booting worker with pid: 77
```

Лог воркера:

```shell
sudo docker compose logs worker
```

```text
worker-1  | User information: uid=0 euid=0 gid=0 egid=0
worker-1  | 
worker-1  |   warnings.warn(SecurityWarning(ROOT_DISCOURAGED.format(
worker-1  |  
worker-1  |  -------------- celery@0a10f82c8415 v5.4.0 (opalescent)
worker-1  | --- ***** ----- 
worker-1  | -- ******* ---- Linux-5.15.0-130-generic-x86_64-with-glibc2.36 2025-01-04 03:22:34
worker-1  | - *** --- * --- 
worker-1  | - ** ---------- [config]
worker-1  | - ** ---------- .> app:         config:0x7f543c451df0
worker-1  | - ** ---------- .> transport:   redis://redis:6379//
worker-1  | - ** ---------- .> results:     redis://redis:6379/
worker-1  | - *** --- * --- .> concurrency: 4 (prefork)
worker-1  | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
worker-1  | --- ***** ----- 
worker-1  |  -------------- [queues]
worker-1  |                 .> celery           exchange=celery(direct) key=celery
worker-1  |                 
worker-1  | 
worker-1  | [tasks]
worker-1  |   . ids.tasks.process_dump_file

```

<hr />

</details>

## Эксплуатация

### Документация API

API задокументирован при помощи Swagger (`drf-spectacular`).

Тестирование API: `http://127.0.0.1/api/docs/`

YAML: `http://127.0.0.1/api/schema/`

### Административная панель

Админка сервиса доступна по адресу `http://127.0.0.1/admin`.

Учётные данные для первого входа: `admin:admin`.

> [!IMPORTANT]
> Учётные данные рекомендуется сменить сразу после развёртывания на более устойчивые.
