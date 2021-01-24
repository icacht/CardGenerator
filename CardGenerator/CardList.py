import collections.abc as tp
from typing import Any
from dataclasses import dataclass, InitVar
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from . import CardStyle as CS
from . import DeckConstractor as DC
from . import FileWriter as FW

@dataclass
class CardList:
    style: InitVar[dict[str, dict[str, str]]]
    text: list[dict[str, str]]
    deck: dict[str, Any] = None
    file_root: Path = Path('.')

    loadedStyle: dict[str, CS.CardStyle] = None

    def __post_init__(self, style):
        self.loadedStyle = {
            k: CS.CardStyle(**s, file_root=self.file_root)
            for k, s in style.items()}

    def GenerateSVG(self) -> tp.Iterator[tuple[
                                dict[str, str],
                                dict[str, tuple[str, ET.ElementTree]]]]:
        for t in self.text:
            print(t['title'])
            yield t, {k: s.GenerateSVG(t) for k, s in self.loadedStyle.items()}

    def GenerateFile(self, dist_path: Path, file_type: str) -> None:
        for _text, trees in self.GenerateSVG():
            for name, tree in trees.values():
                FW.writeFile(tree, dist_path / name, file_type)

    def ConstractDeck(self, file_path: Path, img_file_type: str) -> None:
        if self.deck is None:
            raise Exception("Deck Settings is Not Found.")

        with DC.DeckConstractor(
                archive_name=file_path,
                **self.deck,
                file_root=self.file_root) as deck_constractor:
            for text, trees in self.GenerateSVG():
                imgs = {
                    k: (tree, img_file_type)
                    for k, (_name, tree) in trees.items()}
                deck_constractor.AddCard(text, imgs)
            deck_constractor.WriteRoot()

def loadJson(card_list_file: str):
    file_path = Path(card_list_file)
    with file_path.open(encoding='utf-8') as f:
        card_list_dict = json.load(f)
    
    return CardList(**card_list_dict, file_root=file_path.parent)
