# Text to Speech Program

This package provides a text-to-speech server, using `gtts` and `playsound`, and a client program to interact with the server.

## Instalação

### 1. Install the package locally

To install the package locally, follow the instructions below:

```bash
git clone https://github.com/trucomanx/text_to_speech_program.git
cd text_to_speech_program/src
python setup.py install
```

### 2. Create a tar.gz package for distribution

If you want to package the project for distribution via PyPI or to other users:

```bash
python3 setup.py sdist
```

This will generate a `*.tar.gz` file inside the `dist/` folder. The package can be installed using:

```bash
pip install dist/text_to_speech_program-*.tar.gz
```

## Uso

### 1. Start the server

To start the text to speech server, use the command below:

```bash
tts-program-server
```

This starts a server that will listen on port `5000` and will be ready to receive text conversion requests.

### 2. Start the client

The client can be used to submit conversion jobs or remove pending jobs from the server.

#### Send a JSON file:

```bash
tts-program-client enviar /caminho/para/arquivo.json
```

JSON file example:

```json
{
    "text": "Some text to convert",
    "language": "en",
    "split_pattern": [".", "\n\n"]
}
```
#### Remove a task from the stack using the ID:

```bash
tts-program-client apagar <ID>
```

Replace `<ID>` with the unique ID returned when adding a task.

## Dependencies

The main dependencies of the package are:

* `Flask` ​​for the server
* `gtts` for text-to-speech
* `playsound` for audio playback
* `requests` for the client to interact with the server

You can install all dependencies with:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the GPL license. See the `src/LICENSE` file for more details.
