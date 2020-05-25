import pygame.mixer
import json


class SoundHelper:
    channel: pygame.mixer.Channel
    data: json
    paused: bool

    def __init__(self):
        self.paused = False
        self.init_channel()
        with open('sound_pack.txt') as json_file:
            self.data = json.load(json_file)

    def init_channel(self):
        self.channel = pygame.mixer.find_channel()

    # for all possible sound names take a look at SoundPack.py
    def play_sound(self, sound_name: str):
        if not self.paused:
            sound = pygame.mixer.Sound(self.data[sound_name])
            self.channel.play(sound)

    # is needed because channel.pause() and channel.stop() do not work....
    def stop_channel(self):
        self.paused = True

    def resume_channel(self):
        self.paused = False
