import shutil
import sys
import re
from pathlib import Path

all_extensions = set()
folders = list()
registered_extensions = {
    "images": [],
    "video": [],
    "documents": [],
    "audio": [],
    "archives": [],
    "others": []
}

EXTENSIONS_DICT = {
    "images": (".jpeg", ".png", ".jpg", ".svg", ".dng"),
    "video": (".avi", ".mp4", ".mov", ".mkv"),
    "documents": (".doc", ".docx", ".txt", ".pdf", ".xls", ".xlsx"),
    "audio": (".mp3", ".ogg", ".wav", ".amr"),
    "archives": (".zip", ".gz", ".tar")
}

UKRAINIAN_SYMBOLS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", 
    "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
    "h", "ts", "ch", "sh", "sch", "", "ju", "ja"
)


TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split(".")
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


# отримуємо ім'я файлу та повертаємо його розширення у нижньому регістрі
def get_extensions(file_name):
    return Path(file_name).suffix.lower()


# виконуємо рекурсивне сканування папки та групування файлів за категоріями відповідно до їх розширень
def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            folders.append(item)
            scan(item)
            continue

        extension = get_extensions(item.name)
        new_name = folder / item.name
        added_to_category = False

        for category, ext_list in EXTENSIONS_DICT.items():
            if extension in ext_list:
                registered_extensions[category].append(new_name)
                added_to_category = True
                break

        if not added_to_category:
            registered_extensions["others"].append(new_name)


# обробляємо файли і переносимо їх у відповідну папку залежно від категорії
def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    if dist == "others":
        new_name = path.name
    else:
        new_name = normalize(path.name)

    new_path = target_folder / new_name
    path.replace(new_path)


# обробляємо архіви та переміщуємо їх у створені папки
def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.stem)  

    archive_folder = (target_folder / "archives" / new_name)  
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

# рекурсивно видаляємо порожні папки
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


# рекурсивно видаляє порожні папки з кореневої папки
def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


#  обробляємо та сортуємо файли в папках
def main():
    path = sys.argv[1]
    print(f"Scanning in: {path}")
    folder_path = Path(path)
    
    scan(folder_path)

    for ext, container in registered_extensions.items():
        if ext in EXTENSIONS_DICT:
            for file in container:
                hande_file(file, folder_path, ext)
        elif ext == "archives":
            for file in container:
                handle_archive(file, folder_path, "archives")
        elif ext == "others":
            for file in container:
                hande_file(file, folder_path, "others")

    for container in registered_extensions.values():
        for file in container:
            extension = get_extensions(file.name)
            all_extensions.add(extension)

    remove_empty_folders(folder_path)


if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Scanning in: {path}")

    arg = Path(path)
    main(arg)
    scan(arg)

    # виводимо списки файлів та розширень відповідно до категорій
    print(f"Images: {registered_extensions['images']}\n")
    print(f"Video: {registered_extensions['video']}\n")
    print(f"Documents: {registered_extensions['documents']}\n")
    print(f"Audio: {registered_extensions['audio']}\n")
    print(f"Archives: {registered_extensions['archives']}\n")
    print(f"Others: {registered_extensions['others']}\n")
    print(f"All extensions: {all_extensions}\n")