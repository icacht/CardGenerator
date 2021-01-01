from dataclasses import dataclass, InitVar
from pathlib import Path
import json
import xml.etree.ElementTree as ET

from . import StyleElement as SE
from . import SVGProcessing as SP

def readExpandSvg(file_path: str):
    start_mark = '<!--element'
    end_mark = '-->'

    buf = Path(file_path).read_text(encoding='UTF-8')
    start_index = buf.index(start_mark)
    end_index = buf.index(end_mark, start_index)

    elementBuf = buf[start_index: end_index].lstrip(start_mark)
    elements = json.loads(elementBuf)

    return buf, elements

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
