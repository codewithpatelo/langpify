"""Tests para el módulo example."""

import pytest

from src.langpify import example


def test_hello_world():
    """Test para la función hello_world."""
    assert example.hello_world() == "Hello, World!"


class TestExample:
    """Tests para la clase Example."""

    def test_init(self):
        """Test para el constructor de Example."""
        obj = example.Example()
        assert obj.name == "World"

        obj = example.Example(name="Python")
        assert obj.name == "Python"

    def test_greet(self):
        """Test para el método greet."""
        obj = example.Example()
        assert obj.greet() == "Hello, World!"

        obj = example.Example(name="Python")
        assert obj.greet() == "Hello, Python!"

    def test_process_data(self):
        """Test para el método process_data."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25, "city": "New York"},
            {"city": "Boston", "country": "USA"},
        ]
        result = example.Example.process_data(data)
        assert result == {"name": 2, "age": 2, "city": 2, "country": 1}
