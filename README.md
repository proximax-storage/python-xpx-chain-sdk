NEM2 SDK Python
===============

**Table of Contents**

- [Getting Started](#getting-started)
- [Optimization](#optimization)
- [Testing](#testing)
- [License](#license)
- [Contributing](#contributing)

# Getting Started



# Optimization

The NEM2 SDK makes copious use of assertions to ensure functionality is correct during debugging, and during use of the client, it may be preferable to disable these assertions. This may be done by either setting the environment variable `PYTHONOPTIMIZE=TRUE`, or through the command-line flag `-O`.

In addition, installing [uvloop](https://github.com/magicstack/uvloop) may further improve asynchronous code performance.

# Testing

The NEM2 SDK uses numerous tools to ensure type correctness, robust testing, and style conventions are preserved over multiple configurations. Before submitting any contributions, please resolve any issues that result from the following commands before committing:

```bash
# Run tox, which invokes numerous virtual envs to validate all configurations
# Invokes the unittest suite.
# Invokes the randomly-generated unittest suite.
# Invokes the linters, flake8 and pylint.
# Invokes bandit, a which checks for possible security risks.
# Invokes the type-checker, mypy.
# Invokes the complexity and maintainability checker, radon.
# Invokes the code coverage generator, coverage.
# Invokes the documentation builder, Sphinx.
$ tox
```

# License

Lexical is licensed under the Apache 2.0 license. See the LICENSE for more information. 

# Contributing

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in lexical by you, as defined in the Apache-2.0 license, shall be licensed as above, without any additional terms or conditions.
