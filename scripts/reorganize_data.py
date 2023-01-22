from argparse import ArgumentParser
from shutil import copy, move
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
    for text_file in Path(input_folder).rglob("**/*"):
        filename = text_file.stem
        suffix = re.sub("\.", "", text_file.suffix)
        if suffix not in ["train", "test", "txt"]:
            continue
        source = text_file.parent.stem
        if source == "challenge" and suffix == "txt":
            continue
        output_folder_file = output_folder / source
        output_folder_file.mkdir(exist_ok=True, parents=True)
        filename = str(filename).split("_")[-1]
        filename = "french" if filename == "francais" else filename
        suffix = "train" if suffix == "txt" else suffix
        if filename not in languages:
            continue
        if source not in ["bibleis", "cormande"]:
            copy(text_file, output_folder_file)
            move(output_folder_file / text_file.name, output_folder_file / f"{filename}.{suffix}")
            continue
        pattern = r".*\[VERSE\]" if source == "bibleis" else (r".*\[BAM_COR\]" if filename == "bambara" else r".*\[FR_COR\]")
        with open(output_folder_file / f"{filename}.{suffix}", "w") as output_file:
            for line in clean_metadata(text_file, pattern):
                output_file.write(f"{line}\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_folder",
                        help="The folder containing the text files.")
    parser.add_argument("-o", "--output_folder",
                        help="The folder where the preocessed files will be stored.")
    
    args = parser.parse_args()
    reorganize_files(args.input_folder, args.output_folder)