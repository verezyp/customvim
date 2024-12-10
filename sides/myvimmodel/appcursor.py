from abc import ABC, abstractmethod
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimmodel.appmodel import ModelBase


class CursorBase(ABC):

    @abstractmethod
    def move(self, y, x):
        pass

    @abstractmethod
    def get_pos(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_pos(self, y, x):
        pass


class CursorCursesDefault(CursorBase):

    def __init__(self, text_module_inst: CursesTextModule, model: ModelBase):
        self._inst = text_module_inst
        self._model = model
        self._x = 0
        self._y = 0

    def get_pos(self):
        return self._y, self._x

    def set_pos(self, y, x):
        self._y, self._x = y, x

    def move(self, y, x):
        len_buf = len(self._model.buffer)
        print(f"=== {len_buf} ===")
        if y < 0 or y > len_buf - 1:
            return None

        len_str = len(self._model.get_str(y))

        if x < 0:
            return None

        if x > len_str:
            x = len_str - 1

        self._y = y
        self._x = x
        self._inst.cursor_move(y, x)
