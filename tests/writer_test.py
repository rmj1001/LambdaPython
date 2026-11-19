from collections.abc import Iterable
from dataclasses import FrozenInstanceError
from unittest import TestCase
from src.monads.writer import Writer


class TestWriter(TestCase):
    def test_flat_map(self):
        original: Writer[int] = Writer(0, ('Test',))
        target: Writer[int] = Writer(10, ('Test', 'Test2'))

        self.assertEqual(
            original.flat_map(lambda x: Writer(x + 10, ('Test2',))),
            target
        )

    def test_flatten(self):
        original: Writer[Writer[int]] = Writer(Writer(0, ('Inner',)), ('Outer',))
        target: Writer[int] = Writer(0, ('Outer', 'Inner'))

        self.assertEqual(
            original.flatten(),
            target
        )

    def test_map(self):
        original: Writer[int] = Writer(0, ('Init',))

        self.assertEqual(
            original.map(lambda x: x + 10),
            Writer(10, ('Init',))
        )

        self.assertEqual(
            original.map(lambda x: x + 10, 'Test'),
            Writer(10, ('Init','Test',))
        )

        self.assertEqual(
            original.map(lambda x: x + 10, lambda x: f'Value is {x}'),
            Writer(10, ('Init','Value is 10',))
        )

    def test_map_log(self):
        original: Writer[int] = Writer(0, ('Test1',))

        self.assertEqual(
            original.map_log('Test2'),
            Writer(0, ('Test1', 'Test2'))
        )

        self.assertEqual(
            original.map_log(lambda x: f'Value is {x}'),
            Writer(0, ('Test1', 'Value is 0'))
        )

    def test_log(self):
        w: Writer[None] = Writer(None, ('Test',))

        self.assertEqual(
            Writer.log('Test'),
            w
        )

    def test_val(self):
        w: Writer[int] = Writer(0, ())

        self.assertEqual(
            Writer.val(0),
            w
        )

    def test_inspect(self):
        w: Writer[int] = Writer(0, ('Test1', 'Test2'))
        values: list[int] = []

        # noinspection shadowing-names
        def update_values(x: int) -> None: values.append(x)

        # Inspect w and make sure the same object is returned
        self.assertIs(
            w.inspect(update_values),
            w
        )

        # Make sure the `update_values` function passed is run
        self.assertEqual(
            values,
            [0]
        )

    def test_inspect_logs(self):
        w: Writer[int] = Writer(0, ('Test1', 'Test2'))
        logs: list[str] = []

        # noinspection shadowing-names
        def update_logs(l: Iterable[str]) -> None: logs.extend(l)

        # Inspect w and make sure the same object is returned
        self.assertIs(
            w.inspect_logs(update_logs),
            w
        )

        # Make sure the `update_logs` function passed is run
        self.assertEqual(
            logs,
            ['Test1', 'Test2']
        )

    def test_pattern_matching(self):
        w: Writer[int] = Writer(0, ('test',))

        match w:
            case Writer(value, logs):
                self.assertEqual(value, 0)
                self.assertEqual(logs, ('test',))
            case _:
                self.fail()

    def test_frozen(self):
        w: Writer[int] = Writer(0, ())

        with self.assertRaises(FrozenInstanceError):
            setattr(w, 'value', 5)

    def test_functor_laws(self):
        f_id = lambda x: x
        f = lambda x: x + 1
        g = lambda x: x * 2

        w = Writer(5, ('Test',))

        # Identity: w.map(f_id) == w
        self.assertEqual(
            w.map(f_id),
            w
        )

        # Associativity: w.map(f).map(g) == w.map( lambda x: g( f(x) ) )
        self.assertEqual(
            w.map(f).map(g),
            w.map(lambda x: g(f(x)))
        )

    def test_monad_laws(self):
        f = lambda x: Writer(x - 5, ('Minus 5',))
        g = lambda x: Writer(x / 7, ('Divide 7',))

        w = Writer(5, ('Test',))

        # Left identity: w.unit(a).flat_map(f) = f(a)
        self.assertEqual(
            Writer.val(3).flat_map(f), f(3)
        )

        # Right identity: w.flat_map(Writer.unit) = w
        self.assertEqual(
            w.flat_map(Writer.val),
            w
        )

        # Associativity
        self.assertEqual(
            w.flat_map(f).flat_map(g),
            w.flat_map(lambda x: f(x).flat_map(g))
        )
