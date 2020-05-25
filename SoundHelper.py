import pygame.mixer
import json


class SoundHelper:
    channel: pygame.mixer.Channel
    data: json

    def __init__(self):
        self.init_channel()
        with open('sound_pack.txt') as json_file:
            self.data = json.load(json_file)

    def init_channel(self):
        channel_number = pygame.mixer.find_channel()
        self.channel = pygame.mixer.Channel(channel_number)

    # for all possible sound names take a look at SoundPack.py
    def play_sound(self, sound_name: str):
        sound = pygame.mixer.Sound(self.data[sound_name])
        self.channel.play(sound)

    def stop_channel(self):
        self.channel.stop()
