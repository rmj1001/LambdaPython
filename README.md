# MonadicPython

Usable monads for Python development, such as Maybe and Result.

## Maybe

Maybe represents states where data can be something (Some) or nothing (Nada). This is useful for data processing
scenarios that do not need explicit errors passed along a pipeline, but where data can still fail to produce something.

Maybe is meant to replace `type | None` unions, but it also handles functions that raise exceptions.

To convert an existing function to return a Maybe, use the `@maybe` decorator.

## Result

Result represents states where a function is successful (Ok) or fails (Err). This is used in lieu of raising and
handling exceptions.

To convert an existing function to return a Result, use the `@resultify` decorator.
