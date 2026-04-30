from src.fr_audio.main_cli import fetch_verb_conjugation, download_audios
import shutil
from pathlib import Path

import pytest

def test_fetch_verb_conjugation():
    expected_result = "j'ai\ttu as\til a\telle a\ton a\tnous avons\tvous avez\tils ont\telles ont".split(
        "\t"
    )
    actual_result = fetch_verb_conjugation("fr", "avoir", "indicatif", "présent")
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