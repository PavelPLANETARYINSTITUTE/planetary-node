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

# Создание изолированных директорий для зашифрованной Базы Открытий Планетарного Института
RUN mkdir -p /data/pi/db /data/pi/node_config /app

# Установка рабочей директории
WORKDIR /app

# Настройка прав доступа и полная изоляция (запуск от имени несистемного пользователя)
RUN adduser -D -u 10001 pi_operator && \
    chown -R pi_operator:pi_operator /data/pi /app

USER pi_operator

# Инициализация локального узла распределенной P2P-сети IPFS в энергосберегающем режиме
RUN ipfs init --profile low-power

# Открытие сетевых портов: 4001 (P2P-трафик протокола Гидра), 8080 (Локальный веб-интерфейс)
EXPOSE 4001
EXPOSE 8080

# Команда для старта демона децентрализованной сети при запуске ноды
ENTRYPOINT ["ipfs", "daemon", "--migrate=true"]
