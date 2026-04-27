import argparse
import re
from pathlib import Path

import time
from urllib.parse import quote
import base64
import requests
import curl_cffi as cc_requests
from bs4 import BeautifulSoup

import pytest
from unittest.mock import MagicMock
import shutil

# ALL_TENSES = ['Indicatif Présent', 'Indicatif Imparfait', 'Indicatif Futur',
#           'Indicatif Passé simple', 'Indicatif Passé composé', 'Indicatif Plus-que-parfait',
#           'Indicatif Passé antérieur', 'Indicatif Futur antérieur',
#           'Subjonctif Présent', 'Subjonctif Imparfait', 'Subjonctif Plus-que-parfait', 'Subjonctif Passé',
#           'Conditionnel Présent', 'Conditionnel Passé première forme', 'Conditionnel Passé deuxième forme',
#           'Participe Présent', 'Participe Passé composé', 'Participe Passé',
#           'Impératif Présent', 'Impératif Passé',
#           'Infinitif Présent', 'Infinitif Passé']


def get_audio_url(text: str) -> str:
    """
    Enter a French phrase to generate corresponding audio URL.

    Args:
        text (str): a French phrase
    Returns:
        str: audio url
    """
    voice_id = encode_voice_uid(text)
    return f"https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Bruno22k?inputText={voice_id}"


def encode_voice_uid(text: str) -> str:
    """
    Convert a French phrase to an voice unique ID.

    Args:
        text (str): A French phrace
    Returns:
        str: voice unique ID
    """
    # Mimic javascript encodeURIComponent
    encoded = quote(text, safe="~()*!'")

    # Convert hex escapes to their actual character equivalents
    binary_string = re.sub(
        r"%([0-9,A-F]{2})", lambda m: chr(int(m.group(1), 16)), encoded
    )

    # Mimic javascript btoa
    binary_bytes = binary_string.encode("latin-1")
    return base64.b64encode(binary_bytes).decode("utf-8")


def get_request_header() -> dict[str, str]:
    """
    Return requested headers for Reverso.

    Resturns:
        dict[str, str]: requested headers
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.7",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://conjugator.reverso.net/conjugation-french.html",
    }
    return headers


def fetch_html_text(verb: str) -> str:
    """
    Fetches the HTML content for a French infinitive. \
    This function generates a URL based on the input verb, requests the page, \
    and returns the raw HTML as a text string.

    Args: 
        verb (str): a French infinitive verb
    Returns:
        str: The raw HTML content or an empty string if the request fails
    """
    url = f"https://conjugator.reverso.net/conjugation-french-verb-{verb}.html"

    response = requests.get(url, headers=get_request_header())
    if response.status_code == 200:
        return response.text
    print("fail to get html:", response.status_code)
    if response.status_code == 404:
        print("[404] The verb entered does not match any possible conjugation table.")
    elif response.status_code == 403:
        print("[403] Request forbidden")
    return ""


def fetch_verb_conjugation(bs: BeautifulSoup, tense: str) -> set[str]:
    """
    Extracts a set of French conjugated verb phrases \
        from the provided HTML for a specific tense. 

    Args:
        bs (BeautifulSoup): A data structure representing a parsed HTML
        tense (str): A specific French tense 
    Returns:
        set[str]: A set of French conjugated verb phrases regarding the tense \
            or an empty set if the requested tense not found
    """
    result = bs.find_all(attrs={"mobile-title": tense})
    conj_verbs = set()
    if len(result) == 1:
        for phrase in result[0].find_all("li"):
            subject, *rest = phrase.find_all("i")
            verb_part = "".join([v.string for v in rest])
            if "il" in subject.string:  # for il/elle or ils/elles
                subject = subject.string.split("/")[0]
                conj_verbs.add(f"{subject} {verb_part}")
            else:
                subject = subject.string
                conj_verbs.add(f"{subject}{verb_part}")
    else:
        print(f"Entering the wrong tense: {len(result)} of results was found")
    return conj_verbs


def download_audios(
    session: cc_requests.Session, folder_name: Path, conj_verbs: set[str]
):
    """
    Download MP3 audio files for a set of French conjugated phrases.
    
    Args:
        session (curl_cffi.Session): A session object from curl_cffi used to \
            impersonate browser TLS/JA3 and HTTP/2 fingerprints.
        folder_name (pathlib.Path): The Path of the directory where audio files will be stored \
        conj_verbs (set[str]): A set of French conjugated phrases
    Returns:
        bool: Return True if successfully downloaded all audio files.
    """
    success = True
    folder_name.mkdir(parents=True, exist_ok=True)

    for verb in conj_verbs:
        url = get_audio_url(verb)
        response = session.get(url)
        if response.status_code == 200:
            file = folder_name / f"{verb.replace(' ', '_')}.mp3"
            with open(file, "wb") as f:
                f.write(response.content)
        else:
            success = False
            print(f"Failed to download: {verb}.mp3")
        time.sleep(1)

    return success


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
    parse.add_argument("--inf_past", action="store_true", help="Infinitif Passé")

    args = parse.parse_args()
    html = fetch_html_text(args.inf_verb)

    if html != "":
        bs = BeautifulSoup(html, "html.parser")
        session = cc_requests.Session(impersonate="chrome120")
        folder = Path(args.inf_verb)

        result = fetch_verb_conjugation(bs, "Infinitif Présent")
        download_audios(session, folder / "Infinitif_Présent", result)

        if args.present:
            result = fetch_verb_conjugation(bs, "Indicatif Présent")
            download_audios(session, folder / "Indicatif_Présent", result)
        if args.future:
            result = fetch_verb_conjugation(bs, "Indicatif Futur")
            download_audios(session, folder / "Indicatif_Futur", result)
        if args.past:
            result = fetch_verb_conjugation(bs, "Indicatif Passé composé")
            download_audios(session, folder / "Indicatif_Passé_composé", result)
        if args.past_simple:
            result = fetch_verb_conjugation(bs, "Indicatif Passé simple")
            download_audios(session, folder / "Indicatif_Passé_simple", result)
        if args.conditional:
            result = fetch_verb_conjugation(bs, "Conditionnel Présent")
            download_audios(session, folder / "Conditionnel_Présent", result)
        if args.imperative:
            result = fetch_verb_conjugation(bs, "Impératif Présent")
            download_audios(session, folder / "Impératif_Présent", result)
        if args.inf_past:
            result = fetch_verb_conjugation(bs, "Infinitif Passé")
            download_audios(session, folder / "Infinitif_Passé", result)

        print("Complete download.")


if __name__ == "__main__":
    main()


#
def test_get_audio_url():
    domain = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Bruno22k?inputText="
    assert get_audio_url("test") == f"{domain}dGVzdA=="
    assert get_audio_url("") == f"{domain}"


def test_encode_voice_uid():
    assert encode_voice_uid("j'ai") == "aidhaQ=="
    assert encode_voice_uid("ils eurent") == "aWxzIGV1cmVudA=="
    assert encode_voice_uid("nous eûmes") == "bm91cyBlw7ttZXM="
    assert encode_voice_uid("tu as eu") == "dHUgYXMgZXU="
    assert encode_voice_uid("vous aurez") == "dm91cyBhdXJleg=="
    assert encode_voice_uid("il a eu") == "aWwgYSBldQ=="


def test_get_request_header():
    assert isinstance(get_request_header(), dict)


def test_fetch_html_text_ampty_input():
    # Test ampty input
    expected_result = [
        "Verb of the day: ",
        "Most popular verbs",
        "Translate, conjugate, spellcheck in one click, from your browser",
    ]
    actual_html = fetch_html_text("")
    actual_result = BeautifulSoup(actual_html, "html.parser").find_all("p")
    actual_result = [e.string for e in actual_result if e.string]
    assert expected_result == actual_result[:-1]
    time.sleep(1)


def test_fetch_html_text_normal_input():
    # Test normal input
    expected_result = """
        Présent, Imparfait, Futur, Passé simple, Passé composé, Plus-que-parfait, 
        Passé antérieur, Futur antérieur, Présent, Imparfait, Plus-que-parfait, 
        Passé, Présent, Passé première forme, Passé deuxième forme, Présent, 
        Passé composé, Passé, Présent, Passé, Présent, Passé
    """.replace("\n", "").split(",")
    expected_result = [e.strip() for e in expected_result]

    actual_html = fetch_html_text("pouvoir")
    actual_result = BeautifulSoup(actual_html, "html.parser").find_all("p")
    actual_result = [e.string for e in actual_result if e.string]
    assert expected_result == actual_result[:-1]
    time.sleep(1)


def test_fetch_html_text_invalid_input():
    # Test verb entered does not match any possible verb
    actual_html = fetch_html_text("abc")
    assert actual_html == ""


def test_fetch_verb_conjugation():
    except_result = set(["il a", "tu as"])
    test = '<div class="blue-box-wrap" mobile-title="Indicatif Présent"><p>Présent</p><ul class="wrap-verbs-listing"><li><i class="graytxt">il/elle</i><i class="verbtxt">a</i></li><li><i class="graytxt">tu </i><i class="verbtxt">as</i></li></ul></div>'
    actual_result = fetch_verb_conjugation(BeautifulSoup(test), "Indicatif Présent")
    assert except_result == actual_result


def test_download_audios_success(temp_output_dir):
    mock_session = MagicMock()
    mock_response = MagicMock()

    mock_response.status_code = 200
    mock_response.content = b"fake_mp3_binary_data"
    mock_session.get.return_value = mock_response

    test_url = get_audio_url("test_audio")
    test_file = temp_output_dir / "test_audio.mp3"
    result = download_audios(mock_session, temp_output_dir, set(["test_audio"]))

    assert result is True
    assert test_file.exists()
    assert test_file.read_bytes() == b"fake_mp3_binary_data"
    mock_session.get.assert_called_once_with(test_url)


def test_download_audios_failure(temp_output_dir):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 404  # Simulate not found
    mock_session.get.return_value = mock_response

    test_file = temp_output_dir / "test_audio.mp3"
    result = download_audios(mock_session, temp_output_dir, set(["test_audio"]))

    assert result is False
    assert not test_file.exists()


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
