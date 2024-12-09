from vimmodules.sides.myvimview.appview import *
from vimmodules.sides.myvimcontroller.appcommands import *
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimmodel.appclipmod import *
from enum import Enum


class MODE(Enum):
    NAVIGATION = "NAVI"
    INPUT = "INPUT"
    SEARCH = "SEARCH"
    COMMAND = "COMMAND"


class ControllerBase(ABC):
    pass


class Executor:
    _command_buffer: list[CommandBase]
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Executor, cls).__new__(cls)
        return cls._instance

    def push_and_exec(self, command: CommandBase):
        command.exec()
        self._command_buffer.append(command)

    def undo_last(self):
        pass

    def undo_string_spec(self, num: int):
        pass

    def undo_all(self):
        pass

    def tmp(self):
        print(id(self))


class AnyModeControllerBase(ABC):
    _executor_inst = Executor()

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass


class NaviModeController(AnyModeControllerBase):

    def __init__(self):
        super().__init__()
        self._tmp_str = ""

    def handle(self, key: int):
        self._executor_inst.tmp()
        key = chr(key)


class InputModeController(AnyModeControllerBase):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        self._executor_inst.tmp()


class SearchModeController(AnyModeControllerBase):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        self._executor_inst.tmp()


class CommandModeController(AnyModeControllerBase):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        self._executor_inst.tmp()


class ControllerDefault(ControllerBase):
    _model_inst: ModelBase
    _view_inst: ViewBase
    _cursor_inst: CursorBase
    _mode: str = "NAVI"
    _to_exec: list[CommandBase]
    _clipboard: ClipBoardBase
    _last_search: CommandBase
    _current_mode_state: AnyModeControllerBase = None
    _mode_state_list: dict[str, AnyModeControllerBase]

    def __init__(self, model: ModelBase, view: ViewBase, v2: ViewBase):
        self._model_inst = model
        self._view_inst = view
        self._model_inst.mode = "NAVI"
        self._to_exec = []
        self._clipboard = ClipBoardPyperClip()
        self._cursor_inst = self._view_inst.cursor
        self._sbm = StatusBarModel(model.filename)
        self._sbm.registry(v2)
        self._cursor_inst.registry(v2)
        self._model_inst.registry(v2)
        self._mode_state_list = {"NAVI": NaviModeController(), "INPUT": InputModeController(),
                                 "SEARCH": SearchModeController(), "COMMAND": CommandModeController()}
        self._current_mode_state = self._mode_state_list["NAVI"]

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
            case "n":
                self._to_exec.append(self._last_search)
            case "N":
                dir = ""
                if self._last_search.direction == "TOP":
                    dir = "BOT"
                elif self._last_search.direction == "BOT":
                    dir = "TOP"
                self._to_exec.append(
                    SearchStrFromCurTo(dir, self._last_search.text, self._view_inst.cursor,
                                       self._model_inst))
                self._last_search = self._to_exec[-1]

    def search_handle(self, key):

        if not self.validate_symbol(key):
            return None

        text = ""

        direction = ""
        if chr(key) == "/":
            direction = "BOT"
        elif chr(key) == "?":
            direction = "TOP"

        while True:
            new_key = (self._view_inst.text_module.getch())
            # print(new_key)
            if new_key == 10:
                self._to_exec.append(
                    SearchStrFromCurTo(direction, text, self._view_inst.cursor, self._model_inst))
                self._last_search = self._to_exec[-1]
                break

            elif self.validate_symbol(new_key):
                text += chr(new_key)

            else:
                break

    def cursor_movement(self, key):
        if key == KEY_UP:
            CursorMoveOneDefault("UP", self._view_inst.cursor).exec()
        elif key == KEY_DOWN:
            CursorMoveOneDefault("DOWN", self._view_inst.cursor).exec()
        elif key == KEY_LEFT:
            CursorMoveOneDefault("LEFT", self._view_inst.cursor).exec()
        elif key == KEY_RIGHT:
            CursorMoveOneDefault("RIGHT", self._view_inst.cursor).exec()
        else:
            return 0
        return 1

    def mode_handle(self, key):
        if key == 27:  # ESC
            self._mode = "NAVI"
            self._sbm.mode = self._mode

        elif self._mode == "NAVI" and (key == ord('/') or key == ord('?')):
            self._mode = "SEARCH"
            self._sbm.mode = self._mode
            # print('///')

        elif self._mode == "NAVI" and key == ord(':'):
            self._mode = "COMMAND"
            self._sbm.mode = self._mode

        elif self._mode == "NAVI" and chr(key) in "iIASr":
            self._mode = "INPUT"
            self._sbm.mode = self._mode
        else:
            return False
        self._current_mode_state = self._mode_state_list[self._mode]
        return True

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
        if key == ord('4'):
            self._sbm.mode = "TEST"
            return

        if self.cursor_movement(key):
            return None

        self.mode_handle(key)
        # self._model_inst.mode = self._mode
        self._current_mode_state.handle(key)
        # self._view_inst.display()  # ?????

        match self._mode:
            case "NAVI":
                self.navi_handle(key)
            case "SEARCH":
                self.search_handle(key)
            case "INPUT":
                if self.validate_symbol(key):
                    self._to_exec.append(InsertDefault(chr(key), self._model_inst, self._view_inst.cursor))
                elif key == 8:  # BACKSPACE
                    self._to_exec.append(EraseCharDefault(self._model_inst, self._view_inst.cursor))
        self._model_inst.mode = self._mode
        self.execute()
