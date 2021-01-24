from dataclasses import field
import subprocess
import tempfile
import hashlib
from pathlib import Path
from zipfile import ZipFile
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

def writeFile(tree: ET.ElementTree, file_path: Path, type: str) -> None:
    dist_file_name = str(file_path.with_suffix(f".{type}"))
    Types[type](tree, dist_file_name)


class ResourceArchiver:
    def __init__(self, file_name: Path):
        file_name_zip = file_name.with_suffix('.zip')
        self.zipFile = ZipFile(file_name_zip, 'w')
        self.file_name_cache: dict[str, str] = {}

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _treceback):
        self.close()
        return False
    
    def close(self) -> None:
        self.zipFile.close()

    def AddTextFile(self, text: str, arcname: str=None) -> str:
        if arcname is None:
            text_b = bytes(text, encoding='utf-8')
            name = hashlib.sha256(text_b).hexdigest()
        else:
            name = arcname
        self.zipFile.writestr(name, text)
        return name

    def AddResource(self, file_path: Path, arcname: str=None) -> str:
        if str(file_path) in self.file_name_cache:
            return self.file_name_cache[str(file_path)]

        if arcname:
            self.zipFile.write(file_path, arcname)
            return arcname

        data = file_path.read_bytes()
        name = hashlib.sha256(data).hexdigest()
        self.zipFile.write(file_path, name + file_path.suffix)
        self.file_name_cache[str(file_path)] = name
        return name

    def AddSVG(self, tree: ET.ElementTree, file_type: str, arcname: str=None) -> str:
        temp_file = tempfile.NamedTemporaryFile(
                        mode="w+b", suffix=f'.{file_type}', delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()

        try:
            writeFile(tree, temp_path, file_type)
            name = self.AddResource(temp_path, arcname)
        finally:
            temp_path.unlink()
        return name
