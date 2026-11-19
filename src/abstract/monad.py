from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.abstract.functor import Functor


@dataclass(frozen=True)
class Monad[T](Functor[T], ABC):
    @abstractmethod
    def flat_map[U](self, fn) -> Monad[U]:
        """
        Map a function to the internal value that takes the
        internal value as a parameter and returns a new monad
        :param fn: fn(t) -> Monad[U]
        :return: Monad[U]
        """
