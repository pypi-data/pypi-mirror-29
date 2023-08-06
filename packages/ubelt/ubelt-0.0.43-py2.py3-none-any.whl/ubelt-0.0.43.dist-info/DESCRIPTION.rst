UBelt is a "utility belt" of commonly needed utility and helper functions. It is a migration of the most useful parts of `utool`   (https://github.com/Erotemic/utool) into a minimal and standalone module.

The `utool` library contains a number of useful utility functions, however a number of these are too specific or not well documented. The goal of this migration is to slowly port over the most re-usable parts of `utool` into a stable package.

In addition to utility functions `utool` also contains a custom doctest   harness and code introspection and auto-generation features. A rewrite of the test harness has been ported to a new module called: [`xdoctest`](https://github.com/Erotemic/xdoctest).  A small subset of the auto-generation and code introspection will be ported / made visible through `ubelt`.

