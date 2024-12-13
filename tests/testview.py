import pytest
from vimmodules.sides.myvimmodel.appmodel import ModelDefault
from vimmodules.sides.myvimview.appview import ViewDefault
from vimmodules.sides.myvimetc.cursesadapt import CursesTextModule


@pytest.fixture
def view():
    view = ViewDefault(ModelDefault("testfile2"), CursesTextModule())
    return view


def test_display(view):
    s = view.display()
    assert len(s) == 28
