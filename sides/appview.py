from abc import ABC, abstractmethod
from cursesadapt import *
from appmodel import *
import os
import ctypes


class ViewBase(ABC):

    @abstractmethod
    def display(self):
        pass


class CursorBase(ABC):

    @abstractmethod
    def move(self, y, x):
        pass

    @abstractmethod
    def get_pos(self) -> tuple[int, int]:
        pass


class CursorCursesDefault(CursorBase):

    def __init__(self, text_module_inst: CursesTextModule, model: ModelBase):
        self._inst = text_module_inst
        self._model = model
        self._x = 0
        self._y = 0

    def get_pos(self):
        return self._y, self._x

    def move(self, y, x):
        if y < 0 or y > len(self._model.buffer) - 1 or x > len(self._model.get_str(y)) or x < 0:
            return
        self._y = y
        self._x = x
        self._inst.cursor_move(y, x)


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
        self.set_console_size(120, 30)
        self._cursor_inst = CursorCursesDefault(mod, model)
        self.screen_configure()

    def screen_configure(self):
        screen = self._text_module
        screen.noecho()  # Отключаем отображение вводимых символов
        screen.cbreak()  # Оперативное получение символов без ожидания Enter
        screen.keypad(True)  # Включаем обработку специальных клавиш (стрелок)
        screen.set_cursor(1)  # Включаем отображение курсора

    def set_edges(self, top_val: int, bot_val: int):
        self._scr_top_str, self._scr_bot_str = top_val, bot_val

    @staticmethod
    def set_console_size(width, height):
        # Установить размер буфера
        os.system(f"mode con: cols={width} lines={height}")

        # Получить дескриптор консоли
        hwnd = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        # Задать размер окна консоли
        rect = ctypes.create_string_buffer(22)  # Для хранения координат окна
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hwnd, rect)

        # Получение размеров консоли (строки как байты)
        left, top, right, bottom = 0, 0, width - 1, height - 1

        # Применяем размеры окна
        ctypes.windll.kernel32.SetConsoleWindowInfo(hwnd, True, ctypes.byref(
            (ctypes.c_short * 4)(left, top, right, bottom)
        ))

    def display(self):  # 0 - 28 string +  last - status_bar (set_console_size(120, 30))

        stdscr = self._text_module

        while True:
            cursor_y, cursor_x = self._cursor_inst.get_pos()
            text_array = []
            buf_size = len(self._model_inst.buffer)

            if buf_size < self._scr_bot_str:
                self._scr_bot_str = buf_size - 1

            for i in range(buf_size):
                text_array.append(self._model_inst.get_str(i))

            stdscr.clear_scr()

            max_y, max_x = stdscr.getmaxyx()

            for idx, line in enumerate(text_array):
                if idx >= max_y - 1:
                    break
                stdscr.add_str(idx, 0, line[:max_x - 1])

            status_bar = "'q' для выхода. FILE = {?}. MODE = <?>. POS = {?, ?}"
            stdscr.add_str(max_y - 1, 0, status_bar[:max_x - 1])

            self._cursor_inst.move(cursor_y, cursor_x)

            stdscr.refresh_scr()

            # key = stdscr.getch()
            #
            # if key == ord('q'):
            #     break
            #
            # if key == curses.KEY_UP and cursor_y > 0:
            #     cursor_y -= 1
            # elif key == curses.KEY_DOWN and cursor_y < max_y - 2:
            #     cursor_y += 1
            # elif key == curses.KEY_LEFT and cursor_x > 0:
            #     cursor_x -= 1
            # elif key == curses.KEY_RIGHT and cursor_x < max_x - 2:
            #     cursor_x += 1

#
# if __name__ == '__main__':
#     m = ModelDefault("file3")
#     v = ViewDefault(m)
#     v.display()
