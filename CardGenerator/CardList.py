import collections.abc as tp
from dataclasses import dataclass, InitVar
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from . import CardStyle as CS

objects = list[dict[str, str]]

@dataclass
class CardList:
    style: InitVar[objects]
    text: objects

    loadedStyle: list[CS.CardStyle] = None

    def __post_init__(self, style):
        self.loadedStyle = [CS.CardStyle(**s) for s in style]

    def GenerateSVG(self) -> tp.Iterator[tp.Iterator[tuple[str, ET.ElementTree]]]:
        for t in self.text:
            print(t['title'])
            yield (s.GenerateSVG(t) for s in self.loadedStyle)

def loadJson(card_list_file: str):
    with Path(card_list_file).open(encoding='utf-8') as f:
        card_list_dict = json.load(f)
    
    return CardList(**card_list_dict)
