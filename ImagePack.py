import json
import os.path

'''
images need to be stored in a folder named like the image pack that they are using
if a certain image does not exist in that folder, the default image will be used 
'''


class ImagePack:
    image_pack_name: str
    image_dictionary: dict
    directory_name: str

    def __init__(self, image_pack_name: str):
        self.image_pack_name = image_pack_name
        self.create_image_dictionary()
        self.check_if_images_exist()
        self.create_json_file()

    # Pawn_1, Pawn_2, ... need to be provided as images in the respective player's color
    def create_image_dictionary(self):
        if self.image_pack_name == "default":
            self.directory_name = "default"
        elif self.image_pack_name == "test":
            self.directory_name = "test"
        # if nothing applies set it to default
        else:
            self.directory_name = "default"

        self.image_dictionary = {
            "pawn_player_1": 'images/' + self.directory_name + '/PawnPlayer1.png',
            "pawn_player_2": 'images/' + self.directory_name + '/PawnPlayer2.png',
            "pawn_player_3": 'images/' + self.directory_name + '/PawnPlayer3.png',
            "pawn_player_4": 'images/' + self.directory_name + '/PawnPlayer4.png',
            "background_image_game": 'images/' + self.directory_name + '/GameField.jpg',
            "background_image_start_screen": 'images/' + self.directory_name + '/StartScreen.jpg',
            "start_button": 'images/' + self.directory_name + '/StartButton.png',
            "maedn_logo": 'images/' + self.directory_name + '/MaednLogo.png',
            "ingame_rules_button": 'images/' + self.directory_name + '/RulesButtonIngame.png',
            "ingame_help_button": 'images/' + self.directory_name + '/HelpButtonIngame.png',
            "help_image_1": 'images/' + self.directory_name + '/HelpImage1.png',
            "rules_image_1": 'images/' + self.directory_name + '/RulesImage1.png',
            "back_arrow_image": 'images/' + self.directory_name + '/BackArrow.png',
            "player_arrow_up": 'images/' + self.directory_name + '/PlayerArrowUp.png',
            "player_arrow_down": 'images/' + self.directory_name + '/PlayerArrowDown.png',
            "dice_image_1": 'images/' + self.directory_name + '/Dice1.png',
            "dice_image_2": 'images/' + self.directory_name + '/Dice2.png',
            "dice_image_3": 'images/' + self.directory_name + '/Dice3.png',
            "dice_image_4": 'images/' + self.directory_name + '/Dice4.png',
            "dice_image_5": 'images/' + self.directory_name + '/Dice5.png',
            "dice_image_6": 'images/' + self.directory_name + '/Dice6.png',
            }

    def check_if_images_exist(self):
        for key in self.image_dictionary:
            image_path = self.image_dictionary[key]
            if os.path.exists(image_path):
                pass
            else:
                # if the image doesn't exist use the default image
                self.set_to_default_image(key)

    def set_to_default_image(self, key: str):
        split = self.image_dictionary[key].split("/")
        image_name = split[-1]
        self.image_dictionary[key] = "images/default/" + image_name

    def create_json_file(self):
        # clear existing data
        open("image_pack.txt", "w").close()
        # write new data
        with open('image_pack.txt', 'w') as outfile:
            json.dump(self.image_dictionary, outfile)

