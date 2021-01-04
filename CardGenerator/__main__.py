import argparse
from pathlib import Path

from . import CardList
from . import FileWriter as FW

def main():
    parser = argparse.ArgumentParser('Generate Card Image.')
    parser.add_argument('card_list_file', help='Card Text Json File.')
    parser.add_argument('--file_type', '-t', choices=FW.Types.keys(), default='svg',
        help='Output File Type.')
    parser.add_argument('--dist_dir', '-d', default='.', help='Output Directory.')
    parser.add_argument('--udonarium_deck', '-ud', default='', metavar='FILE_NAME',
        help="Output Udonarium Deck File.")
    args = parser.parse_args()

    card_list = CardList.loadJson(args.card_list_file)
    dist_path = Path(args.dist_dir)
    if args.udonarium_deck:
        card_list.ConstractDeck(dist_path / args.udonarium_deck, args.file_type)
    else:
        card_list.GenerateFile(dist_path, args.file_type)

if __name__ == '__main__':
    main()
