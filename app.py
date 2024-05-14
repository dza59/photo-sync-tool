import streamlit as st
import os
from pathlib import Path
import shutil
import time


def sync_folders(main_folder):
    if not main_folder.exists():
        return "The specified folder does not exist.", [], []

    jpg_folder = main_folder / 'jpg'
    raw_folder = main_folder / 'Raw'
    temp_folder = main_folder / 'temp'

    # loop all JPG and CR3 files
    jpg_files = {f.stem: f for f in jpg_folder.glob('*.JPG')}
    raw_files = {f.stem: f for f in raw_folder.glob('*.CR3')}

    # get unmatched files
    unmatched_jpg = jpg_files.keys() - raw_files.keys()
    unmatched_raw = raw_files.keys() - jpg_files.keys()

    if not unmatched_jpg and not unmatched_raw:
        return "JPG and RAW photos are already synced. No sync needed.", [], []

    temp_folder.mkdir(exist_ok=True)

    # move unmatched files to a temp folder
    for file_stem in unmatched_jpg:
        shutil.move(str(jpg_folder / (file_stem + '.JPG')), str(temp_folder))
    for file_stem in unmatched_raw:
        shutil.move(str(raw_folder / (file_stem + '.CR3')), str(temp_folder))

    return "Unmatched files moved to temporary folder. Please review before final deletion.", list(unmatched_jpg), list(unmatched_raw)


def main():
    st.cache_data.clear()
    st.set_page_config(page_title="JPG and RAW Photo Sync by Danni Zhang ✨")
    st.title("JPG and RAW Photo Sync Tool 📷")
    st.subheader('by Danni Z. ✨')

    # get folder path
    folder_path = st.text_input("Enter the folder path:")

    if st.button("🔁 Sync Folders"):
        if folder_path:
            main_folder = Path(folder_path)
            with st.spinner('🏃 ...'):
                result, unmatched_jpg, unmatched_raw = sync_folders(
                    main_folder)
            st.write(result)

            if unmatched_jpg or unmatched_raw:
                # store results in session state
                st.session_state.unmatched_jpg = unmatched_jpg
                st.session_state.unmatched_raw = unmatched_raw
                st.session_state.main_folder = folder_path

                st.write("Unmatched JPG files:", unmatched_jpg)
                st.write("Unmatched RAW files:", unmatched_raw)
            else:
                st.write("💃 No unmatched files to delete. 🕺🏼 🎉")
        else:
            st.error("⚠️ Please enter a valid folder path.")

    # comfirm deleting unmatched files
    if 'unmatched_jpg' in st.session_state and 'unmatched_raw' in st.session_state:
        if st.session_state.unmatched_jpg or st.session_state.unmatched_raw:
            warning = st.warning(
                "⚠️ Unmatched files moved to temporary folder. Please review before final deletion.")

            del_btn = st.button("💀 Delete Duplicate Files")
            if del_btn:
                with st.spinner('🏃 Running ...'):
                    temp_folder = Path(st.session_state.main_folder) / 'temp'
                    shutil.rmtree(temp_folder)

                    # clear session state after all done
                    del st.session_state.unmatched_jpg
                    del st.session_state.unmatched_raw
                    del st.session_state.main_folder

                st.success(
                    "Unmatched files and temporary folder have been permanently deleted.")
                warning.empty()
                time.sleep(2)
                st.rerun()


if __name__ == "__main__":
    main()
