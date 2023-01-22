from random import shuffle
from pathlib import Path
from argparse import ArgumentParser

def split_train_dev(input_folder) -> None:
    input_folder = Path(input_folder)
    with open(input_folder / "bambara.txt") as bambara:
        with open(input_folder / "french.txt") as french:
            lines = list(zip(bambara, french))
    
        shuffle(lines)
        n_lines = len(lines)
        test_size = int(0.35 * n_lines)
        test = lines[:test_size]
        train = lines[test_size:]

        test_bambara, test_french = zip(*test)
        train_bambara, train_french = zip(*train)

        with open(input_folder / f"bambara.test", "w") as test_bambara_file:
            test_bambara_file.write("".join(test_bambara))
        with open(input_folder / f"french.test", "w") as test_french_file:
            test_french_file.write("".join(test_french))
        with open(input_folder / f"bambara.train", "w") as train_bambara_file:
            train_bambara_file.write("".join(train_bambara))
        with open(input_folder / f"french.train", "w") as train_french_file:
            train_french_file.write("".join(train_french))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_texts_folder",
    help="Folder containing the text files.")
    args = parser.parse_args()

    split_train_dev(args.input_texts_folder)
