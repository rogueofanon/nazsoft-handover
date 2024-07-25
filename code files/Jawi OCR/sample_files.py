import os
import random
import shutil
import argparse

def pick_samples(source_folder, destination_folder, num_files=52):
    """
    Function that picks `num_files` of files from a source folder to a destination folder.
    """

    # List all files in source directory
    all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    all_files = [f for f in all_files if ' ' not in f]

    # Check if there are enough files to select from
    if len(all_files) < num_files:
        raise ValueError(f"Not enough files in the source folder. Found {len(all_files)}, need {num_files}.")
    
    # Randomly select the specified number of files
    selected_files = random.sample(all_files, num_files)

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy selected files to the destination folder
    for file_name in selected_files:
        src_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(destination_folder, file_name)
        shutil.copy(src_path, dest_path)
        print(f"Copied {file_name} to {destination_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomly pick files from a source folder and copy them to a destination folder.")
    parser.add_argument("-s", "--source", type=str, required=True, help="Path to the source folder")
    parser.add_argument("-d", "--destination", type=str, required=True, help="Path to the destination folder")
    parser.add_argument("-n", "--num-files", type=int, default=52, help="Number of files to extract")

    args = parser.parse_args()

    pick_samples(args.source, args.destination, args.num_files)