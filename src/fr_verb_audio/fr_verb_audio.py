import argparse
import asyncio
import logging
from pathlib import Path

import edge_tts
from verbecc import CompleteConjugator, localization, Moods, Tenses

# for unit test
import pytest
import shutil

logging.getLogger("verbecc").setLevel(logging.WARNING)


def fetch_verb_conjugation(
    lang: str, infinitive: str, mood: str, tense: str
) -> list[str]:
    """
    Fetch a set of French conjugated verb phrases from verbecc. 

    Args:
        lang (str): language (eg. 'fr', 'es', 'ca', etc.)
        infinitive (str): infinitive verb
        mood (str): Grammatical mood (eg. 'indicative', 'imperative', 'conditional', etc.)
        tense (str): GRammatical tense (eq. 'present', 'past', 'future', etc.)
    Returns:
        set[str]: A set of French conjugated verb phrases regarding the tense \
            or an empty set if the requested tense not found
    """
    m = localization.xmood(lang, mood)
    t = localization.xtense(lang, tense)
    cc = CompleteConjugator(lang).conjugate(infinitive)

    return [c[0] for c in cc[m][t]]


def download_audios(folder: Path, voice_model: str, conj_phrases: list[str]) -> bool:
    """
    Download MP3 audio files for a set of French conjugated phrases.

    Args:
        folder (pathlib.Path): The Path of the directory where audio files will be stored
        voice_model (str): voice model (eg. 'fr-CA-JeanNeural')
        conj_phrases (list[str]): A list of French conjugated phrases
    Returns:
        bool: Return True if successfully downloaded all audio files.
    """
    folder.mkdir(parents=True, exist_ok=True)
    if len(conj_phrases) == 0:
        return False

    async def run_batch():
        tasks = []
        for phrase in conj_phrases:
            file = folder / f"{phrase.replace(' ', '_')}.mp3"
            # create tasks
            tasks.append(edge_tts.Communicate(phrase, voice_model).save(file))

        # run all the tasks at the same time
        await asyncio.gather(*tasks)

    try:
        asyncio.run(run_batch())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


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
        "--past_simple", action="store_true", help="Indicatif Passé Simple"
    )

    parse.add_argument(
        "--conditional", action="store_true", help="Conditionnel Présent"
    )
    parse.add_argument("--imperative", action="store_true", help="Impératif Présent")
    parse.add_argument("--past_participle", action="store_true", help="Participe Passé")

    args = parse.parse_args()

    lang = "fr"
    infinitive = args.inf_verb
    voice_model = "fr-CA-JeanNeural"
    folder = Path(args.inf_verb)

    download_audios(folder / "infinitive_present", voice_model, [infinitive])

    if args.present:
        mood, tense = Moods.en.Indicative, Tenses.en.Present
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.future:
        mood, tense = Moods.en.Indicative, Tenses.en.Future
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.past:
        mood, tense = Moods.en.Indicative, Tenses.en.PastPerfect
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.past_simple:
        mood, tense = Moods.en.Indicative, Tenses.en.PastSimple
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.conditional:
        mood, tense = Moods.en.Conditional, Tenses.en.Present
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.imperative:
        mood, tense = Moods.en.Imperative, Tenses.en.Present
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)
    if args.past_participle:
        mood, tense = Moods.en.Participle, Tenses.en.PastParticiple
        result = fetch_verb_conjugation(lang, infinitive, mood, tense)
        sub_folder = folder / f"{mood}_{tense}"
        download_audios(sub_folder, voice_model, result)

    print("Complete download.")


if __name__ == "__main__":
    main()


# Unit Test


def test_fetch_verb_conjugation():
    expected_result = "j'ai\ttu as\til a\telle a\ton a\tnous avons\tvous avez\tils ont\telles ont".split(
        "\t"
    )
    actual_result = fetch_verb_conjugation("fr", "avoir", "indicative", "present")
    assert expected_result == actual_result


def test_download_audios_success(temp_output_dir):
    file = temp_output_dir / "j'ai.mp3"
    result = download_audios(temp_output_dir, "fr-CA-JeanNeural", ["j'ai"])
    assert result is True
    assert file.exists()


def test_download_audios_failure(temp_output_dir):
    file = temp_output_dir / ".mp3"
    result = download_audios(temp_output_dir, "fr-CA-JeanNeural", [""])
    assert result is True
    assert file.exists()

    result = download_audios(temp_output_dir, "fr-CA-JeanNeural", [])
    assert result is False


@pytest.fixture
def temp_output_dir():
    # Setup: Define where to put test files
    base_tmp = Path("test_tmp")
    test_path = base_tmp / "tense"

    # Yield: Hand this path to the test function
    yield test_path

    # Teardown: This runs AFTER the test function finishes
    if test_path.exists():
        shutil.rmtree(base_tmp)
        print(f"\nSuccessfully cleaned up {base_tmp}")
