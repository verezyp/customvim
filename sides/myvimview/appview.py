from abc import ABC, abstractmethod
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimmodel.appmodel import *
import os
import ctypes


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


class ViewBase(ABC):

    @abstractmethod
    def display(self):
        pass

    @property
    @abstractmethod
    def text_module(self) -> ITextModule:
        pass

    @property
    @abstractmethod
    def cursor(self) -> CursorBase:
        pass


class CursorCursesDefault(CursorBase, ObservableBaseMixin, ObserverBase):

    def __init__(self, text_module_inst: CursesTextModule, model: ModelBase):
        self._inst = text_module_inst
        self._model = model
        self._x = 0
        self._y = 0
        self._buf_link = []

    def notify(self, arg_dict):
        if arg_dict["buffer"]:
            self._buf_link = arg_dict["buffer"]

    def update(self):
        d = {'cur_y': self._y, 'cur_x': self._x}
        for obs in self._obs_list:
            obs.notify(d)

    def get_pos(self):
        return self._y, self._x

    def set_pos(self, y, x):
        self._y, self._x = y, x

    def move(self, y, x):
        len_buf = len(self._model.buffer)
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
        self.update()


from vimmodules.sides.myvimmodel.appmodel import ObserverBase


class ViewStatusBar(ViewBase, ObserverBase):  # subs to StatBarModel, CursorModel, CoreModel
    _buf = [None, "pp", 0, 0]

    def __init__(self, text_mod: ITextModule):
        self._text_module = text_mod
        self._win = curses.newwin(1, 120, 30 - 1, 0)
        self.screen_configure()

    def notify(self, arg_dict: dict):
        if 'filename' in arg_dict:
            self._buf[0] = arg_dict["filename"]
        if 'mode' in arg_dict:
            self._buf[1] = arg_dict["mode"]
        if 'cur_y' in arg_dict:
            self._buf[2] = arg_dict["cur_y"]
        if 'amount' in arg_dict:
            self._buf[3] = arg_dict["amount"]

    def screen_configure(self):
        screen = self._text_module
        # screen.noecho()  # Отключаем отображение вводимых символов
        # screen.cbreak()  # Оперативное получение символов без ожидания Enter
        # screen.keypad(True)  # Включаем обработку специальных клавиш (стрелок)
        # screen.set_cursor(1)  # Включаем отображение курсора

    def display(self):
        stdscr = self._text_module
        # stdscr.clear_scr()
        file = self._buf[0]
        mode = self._buf[1]
        cursor_y = self._buf[2]
        amount = self._buf[3]
        max_y, max_x = 30, 120

        status_bar = f"FILE: {file}. MODE: {mode}. CUR_STR: {cursor_y}. AMOUNT: {amount}"
        self._win.refresh()
        self._win.addstr(0, 0, status_bar[:max_x - 1])
        self._win.refresh()

    @property
    def text_module(self) -> ITextModule:
        pass

    @property
    def cursor(self) -> CursorBase:
        pass


class ViewDefault(ViewBase):
    _cursor_inst: CursorBase
    _text_module: ITextModule
    _model_inst: ModelBase
    _scr_top_str: int = 0
    _scr_bot_str: int = 30

    def __init__(self, model: ModelBase):
        mod = CursesTextModule()
        self._text_module = mod
        self._model_inst = model
        self._set_console_size(120, 30)
        self.screen_configure()
        self._cursor_inst = CursorCursesDefault(mod, model)

    @property
    def text_module(self):
        return self._text_module

    @property
    def cursor(self) -> CursorBase:
        return self._cursor_inst

    def screen_configure(self):
        screen = self._text_module
        screen.noecho()  # Отключаем отображение вводимых символов
        screen.cbreak()  # Оперативное получение символов без ожидания Enter
        screen.keypad(True)  # Включаем обработку специальных клавиш (стрелок)
        screen.set_cursor(1)  # Включаем отображение курсора

    def set_edges(self, top_val: int, bot_val: int):
        self._scr_top_str, self._scr_bot_str = top_val, bot_val

    @staticmethod
    def _set_console_size(width, height):
        os.system(f"mode con: cols={width} lines={height}")

        hwnd = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        rect = ctypes.create_string_buffer(22)
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hwnd, rect)

        left, top, right, bottom = 0, 0, width - 1, height - 1

        ctypes.windll.kernel32.SetConsoleWindowInfo(hwnd, True, ctypes.byref(
            (ctypes.c_short * 4)(left, top, right, bottom)
        ))

    def display(self):  # 0 - 28 string + last - status_bar (set_console_size(120, 30))

        stdscr = self._text_module
        max_y, max_x = stdscr.getmaxyx()
        win2 = curses.newwin(max_y - 1, max_x - 1, 0, 0)
        cursor_y, cursor_x = self._cursor_inst.get_pos()

        main_text = []
        buf_size = len(self._model_inst.buffer)

        if buf_size < self._scr_bot_str:
            self._scr_bot_str = buf_size - 1

        for i in range(buf_size):
            main_text.append(self._model_inst.get_str(i))

        # stdscr.clear_scr()
        win2.clear()
        max_y, max_x = stdscr.getmaxyx()

        for idx, line in enumerate(main_text):
            if idx >= max_y - 1:
                break
            win2.addstr(idx, 0, line[:max_x - 1])
            # stdscr.add_str(idx, 0, line[:max_x - 1])

        mode = self._model_inst.mode
        file = self._model_inst.filename
        amount = len(self._model_inst.buffer)

        # status_bar = f"FILE: {file}. MODE: {mode}. CUR_STR: {cursor_y}. AMOUNT: {amount}"
        # stdscr.add_str(max_y - 1, 0, status_bar[:max_x - 1])

        # self._cursor_inst.move(cursor_y, cursor_x)

        # self._cursor_inst.set_pos(cursor_y, cursor_x)
        win2.refresh()
        # stdscr.refresh_scr()