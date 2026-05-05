# Download French Verb Conjugation Audios

[![PyPI - Version](https://img.shields.io/pypi/v/fr-audio.svg)](https://pypi.org/project/fr-audio)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fr-audio.svg)](https://pypi.org/project/fr-audio)

A CLI tool for downloading MP3 audio of French verb conjugations. 
Provide the infinitive form of a verb and use options to specify which tenses to download. 
By default, only the infinitive form audio is downloaded.

Currently supported common tenses include: indicatif présent, indicatif futur simple, indicatif passé composé, indicatif passé simple, conditionnel présent, and impératif présent.

## Installation

- From PyPI
```
    pip install fr-audio
```
- From Git
```
    git clone https://github.com/yenyen1/french-conjugation-verb-audio.git 
    cd french-conjugation-verb-audio 
    pip install .
```

## Usage


```
# Print help
fr-audio --help

# Download infinitive present verb audio
fr-audio aller

# Download present tense
fr-audio aller --present

# Download multiple tenses
fr-audio aller --present --past --past_simple --future

```

*Note*: The first run may take about a minute to download the model.

## Credits
This tool uses the following Python libraries:
- [verbecc](https://github.com/bretttolbert/verbecc?tab=readme-ov-file): A Python library for verb conjugation, enhanced with machine learning techniques.
- [edge-tts](https://github.com/rany2/edge-tts?tab=readme-ov-file): A Python module that allows access to Microsoft Edge’s online text-to-speech service from Python code.

