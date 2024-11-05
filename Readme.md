<h1 align="center"> Smart IDS </h1>

<p align="center">
<a href="https://github.com/light-hat/shop_service/actions"><img alt="Unit test status" src="https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

<p align="center">
Асинхронный API для обнаружения атак в дампах сетевого трафика методами машинного обучения.
</p>

## Содержание

<!-- TOC -->
* [Smart IDS](#smart-ids)
  * [Пару слов о модели](#пару-слов-о-модели)
  * [Требования](#требования)
    * [Аппаратное окружение](#аппаратное-окружение)
    * [Программное окружение](#программное-окружение)
  * [Развёртывание](#развёртывание)
    * [Preflight](#preflight)
    * [Конфигурирование](#конфигурирование)
    * [Запуск проекта](#запуск-проекта)
  * [Эксплуатация](#эксплуатация)
    * [Схема работы](#схема-работы)
    * [Документация API](#документация-api)
    * [Административная панель](#административная-панель)
    * [Управление проектом через Make](#управление-проектом-через-make)
    * [Мониторинг](#мониторинг)
    * [Масштабирование](#масштабирование)
<!-- TOC -->

## Пару слов о модели

Для инференса взята модель [rdpahalavan/bert-network-packet-flow-header-payload](https://huggingface.co/rdpahalavan/bert-network-packet-flow-header-payload) на Hugging Face.

## Требования

### Аппаратное окружение

| Требование | Минимум         | Рекомендуется  |
|------------|-----------------|----------------|
| CPU        | `6 ядер`        | `12 ядер`      |
| RAM        | `16 Гб`         | `32 Гб`        |
| Диск       | `80 Гб`         | `150 Гб`       |
| GPU        | `8-16 Гб VRAM`  | `32 Гб VRAM`   |

### Программное окружение

> [!TIP]
> Операционная система в принципе не имеет значения, если соблюдены требования к программному и аппаратному окружению.

| Требование               | Минимальная версия | Рекомендуемая версия           |
|--------------------------|--------------------|--------------------------------|
| Docker                   | `19.03`            | `20.10 или выше`               |
| Docker Compose           | `1.27`             | `1.29 или выше`                |
| NVIDIA драйверы          | `418.87`           | `последняя стабильная версия`  |
| CUDA                     | `11.0`             | `последняя стабильная версия`  |
| NVIDIA Container Toolkit | `1.0`              | `последняя стабильная версия`  |

## Развёртывание

### Preflight

- Проверка установки `Docker`:

```shell
docker --version
```

<details>
  <summary>Что примерно должно быть в ответе</summary>

```
Docker version 27.2.0, build 3ab4256
```

</details>

- Проверка установки `Docker Compose`:

```shell
docker-compose --version
```

<details>
  <summary>Что примерно должно быть в ответе</summary>

```
Docker Compose version v2.29.2-desktop.2
```

</details>

- `Драйвера NVIDIA`:

```shell
nvidia-smi
```

<details>
  <summary>Что примерно должно быть в ответе</summary>

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.57.02    Driver Version: 470.57.02    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:1E.0 Off |                    0 |
| N/A   42C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

```

</details>

- `NVIDIA Container Toolkit`:


> [!NOTE]
> В **Windows** поддержка **NVIDIA Container Toolkit** доступна через **WSL 2** (Windows Subsystem for Linux), так как Docker на Windows работает внутри WSL.

```shell
dpkg -l | grep nvidia-container-toolkit
```

<details>
  <summary>Что примерно должно быть в ответе</summary>

```
nvidia-container-toolkit   1.5.0-1   all   NVIDIA container runtime library

```

</details>

### Конфигурирование

Для начала клонируйте репозиторий:

```shell
git clone https://github.com/light-hat/smart_ids
cd smart_ids
```

В корне репозитория создайте `.env` файл со следующим содержимым:

```
MODEL_REPOSITORY=/models
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

- `MODEL_REPOSITORY`: путь к папке моделей в контейнере Triton (рекомендуется оставить значение по умолчанию);

- `API_URL`: адрес, на котором будет развёрнут сервис;

- `API_PORT`: порт, на котором будет принимать запросы сервис;

- `POSTGRES_HOST`: хост базы данных (имя сервиса в стеке приложений);

- `POSTGRES_PORT`: порт базы данных;

- `POSTGRES_USER`: пользователь базы данных;

- `POSTGRES_PASSWORD`: пароль от базы данных;

- `POSTGRES_DB`: имя базы данных, используемой сервисом;

- `GF_SECURITY_ADMIN_PASSWORD`: имя пользователя для авторизации в Grafana;

- `GF_SECURITY_ADMIN_USER`: пароль для авторизации в Grafana.

### Запуск проекта

Запустите стек приложений на Docker следующей командой:

```shell
docker-compose up -d --build
```

<details>
  <summary>Что примерно должно быть в ответе</summary>

`TODO`: Указать лог, когда починю Triton Inference Server

</details>

<details>
  <summary>Как выглядит здоровый лог при запуске</summary>

Для просмотра логов стека приложений выполните следующую команду:

```shell
docker-compose logs
```

`TODO`: Указать лог, когда закончу всё

</details>

## Эксплуатация

### Схема работы

`TODO`: диаграмма последовательности работы API.

### Документация API

`TODO`: вставить фотку сваггера по готовности.

API задокументирован при помощи Swagger (`drf-spectacular`).

Тестирование API: `http://127.0.0.1/swagger/`

YAML: `http://127.0.0.1/schema/`

### Административная панель

`TODO`: вставить фотки админки по готовности.

Админка сервиса доступна по адресу `http://127.0.0.1/admin`.

Учётные данные для первого входа: `admin:admin`.

> [!IMPORTANT]
> Учётные данные рекомендуется сменить сразу после развёртывания на более устойчивые.

### Управление проектом через Make

`TODO`: По готовности Makefile описать управление проектом

### Мониторинг

`TODO`: описать работу с системой мониторинга по готовности

### Масштабирование

`TODO`: по готовности описать репликацию и балансировку нагрузки методами Docker Compose.
