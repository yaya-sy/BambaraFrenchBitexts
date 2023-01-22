from shutil import copy
from pathlib import Path
import re

def clean_metadata(bibleis_file: str, pattern):
    with open(bibleis_file, "r") as text_file:
        for line in text_file:
            line = re.sub(pattern, "", line)
            line = line.strip()
            yield line

def reorganize_files(input_folder: str,
                     output_folder: str) -> None:
    languages = ["bambara", "french", "dioula"]
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)
    for text_file in Path(input_folder).rglob("*.txt"):
        filename = text_file.stem
        source = text_file.parent.stem
        output_folder_file = output_folder / source
        output_folder_file.mkdir(exist_ok=True, parents=True)
        filename = str(filename).split("_")[-1]
        filename = "french" if filename == "francais" else filename
        if filename not in languages:
            continue
        if source not in ["bibleis", "cormande"]:
            copy(text_file, output_folder_file)
            continue
        pattern = r".*\[VERSE\]" if source == "bibleis" else (r".*\[BAM_COR\]" if filename == "bambara" else r".*\[FR_COR\]")
        with open(output_folder_file / f"{filename}.txt", "w") as output_file:
            for line in clean_metadata(text_file, pattern):
                output_file.write(f"{line}\n")

reorganize_files("data/raw", "data/reorganized")