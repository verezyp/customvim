import pytest
from unittest.mock import MagicMock, patch
from vimmodules.sides.myvimcontroller.appcontroller import *
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimmodel.appcursor import CursorCursesDefault
from vimmodules.sides.myvimetc.cursesadapt import *
import pytest

from vimmodules.sides.myvimmodel.appmodel import ModelDefault
from vimmodules.sides.myvimcontroller.appcommands import *


class MockAdapter(ITextModule):

    def __init__(self):
        self._str = ""

    def input_to(self, val: chr):
        self._str = val

    def clear_scr(self):
        pass

    def add_str(self, row: int, col: int, in_str: str):
        pass

    def refresh_scr(self):
        pass

    def cursor_move(self, y_pos: int, x_pos: int):
        pass

    def getch(self):
        return ord(self._str)

    def set_cursor(self, val):
        pass

    def wrapper(self, func):
        pass

    def end_win(self):
        pass

    def cbreak(self):
        pass

    def keypad(self, val):
        pass

    def noecho(self):
        pass

    def getmaxyx(self):
        pass

    def start_config(self):
        pass

    def newwin(self, nlines, ncols, beg_y, beg_x):
        pass

    def win_clear(self, win):
        pass

    def win_refresh(self, win):
        pass

    def start_color(self):
        pass

    def init_pair(self, num, color1, color2):
        pass

    def win_addstr(self, y, x, s, win, color=None):
        pass


@pytest.fixture
def mas():
    f_name = "testfile3"
    model = ModelDefault(f_name)

    text_module = MockAdapter()

    view = ViewDefault(model, text_module)

    view_status_bar = ViewStatusBar(text_module)

    clipboard = ClipBoardPyperClip()

    stat_bar_model = StatusBarModel(f_name)

    cursor = CursorCursesDefault(text_module, model)

    deco = ViewDecoratorDefault(view)

    stat_bar_model.registry(view_status_bar)
    stat_bar_model.registry(cursor)
    cursor.registry(view_status_bar)
    cursor.registry(view)
    model.registry(view_status_bar)

    ctrl = ControllerDefault(model, deco, view_status_bar, cursor, stat_bar_model, clipboard)
    return ctrl, cursor, model, text_module


def test_w(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]

    mock.input_to('w')
    ctrl.process()
    assert cursor.get_pos() == (0, 7)


def test_move(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]
    cursor.move(3, 3)
    mock.input_to('g')
    ctrl.process()
    mock.input_to('g')
    ctrl.process()
    assert cursor.get_pos() == (0, 0)


def test_change_mode(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]
    mock.input_to("i")
    ctrl.process()
    assert ctrl._mode == "INPUT"


def test_esc(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]
    mock.input_to("i")
    ctrl.process()
    assert ctrl._mode == "INPUT"

    ctrl.process()
    mock.input_to(chr(27))
    ctrl.process()
    assert ctrl._mode == "NAVI"


def test_input(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]

    mock.input_to("i")
    ctrl.process()

    mock.input_to("2")
    ctrl.process()

    mock.input_to("2")
    ctrl.process()

    mock.input_to("2")
    ctrl.process()
    assert model.get_str(0) == "222qwerty wertyui rtyuiop\n"


def test_cursor_arr(mas):
    ctrl = mas[0]
    cursor = mas[1]
    model = mas[2]
    mock = mas[3]
    mock.input_to(chr(258))
    ctrl.process()
    assert cursor.get_pos() == (1, 0)
    mock.input_to(chr(259))
    ctrl.process()
    assert cursor.get_pos() == (0, 0)
    mock.input_to(chr(261))
    ctrl.process()
    assert cursor.get_pos() == (0, 1)
    mock.input_to(chr(260))
    ctrl.process()
    assert cursor.get_pos() == (0, 0)
