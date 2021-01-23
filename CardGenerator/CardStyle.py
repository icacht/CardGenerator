from dataclasses import dataclass, InitVar
from typing import Any
from pathlib import Path
import json
import xml.etree.ElementTree as ET

from . import StyleElement as SE
from . import SVGProcessing as SP

def separateElements(text: str) -> dict[str, Any]:
    start_mark = '<!--element'
    end_mark = '-->'

    start_index = text.index(start_mark)
    end_index = text.index(end_mark, start_index)

    elementBuf = text[start_index: end_index].lstrip(start_mark)
    elements = json.loads(elementBuf)

    return elements

def readExpandSvg(file_path: str) -> tuple[str, dict[str, Any]]:
    buf = Path(file_path).read_text(encoding='UTF-8')
    return buf, separateElements(buf)

@dataclass
class CardStyle:
    style_file: InitVar[str]
    file_name: str = "{0}"

    loadedSvg: str = None
    loadedElements: dict[str, SE.Element] = None

    def __post_init__(self, style_file):
        (self.loadedSvg, elements) = readExpandSvg(style_file)
        self.loadedElements = {k: SE.Element(**v) for k, v in elements.items()}

    def GenerateSVG(self, texts: dict[str, str]) -> tuple[str, ET.ElementTree]:
        name = self.file_name.format(texts['title'])
        return name, SP.generateSVGContent(self.loadedSvg, texts, self.loadedElements)
