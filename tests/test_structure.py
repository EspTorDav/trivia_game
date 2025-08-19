import os
import pytest

@pytest.mark.parametrize("directory", ["src", "tests", "docs", "data"])
def test_directories_exist(directory):
    assert os.path.isdir(directory), f"❌ La carpeta {directory}/ no existe"

@pytest.mark.parametrize("file", ["README.md", ".gitignore", "data/questions.json"])
def test_files_exist(file):
    assert os.path.isfile(file), f"❌ El archivo {file} no existe"
