import os
import re
import argparse

# Function to update the .ass file with the extracted sn tag


def update_ass_file(file_path):
    # Read the original .ass file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract the sn-xxxxx tag from the file name
    match = re.search(r'\[sn-(\d+)\]', file_path)
    if match:
        sn_tag = match.group(1)
    else:
        print(f"No [sn-xxxxx] tag found in {file_path}")
        return

    # Update the .ass file content
    updated_lines = []
    for line in lines:
        if line.startswith("Title:"):
            updated_lines.append(line)
            updated_lines.append(f"Update Details: anigamer-{sn_tag}\n")
        else:
            updated_lines.append(line)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

# Function to rename files


def rename_files(base_name, sn_tag, file_dir):
    ass_file = os.path.join(file_dir, f"{base_name}[sn-{sn_tag}].ass")
    mp4_file = os.path.join(file_dir, f"{base_name}[sn-{sn_tag}].mp4")
    new_ass_file = os.path.join(file_dir, f"{base_name}.ass")
    new_mp4_file = os.path.join(file_dir, f"{base_name}.mp4")

    # Rename the .ass file
    if os.path.exists(ass_file):
        os.rename(ass_file, new_ass_file)
        print(f"Renamed {ass_file} to {new_ass_file}")

    # Rename the .mp4 file if it exists
    if os.path.exists(mp4_file):
        os.rename(mp4_file, new_mp4_file)
        print(f"Renamed {mp4_file} to {new_mp4_file}")

# Function to process a single .ass file


def process_ass_file(file_path):
    # Extract base file name (without sn tag)
    file_dir, file_name = os.path.split(file_path)
    base_name_match = re.match(r"(.*)\[sn-(\d+)\]\.ass", file_name)

    if base_name_match:
        base_name = base_name_match.group(1)
        sn_tag = base_name_match.group(2)

        # Update the .ass file content
        update_ass_file(file_path)

        # Rename the .ass and corresponding .mp4 files
        rename_files(base_name, sn_tag, file_dir)
    else:
        print(f"Invalid file name format: {file_path}")

# Function to scan all .ass files in a directory and its subdirectories


def scan_and_process_ass_files(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".ass"):
                file_path = os.path.join(root, file)
                process_ass_file(file_path)

# Main function to parse command-line arguments and run the script


def main():
    parser = argparse.ArgumentParser(
        description="Process .ass files and update sn tags.")
    parser.add_argument("folder_path", type=str,
                        help="Path to the folder containing .ass files.")
    args = parser.parse_args()

    # Scan and process all .ass files in the provided folder path
    scan_and_process_ass_files(args.folder_path)


if __name__ == "__main__":
    main()
