# Based on https://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/

import os
import argparse
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
 
def watermark_text(input_image_path,
                   output_image_path,
                   text, pos):
    photo = Image.open(input_image_path)
 
    # make the image editable
    drawing = ImageDraw.Draw(photo)
 
    black = (3, 8, 12)
    font = ImageFont.truetype("Pillow/Tests/fonts/DejaVuSans.ttf", 40)
    drawing.text(pos, text, fill=black, font=font)
    photo.show()
    photo.save(output_image_path)
 
def watermark_with_transparency(input_image_path,
                                output_image_path,
                                watermark_image_path,
                                display_preview):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    width, height = base_image.size
    wm_width, wm_height = watermark.size

    pos_x = width - wm_width
    pos_y = height - wm_height - 5
    pos_y = 0

    pos_x = 1280 - wm_width
    pos_y = 720 - wm_height - 5
 
    # use base image to create a new file
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    # Resize!
    transparent.thumbnail((1280, 720))
    # Now add watermark
    transparent.paste(watermark, (pos_x, pos_y), mask=watermark)
    if display_preview:
        transparent.show()
    transparent.save(output_image_path)

    return

def find_images(inputpath):
    images = []

    with os.scandir(inputpath) as listOfFiles:
        for f in listOfFiles:
           if f.is_file():
                _, ext = os.path.splitext(f)
                ext = ext.lower()
                if ext == ".png" or ext == ".jpg":
                    images.append(f.path)

    return images

 
def main (argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        default=None,
        help="Process All files in directory",
    )
    parser.add_argument(
        "watermark",
        default=None,
        help="Path to watermark file",
    )

    parser.add_argument(
        "-f", "--file",
        default=False,
        action="store_true",
        help="Process a `directory` input as a Single File instead of directory",
    )

    parser.add_argument(
        "-s", "--suffix",
        default=None,
        help="Append a suffix to generated files. Defaults to overwriting",
    )

    parser.add_argument(
        "-d", "--display",
        default=False,
        action="store_true",
        help="Show the preview",
    )

    args = parser.parse_args() 

    if args.file == False:
        images = find_images(args.directory)
    else:
        images = [args.directory]

    for i in images:

        # We're only going to save PNGs because JPGs don't like alpha
        oFile, ext = os.path.splitext(i)
        if args.suffix != None:
            oFile = oFile + args.suffix
        if ext == ".jpg":
            ext = ".png"

        oFile = "{}{}".format(oFile, ext)

        watermark_with_transparency(
            i,
            oFile,
            args.watermark,
            args.display,
        )

   
if __name__== "__main__":
  main(sys.argv)