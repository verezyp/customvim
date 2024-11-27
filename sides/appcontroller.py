from abc import ABC, abstractmethod

import cursesadapt
from appmodel import *
from appview import *
from appcommands import *
from cursesadapt import *
from appclipmod import *


class ControllerBase(ABC):
    pass


class ControllerDefault(ControllerBase):
    _model_inst: ModelBase
    _view_inst: ViewBase
    _cursor_inst: CursorBase
    _mode: str = "NAVI"
    _to_exec: list[CommandBase]
    _clipboard: ClipBoardBase

    def __init__(self, model: ModelBase, view: ViewBase):
        self._model_inst = model
        self._view_inst = view
        self._model_inst.mode = "NAVI"
        self._to_exec = []
        self._clipboard = ClipBoardPyperClip()

    def navi_handle(self, key):
        # print(chr(key))
        match chr(key):

            #  -- - -- INPUT  -- - --

            case "i":
                self._mode = "INPUT"
            case "I":
                self._mode = "INPUT"
                self._to_exec.append(CursorMoveToStrSideDefault("START", self._view_inst.cursor, self._model_inst))
            case "A":
                self._mode = "INPUT"
                self._to_exec.append(CursorMoveToStrSideDefault("END", self._view_inst.cursor, self._model_inst))
            case "S":
                self._mode = "INPUT"
                self._to_exec.append(MakeEmptyDefault(self._model_inst, self._view_inst.cursor))
            case "r":
                key = self._view_inst.text_module.getch()
                if self.validate_symbol(key):
                    self._to_exec.append(ReplaceDefault(chr(key), self._view_inst.cursor, self._model_inst))

            # -- - -- NAVIGATION -- - --

            case "^" | "0":
                self._to_exec.append(CursorMoveToStrSideDefault("START", self._view_inst.cursor, self._model_inst))
            case "$":
                self._to_exec.append(CursorMoveToStrSideDefault("END", self._view_inst.cursor, self._model_inst))
            case "w":
                self._to_exec.append(CursorMoveWordSideDefault("w", self._view_inst.cursor, self._model_inst))
            case "b":
                self._to_exec.append(CursorMoveWordSideDefault("b", self._view_inst.cursor, self._model_inst))
            case "g":
                key = self._view_inst.text_module.getch()
                if self.validate_symbol(key) and chr(key) == "g":
                    self._to_exec.append(CursorMoveToFileStartDefault(self._view_inst.cursor, self._model_inst))
            case "G":
                self._to_exec.append(CursorMoveToFileEndDefault(self._view_inst.cursor, self._model_inst))
            case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                number_str = chr(key)
                while True:
                    new_key = chr(self._view_inst.text_module.getch())
                    if new_key in "0123456789":
                        number_str = number_str + new_key
                    elif new_key == "G":
                        num = int(number_str)
                        self._to_exec.append(CursorMoveToNDefault(num, self._view_inst.cursor, self._model_inst))
                        break
                    else:
                        break
            case "d":
                new_key = chr(self._view_inst.text_module.getch())
                if new_key == "d":
                    self._to_exec.append(
                        CutFullDefault(self._model_inst, self._view_inst.cursor,
                                       self._clipboard))
                elif new_key == "i":
                    new_key2 = chr(self._view_inst.text_module.getch())
                    if new_key2 == "w":
                        self._to_exec.append(EraseDiwDefault(self._view_inst.cursor, self._model_inst))

            case "y":
                new_key = chr(self._view_inst.text_module.getch())
                if new_key == "y":
                    self._to_exec.append(
                        CopyStrDefault(self._view_inst.cursor, self._model_inst, self._clipboard))
                elif new_key == "w":
                    self._to_exec.append(
                        CopyWordCurPosDefault(self._view_inst.cursor, self._model_inst, self._clipboard))

            case "p":
                self._to_exec.append(PasteCurPos(self._view_inst.cursor, self._model_inst, self._clipboard))

    def cursor_movement(self, key):
        if key == cursesadapt.KEY_UP:
            CursorMoveOneDefault("UP", self._view_inst.cursor).exec()
        elif key == cursesadapt.KEY_DOWN:
            CursorMoveOneDefault("DOWN", self._view_inst.cursor).exec()
        elif key == cursesadapt.KEY_LEFT:
            CursorMoveOneDefault("LEFT", self._view_inst.cursor).exec()
        elif key == cursesadapt.KEY_RIGHT:
            CursorMoveOneDefault("RIGHT", self._view_inst.cursor).exec()
        else:
            return 0
        return 1

    def mode_handle(self, key):
        if key == 27:  # ESC
            self._mode = "NAVI"
            return None

    @staticmethod
    def validate_symbol(key):
        char = chr(key)
        allowed = "1234567890-=!@#$%^&*()_+!!\"№;%:?*()_+йцукенгшщзхъ\\/|фывапролджэяч" \
                  "смитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРО ЛДЖЭЯЧСМИТЬБЮ.qwertyuiop" \
                  "[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./<>,.?/;:'`ёЁ~/"
        return char in allowed

    def execute(self):
        if self._to_exec:
            self._to_exec.pop().exec()

    def process(self):

        key = self._view_inst.text_module.getch()
        # print(key)
        if self.cursor_movement(key):
            return None

        self.mode_handle(key)

        match self._mode:
            case "NAVI":
                self.navi_handle(key)
            case "INPUT":
                if self.validate_symbol(key):
                    self._to_exec.append(InsertDefault(chr(key), self._model_inst, self._view_inst.cursor))
                elif key == 8:  # BACKSPACE
                    self._to_exec.append(EraseCharDefault(self._model_inst, self._view_inst.cursor))
        self._model_inst.mode = self._mode

        self.execute()


if __name__ == '__main__':
    m = ModelDefault("file3")
    v = ViewDefault(m)
    c = ControllerDefault(m, v)

    while True:
        v.display()
        c.process()
