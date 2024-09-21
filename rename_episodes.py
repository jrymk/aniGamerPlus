import os
import re
import sys


def rename_files_in_directory(directory, season_offset, episode_offset):
    # Regex pattern to match filenames like `咒術迴戰 第二季[S001E25.5][sn-34152].mp4` or `.ass`
    # Allows for any number of digits in the season and episode, and episodes can have decimals
    pattern = re.compile(
        r'(.*\[S)(\d+)(E)(\d+(\.\d+)?)(\]\[sn-\d+\]\.(mp4|ass))')

    # List all files in the directory
    files = os.listdir(directory)

    # Go through each file and rename it if it matches the pattern
    for file in files:
        match = pattern.search(file)
        if match:
            prefix = match.group(1)  # '咒術迴戰 第二季[S'
            season_number = int(match.group(2))  # Season number
            episode_letter = match.group(3)  # 'E'
            # Episode number (can be a float)
            episode_number = float(match.group(4))
            suffix = match.group(6)  # '][sn-34152].mp4' or '][sn-34152].ass'

            # Calculate new season and episode numbers
            new_season_number = season_number + season_offset
            new_episode_number = episode_number + episode_offset

            # Format the new season and episode numbers
            # Keep the original length of season number
            new_season_str = f'{new_season_number:0{len(match.group(2))}d}'
            # For episode numbers, if it's an integer, display it without decimals, otherwise keep the decimal places
            if new_episode_number.is_integer():
                new_episode_str = f'{int(new_episode_number):0{
                    len(match.group(4).split(".")[0])}d}'
            else:
                new_episode_str = f'{new_episode_number:.{
                    len(match.group(4).split(".")[1])}f}'

            # Create the new filename
            new_file_name = f'{prefix}{new_season_str}{
                episode_letter}{new_episode_str}{suffix}'

            # Get the full paths for the old and new filenames
            old_file_path = os.path.join(directory, file)
            new_file_path = os.path.join(directory, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {file} -> {new_file_name}')


if __name__ == "__main__":
    # Ensure the user provides the directory, season offset, and episode offset
    if len(sys.argv) != 4:
        print("Usage: python rename_files.py <directory> <season_offset> <episode_offset>")
        sys.exit(1)

    # Parse command-line arguments
    directory = sys.argv[1]
    season_offset = int(sys.argv[2])
    # Change to float to allow for decimal episode offsets
    episode_offset = float(sys.argv[3])

    # Call the function to rename files
    rename_files_in_directory(directory, season_offset, episode_offset)
