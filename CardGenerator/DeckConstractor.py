from dataclasses import dataclass, InitVar
from pathlib import Path
import xml.etree.ElementTree as ET

from . import FileWriter as FW

DeckBase =\
"""<?xml version="1.0" encoding="UTF-8"?>
<card-stack location.name="table" location.x="0" location.y="0" posZ="0" rotate="0" zindex="14" owner="" isShowTotal="true">
  <data name="card-stack">
    <data name="image">
      <data type="image" name="imageIdentifier"></data>
    </data>
    <data name="common">
      <data name="name"></data>
    </data>
    <data name="detail">
    </data>
  </data>
  <node name="cardRoot">
  </node>
</card-stack>"""

CardBase =\
"""<card location.name="table" location.x="0" location.y="0" posZ="0" state="1" rotate="0" owner="" zindex="0">
    <data name="card">
        <data name="image">
            <data type="image" name="imageIdentifier"></data>
            <data type="image" name="front"></data>
            <data type="image" name="back"></data>
        </data>
        <data name="common">
            <data name="name"></data>
            <data name="size">2</data>
        </data>
        <data name="detail">
        </data>
    </data>
</card>"""

def findElement(element: ET.Element, tagPattern: str) -> ET.Element:
    e = element.find(tagPattern)
    if e is None:
        raise Exception(f"Not Found {tagPattern}.")
    return e

def addText(element: ET.Element, tagPattern: str, text: str) -> None:
    (findElement(element, tagPattern)).text = text

@dataclass
class CardText:
    key: str
    name: str
    type: str = "normal"

@dataclass
class DeckConstractor:
    deck_name: str
    card_name_key: str
    card_text: InitVar[list[dict[str, str]]]
    card_up: str = None
    card_up_key: str = None
    card_down: str = None
    card_down_key: str = None

    loadedCardText: list[CardText] = None
    loadedCardUp: str = None
    loadedCardDown: str = None

    def __post_init__(self, card_text) -> None:
        self.loadedCardText = [CardText(**t) for t in card_text]

    def InitDeck(self, fp: FW.ResourceArchiver):
        self.root = ET.fromstring(DeckBase)
        addText(self.root,
            ".//data[@name='common']/data[@name='name']", self.deck_name)
        self.cardRoot = findElement(self.root, ".//node[@name='cardRoot']")

        if self.card_up:
            self.loadedCardUp = fp.AddResource(Path(self.card_up))
        if self.card_down:
            self.loadedCardDown = fp.AddResource(Path(self.card_down))

    def AddCard(self, text: dict[str, str], img: dict[str, str]) -> None:
        card = ET.fromstring(CardBase)

        addText(card, ".//data[@name='common']/data[@name='name']", text[self.card_name_key])
        addText(card,
            ".//data[@name='image']/data[@type='image'][@name='front']",
            self.loadedCardUp if self.loadedCardUp else img[self.card_up_key])
        addText(card,
            ".//data[@name='image']/data[@type='image'][@name='back']",
            self.loadedCardDown if self.loadedCardDown else img[self.card_down_key])

        detail = findElement(card, ".//data[@name='detail']")
        for ct in self.loadedCardText:
            e = ET.Element('data')

            e.set('name', ct.name)
            if ct.type != 'normal':
                e.set('type', ct.type)
            e.text = text[ct.key]

            detail.append(e)
 
        self.cardRoot.append(card)

    def GetRoot(self) -> ET.Element:
        return self.root
