# Text to Speech Program

Este pacote fornece um servidor de conversão de texto para fala, usando `gtts` e `playsound`, além de um programa cliente para interagir com o servidor.

## Instalação

### 1. Instalar o pacote localmente

Para instalar o pacote localmente, siga as instruções abaixo:

```bash
git clone https://github.com/trucomanx/text_to_speech_program.git
cd text_to_speech_program/src
python setup.py install
```

### 2. Criar um pacote tar.gz para distribuição

Caso queira empacotar o projeto para distribuição via PyPI ou para outros usuários:

```bash
python3 setup.py sdist
```

Isso gerará um arquivo `*.tar.gz` dentro da pasta `dist/`. O pacote pode ser instalado usando:

```bash
pip install dist/text_to_speech_program-*.tar.gz
```

## Uso

### 1. Iniciar o servidor

Para iniciar o servidor de texto para fala, utilize o comando abaixo:

```bash
tts-program-server
```

Isso inicializa um servidor que escutará na porta `5000 e estará pronto para receber solicitações de conversão de texto.

### 2. Usar o cliente

O cliente pode ser usado para enviar tarefas de conversão ou remover tarefas pendentes do servidor.

#### Enviar um arquivo JSON:

```bash
tts-program-client enviar /caminho/para/arquivo.json
```

Exemplo de conteúdo de um arquivo JSON:

```json
{
    "text": "Some text to convert",
    "language": "en",
    "split_pattern": [".", "\n\n"]
}
```
#### Remover uma tarefa da pilha usando o ID:

```bash
tts-program-client apagar <ID>
```

Substitua `<ID>` pelo ID único retornado ao adicionar uma tarefa.

## Dependências

As principais dependências do pacote são:

* `Flask` para o servidor
* `gtts` para conversão de texto para fala
* `playsound` para reprodução de áudio
* `requests` para o cliente interagir com o servidor

Você pode instalar todas as dependências com:

```bash
pip install -r requirements.txt
```

## Licença

Este projeto está licenciado sob a licença GPL. Consulte o arquivo `src/LICENSE para mais detalhes.
