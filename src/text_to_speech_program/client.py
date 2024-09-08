#!/usr/bin/python3
import requests
import json
import sys
import os

# URL do servidor
SERVER_URL = 'http://localhost:5000'

def send_json_from_file(filepath):
    # Verificar se o arquivo existe
    if not os.path.isfile(filepath):
        print(f"Arquivo {filepath} não encontrado.")
        return

    # Carregar o conteúdo do arquivo JSON
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Erro ao ler o arquivo JSON {filepath}.")
        return

    # Enviar solicitação POST ao servidor
    response = requests.post(f'{SERVER_URL}/add_task', json=data)

    if response.status_code == 200:
        print(f"Tarefa enviada com sucesso! ID: {response.json()['id']}")
    else:
        print("Erro ao enviar a tarefa.")

def remove_task(task_id):
    # Enviar solicitação DELETE ao servidor
    response = requests.delete(f'{SERVER_URL}/remove_task/{task_id}')

    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Erro ao remover a tarefa.")

if __name__ == "__main__":
    # Verificar o comando recebido
    if len(sys.argv) < 2:
        print("Uso: python cliente.py <comando> <argumentos>")
        print("Comandos:")
        print("  enviar <caminho_arquivo_json>")
        print("  apagar <ID>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "enviar":
        if len(sys.argv) != 3:
            print("Uso: python cliente.py enviar <caminho_arquivo_json>")
            sys.exit(1)

        filepath = sys.argv[2]
        send_json_from_file(filepath)

    elif command == "apagar":
        if len(sys.argv) != 3:
            print("Uso: python cliente.py apagar <ID>")
            sys.exit(1)

        task_id = sys.argv[2]
        remove_task(task_id)

    else:
        print("Comando não reconhecido. Use 'enviar' ou 'apagar'.")

