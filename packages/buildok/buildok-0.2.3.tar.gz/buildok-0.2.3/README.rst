# Buildok
[![Build Status](https://travis-ci.org/lexndru/buildok.svg?branch=master)](https://travis-ci.org/lexndru/buildok)

A tool to automate build steps from README files.

## Getting started
There are two possible ways to make use of this tool. You either create a file named `.build` and write each step on a line;
or write a new section in your `README.md` file starting with one of the following statements: "how to build ok" or "build ok steps".
Each step you write has to respect the following pattern: `n) build step <punctuation>` where `n` is a number and `<punctuation>` is one of the following: `.`, `!` or `?`.

#### Install
```
$ python setup.py install
$ build -h
```

#### Run tests
```
$ python test.py
```

## Supported statements
 - open link
 - copy files
 - move files
 - rename files
 - remove files
 - make directory
 - make symlink
 - change working directory
 - change permissions
 - change owner and group
 - exec shell commands
 - kill process

## How to build OK
1) Create folder `/tmp/_buildok`.
2) Go to `/tmp/_buildok`!
3) Run `pwd`!
4) Open link `https://github.com/lexndru/buildok`.
5) Run `echo Hello, friendly world`.

## License
Copyright 2018 Alexandru Catrina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
