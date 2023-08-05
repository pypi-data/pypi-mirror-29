========
Tilesman
========

Given any photo, will create a pyramid of tiles split into different photo resolution levels,
represented in a folder hierarchy. Each folder is saved in the same directory as the original
image and is named against the resolution level it represents, starting on L-1 (full
resolution, most number of tiles) and going all the way down to 0 (1 x 1 resolution, a single
layer). Number of resolution levels is defined by the equation L = 1 + ⌈log2 max(n, m)⌉


Pre-requisites
==============

	Python 3.0+

	pip 9.0.0+

	Pillow 5.0.0+


Installation
============

	pip install tilesman


Usage
=====

For detailed argument options:

	tilesman -h

To tile a photo

	tilesman -p /path/to/the/photo -w <tile_max_width> -e <tile_max_height>


Tests
=====

After downloading the source code from "https://github.com/furzedo/Tilesman":

	cd /where/you/saved/tilesman/source

	python -m unittest -v tilesman/tests/test_*
