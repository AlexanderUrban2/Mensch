import pygame.mixer
import json


class SoundHelper:
    channel: pygame.mixer.Channel
    data: json
    paused: bool

    def __init__(self):
        # used because channel.pause() and channel.stop() don't seem to work
        self.paused = False
        self.init_channel()
        with open('sound_pack.txt') as json_file:
            self.data = json.load(json_file)

    # find an unused channel and use it for playing the sound effects
    def init_channel(self):
        self.channel = pygame.mixer.find_channel()

    # for all possible sound names take a look at SoundPack.py
    def play_sound(self, sound_name: str):
        # only play a sound if the channel is not paused
        if not self.paused:
            sound = pygame.mixer.Sound(self.data[sound_name])
            self.channel.play(sound)

    # is needed because channel.pause() and channel.stop() do not work....
    def stop_channel(self):
        self.paused = True

    def resume_channel(self):
        self.paused = False

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def play_background_music(self):
        pygame.mixer.music.load(self.data["background_music"])
        # play the music in an infinite loop
        pygame.mixer.music.play(-1)
