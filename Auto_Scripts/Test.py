import pytest


def test_passing(x, y):
    print("test--1")
    return x + y


def test_1():
    assert test_passing(1, 1) == 2


if __name__ == '__main__':
    pytest.main("Test.py")  # 调用pytest的main函数执行测试


