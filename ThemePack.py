# Author: Christoph Böhringer, Alexander Urban
# Date: 05/28/2020
# Version: 2.0

import ImagePack
import SoundPack
import TextColorPack

"""
steps to create a new usable theme:
 - create a new directory in /music and /images with the same same
 - fill the directories with the sound/image files you want to use (images must be .png and sounds .wav)
    -> the files must use the same names as the files in the default directory (e.g. GameField.png as the image used
        as the background when you are playing)
 - if you don't provide a file for a specific sound/image the default one will be used
 - you can also change the text colors that are used by adding new colors for your theme in TextColorPack.py
 - now add the name of your directory/theme in THEME_LIST() in main.py
"""


class ThemePack:
    theme_pack_name: str

    """
    desc: 
        - init
    param:
        - theme_pack_name: str -> the name used to create the ImagePack, SoundPack and TextColorPack
    return:
        - none
    """
    def __init__(self, theme_pack_name: str):
        self.theme_pack_name = theme_pack_name
        self.init_packs()

    def init_packs(self):
        image_pack = ImagePack.ImagePack(self.theme_pack_name)
        sound_pack = SoundPack.SoundPack(self.theme_pack_name)
        text_color_pack = TextColorPack.TextColorPack(self.theme_pack_name)
