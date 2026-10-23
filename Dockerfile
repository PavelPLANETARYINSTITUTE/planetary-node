# Легковесный базовый образ на базе Alpine Linux для минимизации размера узла
FROM alpine:3.19

# Установка необходимых системных зависимостей, библиотек криптографии и IPFS
RUN apk update && apk add --no-cache \
    curl \
    bash \
    python3 \
    py3-pip \
    go-ipfs \
    openssl \
    ca-certificates

# Создание изолированных директорий для зашифрованной Базы Открытий и приложения
RUN mkdir -p /data/pi/db /data/pi/node_config /app /app/scripts

# Установка рабочей директории
WORKDIR /app

# Настройка прав доступа и полная изоляция (создание несистемного пользователя)
RUN adduser -D -u 10001 pi_operator && \
    chown -R pi_operator:pi_operator /data/pi /app

# Копируем скрипт приветствия в изолированную директорию контейнера
COPY --chown=pi_operator:pi_operator scripts/welcome_msg.sh /app/scripts/welcome_msg.sh

# Делаем скрипт исполняемым
RUN chmod +x /app/scripts/welcome_msg.sh

USER pi_operator

# Инициализация локального узла распределенной P2P-сети IPFS в энергосберегающем режиме
RUN ipfs init --profile low-power

# Открытие сетевых портов: 4001 (P2P-трафик протокола Гидра), 8080 (Локальный веб-интерфейс)
EXPOSE 4001
EXPOSE 8080

# Точка входа: запуск приветственного сообщения ИИ и Павла, затем старт P2P-демона
ENTRYPOINT ["/bin/bash", "-c", "/app/scripts/welcome_msg.sh && ipfs daemon --migrate=true"]
