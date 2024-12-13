from vimmodules.sides.myvimmodel.appcursor import CursorCursesDefault
from vimmodules.sides.myvimetc.cursesadapt import *
import pytest

from vimmodules.sides.myvimmodel.appmodel import ModelDefault


@pytest.fixture
def cursor():
    cursor = CursorCursesDefault(CursesTextModule(), ModelDefault("testfile"))
    return cursor


def test_movement(cursor):
    cursor.move(1, 1)
    assert cursor.get_pos() == (1, 0)
    cursor.move(0, 3)
    assert cursor.get_pos() == (0, 3)
    cursor.move(55, 1)
    assert cursor.get_pos() == (0, 3)
