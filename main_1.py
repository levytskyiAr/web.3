import sys
import re
import shutil
from pathlib import Path
import concurrent.futures

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'DOCX': DOCX_DOCUMENT,
    'TXT': TXT_DOCUMENT,
    'PDF': PDF_DOCUMENT,
    'XLSX': XLSX_DOCUMENT,
    'PPTX': PPTX_DOCUMENT,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str) -> str:
    translate_name = re.sub(r'[^\w.]', '_', name.translate(TRANS))
    return translate_name

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def process_files(files, target_folder):
    for file in files:
        handle_media(file, target_folder)

def process_directory(directory):
    scan(directory)

    categories = [
        (JPEG_IMAGES, directory / 'images' / 'JPEG'),
        (JPG_IMAGES, directory / 'images' / 'JPG'),
        (PNG_IMAGES, directory / 'images' / 'PNG'),
        (SVG_IMAGES, directory / 'images' / 'SVG'),
        (AVI_VIDEO, directory / 'videos' / 'AVI'),
        (MP4_VIDEO, directory / 'videos' / 'MP4'),
        (MOV_VIDEO, directory / 'videos' / 'MOV'),
        (MKV_VIDEO, directory / 'videos' / 'MKV'),
        (MP3_AUDIO, directory / 'audio' / 'MP3'),
        (OGG_AUDIO, directory / 'audio' / 'OGG'),
        (WAV_AUDIO, directory / 'audio' / 'WAV'),
        (AMR_AUDIO, directory / 'audio' / 'AMR'),
        (DOCX_DOCUMENT, directory / 'documents' / 'DOCX'),
        (TXT_DOCUMENT, directory / 'documents' / 'TXT'),
        (PDF_DOCUMENT, directory / 'documents' / 'PDF'),
        (XLSX_DOCUMENT, directory / 'documents' / 'XLSX'),
        (PPTX_DOCUMENT, directory / 'documents' / 'PPTX'),
        (ZIP_ARCHIVES, directory / 'archives' / 'ZIP'),
        (GZ_ARCHIVES, directory / 'archives' / 'GZ'),
        (TAR_ARCHIVES, directory / 'archives' / 'TAR'),
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for files, target_folder in categories:
            future = executor.submit(process_files, files, target_folder)
            futures.append(future)

        concurrent.futures.wait(futures)

def main(folder: Path):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for item in folder.iterdir():
            if item.is_dir():
                future = executor.submit(process_directory, item)
                futures.append(future)

        concurrent.futures.wait(futures)

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_process = Path(sys.argv[1])
        main(folder_process)