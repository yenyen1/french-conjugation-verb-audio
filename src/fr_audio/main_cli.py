from fr_audio.config import Model, Moods, Tenses
from fr_audio.audio import download_audios
from fr_audio.conjugation import fetch_verb_conjugation

import argparse
from pathlib import Path


def main():
    parse = argparse.ArgumentParser(
        prog="get_fr_verb_audio",
        description="""Download MP3 audio for French verb conjugations. \
            Enter the infinitive form and use the options to specify which tenses to download. \
            By default, it only downloads the infinitive verb.""",
    )
    parse.add_argument("inf_verb", help="Infinitif Présent Verb")

    parse.add_argument("--present", action="store_true", help="Indicatif Présent")
    parse.add_argument("--future", action="store_true", help="Indicatif Futur")
    parse.add_argument("--past", action="store_true", help="Indicatif Passé Composé")
    parse.add_argument(
        "--past-simple", action="store_true", help="Indicatif Passé Simple"
    )

    parse.add_argument(
        "--conditional", action="store_true", help="Conditionnel Présent"
    )
    parse.add_argument("--imperative", action="store_true", help="Impératif Présent")

    args = parse.parse_args()

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

    print("Complete download.")


if __name__ == "__main__":
    main()
