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
    deck: InitVar[dict[str, Any]] = None

    loadedDeck: DC.DeckConstractor = None
    loadedStyle: dict[str, CS.CardStyle] = None

    def __post_init__(self, style, deck):
        self.loadedStyle = {k: CS.CardStyle(**s) for k, s in style.items()}
        if deck:
            self.loadedDeck = DC.DeckConstractor(**deck)

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
        if self.loadedDeck is None:
            raise Exception("Deck Settings is Not Found.")

        with FW.ResourceArchiver(file_path) as fp:
            self.loadedDeck.InitDeck(fp)

            for text, trees in self.GenerateSVG():
                imgs = {k: fp.AddSVG(tree, img_file_type) for k, (_name, tree) in trees.items()}
                self.loadedDeck.AddCard(text, imgs)

            deck_str = ET.tostring(self.loadedDeck.GetRoot(), encoding='UTF-8', xml_declaration=True)
            fp.AddTextFile(deck_str, "data.xml")

def loadJson(card_list_file: str):
    with Path(card_list_file).open(encoding='utf-8') as f:
        card_list_dict = json.load(f)
    
    return CardList(**card_list_dict)
