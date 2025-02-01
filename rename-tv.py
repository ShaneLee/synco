#!usr/bin/env python3

import os
import re

def rename_tv_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith((".mkv", ".mp4", ".avi")):
                # Extract show name, season, and episode using regex
                match = re.search(r'(.*?)[._ -]+S(\d{2})E(\d{2})', file, re.IGNORECASE)
                if match:
                    show_name, season, episode = match.groups()
                    show_name_clean = re.sub(r'[._]', ' ', show_name).strip().title()
                    season_folder = f"Season {int(season)}"
                    new_filename = f"{show_name_clean} - S{season}E{episode}{os.path.splitext(file)[1]}"

                    show_folder_path = os.path.join(root_dir, show_name_clean)
                    season_folder_path = os.path.join(show_folder_path, season_folder)
                    os.makedirs(season_folder_path, exist_ok=True)

                    old_path = os.path.join(dirpath, file)
                    new_path = os.path.join(season_folder_path, new_filename)
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                else:
                    print(f"Skipped: {file} (No matching pattern)")

if __name__ == "__main__":
    root_directory = os.path.expanduser("media/tv")
    rename_tv_files(root_directory)
