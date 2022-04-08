# ESCPOS-rasterImage
Bash Script to automatically scale an image to the maximum possible size
Python script to generate a Raster Image used with the GS * in ESCPOS

Based on: https://www.epson-biz.com/modules/ref_escpos/index.php?content_id=91

Usage:

```
# Scale image (Will automatically use the biggest size possible
# If no scaling should be applied ensure the file is a monochrome bmp not bigger than 12KB
./scaleImage.sh {INPUT} {INPUT_RESIZED}

# Generate Raster Image
./generateRasterImg.py {INPUT_RESIZED} {OUTPUT}
```
