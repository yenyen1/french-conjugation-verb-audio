from fr_audio.audio import download_audios, download_audio_with_specified_filename

import shutil
from pathlib import Path

import pytest


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


def test_download_audio_with_specified_filename_failure(temp_output_dir):
    temp_output_dir.mkdir(parents=True, exist_ok=True)
    file = temp_output_dir / "test.mp3"
    result = download_audio_with_specified_filename(file, "fr-CA-JeanNeural", "")
    assert result is False
    assert not file.exists()


def test_download_audio_with_specified_filename_success(temp_output_dir):
    temp_output_dir.mkdir(parents=True, exist_ok=True)
    file = temp_output_dir / "test.mp3"
    result = download_audio_with_specified_filename(
        file, "fr-CA-JeanNeural", "Vous devez remplir un formulaire"
    )
    assert result is True
    assert file.exists()


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
