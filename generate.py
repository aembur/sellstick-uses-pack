#!/usr/bin/env python
from PIL import Image, ImageEnhance
from configparser import ConfigParser
from shutil import copyfile, make_archive, rmtree
import sys
import os

root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
folders = "temp/assets/minecraft/mcpatcher/cit/icons/sellsticks/"
final_path = os.path.join(root_path, folders)

stick_img = Image.open("resource/stick.png")
chars_img = Image.open("resource/chars.png")
chars_dim = [chars_img.width // 10, chars_img.height]
chars_arr = [chars_img.crop((chars_dim[0] * i, 0, chars_dim[0] * i + chars_dim[0], chars_dim[1])) for i in range(10)]

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


def main():
  # read config file
  config = ConfigParser()
  config.read("resource/config.cfg")
  options = config["options"]
  uses = options.getint("max_uses")
  pack_format = options.getint("pack_format")
  
  # parse if config is valid
  if uses < 0:
    sys.exit("Uses cannot be less than 0.")
    
  if not pack_format in formats.keys():
    sys.exit("Invalid pack format.")
  
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