#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
from shutil import copyfile, make_archive, rmtree
import argparse
import sys
import os

version = "2.0"

parser = argparse.ArgumentParser(description="Generates a SellStick uses pack.")
req_args = parser.add_argument_group("required arguments")
parser.add_argument("-u", type=int, help="specify how many uses to generate (default is 50)",
                    default=50, required=False, metavar="uses")
args = parser.parse_args()

root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
root_folders = "temp/assets/minecraft/"
models_folder = os.path.join(root_folders, "models/item")
textures_folder = os.path.join(root_folders, "textures/item")
cit_folder = os.path.join(root_folders, "mcpatcher/cit/sellstick")

transparent_bg = Image.new('RGBA', (32, 32), (255, 0, 0, 0))

font_path = "resource/mineglyph-faithful.ttf"
text_font = ImageFont.truetype(font_path, 16)


def main():
  uses = args.u

  if uses < 0:
    sys.exit("Uses cannot be less than 0.")
  
  os.makedirs(models_folder)
  os.makedirs(textures_folder)
  os.makedirs(cit_folder)

  for i in range(1, uses + 1):
    generate(str(i))
    
  copyfile(root_path + "/resource/pack.mcmeta", root_path + "/temp/pack.mcmeta")
  copyfile(root_path + "/resource/pack.png", root_path + "/temp/pack.png")
  make_archive(f"SSUP V{version}", "zip", "temp")

  rmtree(root_path + "/temp")
  

def generate(uses: str):
  # generate uses overlay image
  img = transparent_bg.copy()
  overlay = ImageDraw.Draw(img)
  overlay.text((0, 0), uses, font=text_font, anchor="lt", fill=(0, 255, 0))
  img.save(f"{textures_folder}/sellstick_use_{uses}.png")

  # generate custom model
  with open("resource/model.template", "r") as template, open(f"{models_folder}/sellstick_{uses}.json", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[USE]]", uses))

  # generate cit properties file
  with open("resource/properties.template", "r") as template, open(f"{cit_folder}/sellstick{uses}.properties", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[USE]]", uses))


if __name__ == "__main__":
  main()