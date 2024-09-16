#!/usr/bin/python3

from flask import Flask, request, jsonify
import os
import uuid
import threading
from queue import Queue
import time
from langdetect import detect

from . import work_audio

app = Flask(__name__)

# Pilha para armazenar as tarefas
task_stack = Queue()


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

                # Reproduzir o áudio
                work_audio.play_audio_file(audio_filepath, speed);

                # Remover o arquivo de áudio após reprodução
                os.remove(audio_filepath)
        
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
    
    return jsonify({"id": task_id})

# Rota para remover um item da pilha por ID
@app.route('/remove_task/<task_id>', methods=['DELETE'])
def remove_task(task_id):
    temp_stack = []
    
    # Desempilhar para verificar se o ID está na pilha
    while not task_stack.empty():
        task = task_stack.get()
        if task[0] != task_id:
            temp_stack.append(task)
    
    # Reempilhar os itens que não foram removidos
    for task in temp_stack:
        task_stack.put(task)
    
    return jsonify({"message": f"Tasks with ID {task_id} removed."})

# Iniciar a thread para processar a pilha de forma assíncrona
task_processor_thread = threading.Thread(target=process_tasks, daemon=True)
task_processor_thread.start()

def main():
    app.run(debug=True);

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();

