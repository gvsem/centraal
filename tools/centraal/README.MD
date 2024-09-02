# Centraal CLI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



### Introduction

Centraal clusters require common and consistent tools of management and maintenance. Centraal CLI is a common way to deploy and enroll new clusters.

## Getting started

### Installation and usage

### Development

#### on macOS

- Open project directory: `cd ./tools/centraal`
- Install [python](https://wiki.python.org/moin/BeginnersGuide/Download) and [pipx](https://pipx.pypa.io/stable/installation/): ``brew install python pipx``
- Export binaries to PATH: `echo 'export PATH="/usr/local/opt/python@3.12/libexec/bin:$PATH"' >> ~/.zshrc`
- Install [poetry](https://python-poetry.org/docs/#installing-with-pipx): ``pipx install poetry==1.2.0``
- (optionally) Add autocompletions:
    - `poetry completions bash >> ~/.bash_completion`
    - `mkdir -p ~/.zfunc && poetry completions zsh > ~/.zfunc/_poetry && echo -n "fpath+=~/.zfunc \n autoload -Uz compinit && compinit" >> ~/.zshrc`
- Install pre-commit git hooks: `pre-commit install`
