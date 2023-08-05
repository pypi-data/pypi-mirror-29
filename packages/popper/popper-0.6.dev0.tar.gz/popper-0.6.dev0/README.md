# Popper-CLI

A CLI tool to help bootstrap projects that follow the 
[Popper](https://github.com/systemslab/popper) convention.

## Install

### Manual

```bash
git clone --recursive git@github.com:systemslab/popper
export PATH=$PATH:$PWD/popper/cli/bin
```

> **NOTE**: the `--recursive` flag is needed in order to checkout all 
the dependencies.

### `pip`

[`pip`](https://pypi.python.org/pypi) package [coming 
soon](https://github.com/systemslab/popper/issues/216). In the 
meantime:

```bash
git clone git@github.com:systemslab/popper
cd popper/cli
pip install .
```

## Usage

To get an overview and list of commands check out the command line 
help:

```bash
popper --help
```
