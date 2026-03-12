from __future__ import annotations

from typing import TypeVar

# NOTE: from __future__ import annotatiosn: dit laat de type checkers weten dat types die nog niet bestaan
# wel later zullen toegevoegd worden...
#
# Typevar is een hulpmiddel om generiek types te maken
# Generiek: code die werkt met meerdere types... (bv een stack kan zowel ints als string als elementen hebben, als eigen
# gemaakte gegevenstypes...)

T = TypeVar("T")  # Hier zeg je van, T kan eender wel type zijn


class StackOverflowError(BaseException):
    """
    NOTE: maakt een nieuwe exception die erft van BaseException
    Hij erft dus het gedrag van de parent class, dus er is mogelijkheid om raise en except te gebruiken
    Waarom dan toch eigen class maken? Wel omdat je de exception dan wel een betekenisvolle naam kan geven...
    En het maakt ook dat je dus verschillende soort erros kan gebruiken, door te raisen ergens kan die exception
    dan opgevangen worden in bv een try except block...

    Het gaat er vooral om een type fout te onderscheiden en niet overal gewoon raise Exception te doen...

    Alsook later kan je nog extra info in de class toevoegen...
    """

    pass


class StackUnderflowError(BaseException):
    pass


class Stack[T]:
    """A stack is an abstract data type that serves as a collection of
    elements with two principal operations: push() and pop(). push() adds an
    element to the top of the stack, and pop() removes an element from the top
    of a stack. The order in which elements come off of a stack are
    Last In, First Out (LIFO).
    https://en.wikipedia.org/wiki/Stack_(abstract_data_type)

    NOTE: list kan worden gebruikt voor een effectieve en efficiente manier om een stack te implemeteren
    """

    def __init__(self, limit: int = 10):
        # dit kan dus een list van ints zijn, een list van strings, ...
        self.stack: list[T] = []
        self.limit = limit

    def __bool__(self) -> bool:
        # als list leeg dan False, als niet leeg True
        return bool(self.stack)

    def __str__(self) -> str:
        # je returned de string representation van de list, logisch want list wordt gebruikt als implementatie voor een stack
        return str(self.stack)

    def push(self, data: T) -> None:
        """
        Push an element to the top of the stack.

        >>> S = Stack(2) # stack size = 2
        >>> S.push(10)
        >>> S.push(20)
        >>> print(S) # NOTE: deze gebruikt dus gewoon de stringrepresentatie van een list..
        [10, 20]

        >>> S = Stack(1) # stack size = 1
        >>> S.push(10)
        >>> S.push(20)
        Traceback (most recent call last):
        ...
        data_structures.stacks.stack.StackOverflowError

        """
        # NOTE: je kan telkens maar 1 iets pushen dus kijken of de lengte == limit is voldoende...
        if len(self.stack) >= self.limit:
            raise StackOverflowError
        self.stack.append(data)
        # we gebruiken dus gewoon append methode van de list class

    def pop(self) -> T:  # merk op, generic type hier heel handig
        """
        Pop an element off of the top of the stack.
        NOTE: en return het element

        >>> S = Stack()
        >>> S.push(-5)
        >>> S.push(10)
        >>> S.pop()
        10

        >>> Stack().pop()
        Traceback (most recent call last):
            ...
        data_structures.stacks.stack.StackUnderflowError
        """
        if not self.stack:
            raise StackUnderflowError
        return self.stack.pop()

    def peek(self) -> T:
        """
        Peek at the top-most element of the stack.

        >>> S = Stack()
        >>> S.push(-5)
        >>> S.push(10)
        >>> S.peek()
        10

        >>> Stack().peek()
        Traceback (most recent call last):
            ...
        data_structures.stacks.stack.StackUnderflowError
        """
        if not self.stack:
            raise StackUnderflowError
        return self.stack[-1]

    def is_empty(self) -> bool:
        """
        Check if a stack is empty.

        >>> S = Stack()
        >>> S.is_empty()
        True

        >>> S = Stack()
        >>> S.push(10)
        >>> S.is_empty()
        False
        """
        return not bool(self.stack)

    def is_full(self) -> bool:
        """
        >>> S = Stack()
        >>> S.is_full()
        False

        >>> S = Stack(1)
        >>> S.push(10)
        >>> S.is_full()
        True
        """
        return self.size() == self.limit

    def size(self) -> int:
        """
        Return the size of the stack.

        >>> S = Stack(3)
        >>> S.size()
        0

        >>> S = Stack(3)
        >>> S.push(10)
        >>> S.size()
        1

        >>> S = Stack(3)
        >>> S.push(10)
        >>> S.push(20)
        >>> S.size()
        2
        """
        return len(self.stack)

    def __contains__(self, item: T) -> bool:
        """
        Check if item is in stack

        >>> S = Stack(3)
        >>> S.push(10)
        >>> 10 in S
        True

        >>> S = Stack(3)
        >>> S.push(10)
        >>> 20 in S
        False
        """
        return item in self.stack


def test_stack() -> None:
    """
    >>> test_stack()
    """
    stack: Stack[int] = Stack(10)
    assert bool(stack) is False
    assert stack.is_empty() is True
    assert stack.is_full() is False
    assert str(stack) == "[]"

    try:
        _ = stack.pop()
        raise AssertionError  # This should not happen
    except StackUnderflowError:
        assert True  # This should happen

    try:
        _ = stack.peek()
        raise AssertionError  # This should not happen
    except StackUnderflowError:
        assert True  # This should happen

    for i in range(10):
        assert stack.size() == i
        stack.push(i)

    assert bool(stack)
    assert not stack.is_empty()
    assert stack.is_full()
    assert str(stack) == str(list(range(10)))
    assert stack.pop() == 9
    assert stack.peek() == 8

    stack.push(100)
    assert str(stack) == str([0, 1, 2, 3, 4, 5, 6, 7, 8, 100])

    try:
        stack.push(200)
        raise AssertionError  # This should not happen
    except StackOverflowError:
        assert True  # This should happen

    assert not stack.is_empty()
    assert stack.size() == 10

    assert 5 in stack
    assert 55 not in stack


if __name__ == "__main__":
    test_stack()

    import doctest

    doctest.testmod()
