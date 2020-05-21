import json
import os.path
import pygame.mixer

'''
sound files need to be stored in a folder named like the theme pack that they are using
if a certain sound file does not exist in that folder, the default sound will be used 
all sound files are .wav
'''


class SoundPack:
    sound_pack_name: str
    directory_name: str
    sound_dictionary: dict

    def __init__(self, sound_pack_name: str):
        self.sound_pack_name = sound_pack_name
        self.create_sound_dictionary()
        self.check_if_sound_files_exist()
        self.create_json_file()

        pygame.mixer.init()
        self.start_music()

    def create_sound_dictionary(self):
        if self.sound_pack_name == "default":
            self.directory_name = "default"
        elif self.sound_pack_name == "test":
            self.directory_name = "test"
        elif self.sound_pack_name == "dark":
            self.directory_name = "dark"
        elif self.sound_pack_name == "heart":
            self.directory_name = "heart"
        # if nothing applies set it to default
        else:
            self.directory_name = "default"

        self.sound_dictionary = {
            "background_music": 'music/' + self.directory_name + '/background_music.wav',
            "hit_enemy_pawn_sound": 'music/' + self.directory_name + '/hit_enemy_pawn_sound.wav',
            "hit_own_pawn_sound": 'music/' + self.directory_name + '/hit_own_pawn_sound.wav',
            "unfortunate_sound": 'music/' + self.directory_name + '/unfortunate_sound.wav',
            "victory_sound": 'music/' + self.directory_name + '/victory_sound.wav',
        }

    def check_if_sound_files_exist(self):
        for key in self.sound_dictionary:
            sound_path = self.sound_dictionary[key]
            if os.path.exists(sound_path):
                pass
            else:
                # if the image doesn't exist use the default image
                self.set_to_default_sound(key)

    def set_to_default_sound(self, key: str):
        split = self.sound_dictionary[key].split("/")
        # get the file name
        sound_name = split[-1]
        self.sound_dictionary[key] = "images/default/" + sound_name

    def create_json_file(self):
        # clear existing data
        open("sound_pack.txt", "w").close()
        # write new data
        with open('sound_pack.txt', 'w') as outfile:
            json.dump(self.sound_dictionary, outfile)

    def start_music(self):
        with open('sound_pack.txt') as json_file:
            data = json.load(json_file)
        pygame.mixer.music.load(data["background_music"])
        pygame.mixer.music.play(-1)
        # music is fucking loud
        pygame.mixer.music.set_volume(.03)
