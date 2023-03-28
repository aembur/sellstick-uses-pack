#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
from shutil import copyfile, make_archive, rmtree
import argparse
import sys
import os

version = "1.3"

parser = argparse.ArgumentParser(description="Generates a SellStick uses pack.")
req_args = parser.add_argument_group("required arguments")
req_args.add_argument("-p", help="pack format (see https://minecraft.fandom.com/wiki/Pack_format for info)",
                      type=int, metavar="format", required=True)
parser.add_argument("-u", type=int, help="specify how many uses to generate (default is 50)",
                    default=50, required=False, metavar="uses")
args = parser.parse_args()

root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
folders = "temp/assets/minecraft/mcpatcher/cit/icons/sellsticks/"
final_path = os.path.join(root_path, folders)

stick_img = Image.open("resource/stick.png")
# upscale the stick image so fonts actually look good
stick_img = stick_img.resize((32, 32), Image.Resampling.NEAREST)

font_path = "resource/mineglyph-faithful.ttf"
# for bitmap fonts, font size should match the resolution
text_font = ImageFont.truetype(font_path, 16)


def main():
  uses = args.u
  pack_format = args.p

  if uses < 0:
    sys.exit("Uses cannot be less than 0.")
  
  os.makedirs(final_path) # create folder structure

  for i in range(1, uses + 1):
    generate(str(i))
    
  # generate pack.mcmeta
  with open("resource/pack.template", "r") as template, open("temp/pack.mcmeta", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[FORMAT]]", str(pack_format)))

  copyfile(root_path + "/resource/pack.png", root_path + "/temp/pack.png")
  make_archive(f"SSUP V{version} P{pack_format}", "zip", "temp")
  
  # clean up temp folder
  rmtree(root_path + "/temp")
  

def generate(uses: str):
  # generate image
  stick = stick_img.copy()
  img = ImageDraw.Draw(stick)
  img.text((0, 0), uses, font=text_font, anchor="lt", fill=(0, 255, 0))

  stick.save(f"{final_path}sellstick_{uses}.png")

  # generate properties file
  with open("resource/properties.template", "r") as template, open(f"{final_path}sellstick_{uses}.properties", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[USE]]", uses))


if __name__ == "__main__":
  main()