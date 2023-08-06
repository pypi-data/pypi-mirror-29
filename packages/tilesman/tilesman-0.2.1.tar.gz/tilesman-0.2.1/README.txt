========
Tilesman
========

Tilesman is designed to create a hierarchy of tiled representations of the supplied photos.
Starting with the photo in its original pixel resolution, Tilesman will create the minimum
number of tiles, as per dimensions supplied as arguments, and save them in a numbered folder.
After that, the photo will be resized to 1/2 of its original size and the tiling process
will be applied recurvively until the photo reaches the minimum size of 1 x 1 pixels. At this
stage, a hierarchy of folders is expected to exist, named from "0" (1 x 1 pixels image,
one tile) up to the highest numbered folder (original size photo, maximum number of tiles).
Tiles can have dimensions smaller than the requested sizes, when they are extracted from the
edges of x and y axes.


Pre-requisites
==============

	Python 3.3+

	pip 9.0.0+

	Pillow 5.0.0+


Installation
============

	pip install tilesman


Usage (in your Python code)
===========================

Processing a single photo

	from tilesman.core import photo_tiling

	photo_tiling('/path/to/the/photo', tile_max_width, tile_max_height)

Processing several photos in a directory (parallel processing)

	from tilesman.core import batch_photo_tiling

	batch_photo_tiling('/path/to/the/photo/directory', tile_max_width, tile_max_height)


Usage (as a command line utility)
=================================

For detailed argument options:

	tilesman -h

To tile a photo

	tilesman -p /path/to/the/photo_or_directory -w <tile_max_width> -e <tile_max_height>


Tests
=====

	cd /where/you/saved/tilesman/source

	python -m unittest -v tilesman/tests/test_*
