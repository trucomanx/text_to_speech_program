#!/usr/bin/python3

from flask import Flask, request, jsonify
import os
import uuid
import threading
from queue import Queue
import time
from langdetect import detect
import json
from . import work_audio

app = Flask(__name__)

# Pilha para armazenar as tarefas
task_stack = Queue()

# Pilha para armazenar as play tarefas
play_stack = Queue()

def detectar_linguagem(texto):
    try:
        linguagem = detect(texto)
        return linguagem
    except Exception as e:
        return "en";

def split_text(input_text,pattern_list):
    text=str(input_text);
    for pattern in pattern_list:
        text = text.replace(pattern, '&');
    sentences = [sentence.strip() for sentence in text.split('&') if sentence]
    return sentences

# Função assíncrona para processar a pilha
def process_play():
    while True:
        if not play_stack.empty():
            task = play_stack.get()
            task_id, task_filepath, task_speed = task
            
            # Reproduzir o áudio
            work_audio.play_audio_file(task_filepath, task_speed);

            # Remover o arquivo de áudio após reprodução
            os.remove(task_filepath);
        
        time.sleep(0.001);


# Função assíncrona para processar a pilha
def process_tasks():
    while True:
        if not task_stack.empty():
            task = task_stack.get()
            task_id, task_data = task
            
            text          = task_data["text"];
            language      = task_data["language"];
            split_pattern = task_data["split_pattern"];
            speed         = task_data["speed"];
        
            if text.strip():
                # Converter o texto em fala usando gTTS
                audio_filepath = work_audio.text_to_audio_file(text,language)

                play_stack.put((task_id, audio_filepath, speed));
        
        time.sleep(0.001)

# Rota para receber os dados do cliente
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task_id = str(uuid.uuid4())
    
    if data["language"]=='':
        data["language"]=detectar_linguagem(data["text"]);
    
    sentences=split_text(data["text"],data["split_pattern"]);
    
    for m in range(len(sentences)):
        data_part=dict();
        data_part["text"]=sentences[m];
        data_part["speed"]=data["speed"];
        data_part["language"]=data["language"];
        data_part["split_pattern"]=data["split_pattern"];
        
        task_stack.put((task_id, data_part))
    print("Work end in id:",task_id)
    
    return jsonify({"id": task_id})


def remove_id_from_stack(name_stack,task_id):
    temp_stack = []
    
    # Desempilhar para verificar se o ID está na pilha
    while not name_stack.empty():
        task = name_stack.get()
        if task[0] != task_id:
            temp_stack.append(task)
        else:
            if isinstance(task[1], str):
                if os.path.exists(task[1]):
                    try:
                        os.remove(task[1])
                    except:
                        pass  # Silencia qualquer erro
    
    # Reempilhar os itens que não foram removidos
    for task in temp_stack:
        name_stack.put(task);

# Rota para remover um item da pilha por ID
@app.route('/remove_task/<task_id>', methods=['DELETE'])
def remove_task(task_id):
    remove_id_from_stack(task_stack,task_id)
    remove_id_from_stack(play_stack,task_id)
    '''
    temp_stack = []
    
    # Desempilhar para verificar se o ID está na pilha
    while not task_stack.empty():
        task = task_stack.get()
        if task[0] != task_id:
            temp_stack.append(task)
    
    # Reempilhar os itens que não foram removidos
    for task in temp_stack:
        task_stack.put(task)
    '''
    
    return jsonify({"message": f"Tasks with ID {task_id} removed."})

# Iniciar a thread para processar a pilha de forma assíncrona
task_processor_thread = threading.Thread(target=process_tasks, daemon=True)
task_processor_thread.start()

# Iniciar a thread para processar a pilha de reprodução
play_processor_thread = threading.Thread(target=process_play, daemon=True)
play_processor_thread.start()

################################################################################

DEFAULT_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000
}

def load_config():
    """Carrega a configuração do arquivo JSON, criando-o com valores padrão se não existir."""
    home_directory = os.path.expanduser('~')
    config_directory = os.path.join(home_directory, '.config', 'text_to_speech_program')
    config_path = os.path.join(config_directory, 'config.json')

    # Cria o diretório de configuração se não existir
    os.makedirs(config_directory, exist_ok=True)

    if not os.path.exists(config_path):
        # Cria o arquivo com valores padrão se não existir
        with open(config_path, 'w') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
    
    # Carrega a configuração do arquivo
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config

def main():
    '''
    Modo de Depuração (debug=True)

    Recarga Automática: Quando você faz alterações no código do servidor, 
    o Flask recarrega automaticamente o servidor para refletir essas mudanças sem que você precise reiniciar manualmente. 
    Isso é útil durante o desenvolvimento, pois permite ver as alterações imediatamente.

    Mensagens de Erro Detalhadas: O Flask exibe mensagens de erro mais detalhadas e rastreamentos (tracebacks) 
    quando ocorre um erro, ajudando a identificar e corrigir problemas no código.

    Desenvolvimento Seguro: O modo de depuração não deve ser usado em produção, 
    pois pode revelar informações sensíveis e tornar o aplicativo vulnerável a ataques. 
    É destinado apenas para o ambiente de desenvolvimento.
    '''
    
    config = load_config()
    host = config.get('host', '0.0.0.0')  # Valor padrão se não especificado
    port = config.get('port', 5000)        # Valor padrão se não especificado
    
    #app.run(debug=True); # http://localhost:5000
    #app.run(host=host, port=port, debug=True)
    app.run(host=host, port=port)

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();

