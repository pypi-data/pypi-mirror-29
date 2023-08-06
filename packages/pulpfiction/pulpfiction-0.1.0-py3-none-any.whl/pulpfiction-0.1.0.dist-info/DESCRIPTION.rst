# Pulp Fiction

<div align="center">
  <img src="./images/jules.png" width="256" height="256" alt="Jules Winnfield art by icassu">
</div>

_(English, *****! Do you speak it?)_

A simple tool to detect non-English commments in a code base (directory).

Inspired by the fictional character, [Jules Winnfield, played by Samuel L Jackson in the film, Pulp Fiction](https://www.urbandictionary.com/define.php?term=Jules%20Winnfield).

## Install

```shell
# requires Python3
$ pip install pulpfiction

## Usage

```shell
$ jules --help

Usage: jules [OPTIONS]

  Simple tool to detect non-English commments in a code base..

Options:
  --path TEXT           path to project or repository
  --help                Show this message and exit.
```

```shell
# by default, it looks at the current directory or $PWD
# alternatively,
$ jules --path=~/personal/my-awesome-git-project
```

Script exits with `sys.exit(0)` if successful, else the earliest invalid comment is found and raised.



