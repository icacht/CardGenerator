import collections.abc as tp

def adjustFontSize(text: str, size_max: int, width: int, linage: int) -> int:
    max_width = width * linage
    min_size = max_width // len(text)
    return min(size_max, min_size)

def wrap(text: str, length: int) -> tp.Iterator[str]:
    EndChar = ['。', '、', '」', '】', ')', '）']
    BeginningChar = ['「', '【', '(', '（']

    while text:
        l = length
        if len(text) > l and (text[l] in EndChar):
            l += 1
        if len(text) > l - 1 and (text[l-1] in BeginningChar):
            l -= 1
        t = text[:l]
        yield t
        text = text[l:]

def wrapText(text: str, size: int, width: int) -> list[str]:
    length = width // size
    return list(wrap(text, length))
