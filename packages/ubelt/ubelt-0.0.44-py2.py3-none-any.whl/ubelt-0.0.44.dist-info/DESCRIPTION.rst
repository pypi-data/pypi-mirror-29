UBelt is a "utility belt" of commonly needed utility and helper functions. It is a migration of the most useful parts of `utool`   (https://github.com/Erotemic/utool) into a minimal and standalone module.

The `utool` library contains a number of useful utility functions, however a number of these are too specific or not well documented. The goal of this migration is to slowly port over the most re-usable parts of `utool` into a stable package.

The doctest harness in `utool` was ported and rewritten in a new module called: [`xdoctest`](https://github.com/Erotemic/xdoctest), which integrates with `pytest` as a plugin. All of the doctests in `ubelt` are run using `xdoctest`.

A small subset of the static-analysis and code introspection tools in `xdoctest` are made visible through `ubelt`.

In addition to utility functions `utool` also contains a feature for auto-generating `__init__.py` files. See `ubelt/__init__.py` for an example.

UBelt is cross platform and all top-level functions behave similarly on Windows, Mac, and Linux (up to some small unavoidable differences). Every function in `ubelt` is written with a doctest, which provides helpful documentation and example usage as well as helping achieve 100% test coverage.

