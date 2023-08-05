## imgaug extended

This is an extension to imgaug, found at <https://github.com/aleju/imgaug>, which converts a set of input images into a new set of slightly altered images.

It adds three new augmentation implementations: 

* Color Transfer
* Object Insertion
* Polygons 

Outputs examples of `/example/example.py` are:

Color Transfer

![Color Transfer](example/color_transfer_example.png)

Object Insertion

![Object Insertion](example/object_insertion_example.png)

Greyscaled Polygons

![B&W Polygons](example/bw_polygons_example.png)

Channel-wise Polygons

![RGB Polygons](example/rgb_polygons_example.png)


## Requirements and installation

Required packages are *imgaug* (`pip install imgaug`) and its dependencies, view the readme for imgaug for more information.

## List of new augmenters

Augmenter | Description
----------|------------
Color Transfer(I)|Transfers the LAB colors taken from a random item in source images `I` (keys identify an image).
Object Insertion(I,L,S)|Inserts a random image from a list of images, scaled down to size `S` at a random position within location `L`. The anchor of images is set to the center-bottom.
Polygon(P,V,C)|Creates random polygons `P` with shape defined by `V` on an image, that alter pixels caught in a polygon. If `C` is not false, polygons may alter pixels channel-wise. 