#!/bin/bash

# Директория для резервных копий
BACKUP_DIR="/home/user/backup"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Создание директории, если она не существует
mkdir -p "$BACKUP_DIR"

# Архивация файлов
if tar -czf "$BACKUP_FILE" /etc/netplan/00-installer-config.yaml /etc/frr/frr.conf; then
    echo "Backup успешно создан: $BACKUP_FILE"
else
    echo "Ошибка при создании backup" >&2
    exit 1
fi
