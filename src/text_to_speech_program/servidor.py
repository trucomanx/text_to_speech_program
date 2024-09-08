#!/usr/bin/python3

from flask import Flask, request, jsonify
from gtts import gTTS
import os
import uuid
import threading
from playsound import playsound
from queue import LifoQueue
import time

app = Flask(__name__)

# Pilha para armazenar as tarefas
task_stack = LifoQueue()

# Função assíncrona para processar a pilha
def process_tasks():
    while True:
        if not task_stack.empty():
            task = task_stack.get()
            task_id, task_data = task
            text = task_data["text"]
            language = task_data["language"]
            split_pattern = task_data["split_pattern"]

            # Processar o texto (dividir de acordo com o padrão se necessário)
            if split_pattern:
                for pattern in split_pattern:
                    text = text.replace(pattern, ' ')
            
            # Converter o texto em fala usando gTTS
            tts = gTTS(text=text, lang=language)
            filename = f"{task_id}.mp3"
            tts.save(filename)

            # Reproduzir o áudio
            playsound(filename)

            # Remover o arquivo de áudio após reprodução
            os.remove(filename)
        
        time.sleep(1)

# Rota para receber os dados do cliente
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task_id = str(uuid.uuid4())
    task_stack.put((task_id, data))
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

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

