import pytest
from vimmodules.sides.myvimmodel.appmodel import ModelDefault


@pytest.fixture
def model():
    return ModelDefault("testfile")


def test_get_str(model):
    assert model.get_str(0) == "12345\n"
    assert model.get_str(1) == "\n"
    assert model.get_str(2) == "33\n"
    assert model.get_str(3) == "44\n"
    assert model.get_str(4) == "55"


def test_insert(model):
    model.str_sub_sys.insert_str(0, 0, "Q")
    assert model.get_str(0) == "Q12345\n"

    model.str_sub_sys.insert_str(0, 3, "X")
    assert model.get_str(0) == "Q12X345\n"

    model.str_sub_sys.insert_str(0, 7, "Z")
    assert model.get_str(0) == "Q12X345Z\n"

    model.str_sub_sys.insert_str(2, 0, "A")
    assert model.get_str(2) == "A33\n"

    model.str_sub_sys.insert_str(2, 1, "B")
    assert model.get_str(2) == "AB33\n"

    model.str_sub_sys.insert_str(2, 4, "C")
    assert model.get_str(2) == "AB33C\n"

    model.str_sub_sys.insert_str(3, 0, "D")
    assert model.get_str(3) == "D44\n"

    model.str_sub_sys.insert_str(3, 1, "E")
    assert model.get_str(3) == "DE44\n"

    model.str_sub_sys.insert_str(3, 4, "F")
    assert model.get_str(3) == "DE44F\n"

    model.str_sub_sys.insert_str(4, 0, "G")
    assert model.get_str(4) == "G55"

    model.str_sub_sys.insert_str(4, 1, "H")
    assert model.get_str(4) == "GH55"

    model.str_sub_sys.insert_str(4, 3, "I")
    assert model.get_str(4) == "GH5I5"


def test_erase_full(model):
    model.str_sub_sys.erase_full_str(1)
    assert model.get_str(1) == "33\n"


def test_make_emp(model):
    model.str_sub_sys.make_empty(2)
    assert model.get_str(2) == "\n"


def test_erase(model):
    model.str_sub_sys.erase_chr(0, 0)
    assert model.get_str(0) == "2345\n"

    model.str_sub_sys.erase_chr(0, 1)
    assert model.get_str(0) == "245\n"

    model.str_sub_sys.erase_chr(0, 2)
    assert model.get_str(0) == "24\n"


def test_index(model):
    assert model.str_sub_sys.get_word_at_index(0, 1) == "12345"
    assert model.str_sub_sys.viw_b(0, 3) == 0
    assert model.str_sub_sys.viw_w(0, 3) == 6
    assert model.str_sub_sys.find_to(0, 1, "44", "BOT") == (3, 0)


def test_get_from(model):
    r = model.file_sub_sys.get_from("testfile", model)
    r = [i.data() for i in r]
    assert r == [model.get_str(i) for i in range(len(model.buffer))]
