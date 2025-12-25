import argparse
import os
from pathlib import Path
import subprocess
import yaml

from src.helpers import path_to_name


# ====================================================================================
# TRANSCRIBE
# ====================================================================================


def transcribe_audio(src, language, model, output_dir):
    command = [
        "whisper", src,
        "--language", language,
        "--model", model,
        # "--verbose", "False",
        "--output_format", "json",
        "--output_dir", output_dir
    ]
    
    # print(command)
    subprocess.run(command)


# ====================================================================================
# MAIN
# ====================================================================================


def main(dirs: list[str], language, model):
    
    # check if embeddings folder exists, (warn and remove)
    ...

    # get list of audio files
    audio_files = []
    for dir in dirs:
        files = list(Path(dir).rglob("*"))
        audio_files.extend(files)
    
    # for each file, transcribe
    for idx, file in enumerate(audio_files):
        save_dir = f"transcripts/{path_to_name(str(file.parent))}"
        print("\n  {:>3}/{}  TRANSCRIBING  {}".format(idx+1, len(audio_files), file.name))

        os.makedirs(save_dir, exist_ok=True)

        # continue
        ret = transcribe_audio(
            str(file),
            language,
            model,
            save_dir,
        )
    # 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', help='')
    args = parser.parse_args()
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print()
    main(
        config['audio_directories'],
        config['language'],
        config['whisper_model_size'],
    )
    print()
