# competitive-programming

Repo for storing my solutions to competitive programming problems.

## notes.md

I try to write some comments about the problems and my strategy for solving it in the `notes.md` files.

Some of those files have LaTeX equations in them, which are, at the time of writing, not rendered by Github (and that's expected: equations aren't part of Github's markdown flavor). You can either use [the Markdown+Math VS Code extension](https://marketplace.visualstudio.com/items?itemName=goessner.mdmath) or [Typora](https://www.typora.io/) to view the rendered equations.

## Tests

I like writing short unit tests when implementing solutions, it makes me a lot more confident that I didn't make mistakes.

In python, a test is simply a function named `test_something`. When there are some tests, they are meant to be run using `pytest`. The shortcut for running them with coverage is `pipenv run test`.

## History

This repo replaces the previous repo I was using for this purpose: https://github.com/puigfp/ProblemSolvingPython

This repo was literally the first Git repo I every pushed code to. This means most stuff is in French (notes about the problems, commit messages and even the function/variable names in some solutions). The code isn't the prettiest code I've ever written...
