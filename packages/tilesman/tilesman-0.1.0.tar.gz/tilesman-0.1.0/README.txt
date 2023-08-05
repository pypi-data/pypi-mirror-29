========
Tilesman
========

Given any photo, will create a pyramid of tiles split into different photo resolution levels,
represented in a folder hierarchy. Each folder is named against the resolution level it
represents, starting on L-1 (full resolution, most number of tiles) and going all the way down
to 0 (1 x 1 resolution, a single layer). Number of resolution levels is defined by the
equation L = 1 + ⌈log2 max(n, m)⌉


Installation
============

Download the source code from Github and extract to a local directory of your preference


Usage
=====

	cd /where/you/saved/tilesman

	python scripts/main.py -h (for detailed options)

	python scripts/main.py -p /path/to/the/photo -w <tile_max_width> -e <tile_max_height>


Tests
=====

	cd /where/you/saved/tilesman

	python -m unittest -v tilesman/tests/test_*
