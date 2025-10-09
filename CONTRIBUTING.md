# Contributing to Spewer

First off, thank you for considering contributing to Spewer! It's people like you that make open source such a great community.

We welcome any type of contribution, not just code. You can help with:
* **Reporting a bug**
* **Discussing the current state of the code**
* **Submitting a fix**
* **Proposing new features**
* **Becoming a maintainer**

## We Use GitHub Flow

We use GitHub Flow, so all code changes happen through pull requests. We actively welcome your pull requests:

1.  **Fork the repo** and create your branch from `main`.
2.  If you've added code that should be tested, **add tests**.
3.  If you've changed APIs, **update the documentation**.
4.  Ensure the **test suite passes**.
5.  Make sure your code **lints**.
6.  Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/Agent-Hellboy/spewer/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/Agent-Hellboy/spewer/issues/new); it's that easy!

**Great Bug Reports** tend to have:

* A quick summary and/or background
* Steps to reproduce
    * Be specific!
    * Give sample code if you can.
* What you expected would happen
* What actually happens
* Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Setting up your development environment

Ready to contribute? Here's how to set up `spewer` for local development.

1.  Fork the `spewer` repo on GitHub.
2.  Clone your fork locally:
   
    ```
    git clone [https://github.com/your_username/spewer.git](https://github.com/your_username/spewer.git)
    ```
4.  Install your local copy into a virtual environment. Assuming you have `virtualenv` installed, this is how you set up your fork for local development:
    ```
    cd spewer/
    python3 -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"
    ```
5.  Install the pre-commit hooks:
    ```sh
    pre-commit install
    ```
6.  Create a branch for local development:
    ```sh
    git checkout -b name-of-your-bugfix-or-feature
    ```
    Now you can make your changes locally.
7.  When you're done making changes, check that your changes pass the tests and linting, this is done with `tox`:
    ```sh
    tox
    ```
8.  Commit your changes and push your branch to GitHub:
    ```sh
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature
    ```
9.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.

## Code Style

`spewer` uses [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting. The configuration can be found in `pyproject.toml`. We also use pre-commit hooks to automatically format the code before each commit.

By following these guidelines, you'll help us keep the project maintainable and easy to contribute to.

Thank you for your contribution!
