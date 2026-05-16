from pathlib import Path
import asyncio

import edge_tts


def download_audios(folder: Path, voice_model: str, sentences: list[str]) -> bool:
    """
    Download MP3 audio files for a set of French sentences.

    Args:
        folder (pathlib.Path): The Path of the directory where audio files will be stored
        voice_model (str): voice model (eg. 'fr-CA-JeanNeural')
        sentences (list[str]): A list of French sentences
    Returns:
        bool: Return True if successfully downloaded all audio files.
    """
    folder.mkdir(parents=True, exist_ok=True)
    if len(sentences) == 0:
        return False

    async def run_batch():
        tasks = []
        for phrase in sentences:
            file = folder / f"{phrase.replace(' ', '_')}.mp3"
            # create tasks
            tasks.append(edge_tts.Communicate(phrase, voice_model).save(file))

        # run all the tasks at the same time
        await asyncio.gather(*tasks)

    try:
        asyncio.run(run_batch())
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
