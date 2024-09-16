#!/bin/bash

pip install --upgrade text-to-speech-program

# Defina as variáveis que você deseja substituir
USER=$(whoami)  # Nome do usuário atual
GROUP=$(id -gn) # Nome do grupo principal do usuário atual
HOME_DIR=$HOME  # Diretório home do usuário
USERID=$(id -u $USER)
PROGRAM_PATH=$(which tts-program-server)

# Caminho para o arquivo de serviço
SERVICE_FILE="/etc/systemd/system/tts-program-server.service"

# Conteúdo do arquivo de serviço (substitua os placeholders)
SERVICE_CONTENT="[Unit]
Description=Text-to-Speech Program Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
StandardOutput=journal+console
StandardError=journal+console
User=$USER
Group=$GROUP
Environment=XDG_RUNTIME_DIR=/run/user/$USERID
ExecStart=$PROGRAM_PATH
WorkingDirectory=$HOME_DIR
Environment=\"PATH=$PATH:$HOME_DIR/.local/bin\"

[Install]
WantedBy=multi-user.target
"

# Cria o arquivo de serviço temporário e escreve o conteúdo nele
echo "$SERVICE_CONTENT" | sudo tee $SERVICE_FILE > /dev/null

# Recarga do systemd para reconhecer o novo serviço
sudo systemctl daemon-reload

# Habilitar o serviço para iniciar no boot
sudo systemctl enable tts-program-server.service

# Iniciar o serviço imediatamente
sudo systemctl restart tts-program-server.service

# Aguardar um segundo e testar o serviço com o cliente
sleep 1
DICT='{ "text": "Server installed and running. OK", "language": "en", "split_pattern": ["."], "speed": 1.25 }'
echo 'tts-program-client senddict '\'$DICT\'
tts-program-client senddict "$DICT"

