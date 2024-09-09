# Text to Speech Program

This package provides a text-to-speech server, using `gtts` and `playsound`, and a client program to interact with the server.

## Install from source and add to Linux service
Installing text-to-speech server

```bash
git clone https://github.com/trucomanx/text_to_speech_program.git
cd text_to_speech_program
pip install -r requirements.txt
cd src
python3 setup.py sdist
pip install dist/text_to_speech_program-*.tar.gz
```
Adding to Linux service

```bash
curl -fsSL https://github.com/trucomanx/text_to_speech_program/install_user_service.sh | sh
```

## Sending a DICT from string:
Adding a text-to-speech task.

```bash
tts-program-client senddict '{ "text": "Some text to convert. OK", "language": "en", "split_pattern": ["."], "speed":1.25 }'
```

## More information
More information can be found in [README.full.md](README.full.md)
