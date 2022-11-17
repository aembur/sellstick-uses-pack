#!/usr/bin/env python
from PIL import Image, ImageEnhance
from configparser import ConfigParser
from shutil import copyfile, make_archive, rmtree
import argparse
import sys
import os

formats = {1: "1.6.1–1.8.9",
           2: "1.9-1.10.2",
           3: "1.11-1.12.2",
           4: "1.13-1.14.4",
           5: "1.15-1.16.1",
           6: "1.16.2-1.16.5",
           7: "1.17.x",
           8: "1.18.x",
           9: "1.19-1.19.2",
           11: "1.19.3"}

parser = argparse.ArgumentParser(description="Generates a SellStick uses pack.")
req_args = parser.add_argument_group("required arguments")
req_args.add_argument("-p", help="pack format (see https://minecraft.fandom.com/wiki/Pack_format for info)",
                      type=int, choices=formats.keys(), metavar="format", required=True)
parser.add_argument("-u", type=int, help="specify how many uses to generate (default is 50)",
                    default=50, required=False, metavar="uses")
args = parser.parse_args()

root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
folders = "temp/assets/minecraft/mcpatcher/cit/icons/sellsticks/"
final_path = os.path.join(root_path, folders)

stick_img = Image.open("resource/stick.png")
chars_img = Image.open("resource/chars.png")
chars_dim = [chars_img.width // 10, chars_img.height]
chars_arr = [chars_img.crop((chars_dim[0] * i, 0, chars_dim[0] * i + chars_dim[0], chars_dim[1])) for i in range(10)]


def main():
  uses = args.u
  pack_format = args.p
  
  # parse if config is valid
  if uses < 0:
    sys.exit("Uses cannot be less than 0.")
  
  # create folder structure
  os.makedirs(final_path)
  
  # generate images and files
  for i in range(1, uses + 1):
    generate(str(i))
    
  # generate pack.mcmeta
  with open("resource/pack.template", "r") as template, open("temp/pack.mcmeta", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[FORMAT]]", str(pack_format)))
      
  # copy over pack.png
  copyfile(root_path + "/resource/pack.png", root_path + "/temp/pack.png")
  
  # make zip
  pack_version = formats[pack_format]
  make_archive(f"SellStick Uses {pack_version}", "zip", "temp")
  
  # clean up temp folder
  rmtree(root_path + "/temp")
  

def generate(uses: str):
  # generate image
  stick = stick_img.copy()
  for i in range(len(uses)):
    char = chars_arr[int(uses[i])]
    stick.paste(char, (i * chars_dim[0] + 1, 1), mask=char)

  stick.save(f"{final_path}sellstick_{uses}.png")

  # generate properties file
  with open("resource/properties.template", "r") as template, open(f"{final_path}sellstick_{uses}.properties", "a") as new_file:
    for line in template:
      new_file.write(line.replace("[[USE]]", uses))


if __name__ == "__main__":
  main()