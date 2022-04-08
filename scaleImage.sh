#!/bin/bash

# Scale an image to the maximum possible size for the conversion to a GS * ESCPOS raster image

srcFile="$1"
destFile="$2"

# Calculate the optimal dimensions of receipt
# For the conversion to esc/pos "GS *" image, the amount of bits must not be greater than 95968
# 95968 bits = 11996 Bytes * 8
# This is because of (12KB - 4B) The 4B represents the starting steering sequences
widthOriginal="$(identify -format '%w' "$srcFile")"
heightOriginal="$(identify -format '%h' "$srcFile")"
aspectRatio="$(echo "scale=5; $widthOriginal / $heightOriginal" | bc)"


# Calculate the maximum possible width of the image with out going over the max bits
# The following formula is based on altering a square with the dimensions of a square with the maximum amount of pixels
# In this case where the maximum amount of pixels is 95744 the length of a side would be 309,
# However, since ESC/POS Images will be defined as bytes per axis, it is advisable that the value
# can be divided by 8 so we shall use 304 since it is dividable by 8. We loose some pixels this way
# however it makes things much easier
# If a square with the maximum area should be strechted to a aspect ration another rectangle,
# the x axis must be multiplied by a factor (z), while y muste be multiplied by 1/z
# If a square with the maximum area should converted to a given aspect ration z,
# the x axis must be multiplied by z, while y muste be multiplied by 1/z
# z is defined as the square root of aspect ratio sqrt(x/y). The square root because a image has 2 dimensions
# So if we want to calculate the maximum size of a given image without going over the maximum of pixels we use the following formula:
# xNew = 304 * sqrt(x/y)
# yNew = 304 * 1/(sqrt(x/y)
# Since ImageMagick only needs one dimensions we'll use x
xNew="$(echo "scale=5; 304 * sqrt($aspectRatio)" | bc | cut -d . -f1)"
convert -resize "$xNew" "$srcFile" "$destFile"
