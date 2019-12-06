# competitive-programming

Repo for storing my solutions to competitive programming problems.

## readme.md

I try to write some comments about the problems and my strategy for solving it in the `readme.md` files.

Some of those files have LaTeX equations in them, which are, at the time of writing, not rendered by Github (and that's expected: equations aren't part of Github's markdown flavor). You can either use [the Markdown+Math VS Code extension](https://marketplace.visualstudio.com/items?itemName=goessner.mdmath) or [Typora](https://www.typora.io/) to view the rendered equations.

## Dependencies

The dev dependencies (`pytest` and `black`) are managed using [poetry](https://poetry.eustace.io/).

## Tests

I like writing unit tests when implementing solutions, it makes me a lot more confident that I didn't make mistakes.

The tests usually check that the solution works on small inputs, which are either taken from the problem statements or constructed by myself.

When tests are present, they are meant to be run using `pytest`. You should `cd` to a given solution's folder and run `poetry run pytest -vv -s` to run the tests for that solution.

I also find taking a look at the code coverage useful. It allows me to make sure the tests aren't missing an important branch. It's done by running this command: `poetry run pytest -vv -s --cov solve --cov-report html`. The coverage report is located in `htmlcov/index.html`.

## History

This repo replaces the previous repo I was using for this purpose: https://github.com/puigfp/ProblemSolvingPython

This repo was literally the first Git repo I every pushed code to. This means most stuff is in French (notes about the problems, commit messages and even the function/variable names in some solutions). The code isn't the prettiest code I've ever written...
