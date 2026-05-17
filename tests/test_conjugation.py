from fr_audio.conjugation import fetch_verb_conjugation


def test_fetch_verb_conjugation():
    expected_result = "j'ai\ttu as\til a\telle a\ton a\tnous avons\tvous avez\tils ont\telles ont".split(
        "\t"
    )
    actual_result = fetch_verb_conjugation("fr", "avoir", "indicatif", "présent")
    assert expected_result == actual_result
