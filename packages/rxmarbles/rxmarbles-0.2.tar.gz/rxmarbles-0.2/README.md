# About
This is yet another marble diagram generator for documenting Reactive Extensions sources and operators.

# Features

* generating SVG graphics files from a simple text description
* unlimited number of source observable and operator lines
* support for multiple characters long values
* support for grouped (buffered) values
* support for observables of observables (2nd order)
* adjusting starting point of a timeline with number of `.` characters at the beginning of a timeline 
* easier visual adjustment between timelines in source files with white spaces in timeline
* scaling dimension of a default SVG view box for generated diagrams 
* auto-coloring marbles representing identical values 
* generation multiple diagram images from a single file (batch mode)

# Installation
The oneliner installation on Linux (to local user home directory)  is: 

	git clone https://achary@bitbucket.org/achary/rx-marbles.git && \
	cd rx-marbles && \
	pip install --user .

The `marblesgen` executable will become available from the command prompt.

# Running without installation
You can run the generator without installation, from the source code tree, e.g:

	python -m rxmarbles --help

# Example

A simple text file (foo.txt) with a marble diagram can look like this:

	marble foo_example
	{
		source a:     +--A-B--C-#
		operator foo: +--1-2--3-|
	}

To generate SVG image out of it, you can run:

	marblesgen foo.txt 
	
This will produce the following diagram:

![foo_example.svg](https://bitbucket.org/achary/rx-marbles/raw/master/docs/foo_example.svg)

# Requirements
To run this marbles diagram generator, you need Python 2.7.x or 3.x with `pyparsing` module installed.

The generator's code is fairly platform agnostic and can be used on Linux, Window, Macs and possible other platforms
that have proper version of Python installed.

# Unit tests
All unit tests for the generator are located in `tests` subdirectory. They can be executed from top-level project dir with:

	python -m unittest discover tests/

# Details

* [Marble diagram syntax](docs/syntax.md)
* [Generator options](docs/options.md)

# License
Available under [MIT license](LICENSE).

# Other generators

* [staltz/rxmarbles](https://github.com/staltz/rxmarbles)
* [aheckmann/gm](https://github.com/aheckmann/gm)
* [LeeCampbell/MarbleDiagram](https://github.com/LeeCampbell/MarbleDiagram/tree/master/LinqPad)
