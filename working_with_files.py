import hashlib
from os import listdir, walk, remove
from os.path import isdir, getsize, join
from pathlib import Path
from typing import Iterator, List, Dict


def get_all_files_in_dir(repo: Path, extension: str = None) -> Iterator[Path]:
    if not repo.exists():
        raise Exception("directory not found")

    files = _get_list_of_files(repo)

    if extension:
        files = filter(lambda filename: str(filename).endswith(extension), files)

    return files


def _get_list_of_files(dir_name: Path) -> List[Path]:
    list_of_file = listdir(dir_name)
    all_files = []

    for entry in list_of_file:
        full_path = dir_name / entry

        if isdir(full_path):
            all_files += _get_list_of_files(full_path)
        else:
            all_files.append(full_path)

    return all_files


def file_read(file_path: Path):
    with open(file_path, mode='r', encoding="utf-8-sig") as fp:
        return fp.read()


def file_write(data, filename: str or Path, file_path: Path = None) -> None:
    if file_path:
        filename = file_path / filename

    with open(filename, mode='w', encoding="utf-8") as fp:
        fp.write(data)


def all_files_in_directory_generator(directory: str, full_path: bool = False) -> Iterator[str]:
    if not isdir(directory):
        raise Exception("directory not found: ", directory)

    for (dir_path, _, file_names) in walk(directory):
        for file in file_names:
            local_file = join(dir_path, file) if full_path else file
            yield local_file

        break


def chunk_reader(file_object, chunk_size: int = 1024) -> Iterator:
    while True:
        chunk = file_object.read(chunk_size)

        if not chunk:
            return

        yield chunk


def check_for_duplicates_and_remove_if_exist(from_path: str, _hash=hashlib.sha1) -> None:
    hashes = {}

    for file_path in all_files_in_directory_generator(from_path, full_path=True):
        hash_obj = _hash()

        for chunk in chunk_reader(open(file_path, 'rb')):
            hash_obj.update(chunk)

        file_id = (hash_obj.digest(), getsize(file_path))
        duplicate = hashes.get(file_id, None)

        if duplicate:
            remove(file_path)
        else:
            hashes[file_id] = file_path
