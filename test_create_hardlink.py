import pytest
from pathlib import Path
from unittest.mock import patch

from create_hardlink import create_hardlink, MOVIE_DIR, TV_DIR, GAME_DIR, MUSIC_DIR


@pytest.fixture
def setup_paths():
    return {
        'filename': 'example.txt',
        'source_path': Path('/source/path/example.txt'),
        'dest_path_movie': Path(f'{MOVIE_DIR}/example.txt'),
        'dest_path_tv': Path(f'{TV_DIR}/example.txt'),
        'dest_path_game': Path(f'{GAME_DIR}/example.txt'),
        'dest_path_music': Path(f'{MUSIC_DIR}/example.txt')
    }


@patch('create_hardlink.Path.exists')
@patch('create_hardlink.Path.hardlink_to')
def test_create_hardlink_success(mock_hardlink_to, mock_exists, setup_paths):
    # Mock successful hard link creation
    mock_exists.side_effect = [True, True]  # Simulate file existence checks

    result = create_hardlink(setup_paths['filename'], setup_paths['source_path'], MOVIE_DIR)

    # Assert that the hardlink was created and function returned True
    mock_hardlink_to.assert_called_once_with(setup_paths['dest_path_movie'])
    assert result is True


@patch('create_hardlink.Path.exists')
@patch('create_hardlink.Path.hardlink_to')
def test_create_hardlink_file_already_exists(mock_hardlink_to, mock_exists, setup_paths):
    # Simulate that the destination file already exists
    mock_exists.side_effect = [True, True]

    # Test the case where the file already exists
    mock_hardlink_to.side_effect = FileExistsError()

    result = create_hardlink(setup_paths['filename'], setup_paths['source_path'], MOVIE_DIR)

    # Assert that the hardlink creation raised the right error
    mock_hardlink_to.assert_called_once_with(setup_paths['dest_path_movie'])
    assert result is False


@patch('create_hardlink.Path.exists')
@patch('create_hardlink.Path.hardlink_to')
def test_create_hardlink_source_file_not_exist(mock_hardlink_to, mock_exists, setup_paths):
    # Simulate that the source file does not exist
    mock_exists.side_effect = [False]  # Source file not found

    result = create_hardlink(setup_paths['filename'], setup_paths['source_path'], MOVIE_DIR)

    # Assert that the function detected that the source file does not exist
    assert result is False


@patch('create_hardlink.Path.exists')
@patch('create_hardlink.Path.hardlink_to')
def test_create_hardlink_failure(mock_hardlink_to, mock_exists, setup_paths):
    # Simulate an unexpected exception
    mock_exists.side_effect = [True, False]  # First call True (file exists), second call False (creation failed)
    mock_hardlink_to.side_effect = Exception("Unexpected error")

    result = create_hardlink(setup_paths['filename'], setup_paths['source_path'], MOVIE_DIR)

    # Assert that an error was raised during hardlink creation
    mock_hardlink_to.assert_called_once_with(setup_paths['dest_path_movie'])
    assert result is False