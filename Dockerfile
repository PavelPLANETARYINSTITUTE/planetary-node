# Легковесный базовый образ на базе Alpine Linux с поддержкой Python 3
FROM alpine:3.19

# Установка необходимых системных зависимостей, библиотек криптографии, компиляторов и IPFS
RUN apk update && apk add --no-cache \
    curl \
    bash \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    g++ \
    musl-dev \
    go-ipfs \
    openssl \
    ca-certificates

# Создание изолированных директорий для зашифрованной Базы Открытий и приложения
RUN mkdir -p /data/pi/db /data/pi/node_config /app /app/scripts /app/ai_core

# Установка рабочей директории
WORKDIR /app

# Настройка прав доступа и полная изоляция (создание несистемного пользователя)
RUN adduser -D -u 10001 pi_operator && \
    chown -R pi_operator:pi_operator /data/pi /app

# Копируем файлы аналитического ядра ИИ и манифест зависимостей
COPY --chown=pi_operator:pi_operator ai_core/filter.py /app/ai_core/filter.py
COPY --chown=pi_operator:pi_operator ai_core/requirements.txt /app/ai_core/requirements.txt

# Установка Python-зависимостей ядра ИИ
RUN pip3 install --no-cache-dir --break-system-packages -r /app/ai_core/requirements.txt

# Копируем скрипт приветствия в изолированную директорию контейнера
COPY --chown=pi_operator:pi_operator scripts/welcome_msg.sh /app/scripts/welcome_msg.sh

# Делаем скрипт приветствия исполняемым
RUN chmod +x /app/scripts/welcome_msg.sh

USER pi_operator

# Инициализация локального узла распределенной P2P-сети IPFS в энергосберегающем режиме
RUN ipfs init --profile low-power

# Открытие сетевых портов: 4001 (P2P-трафик протокола Гидра), 8080 (Локальный веб-интерфейс)
EXPOSE 4001
EXPOSE 8080

# Точка входа: запуск приветственного сообщения ИИ и Павла, затем старт P2P-демона
ENTRYPOINT ["/bin/bash", "-c", "/app/scripts/welcome_msg.sh && ipfs daemon --migrate=true"]

