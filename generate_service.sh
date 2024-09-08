#!/bin/bash

# Defina as variáveis que você deseja substituir
USER=$(whoami)  # Nome do usuário atual
HOME_DIR=$HOME  # Diretório home do usuário

# Caminho para o arquivo de modelo e o arquivo de saída
TEMPLATE_FILE="tts-program-server.service.in"
SERVICE_FILE="/etc/systemd/system/tts-program-server.service"

# Verifique se o arquivo de modelo existe
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Arquivo de modelo $TEMPLATE_FILE não encontrado!"
    exit 1
fi

# Substituir as variáveis no arquivo de modelo e gerar o arquivo final
sed -e "s|@HOME@|$HOME_DIR|g" \
    -e "s|@USER@|$USER|g" \
    "$TEMPLATE_FILE" > "$SERVICE_FILE"

# Recarga do systemd para reconhecer o novo serviço
sudo systemctl daemon-reload

# Habilitar o serviço para iniciar no boot
sudo systemctl enable tts-program-server.service

# Iniciar o serviço imediatamente
sudo systemctl start tts-program-server.service

echo "Serviço tts-program-server criado e iniciado com sucesso."

