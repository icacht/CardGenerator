import math
import xml.etree.ElementTree as ET

svg_namespace = {
    "default": "http://www.w3.org/2000/svg",
    "xlink": "http://www.w3.org/1999/xlink"
}

def adjustFontSize(text, font_family, size_max, width, linage):
    max_width = width * linage
    min_size = max_width/len(text)
    return min(size_max, int(min_size))

def wrap(text, length):
    while text:
        l = length
        if len(text) > l and (text[l] in ['。', '、', '」', '】', ')', '）']):
            l += 1
        if len(text) > l - 1 and (text[l-1] in ['「', '【', '(', '（']):
            l -= 1
        t = text[:l]
        yield t
        text = text[l:]

def wrapText(text, font_family, size, width):
    length = int(width / size)
    return list(wrap(text, length))

def setText(element, style, text):
    if not text:
        return

    size = adjustFontSize(text, style['font-family'], style['font-size'], style['width'], style['linage-max'])
    texts = wrapText(text, style['font-family'], size, style['width'])
    print(size, texts)

    se = ET.SubElement(element, 'text')
    se.set('font-family', style['font-family'])
    se.set('font-size', str(size))

    height_align = style.get('height-align', '')
    if len(texts) == 1:
        se.text = texts[0]
        y = 0
        if "center" in height_align:
            y -= (style['font-size'] - size) // 3
        if y != 0:
            se.set('y', str(y))
    else:
        line_height = style['line-height']
        for i, t in enumerate(texts):
            see = ET.SubElement(se, 'tspan')
            see.text = t
            see.set('x', "0")

            y = i * line_height
            if 'lower' in height_align:
                y -= line_height * (len(texts) - 1)
            if 'center' in height_align:
                y -= math.ceil(line_height * (len(texts) - 1) / 2)
            see.set('y', str(y))

if __name__ == '__main__':
    import argparse
    import json
    import subprocess
    from pathlib import Path
    import tempfile

    def main():
        inkscape_path = "C:\\Program Files\\Inkscape\\inkscape.com"

        parser = argparse.ArgumentParser()
        parser.add_argument('--format', '-f', choices=['svg', 'png'], default='png')
        parser.add_argument('--dist_dir', '-d', default='.')
        parser.add_argument('config')
        args = parser.parse_args()

        with open(args.config, encoding='utf-8') as f:
            configs = json.load(f)

        for k, v in svg_namespace.items():
            ET.register_namespace(k if k != 'default' else '', v)

        for style in configs['style']:
            print(style)
            with open(style['style_file'], encoding='utf-8') as f:
                s = json.load(f)
                se = s['element']
                sb = s['base_file']

            for t in configs['text']:
                print(t['title'])
                tree = ET.parse(sb)

                for ek, ev in se.items():
                    e = tree.find(f".//default:g[@id='{ek}']", svg_namespace)
                    if e is None:
                        raise Exception("Not Found in SVG.", ek)
                    setText(e, ev, t[ek])

                dist_file = str((Path(args.dist_dir) / style['file_name'].format(t['title'])).with_suffix("."+args.format))
                if args.format == 'svg':
                    tree.write(dist_file, encoding="utf-8", xml_declaration=True)
                elif args.format == 'png':
                    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".svg", delete=False) as f:
                        temp_path = Path(f.name)
                        tree.write(f, encoding="utf-8", xml_declaration=True)
                    command = [inkscape_path, "--without-gui", f"--file={str(temp_path)}", f"--export-png={dist_file}", "-d 350"]
                    subprocess.run(command, shell=True)
                    temp_path.unlink()

    main()
