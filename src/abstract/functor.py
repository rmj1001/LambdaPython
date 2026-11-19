from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Functor[T](ABC):
    @abstractmethod
    def map[U](self, fn: Callable[[T], U]) -> Functor[U]:
        """
        Map a function to Functor that takes the original Functor's value as input
        and returns a new value as the return type
        :param fn: fn(T) -> U
        :return: Functor[U]
        """
