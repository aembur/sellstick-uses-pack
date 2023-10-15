<p align="center">
  <img src="uses.png" alt="SellStick Uses Pack"/>
</p>

A resource pack that shows you how many uses your SellStick have without having to hover over them. Uses Custom Items feature from MCPatcher or Optifine. Made for the Cosmic Craft server, but can be adapted to other servers. Tested on 1.8.9 and 1.12.2.

# Requirements
- MCPatcher or Optifine

# Installation
1. Download the pack from the [releases](https://github.com/aembur/sellstick-uses-pack/releases).
2. Place the file in your `.minecraft/resourcepacks` folder.
3. In Minecraft, go to `Options > Resource Packs` and move the `SSUP` pack to the **Selected Resource Packs**. Ignore any warnings about version mismatch.
4. Make sure **Custom Items** are turned **ON** in `Options > Video Settings > Quality`.

# Generating your own pack
If you want to change the font and font colours, you can do so by adding your own font to the `resource` folder, then editing the `generate.py` to use it.
Afterwards, run `generate.py -u [max uses]` to generate a pack.

# Making this work on other servers
This pack works by matching a regex pattern in the item lore. Making this pack work in other servers is as simple as changing the regex pattern in the `properties.template` file found in the `resource` folder.
