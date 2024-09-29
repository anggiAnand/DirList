#!/usr/bin/python
import os
import random
import shutil
import argparse
import logging
from datetime import datetime

__author__ = "Anggi Ananda"
__version__ = "1.0.1"
now = datetime.now()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


# Set an Argument Parser
parser = argparse.ArgumentParser(
    prog="Directory Sorting",
    description="Simple and Neat PyTube CLI Tools",
    epilog=f"{now.strftime('%Y/%m/%d, %H:%M:%S')}",
)
parser.add_argument("directory", help="Directory To Be Sorted", type=dir_path)
parser.add_argument(
    "--include-hidden",
    help="Include Hidden Files",
    action="store_false",
    required=False,
    dest="include_hidden",
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s {__author__}:{__version__}"
)

# Set a Logger
FORMAT = "%(asctime)s::%(name)s:%(levelname)s:: %(message)s"
logger = logging.getLogger("DirList")
logging.basicConfig(filename="DirList.log", level=logging.INFO, format=FORMAT)

random_number = random.randint(1, 10**10)


class DirList:
    def __init__(self, dir=os.getcwd(), ignore_hidden=True):
        if dir.lower() == "." or "." in dir.lower():
            temp_dir = os.getcwd()
        else:
            temp_dir = dir
        if temp_dir == os.path.expanduser("~") and not ignore_hidden:
            print(
                "To prevent ruining system, we forbid to sort home directory without ignore hidden"
            )
            exit()
        else:
            self.dir = dir
        self.ignore_hidden = ignore_hidden

    def __repr__(self):
        return f"Directory : {os.path.expanduser(self.dir)}"

    def sort(self):
        for folder in self._extensions.keys():
            if os.path.exists(folder) and os.path.isdir(folder):
                pass
            else:
                os.mkdir(folder)
        # TODO : OPTIMIZE THIS CODE, I CANT COME UP WITH SOLUTION HOW TO FIX DUPLICATE FILES.
        for file in self._directory_files:
            matched = False
            ext = os.path.splitext(file)[1][1:]
            for folder, extension in self._extensions.items():
                if ext in extension and os.path.splitext(file)[0] != "dirlist":
                    try:
                        shutil.move(
                            os.path.join(self.dir, file),
                            os.path.join(os.getcwd(), folder),
                        )
                    except Exception:
                        new_name = f"{os.path.splitext(file)[0]}_{random_number}.{ext}"
                        shutil.move(
                            os.path.join(self.dir, file),
                            os.path.join(os.getcwd(), folder, new_name),
                        )
                    logger.info(f"Successfully Moved {file} to {folder} Folder")
                    matched = True
            if not matched and os.path.splitext(file)[0] != "dirlist":
                try:
                    shutil.move(
                        os.path.join(self.dir, file), os.path.join(os.getcwd(), "Other")
                    )
                except Exception:
                    new_name = f"{os.path.splitext(file)[0]}_{random_number}.{ext}"
                    shutil.move(
                        os.path.join(self.dir, file),
                        os.path.join(os.getcwd(), "Other", new_name),
                    )
                logger.info(f"Successfully Moved {file} to {folder} Folder")

    @property
    def _get_current_working_directory_files(self):
        for files in os.listdir(os.getcwd()):
            if self.ignore_hidden and files.startswith("."):
                continue
            if os.path.isfile(os.path.join(os.getcwd(), files)):
                yield files

    @property
    def _directory_files(self):
        for files in os.listdir(self.dir):
            if self.ignore_hidden and files.startswith("."):
                continue
            if os.path.isfile(os.path.join(self.dir, files)):
                yield files

    @property
    def _extensions(self):
        # TODO : ADD MORE EXTENSION!!!
        extensions = {
            "Documents": [
                "doc",
                "docx",
                "txt",
                "pdf",
                "ppt",
                "pptx",
                "csv",
                "xlsx",
                "xlsm",
                "md",
            ],
            "Video": ["mkv", "mp4", "webm", "mov", "avi", "m4v"],
            "Audio": ["mp3", "wav", "flac"],
            "Images": ["psd", "jpg", "png", "tiff", "bmp"],
            "Zip Files": ["zip", "rar", "7z", "iso", "jar", "deb"],
            "Code": [
                "html",
                "css",
                "py",
                "js",
                "php",
                "rb",
                "xml",
                "json",
                "pyw",
                "c",
                "sh",
                "bat",
                "cs",
                "java",
                "pyc",
                "class",
                "rs",
            ],
            "Other": [],
        }
        return extensions


# TODO : Optimize Main Func
def main():
    arguments = parser.parse_args()
    dir_sort = DirList(dir=arguments.directory, ignore_hidden=arguments.include_hidden)

    print(dir_sort)
    dir_sort.sort()
    print("Sort Completed! Check 'DirList.log' For Logs")


if __name__ == "__main__":
    main()
