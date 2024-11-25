import argparse
from abc import ABC, abstractmethod


class ArgsParserBase(ABC):
    @abstractmethod
    def get_filename(self) -> str:
        pass


class ArgsParserDefault(ArgsParserBase):
    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def get_filename(self) -> str:
        self._parser.add_argument(
            "file",
            nargs="?",
            default=None,
            help="File (optional)"
        )

        args = self._parser.parse_args()

        return args.file
