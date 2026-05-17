from fr_audio.config import Model, Moods, Tenses
from fr_audio.audio import download_audios, download_audio_with_specified_filename
from fr_audio.conjugation import fetch_verb_conjugation

import argparse
from pathlib import Path


def create_parser():
    parser = argparse.ArgumentParser(
        prog="fr-audio",
        description="""Download MP3 audio for French learning. \
            Currently supports two features: (1) verb (2) sentence""",
    )

    subparser = parser.add_subparsers(dest="command", metavar="<command>")

    ### 1. verb conjugation
    verb_parser = subparser.add_parser(
        "verb",
        help="""Automatically convert verb conjugations and download conjugated audio. \
            Enter the infinitive form and use the options to specify which tenses to download. \
            By default, it only downloads the infinitive verb.""",
    )
    verb_parser.add_argument("inf_verb", help="Infinitif Présent Verb")
    verb_parser.add_argument("--present", action="store_true", help="Indicatif Présent")
    verb_parser.add_argument("--future", action="store_true", help="Indicatif Futur")
    verb_parser.add_argument(
        "--past", action="store_true", help="Indicatif Passé Composé"
    )
    verb_parser.add_argument(
        "--past-simple", action="store_true", help="Indicatif Passé Simple"
    )
    verb_parser.add_argument(
        "--conditional", action="store_true", help="Conditionnel Présent"
    )
    verb_parser.add_argument(
        "--imperative", action="store_true", help="Impératif Présent"
    )

    ### 2. Sentence
    sentence_parser = subparser.add_parser(
        "sentence", help="Download MP3 audio for input French sentences."
    )
    sentence_parser.add_argument(
        "--sentence", type=str, required=True, help="A French sentence"
    )
    sentence_parser.add_argument(
        "-o", "--output", type=str, default="output.mp3", help="Output file name"
    )

    return parser


def run_verb(args: argparse.ArgumentParser):
    lang = Model.Language
    infinitive = args.inf_verb
    voice_model = Model.VoiceModel
    folder = Path(args.inf_verb)

    download_audios(folder / "infinitif_présent", voice_model, [infinitive])

    if args.present:
        mood, tense = Moods.Indicatif, Tenses.Présent
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.future:
        mood, tense = Moods.Indicatif, Tenses.FuturSimple
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.past:
        mood, tense = Moods.Indicatif, Tenses.PasséComposé
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.past_simple:
        mood, tense = Moods.Indicatif, Tenses.PasséSimple
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.conditional:
        mood, tense = Moods.Conditionnel, Tenses.Présent
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.imperative:
        mood, tense = Moods.Imperatif, Tenses.ImperatifPrésent
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}-{tense}"
        download_audios(sub_folder, voice_model, result)

    print("[INFO] Complete download.")


def run_sentence(args: argparse.ArgumentParser):
    file = Path(args.output)
    download_audio_with_specified_filename(file, Model.VoiceModel, args.sentence)
    print("[INFO] Complete download.")


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "verb":
        run_verb(args)
    elif args.command == "sentence":
        run_sentence(args)


if __name__ == "__main__":
    main()
