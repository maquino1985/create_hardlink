import logging
from pathlib import Path
import sys

MOVIE_DIR = '/share/data/movies'
TV_DIR = '/share/data/tv'
GAME_DIR = '/share/data/games'
MUSIC_DIR = '/share/data/music'

ALLOWED_CATEGORIES = ['game', 'movie', 'tv', 'music']

def create_hardlink(filename: str, save_path: Path, dest_dir: str) -> bool:
    dest_path = Path(dest_dir) / filename
    try:
        # Create hard link
        save_path.hardlink_to(dest_path)

        if dest_path.exists():
            logging.info(f'Link created successfully to {dest_path.absolute()}!')
            return True
        else:
            logging.error(f'Link creation failed!')
            return False
    except FileExistsError:
        logging.error(f'File already exists at {dest_path.absolute()}!')
        return False
    except Exception as e:
        logging.error(f'Error creating hard link: {e}')
        return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info(f'Args: {sys.argv}')
    if len(sys.argv) != 4:
        logging.error('Bad args! Usage: script.py <filename> <category> <save_path>')
        exit(1)

    name = sys.argv[1]
    category = sys.argv[2]
    save_path_str = sys.argv[3]

    if category not in ALLOWED_CATEGORIES:
        logging.error(f'Category is not supported: {category}')
        exit(2)

    save_path = Path(save_path_str)

    if not save_path.exists():
        logging.error(f'Source file not found: {save_path.absolute()}')
        exit(3)

    if category == 'movie':
        create_hardlink(name, save_path, MOVIE_DIR)
    elif category == 'tv':
        create_hardlink(name, save_path, TV_DIR)
    elif category == 'game':
        create_hardlink(name, save_path, GAME_DIR)
    elif category == 'music':
        create_hardlink(name, save_path, MUSIC_DIR)