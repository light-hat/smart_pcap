<h1 align="center"> Smart IDS </h1>

<p align="center">
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Unit test status" src="https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Unit test status" src="https://github.com/light-hat/smart_ids/workflows/Unit%20testing/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pylint status" src="https://github.com/light-hat/smart_ids/workflows/Pylint/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Bandit SAST status" src="https://github.com/light-hat/smart_ids/workflows/SAST/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Flight-hat%2Fsmart_ids?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Flight-hat%2Fsmart_ids.svg?type=shield"/></a>
</p>

<p align="center">
A web service that detects network attacks using ML methods. The project implements GPU-accelerated inference, asynchronous processing of PCAP dumps of network traffic, flexible search based on processing results, web service monitoring and integration with SIEM systems (in the future).
</p>

<p align="center">
<i>Read this in other languages: </i> 
English
<a href="https://github.com/light-hat/smart_ids/blob/master/Readme.ru.md">Русский</a>.
</p>

<h2 align="center"> Tech stack </h2>

<p align="center">

<img src="https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white">
<img src="https://img.shields.io/badge/cuda-000000.svg?style=for-the-badge&logo=nVIDIA&logoColor=green">
<img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white">
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

## Contents

<!-- TOC -->
  * [Contents](#contents)
  * [About model](#about-model)
  * [Requirements](#requirements)
    * [Hardware environment](#hardware-environment)
    * [Software environment](#software-environment)
  * [Deployment](#deployment)
    * [Preparing the server](#preparing-the-server)
    * [Configuration](#configuration)
    * [Run](#run)
  * [Operation](#operation)
    * [API Documentation](#api-documentation)
    * [Admin panel](#admin-panel)
<!-- TOC -->

## About model

The [rdpahalavan/bert-network-packet-flow-header-payload](https://huggingface.co/rdpahalavan/bert-network-packet-flow-header-payload) ML model was used to detect attacks.

A Jupyter Notebook with model details is [here](https://github.com/TPs-ESIR-S9/PcapFileAnalysis/blob/main/NetworkPcapAnalysis.ipynb).

The model has 24 output classes:

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

## Requirements

### Hardware environment

| Requirement | Minimum        | Recommended  |
|-------------|----------------|--------------|
| CPU         | `6 cores`      | `12 cores`   |
| RAM         | `16 GB`        | `32 GB`      |
| Disk        | `80 GB`        | `150 GB`     |
| GPU         | `8-16 GB VRAM` | `32 GB VRAM` |

### Software environment

> [!TIP]
> The operating system, in principle, does not matter if the requirements for the software and hardware environment are met.

| Requirement              | Minimum version     | Recommended version            |
|--------------------------|---------------------|--------------------------------|
| Docker                   | `19.03`             | `20.10 or higher`              |
| Docker Compose           | `1.27`              | `1.29 or higher`               |
| NVIDIA drivers           | `418.87`            | `latest stable version`        |
| CUDA                     | `11.0`              | `latest stable version`        |
| NVIDIA Container Toolkit | `1.0`               | `latest stable version`        |

## Deployment

> [!NOTE]
> Testing was carried out on a server running Ubuntu 22.04 with a Tesla T4 GPU.

### Preparing the server

> [!TIP]
> First, you should install Docker and Docker Compose on your server using this [instruction](https://docs.docker.com/engine/install/ubuntu/) from the official Docker website.

When `Docker` is installed, check your GPU drivers:

```shell
nvidia-smi
```

<details>
  <summary>👀 What should be in the answer?</summary>

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
  <summary>👀 How to install drivers for GPU?</summary>

<hr />

Install tools for compiling drivers and kernel headers:

```shell
sudo apt update
sudo apt-get install build-essential linux-headers-$(uname -r)
```

Next, find the available driver versions:

```shell
ubuntu-drivers devices
```

Find a similar line in the output:

```text
...
driver   : nvidia-driver-535 - distro non-free recommended
...
```

This is the driver version you need to install. Let's do this:

```shell
sudo apt-get install nvidia-driver-535
```

Then restart the server:

```shell
sudo reboot
```

After rebooting, check your GPU drivers again:

```shell
nvidia-smi
```

<hr />

</details>

After that, check if the `NVIDIA Container Toolkit` is installed on the server:

```shell
dpkg -l | grep nvidia-container-toolkit
```

<details>
  <summary>👀 What should be in the answer?</summary>

<hr />

```
ii  nvidia-container-toolkit          1.17.3-1          amd64     NVIDIA Container toolkit
ii  nvidia-container-toolkit-base     1.17.3-1          amd64     NVIDIA Container Toolkit Base

```

<hr />

</details>

> [!TIP]
> If this answer is empty, here is a [manual](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) from the official website on how to install NVIDIA Container Toolkit.

### Configuration

First, clone the repository:

```shell
git clone https://github.com/light-hat/smart_ids
cd smart_ids
```

In the root of the repository, create a `.env` file with the following content:

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

Environment variables in the configuration:

- `API_URL`: URL where the service will be deployed;

- `API_PORT`: port on which the service will receive requests;

- `POSTGRES_HOST`: database host (service name in the docker compose stack);

- `POSTGRES_PORT`: database port;

- `POSTGRES_USER`: database user;

- `POSTGRES_PASSWORD`: database password;

- `POSTGRES_DB`: name of the database used by the service;

- `GF_SECURITY_ADMIN_PASSWORD`: username for authorization in Grafana;

- `GF_SECURITY_ADMIN_USER`: password for authorization in Grafana;

You can do this automatically via a script:

```shell
./configure.sh
```

### Run

Start the application stack on Docker with the following command:

```shell
docker-compose up -d --build
```

<details>
  <summary>👀 What does a healthy log look like at startup?</summary>

<hr />

Inference log:

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

API log:

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

Worker log:

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

## Operation

### API Documentation

API documented using Swagger (`drf-spectacular`).

API testing: `http://127.0.0.1/api/docs/`

YAML: `http://127.0.0.1/api/schema/`

### Admin panel

The service admin area is available at `http://127.0.0.1/admin`.

First login credentials: `admin:admin`.

> [!IMPORTANT]
> It is recommended to change the credentials immediately after deployment to more stable ones.


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Flight-hat%2Fsmart_ids.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Flight-hat%2Fsmart_ids?ref=badge_large)