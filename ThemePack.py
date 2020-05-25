import ImagePack
import SoundPack
import TextColorPack


class ThemePack:
    theme_pack_name: str

    def __init__(self, theme_pack_name: str):
        self.theme_pack_name = theme_pack_name
        self.init_packs()

    def init_packs(self):
        image_pack = ImagePack.ImagePack(self.theme_pack_name)
        sound_pack = SoundPack.SoundPack(self.theme_pack_name)
        text_color_pack = TextColorPack.TextColorPack(self.theme_pack_name)
