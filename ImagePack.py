import json
import os.path

'''
images need to be stored in a folder named like the image pack that they are using
if a certain image does not exist in that folder, the default image will be used 
all images are .png
'''


class ImagePack:
    image_pack_name: str
    image_dictionary: dict
    directory_name: str

    """
                desc: 
                    - init
                param:
                    - image_pack_name: str -> name of the image pack; gets used to identifiy the location 
                                              of the directory in which the images are stored
                                              each directory (meme, dark, default) stores images of its theme
                return:
                    - none
    """
    def __init__(self, image_pack_name: str):
        self.image_pack_name = image_pack_name
        self.create_image_dictionary()
        self.check_if_images_exist()
        self.create_json_file()

    """
                desc: 
                    - create the image dictionary which contains the file paths to all images used in the project
                param:
                    - none
                return:
                    - none
    """
    # Pawn_1, Pawn_2, ... need to be provided as images in the respective player's color
    def create_image_dictionary(self):
        if os.path.exists('images/' + self.image_pack_name):
            self.directory_name = self.image_pack_name
        # if the path doesn't exist set it to default
        else:
            self.directory_name = "default"

        self.image_dictionary = {
            "pawn_player_1": 'images/' + self.directory_name + '/PawnPlayer1.png',
            "pawn_player_2": 'images/' + self.directory_name + '/PawnPlayer2.png',
            "pawn_player_3": 'images/' + self.directory_name + '/PawnPlayer3.png',
            "pawn_player_4": 'images/' + self.directory_name + '/PawnPlayer4.png',

            "sound_on_button": 'images/' + self.directory_name + '/SoundButtonOn.png',
            "sound_off_button": 'images/' + self.directory_name + '/SoundButtonOff.png',

            "theme_image": 'images/' + self.directory_name + '/Theme.png',

            "background_image_game": 'images/' + self.directory_name + '/GameField.png',
            "background_image_start_screen": 'images/' + self.directory_name + '/StartScreen.png',
            "start_button": 'images/' + self.directory_name + '/StartButton.png',
            "maedn_logo": 'images/' + self.directory_name + '/MaednLogo.png',
            "rules_help_background":'images/' + self.directory_name + '/RulesHelpBG.png',

            "ingame_rules_button": 'images/' + self.directory_name + '/RulesButtonIngame.png',
            "ingame_help_button": 'images/' + self.directory_name + '/HelpButtonIngame.png',
            "help_image_1": 'images/' + self.directory_name + '/HelpImage1.png',
            "rules_image_1": 'images/' + self.directory_name + '/RulesImage1.png',

            "back_arrow_image": 'images/' + self.directory_name + '/BackArrow.png',
            "player_arrow_up": 'images/' + self.directory_name + '/PlayerArrowUp.png',
            "player_arrow_down": 'images/' + self.directory_name + '/PlayerArrowDown.png',

            "theme_arrow_right": 'images/' + self.directory_name + '/ThemeArrowRight.png',
            "theme_arrow_left": 'images/' + self.directory_name + '/ThemeArrowLeft.png',

            "dice_image_1": 'images/' + self.directory_name + '/Dice1.png',
            "dice_image_2": 'images/' + self.directory_name + '/Dice2.png',
            "dice_image_3": 'images/' + self.directory_name + '/Dice3.png',
            "dice_image_4": 'images/' + self.directory_name + '/Dice4.png',
            "dice_image_5": 'images/' + self.directory_name + '/Dice5.png',
            "dice_image_6": 'images/' + self.directory_name + '/Dice6.png',

            "victory_image": 'images/' + self.directory_name + '/VictoryImage.png',
            "continue_button_victory": 'images/' + self.directory_name + '/ContinueButtonVictory.png',
            }

    def check_if_images_exist(self):
        for key in self.image_dictionary:
            image_path = self.image_dictionary[key]
            # check if the path stored for the current key exists
            if os.path.exists(image_path):
                pass
            else:
                # if the image doesn't exist use the default image
                self.set_to_default_image(key)

    def set_to_default_image(self, key: str):
        split = self.image_dictionary[key].split("/")
        # get the image name, which is the last part of the path
        image_name = split[-1]
        # set the image to the default one
        self.image_dictionary[key] = "images/default/" + image_name

    def create_json_file(self):
        # clear existing data
        open("image_pack.txt", "w").close()
        # write new data
        with open('image_pack.txt', 'w') as outfile:
            json.dump(self.image_dictionary, outfile)

