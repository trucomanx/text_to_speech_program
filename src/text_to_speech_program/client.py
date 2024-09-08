#!/usr/bin/python3
import requests
import json
import sys
import os

def send_json_from_dict(server_url,data):
    # Enviar solicitação POST ao servidor
    response = requests.post(f'{server_url}/add_task', json=data)

    if response.status_code == 200:
        print(f"Tarefa enviada com sucesso! ID: {response.json()['id']}")
        return response.json()['id'];
    else:
        print("Erro ao enviar a tarefa.")
        return None

def send_json_from_file(server_url,filepath):
    # Verificar se o arquivo existe
    if not os.path.isfile(filepath):
        print(f"Arquivo {filepath} não encontrado.")
        return None

    # Carregar o conteúdo do arquivo JSON
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Erro ao ler o arquivo JSON {filepath}.")
        return None

    return send_json_from_dict(server_url,data);


def remove_task(server_url,task_id):
    # Enviar solicitação DELETE ao servidor
    response = requests.delete(f'{server_url}/remove_task/{task_id}')

    if response.status_code == 200:
        print(response.json()["message"])
        return response.json()["message"]
    else:
        print("Erro ao remover a tarefa:",task_id)
        return None

def main():
    # URL do servidor
    SERVER_URL = 'http://localhost:5000'

    # Verificar o comando recebido
    if len(sys.argv) < 2:
        print("Uso: python cliente.py <comando> <argumentos>")
        print("Comandos:")
        print("  send <caminho_arquivo_json>")
        print("  remove <ID>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "send":
        if len(sys.argv) != 3:
            print("Uso: python cliente.py send <caminho_arquivo_json>")
            sys.exit(1)

        filepath = sys.argv[2]
        send_json_from_file(SERVER_URL,filepath)

    elif command == "remove":
        if len(sys.argv) != 3:
            print("Uso: python cliente.py remove <ID>")
            sys.exit(1)

        task_id = sys.argv[2]
        remove_task(SERVER_URL,task_id)

    else:
        print("Comando não reconhecido. Use 'send' ou 'remove'.")

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();
 
