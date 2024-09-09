# Text to Speech Program

This package provides a text-to-speech server, using `gtts` and `playsound`, and a client program to interact with the server.

## Installing

### 1. Create a tar.gz package for distribution

If you want to package the project for distribution via PyPI or to other users:

```bash
git clone https://github.com/trucomanx/text_to_speech_program.git
cd text_to_speech_program/src
python3 setup.py sdist
```

This will generate a `*.tar.gz` file inside the `dist/` folder. 

### 1. Install the package locally

To install the package `dist/*.tar.gz` locally, follow the instructions below:


```bash
pip install dist/text_to_speech_program-*.tar.gz
```

Execute `which tts-program-server` to see where it was installed probably in `/home/USERNAME/.local/bin/tts-program-server`.

### 2. Add a program to the Linux service

```bash
chmod +x generate_service.sh
./generate_service.sh
```

After the last code, the program server starts at with the operating system.
Now the next commands are accepted (Use them if necessary).

#### Start server Linux service

```bash
sudo systemctl start tts-program-server
```

#### Stop server Linux service

```bash
sudo systemctl stop tts-program-server
```

#### Stop service when beginning Linux

```bash
sudo systemctl disable tts-program-server
```

## Uso

### 1. Start the server

If the program server was not added to the Linux service, then to start the text-to-speech server, use the command below:

```bash
tts-program-server
```

This starts a server that will listen on `http://127.0.0.1:5000` and will be ready to receive text conversion requests.



### 2. Start the client

The client can submit conversion text-to-speech tasks or remove pending jobs from the server.

#### Sending a JSON file:
Adding a text-to-speech task.

```bash
tts-program-client send /caminho/para/arquivo.json
```

JSON file example:

```json
{
    "text": "Some text to convert.\n\n OK",
    "language": "en",
    "split_pattern": [".", "\n\n"],
    "speed":1.25
}
```

#### Sending a DICT from string:
Adding a text-to-speech task.

```bash
tts-program-client senddict '{ "text": "Some text to convert. OK", "language": "en", "split_pattern": ["."], "speed":1.25 }'
```

#### Remove a task from the stack using the ID:

```bash
tts-program-client remove <ID>
```

Replace `<ID>` with the unique ID returned when adding a task.

## Dependencies

The main dependencies of the package are:

* `Flask` ​​for the server
* `gtts` for text-to-speech
* `pydub` for audio playback
* `requests` for the client to interact with the server

You can install all dependencies with:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the GPL license. See the `src/LICENSE` file for more details.
