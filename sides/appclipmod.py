from abc import ABC, abstractmethod
import pyperclip


class ClipBoardBase(ABC):

    @abstractmethod
    def copy(self, in_str: str) -> None:
        pass

    @abstractmethod
    def paste(self) -> str:
        pass


class ClipBoardPyperClip(ClipBoardBase):

    def copy(self, in_str: str) -> None:
        pyperclip.copy(in_str)

    def paste(self) -> str:
        return pyperclip.paste()
