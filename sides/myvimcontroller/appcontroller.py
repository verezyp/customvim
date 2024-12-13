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
    _instance = None
    _command_buffer: list[CommandBase]

    def __init__(self):
        self._command_buffer = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Executor, cls).__new__(cls)
        return cls._instance

    def push_and_exec(self, command: CommandBase):
        command.exec()
        self._command_buffer.append(command)

    def undo_last(self):
        while True:
            try:
                command = self._command_buffer.pop()
                res = command.undo()
                if res is True:
                    break
            except IndexError:
                break


class AnyModeControllerBase(ABC):
    _executor_inst = Executor()

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass


class NaviModeController(AnyModeControllerBase):

    def __init__(self, model: ModelBase, cursor: CursorBase, clipboard: ClipBoardBase):
        super().__init__()
        self._model_inst = model
        self._cursor_inst = cursor
        self._clipboard = clipboard

    def handle(self, key: int, sbm: StatusBarModel):
        key = chr(key)

        match sbm.tmp_str:
            case "^" | "0":
                self._executor_inst.push_and_exec(
                    (CursorMoveToStrSideDefault("START", self._cursor_inst, self._model_inst)))
                sbm.tmp_str = ""
            case "$":
                self._executor_inst.push_and_exec(CursorMoveToStrSideDefault("END", self._cursor_inst,
                                                                             self._model_inst))
                sbm.tmp_str = ""
            case "w":
                self._executor_inst.push_and_exec(CursorMoveWordSideDefault("w", self._cursor_inst, self._model_inst))
                sbm.tmp_str = ""
            case "b":
                self._executor_inst.push_and_exec(CursorMoveWordSideDefault("b", self._cursor_inst, self._model_inst))
                sbm.tmp_str = ""
            case "gg":
                self._executor_inst.push_and_exec(CursorMoveToFileStartDefault(self._cursor_inst, self._model_inst))
                sbm.tmp_str = ""
            case "dd":
                self._executor_inst.push_and_exec(
                    CutFullDefault(self._model_inst, self._cursor_inst,
                                   self._clipboard))
                sbm.tmp_str = ""
            case "diw":
                self._executor_inst.push_and_exec(EraseDiwDefault(self._cursor_inst, self._model_inst))
                sbm.tmp_str = ""
            case "yy":
                self._executor_inst.push_and_exec(
                    CopyStrDefault(self._cursor_inst, self._model_inst, self._clipboard))
                sbm.tmp_str = ""
            case "yw":
                self._executor_inst.push_and_exec(
                    CopyWordCurPosDefault(self._cursor_inst, self._model_inst, self._clipboard))
                sbm.tmp_str = ""
            case "p":
                self._executor_inst.push_and_exec(
                    PasteCurPos(self._cursor_inst, self._model_inst, self._clipboard))
                sbm.tmp_str = ""
            case "U":
                self._executor_inst.push_and_exec(
                    CancelStrAdditional(self._model_inst, self._cursor_inst))
                sbm.tmp_str = ""
            case "x":
                self._executor_inst.push_and_exec(EraseCharDefault(self._model_inst, self._cursor_inst))
                sbm.tmp_str = ""

            case "u":
                self._executor_inst.undo_last()
                sbm.tmp_str = ""

            case _:
                if key == "G":
                    if sbm.tmp_str[: len(sbm.tmp_str) - 1].isdigit():
                        num = int(sbm.tmp_str[: len(sbm.tmp_str) - 1])
                        self._executor_inst.push_and_exec(
                            CursorMoveToNDefault(num, self._cursor_inst, self._model_inst))
                    elif sbm.tmp_str == "G":
                        self._executor_inst.push_and_exec(
                            CursorMoveToFileEndDefault(self._cursor_inst, self._model_inst))
                    sbm.tmp_str = ""
                elif sbm.tmp_str and sbm.tmp_str[0] == 'r' and len(sbm.tmp_str) == 2:
                    self._executor_inst.push_and_exec(
                        ReplaceDefault(sbm.tmp_str[1], self._cursor_inst, self._model_inst))
                    sbm.tmp_str = ""
                elif ord(key) == 338:  # PGDOWN
                    self._executor_inst.push_and_exec((ScreenDownDefault(self._model_inst, self._cursor_inst)))
                    sbm.tmp_str = ""
                elif ord(key) == 339:  # PGUP
                    self._executor_inst.push_and_exec((ScreenUpDefault(self._model_inst, self._cursor_inst)))
                    sbm.tmp_str = ""
                else:
                    allowed = ["g", "d", "di", "y", "p", "r"]
                    if not (sbm.tmp_str in allowed or sbm.tmp_str.isdigit()):
                        sbm.tmp_str = ""


class InputModeController(AnyModeControllerBase):
    def __init__(self, model: ModelBase, cursor: CursorBase):
        super().__init__()
        self._model_inst = model
        self._cursor_inst = cursor
        self._state = 0

    @staticmethod
    def validate_symbol(key):
        char = chr(key)
        allowed = "1234567890-=!@#$%^&*()_+!!\"№;%:?*()_+йцукенгшщзхъ\\/|фывапролджэяч" \
                  "смитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРО ЛДЖЭЯЧСМИТЬБЮ.qwertyuiop" \
                  "[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./<>,.?/;:'`ёЁ~/"
        return char in allowed

    def reset_state(self):
        self._state = 0

    def _pre_commands(self, s):
        match s:
            case "i":
                self._state = 1
            case "I":
                self._executor_inst.push_and_exec(CursorMoveToStrSideDefault("START", self._cursor_inst,
                                                                             self._model_inst))
                self._state = 1
            case "A":
                self._executor_inst.push_and_exec(CursorMoveToStrSideDefault("END", self._cursor_inst,
                                                                             self._model_inst))
                self._state = 1
            case "S":
                self._executor_inst.push_and_exec(MakeEmptyDefault(self._model_inst, self._cursor_inst))
                self._state = 1

    def _default_input(self, key):
        if self.validate_symbol(key):
            self._executor_inst.push_and_exec(InsertDefault(chr(key), self._model_inst, self._cursor_inst))
        elif key == 8:  # BACKSPACE
            self._executor_inst.push_and_exec(EraseCharDefault(self._model_inst, self._cursor_inst))
        elif key == 10:
            self._executor_inst.push_and_exec(InsertEnterDefault(self._model_inst, self._cursor_inst))

    def handle(self, key: int, sbm: StatusBarModel):
        if self._state:
            self._default_input(key)
            sbm.tmp_str = ""
        else:
            self._pre_commands(sbm.tmp_str)
            sbm.tmp_str = ""


class SearchModeController(AnyModeControllerBase):
    _last_search: SearchStrFromCurTo
    _last_search_rev: SearchStrFromCurTo

    def __init__(self, model: ModelBase, cursor: CursorBase):
        super().__init__()
        self._model_inst = model
        self._cursor_inst = cursor
        self._state = 0

    def handle(self, key: int, sbm: StatusBarModel):
        if key == 10:  # ENTER
            match sbm.tmp_str[0]:
                case "/":
                    com = SearchStrFromCurTo("BOT", sbm.tmp_str[1:], self._cursor_inst,
                                             self._model_inst)

                    self._last_search = com
                    self._last_search_rev = SearchStrFromCurTo("TOP", sbm.tmp_str[1:], self._cursor_inst,
                                                               self._model_inst)
                    self._executor_inst.push_and_exec(com)
                    sbm.tmp_str = ""

                case "?":
                    com = SearchStrFromCurTo("TOP", sbm.tmp_str[1:], self._cursor_inst,
                                             self._model_inst)
                    self._last_search = com

                    self._last_search_rev = SearchStrFromCurTo("BOT", sbm.tmp_str[1:], self._cursor_inst,
                                                               self._model_inst)
                    self._executor_inst.push_and_exec(com)
                    sbm.tmp_str = ""

                case "n":
                    if self._last_search:
                        self._executor_inst.push_and_exec(self._last_search)
                        sbm.tmp_str = ""
                case "N":
                    if self._last_search_rev:
                        self._executor_inst.push_and_exec(self._last_search_rev)
                        sbm.tmp_str = ""
                case _:
                    sbm.tmp_str = ""
        elif sbm.tmp_str and sbm.tmp_str[0] not in "/?nN":
            sbm.tmp_str = ""


class CommandModeController(AnyModeControllerBase):
    def __init__(self, model: ModelBase, cursor: CursorBase, view: ViewBase):
        super().__init__()
        self._model_inst = model
        self._cursor_inst = cursor
        self._view_inst = view

    def handle(self, key: int, sbm: StatusBarModel):
        if sbm.tmp_str and sbm.tmp_str[0] == ":" and key == 10:
            match sbm.tmp_str[1:]:
                case "w":
                    self._executor_inst.push_and_exec(WriteDefault(self._model_inst))
                    sbm.tmp_str = ""
                case "x":
                    self._executor_inst.push_and_exec(WriteAndExitDefault(self._model_inst))
                    sbm.tmp_str = ""
                case "q":
                    self._executor_inst.push_and_exec(ExitDefault(self._model_inst))
                    sbm.tmp_str = ""
                case "q!":
                    self._executor_inst.push_and_exec(ForceExitDefault(self._model_inst))
                    sbm.tmp_str = ""
                case "wq!":
                    self._executor_inst.push_and_exec(WriteQuitDefault(self._model_inst))
                    sbm.tmp_str = ""

                case "h":
                    self._executor_inst.push_and_exec(DisplayHelpInfoDefault(self._view_inst))
                    sbm.tmp_str = ""

                case "sy":
                    self._executor_inst.push_and_exec(DisplaySyntaxAdditional(self._view_inst))
                    sbm.tmp_str = ""
                case "e!":
                    self._executor_inst.push_and_exec(CancelAllAdditional(self._model_inst, self._cursor_inst))
                    sbm.tmp_str = ""

                case _:
                    if sbm.tmp_str and sbm.tmp_str[1]:
                        if sbm.tmp_str[1] == "o":
                            self._executor_inst.push_and_exec(
                                OpenFilenameDefault(self._model_inst, self._cursor_inst, sbm.tmp_str[3:]))
                            sbm.tmp_str = ""
                        elif sbm.tmp_str[1] == "w":
                            self._executor_inst.push_and_exec(WriteToFilenameDefault(self._model_inst, sbm.tmp_str[3:]))
                            sbm.tmp_str = ""
                        elif sbm.tmp_str[1:].isdigit():
                            self._executor_inst.push_and_exec(
                                CursorMoveToNDefault(int(sbm.tmp_str[1:]), self._cursor_inst, self._model_inst))
                            sbm.tmp_str = ""
                        elif sbm.tmp_str[1:] == "set num":
                            self._executor_inst.push_and_exec(
                                SetNumAdditional(sbm, self._cursor_inst))
                            sbm.tmp_str = ""


class ControllerDefault(ControllerBase):
    _model_inst: ModelBase
    _view_inst: ViewBase
    _cursor_inst: CursorBase
    _mode: str = "NAVI"
    _clipboard: ClipBoardBase
    _current_mode_state: AnyModeControllerBase = None
    _mode_state_list: dict[str, AnyModeControllerBase]

    def __init__(self, model: ModelBase, view: ViewBase, v2: ViewBase, cursor: CursorBase, sbm: StatusBarModel,
                 clipboard: ClipBoardBase):
        self._model_inst = model
        self._view_inst = view
        self._model_inst.mode = "NAVI"
        self._clipboard = clipboard
        self._cursor_inst = cursor
        self._sbm = sbm
        self._mode_state_list = {"NAVI": NaviModeController(model, self._cursor_inst, self._clipboard),
                                 "INPUT": InputModeController(model, self._cursor_inst),
                                 "SEARCH": SearchModeController(model, self._cursor_inst),
                                 "COMMAND": CommandModeController(model, self._cursor_inst, self._view_inst)}
        self._current_mode_state = self._mode_state_list["NAVI"]

    def cursor_movement(self, key):
        if key == KEY_UP:
            CursorMoveOneDefault("UP", self._cursor_inst).exec()
        elif key == KEY_DOWN:
            CursorMoveOneDefault("DOWN", self._cursor_inst).exec()
        elif key == KEY_LEFT:
            CursorMoveOneDefault("LEFT", self._cursor_inst).exec()
        elif key == KEY_RIGHT:
            CursorMoveOneDefault("RIGHT", self._cursor_inst).exec()
        else:
            return 0
        return 1

    def mode_handle(self, key):
        if key == 27:  # ESC
            self._mode = "NAVI"
            self._sbm.mode = self._mode
            self._tmp_str = ""
            self._mode_state_list["INPUT"].reset_state()

        elif self._mode == "NAVI" and chr(key) in "/?nN":
            self._mode = "SEARCH"
            self._sbm.mode = self._mode
            # print('///')

        elif self._mode == "NAVI" and key == ord(':'):
            self._mode = "COMMAND"
            self._sbm.mode = self._mode

        elif self._mode == "NAVI" and self._sbm.tmp_str and self._sbm.tmp_str in "iIAS":
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

    def status_str_handle(self, key):
        if self.validate_symbol(key):
            self._sbm.tmp_str += chr(key)

        if self._mode != "INPUT":
            if key == 8:
                self._sbm.tmp_str = self._sbm.tmp_str[:-1]

    def process(self) -> None:

        key = self._view_inst.text_module.getch()

        if self.cursor_movement(key):
            return None

        self.status_str_handle(key)

        self.mode_handle(key)

        if self._sbm.tmp_str == "dd":
            pass

        self._current_mode_state.handle(key, self._sbm)

        return None
