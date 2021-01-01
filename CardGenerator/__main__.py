import argparse
from pathlib import Path

from . import CardList
from . import FileWriter as FW

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('card_list_file')
    parser.add_argument('--file_type', '-t', choices=FW.Types.keys(), default='svg')
    parser.add_argument('--dist_dir', '-d', default='.')
    args = parser.parse_args()

    card_list = CardList.loadJson(args.card_list_file)
    for cards in card_list.GenerateSVG():
        for name, tree in cards:
            FW.writeFile(tree, Path(args.dist_dir) / name, args.file_type)

if __name__ == '__main__':
    main()
