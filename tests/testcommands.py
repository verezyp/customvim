from vimmodules.sides.myvimmodel.appcursor import CursorCursesDefault
from vimmodules.sides.myvimetc.cursesadapt import *
import pytest

from vimmodules.sides.myvimmodel.appmodel import ModelDefault
from vimmodules.sides.myvimcontroller.appcommands import *


@pytest.fixture
def mods():
    mod = CursesTextModule()
    model = ModelDefault("testfile3")
    cursor = CursorCursesDefault(mod, model)
    return cursor, model


def test_commands_diw(mods):
    cursor = mods[0]
    model = mods[1]
    cursor.move(0, 11)
    com = EraseDiwDefault(cursor, model)
    com.exec()
    assert model.get_str(0) == "qwerty rtyuiop\n"


def test_command_move(mods):
    cursor = mods[0]
    model = mods[1]
    CursorMoveToFileStartDefault(cursor, model).exec()
    assert cursor.get_pos() == (0, 0)
    CursorMoveToFileEndDefault(cursor, model).exec()
    assert cursor.get_pos() == (4, 2)
    CursorMoveToNDefault(2, cursor, model).exec()
    assert cursor.get_pos() == (2, 0)
    CursorMoveToNDefault(122, cursor, model).exec()
    assert cursor.get_pos() == (2, 0)


def test_command_edit(mods):
    cursor = mods[0]
    model = mods[1]
    InsertDefault("P", model, cursor).exec()
    assert model.get_str(0) == "Pqwerty wertyui rtyuiop\n"
    assert cursor.get_pos() == (0, 1)

    ReplaceDefault("9", cursor, model).exec()
    assert model.get_str(0) == "P9werty wertyui rtyuiop\n"
    assert cursor.get_pos() == (0, 1)
