import xml.etree.ElementTree as ET
import math

from . import TextProcessing as TP
from . import StyleElement as SE

SVGNamespace = {
    "default": "http://www.w3.org/2000/svg",
    "xlink": "http://www.w3.org/1999/xlink"
}

for k, v in SVGNamespace.items():
    ET.register_namespace(k if k != 'default' else '', v)

def setOneLine(sub_element: ET.SubElement, text: str, style: SE.Element, font_size: int):
    sub_element.text = text

    if "center" in style.height_align:
        y = (font_size - style.font_size) // 3
        sub_element.set('y', str(y))

def setLines(sub_element: ET.SubElement, texts: list[str], style: SE.Element):
    y_corrected = 0

    if 'lower' in style.height_align:
        y_corrected += style.line_height * (len(texts) - 1)

    if 'center' in style.height_align:
        y_corrected += math.ceil(style.line_height * (len(texts) - 1) / 2)

    for i, t in enumerate(texts):
        y = i * style.line_height - y_corrected

        e = ET.SubElement(sub_element, 'tspan')
        e.text = t
        e.set('x', "0")
        e.set('y', str(y))

def setText(element: ET.Element, text: str, style: SE.Element):
    if not text:
        return

    font_size = TP.adjustFontSize(
        text, style.font_size, style.width, style.linage_max)
    texts = TP.wrapText(text, font_size, style.width)
    # print(font_size, texts)

    se = ET.SubElement(element, 'text')
    se.set('font-family', style.font_family)
    se.set('font-size', str(font_size))

    if len(texts) == 1:
        setOneLine(se, texts[0], style, font_size)
    else:
        setLines(se, texts, style)

def getSvgGroupElement(tree: ET.ElementTree, key: str) -> ET.Element:
    query = f".//default:g[@id='{key}']"
    e = tree.find(query, SVGNamespace)
    if e is None:
        raise Exception("Not Found in SVG.", key)

    return e

def generateSVGContent(svg_text: str, text_contents: dict[str, str],
                       style_elements: dict[str, SE.Element]) -> ET.ElementTree:
    tree = ET.fromstring(svg_text)
    for k, v in style_elements.items():
        e = getSvgGroupElement(tree, k)
        setText(e, text_contents[k], v)

    return ET.ElementTree(element=tree)
