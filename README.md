# Download French Verb Conjugation Audios

[![PyPI - Version](https://img.shields.io/pypi/v/fr-audio.svg)](https://pypi.org/project/fr-audio)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fr-audio.svg)](https://pypi.org/project/fr-audio)

A CLI tool for downloading MP3 audio of French learning. Currently supports two features:

- **Verb conjugations**: Enter the infinitive form and use the options to specify which tenses you want. The program automatically converts the verb conjugations and downloads the corresponding audio files. Currently supported common tenses include: indicatif présent, indicatif futur simple, indicatif passé composé, indicatif passé simple, conditionnel présent, and impératif présent.
- **French Sentence**: Generate and download MP3 audio for input French sentences.



## Installation

### From PyPI
```
pip install fr-audio
```
### From Git
```
git clone https://github.com/yenyen1/french-conjugation-verb-audio.git 
cd french-conjugation-verb-audio 
pip install .
``` 

## Usage: Download verb conjugation audio

**Note**: The first run may take about a minute to download the model.

### Print help
```
fr-audio verb --help
```

### Download infinitive present verb audio
```
fr-audio verb aller
```

### Download present tense
```
fr-audio verb aller --present
```
### Download multiple tenses 
```
fr-audio verb aller --present --past --past_simple --future
```

## Usage: Download verb conjugation audio

**Note**: The first run may take about a minute to download the model.

### Print help
```
fr-audio sentence --help
```

### Download French sentence audio
```
fr-audio sentence --sentence "Vous devez remplir un formulaire d'inscription."
```


## Credits
This tool uses the following Python libraries:
- [verbecc](https://github.com/bretttolbert/verbecc?tab=readme-ov-file): A Python library for verb conjugation, enhanced with machine learning techniques.
- [edge-tts](https://github.com/rany2/edge-tts?tab=readme-ov-file): A Python module that allows access to Microsoft Edge’s online text-to-speech service from Python code.

