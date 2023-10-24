import os
from googletrans import Translator


def load_translation_record(record_file):
    if not os.path.exists(record_file):
        return set(), {}

    with open(record_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    original_folders = set()
    translation_record = {}

    for line in lines:
        original_name, translated_name = line.strip().split(" -> ")
        original_folders.add(original_name)
        translation_record[original_name] = translated_name

    return original_folders, translation_record


def save_translation_record(record_file, original_folders, translation_record):
    with open(record_file, "w", encoding="utf-8") as file:
        for original_name, translated_name in translation_record.items():
            file.write(f"{original_name} -> {translated_name}\n")


def rename_folders_recursively(root_path, translator, dest_language="en"):
    record_file = "translation_record.txt"
    original_folders, translation_record = load_translation_record(record_file)

    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            if not dir.startswith(".") and dir not in original_folders:
                folder_path = os.path.join(root, dir)
                translated_name = translator.translate(dir, dest=dest_language).text
                new_folder_path = os.path.join(root, translated_name)

                try:
                    os.rename(folder_path, new_folder_path)
                    print(f"Renamed folder: {folder_path} -> {new_folder_path}")
                    original_folders.add(dir)
                    translation_record[dir] = translated_name
                except Exception as e:
                    print(f"An error occurred while renaming: {e}")

    save_translation_record(record_file, original_folders, translation_record)


if __name__ == "__main__":
    translator = Translator()

    root_folder = "your_root_folder_path"

    if os.path.exists(root_folder):
        rename_folders_recursively(root_folder, translator)
        print("Folder renaming completed.")
    else:
        print("The specified root folder does not exist.")
