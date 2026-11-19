from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable, Iterable

type Log[T] = str | Callable[[T], str]

@dataclass(frozen=True)
class Writer[T]:
    value: T
    logs: tuple[str, ...] = ()

    def flat_map[U](self, fn: Callable[[T], Writer[U]]) -> Writer[U]:
        """
        Create a new Writer monad by mapping a function to the monad
        :param fn: Function that takes self.value as a parameter and returns a new Writer monad
        :return: Writer monad
        """
        next_writer = fn(self.value)
        return Writer(next_writer.value, self.logs + next_writer.logs)

    def flatten[U](self: Writer[Writer[U]]) -> Writer[U]:
        """
        Flatten Writer monad by returning a Writer with the inner value and
        appended inner logs to end of current logs.
        :return: Flattened Writer (one level)
        """
        return Writer(self.value.value, self.logs + self.value.logs)

    def inspect(self, fn: Callable[[T], object]) -> Writer[T]:
        """
        Do some function on self.value without modifying the value
        :param fn: Function that takes self.value as parameter without returning value
        :return: self
        """
        fn(self.value)
        return self

    def inspect_logs(self, fn: Callable[[Iterable[str]], object]) -> Writer[T]:
        """
        Do some function on self.logs without modifying them
        :param fn: Function that takes self.logs as parameter without returning value
        :return: self
        """
        fn(self.logs)
        return self

    def map[U](
            self,
            fn: Callable[[T], U],
            log: Log[U] | None = None
    ) -> Writer[U]:
        """
        Create a new Writer monad whose value is fn(self.value), with an optional log
        added to the monad's logs tuple
        :param fn: The function to apply to self.value
        :param log: The optional log message
        :return: Writer monad
        """
        new_val_writer = Writer(fn(self.value), self.logs)

        match log:
            case None:
                return new_val_writer
            case _:
                return new_val_writer.map_log(log)

    def map_log(self, message: Log[T]) -> Writer[T]:
        """
        Create a Writer monad with the same value but
        adding a new log message
        :param message: Log message
        :return: Writer monad
        """
        match message:
            case str():
                return Writer(self.value, self.logs + (message,))
            case _:
                return Writer(self.value, self.logs + (message(self.value),))

    @staticmethod
    def log(message: str) -> Writer[None]:
        """
        Create a Writer monad with just a log message string
        :param message: Log message string
        :return: Writer monad
        """
        return Writer(None, (message,))

    @staticmethod
    def val[U](value: U) -> Writer[U]:
        """
        Create a Writer monad with just a value and no logs
        :param value: The contained value
        :return: Writer monad
        """
        return Writer(value)
