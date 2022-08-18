from pytest import raises
from cpp import *

# cpp // "Construct a vector from an initializer list"
# x: std_vector[int] = _[std::vector<int>v({1, 2, 3})]


# x.push_back(4) // "Adds 4 to the end of the vector"

# _[std::cout] << "Vector x: " << x << _[std::endl] // "prints out [1, 2, 3, 4]"

# cpp // "Range-based for loop over vector x:"
# for i in auto& x:
#     _[std::cout] << "Incrementing " << i << "..." << _[std::endl]
#     i += 1

# _[std::cout] << "Vector after: " << x << _[std::endl]


def test_cout(capsys) -> None:
    x = [1, 2, 3]
    cpp[std::cout] << "Testing: " << x
    assert capsys.readouterr().out == "Testing: [1, 2, 3]"
    cpp[std::cout] << "Testing: " << x << cpp[std::endl]
    assert capsys.readouterr().out == "Testing: [1, 2, 3]\n"


def test_vector() -> None:
    x = [1, 2, 3]
    y = cpp[std :: vector < int > v(x)]  # type: ignore
    assert y == [1, 2, 3]
    y.push_back(4)
    assert y == [1, 2, 3, 4]
    z = cpp[std :: vector < float > v(3, 0.0)]
    assert z == [0.0, 0.0, 0.0]
    w = cpp[std :: vector < float > v({1, 2, 3})]
    assert w == [1.0, 2.0, 3.0]
    w.clear()
    assert w == []
    assert w._datatype == float


def test_vector_conversions() -> None:
    x = [1, 2, 3]
    y = cpp[std :: vector < int > v(x)]  # type: ignore
    y.push_back(4.0)
    assert y == [1.0, 2.0, 3.0, 4.0]
    with raises(TypeError):
        w = ["a", "b", "c"]
        z = cpp[std :: vector < int > v(w)]  # type: ignore


def test_loop_by_reference() -> None:
    x = [1, 2, 3]
    y = cpp[std :: vector < int > v(x)]  # type: ignore
    for i in auto & y:
        i += 1
    assert y == [2, 3, 4]
