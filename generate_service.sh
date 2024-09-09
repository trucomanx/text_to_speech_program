#!/bin/bash

# Defina as variáveis que você deseja substituir
USER=$(whoami)  # Nome do usuário atual
GROUP=$(id -gn) # Nome do grupo principal do usuário atual
HOME_DIR=$HOME  # Diretório home do usuário
USERID=$(id -u $USER)

# Caminho para o arquivo de modelo e o arquivo de saída temporário
TEMPLATE_FILE="tts-program-server.service.in"
TEMP_SERVICE_FILE="/tmp/tts-program-server.service"  # Arquivo temporário
SERVICE_FILE="/etc/systemd/system/tts-program-server.service"

# Verifique se o arquivo de modelo existe
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "File of template $TEMPLATE_FILE not found!"
    exit 1
fi

# Substituir as variáveis no arquivo de modelo e gerar o arquivo temporário
sed -e "s|@HOME@|$HOME_DIR|g" \
    -e "s|@USER@|$USER|g" \
    -e "s|@GROUP@|$GROUP|g" \
    -e "s|@PATH@|$PATH|g" \
    -e "s|@USERID@|$USERID|g" \
    -e "s|@PROGRAM@|`which tts-program-server`|g" \
    "$TEMPLATE_FILE" > "$TEMP_SERVICE_FILE"

# Use sudo para copiar o arquivo temporário para o diretório do systemd
sudo mv "$TEMP_SERVICE_FILE" "$SERVICE_FILE"

# Recarga do systemd para reconhecer o novo serviço
sudo systemctl daemon-reload

# Habilitar o serviço para iniciar no boot
sudo systemctl enable tts-program-server.service

# Iniciar o serviço imediatamente
sudo systemctl restart tts-program-server.service

tts-program-client senddict '{ "text": "Server installed and running.", "language": "en", "split_pattern": ["."], "speed": 1.25 }'
