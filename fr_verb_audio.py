import argparse
import re
import os
import time
import random
from urllib.parse import quote
import base64
import requests
import curl_cffi as cc_requests
from bs4 import BeautifulSoup

# ALL_TENSES = ['Indicatif Présent', 'Indicatif Imparfait', 'Indicatif Futur',
#           'Indicatif Passé simple', 'Indicatif Passé composé', 'Indicatif Plus-que-parfait',
#           'Indicatif Passé antérieur', 'Indicatif Futur antérieur',
#           'Subjonctif Présent', 'Subjonctif Imparfait', 'Subjonctif Plus-que-parfait', 'Subjonctif Passé',
#           'Conditionnel Présent', 'Conditionnel Passé première forme', 'Conditionnel Passé deuxième forme',
#           'Participe Présent', 'Participe Passé composé', 'Participe Passé',
#           'Impératif Présent', 'Impératif Passé',
#           'Infinitif Présent', 'Infinitif Passé']


def get_audio_url(text):
    out = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Bruno22k?inputText="
    return out + encode_voice_uid(text)


def encode_voice_uid(text):
    # Mimic javascript encodeURIComponent
    encoded = quote(text, safe="~()*!'")

    # Convert hex escapes to their actual character equivalents
    binary_string = re.sub(
        r"%([0-9,A-F]{2})", lambda m: chr(int(m.group(1), 16)), encoded
    )

    # Mimic javascript btoa
    binary_bytes = binary_string.encode("latin-1")
    return base64.b64encode(binary_bytes).decode("utf-8")


def get_request_header():
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
    url = "https://conjugator.reverso.net/conjugation-french-verb-" + verb + ".html"
    response = requests.get(url, headers=get_request_header())
    if response.status_code == 200:
        return response.text
    print("fail to get html:", response.status_code)
    if response.status_code == 404:
        print("The verb entered does not match any possible conjugation table.")
    elif response.status_code == 403:
        print("Request forbidden")
    return ""


def fetch_verb_conjugation(bs: BeautifulSoup, tense):
    result = bs.find_all(attrs={"mobile-title": tense})
    conj_verbs = set()
    if len(result) == 1:
        for pronoun in result[0].find_all("li"):
            tmp = pronoun.find_all("i")
            if "il" in tmp[0].string:
                conj = (
                    tmp[0].string.split("/")[0]
                    + " "
                    + "".join([t.string for t in tmp[1:]])
                )
                conj_verbs.add(conj)
            else:
                conj = "".join([t.string for t in tmp])
                conj_verbs.add(conj)
    return conj_verbs


def download_audios(session, inf_verb, dir_name, conj_verbs):
    folder = inf_verb + "/" + dir_name.replace(" ", "_")
    # os -> pathlib
    os.makedirs(folder, exist_ok=True)

    for verb in conj_verbs:
        url = get_audio_url(verb)
        response = session.get(url)
        if response.status_code == 200:
            file = folder + "/" + verb.replace(" ", "_") + ".mp3"
            with open(file, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download: {verb}.mp3")
        time.sleep(random.uniform(1, 3))


def main():
    parse = argparse.ArgumentParser(
        prog="get_fr_verb_audio",
        description="""Download MP3 audio for French verb conjugations. 
                                                   Enter the infinitive form and use the options to specify which tenses to download. 
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

        result = fetch_verb_conjugation(bs, "Infinitif Présent")
        download_audios(session, args.inf_verb, "Infinitif Présent", result)

        if args.present:
            result = fetch_verb_conjugation(bs, "Indicatif Présent")
            download_audios(session, args.inf_verb, "Indicatif Présent", result)
        if args.future:
            result = fetch_verb_conjugation(bs, "Indicatif Futur")
            download_audios(session, args.inf_verb, "Indicatif Futur", result)
        if args.past:
            result = fetch_verb_conjugation(bs, "Indicatif Passé composé")
            download_audios(session, args.inf_verb, "Indicatif Passé composé", result)
        if args.past_simple:
            result = fetch_verb_conjugation(bs, "Indicatif Passé simple")
            download_audios(session, args.inf_verb, "Indicatif Passé simple", result)
        if args.conditional:
            result = fetch_verb_conjugation(bs, "Conditionnel Présent")
            download_audios(session, args.inf_verb, "Conditionnel Présent", result)
        if args.imperative:
            result = fetch_verb_conjugation(bs, "Impératif Présent")
            download_audios(session, args.inf_verb, "Impératif Présent", result)
        if args.inf_past:
            result = fetch_verb_conjugation(bs, "Infinitif Passé")
            download_audios(session, args.inf_verb, "Infinitif Passé", result)

        print("Complete download.")


if __name__ == "__main__":
    main()
