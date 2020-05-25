import ImagePack
import SoundPack
import TextColorPack


class ThemePack:
    sound_pack_name: str
    image_pack_name: str
    text_color_pack_name: str

    def __init__(self, sound_pack_name: str, image_pack_name: str, text_color_pack_name: str):
        self.sound_pack_name = sound_pack_name
        self.image_pack_name = image_pack_name
        self.text_color_pack_name = text_color_pack_name
        self.init_packs()

    def init_packs(self):
        image_pack = ImagePack.ImagePack(self.image_pack_name)
        sound_pack = SoundPack.SoundPack(self.sound_pack_name)
        text_color_pack = TextColorPack.TextColorPack(self.text_color_pack_name)
