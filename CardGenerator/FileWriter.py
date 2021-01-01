import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

def saveSVG(tree: ET.ElementTree, dist_file_name: str):
    tree.write(dist_file_name, encoding="utf-8", xml_declaration=True)

def convertPng(tree: ET.ElementTree, dist_file_name: str):
    inkscape_path = "C:\\Program Files\\Inkscape\\inkscape.com"

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".svg", delete=False) as f:
        temp_path = Path(f.name)
        tree.write(f, encoding="utf-8", xml_declaration=True)

    try:
        command = [
            inkscape_path,
            "--without-gui",
            f"--file={str(temp_path)}",
            f"--export-png={dist_file_name}",
            "-d 350"
        ]
        subprocess.run(command, shell=True)
    finally:
        temp_path.unlink()

Types = {
    'svg': saveSVG,
    'png': convertPng
}

def writeFile(tree: ET.ElementTree, file_path: Path, type: str):
    dist_file_name = str(file_path.with_suffix(f".{type}"))
    Types[type](tree, dist_file_name)
