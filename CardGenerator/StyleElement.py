from dataclasses import dataclass

@dataclass
class Element:
    font_family: str
    font_size: int
    linage_max: int
    width: int
    line_height: int = 0
    height_align: str = ''
