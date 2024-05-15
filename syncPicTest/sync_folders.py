import os
from pathlib import Path
import shutil


def sync_folders(main_folder):
    jpg_folder = main_folder / 'jpg'
    raw_folder = main_folder / 'Raw'

    if not jpg_folder.exists() or not raw_folder.exists():
        return "The 'jpg' and/or 'Raw' folders do not exist in the specified directory.", [], []

    temp_folder = main_folder / 'temp'

    # loop all JPG and CR3 files
    jpg_files = {f.stem: f for f in jpg_folder.glob('*.JPG')}
    raw_files = {f.stem: f for f in raw_folder.glob('*.CR3')}

    # get unmatched files
    unmatched_jpg = jpg_files.keys() - raw_files.keys()
    unmatched_raw = raw_files.keys() - jpg_files.keys()

    if not unmatched_jpg and not unmatched_raw:
        return "💃 JPG and RAW photos are already synced. No sync needed 🕺🏼 🎉", [], []

    return "⚠️ ⚠️  Unmatched files detected. Please review before final deletion.", list(unmatched_jpg), list(unmatched_raw)


def move_files_to_temp(main_folder, unmatched_jpg, unmatched_raw):
    temp_folder = main_folder / 'temp'
    temp_folder.mkdir(exist_ok=True)

    jpg_folder = main_folder / 'jpg'
    raw_folder = main_folder / 'Raw'

    # move unmatched files to a temp folder
    for file_stem in unmatched_jpg:
        shutil.move(str(jpg_folder / (file_stem + '.JPG')), str(temp_folder))
    for file_stem in unmatched_raw:
        shutil.move(str(raw_folder / (file_stem + '.CR3')), str(temp_folder))


def main():
    main_folder = Path(__file__).parent
    result, unmatched_jpg, unmatched_raw = sync_folders(main_folder)
    print(result)

    if unmatched_jpg or unmatched_raw:
        if unmatched_jpg:
            print("Unmatched JPG files:")
            for jpg in unmatched_jpg:
                print(f" - {jpg}.JPG")
        if unmatched_raw:
            print("Unmatched RAW files:")
            for raw in unmatched_raw:
                print(f" - {raw}.CR3")

        delete = input(
            "💀 ⚠️  Do you want to delete the unmatched files? (yes/no, press Enter for yes): ").strip().lower()
        if delete == 'yes' or delete == '':
            move_files_to_temp(main_folder, unmatched_jpg, unmatched_raw)
            temp_folder = main_folder / 'temp'
            shutil.rmtree(temp_folder)
            print("🎉 🎉 folders synced successfully. 🎉 🎉")
        else:
            print("⚠️ Review the unmatched files in the 'temp' folder before deletion.")
    else:
        print("💃 🕺🏼 🎉 No unmatched files to delete. 🎉")


if __name__ == "__main__":
    main()
