#!/usr/bin/env python3

"""
Convert a image to rasterformat required by Epson POS Printer
Based on "GS *" (https://www.epson-biz.com/modules/ref_escpos/index.php?content_id=91)
"""

# Version History
# 0.1   gw    09.06.2021    Inital version

import argparse
import math
import os
import sys

from PIL import Image, ImageOps

def calcIntFromBoolArr(arr):
    """
    Calculate an int from an array of bool values treated as bits
    """
    total = 0
    for index, value in enumerate(arr):
        total += math.pow(2, 7 - index) * value

    return int(total)


if len(sys.argv) != 3:
    print("This program takes only 2 command line arguments:")
    print("./generateRasterImg.py INPUTFILE OUTPUTFILE")
    sys.exit(1)

inputPath = sys.argv[1]
outputPath = sys.argv[2]

if not os.path.isfile(inputPath):
    print(f"Could not find or access {inputPath}")
    sys.exit(2)

imgOriginal = Image.open(inputPath)
imgOriginal = imgOriginal.convert('RGBA')

# Invert originial image
img = Image.new("RGB", imgOriginal.size, (255, 255, 255))
img.paste(imgOriginal, mask=imgOriginal.split()[3])

# Convert down to greyscale
img = img.convert("L")

# Invert: Only works on 'L' images
img = ImageOps.invert(img)

# Monochrome
img = img.convert("1")

width = img.width
height = img.height

# Amount bytes required for each axis
xBytes = math.ceil(width / 8)
yBytes = math.ceil(height / 8)

bits = []
bitCounter = 0
asciiCodes = []

# Loop over each pixel and convert to one 1 byte char
for x in range(0, width):
    for y in range(0, height):
        bitCounter += 1

        if img.getpixel((x, y)) == 0:
            bits.append(False)
        else:
            bits.append(True)

        if bitCounter == 8:
            intVal = calcIntFromBoolArr(bits)
            asciiCodes.append(intVal)
            bitCounter = 0
            bits = []

    # If bitCounter didn't reach 8 add ascii anyway
    if bitCounter != 0:
        intVal = calcIntFromBoolArr(bits)
        asciiCodes.append(intVal)
        bitCounter = 0
        bits = []

# Get amount of remaining bytes
bytesRemaining = (yBytes * xBytes * 8) - len(asciiCodes)

# Fill remaining bytes with zeros
for times in range(bytesRemaining):
    asciiCodes.append(0)

asciiCodes = bytearray(asciiCodes)

output = open(outputPath, "wb")
output.write(
    b"\x1d*" +
    xBytes.to_bytes(
        1,
        "little") +
    yBytes.to_bytes(
        1,
        "little"))
output.write(asciiCodes)
output.close()
