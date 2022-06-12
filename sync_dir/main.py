from os import walk, makedirs
from os.path import isfile, isdir, exists, join, dirname
from hashlib import md5
from time import sleep
from argparse import ArgumentParser
from shutil import copy

def list_dir(folder) -> list:
    return walk(folder)

def read_md5(file: bytes) -> md5:
    return md5(file).hexdigest()

def read_file_dir(file):
    with open(file, 'rb') as f:
        return read_md5(f.read())
    
def copy_file(one: str, two: str) -> bool:
    try:
        create_directory(two)
        copy(one, dirname(two))
        return True
    except Exception as e:
        print(f'Error in copy: {e}')
    return False
    
def compare_two_files_exists_and_md5(one: str, two: str) -> bool:
    if exists(two):
        if read_file_dir(two) == read_file_dir(one):
            return True
        return False
    return False

def create_directory(directory) -> bool:
    try: 
        if not exists(dirname(directory)):
            makedirs(dirname(directory))
            print(f'creating directory: {dirname(directory)}')
        return True
    except Exception as e:
        print(f'error in create directory {e}')
        return False
    return False
    
def change_dirs_files(dir1: str, dir2: str) -> None:
    for directory in list_dir(dir1):
        for file in directory[2]:
            if file:
                dir_file = join(directory[0], file)
                compare = compare_two_files_exists_and_md5(dir_file, join(
                    dir2, dir_file).replace(dir1, dir2))
                if not compare:
                    copy_file(dir_file, join(
                    dir2, dir_file).replace(dir1, dir2))
                    print(f'copy {dir_file} -> {join(dir2, dir_file).replace(dir1, dir2)}')

def call() -> ArgumentParser.parse_args:
    parser = ArgumentParser(description='Sync two directores')
    parser.add_argument('-folder_one', type=str, help='folder directory one')
    parser.add_argument('-folder_two', type=str, help='folder directory two')
    args = parser.parse_args()
    return args

def main():
    args = call()
    print(f'SYNC {args.folder_one} -> {args.folder_two}')
    while True:
        change_dirs_files(args.folder_one, args.folder_two)
        print('sleep work')
        sleep(10)
    

main()
