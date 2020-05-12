import json
'''
template for further image packs:

self.image_dictionary = {
    "pawn_image": ,
    "background_image_game": ,
    "background_image_start_screen": ,
    "start_button": ,
    "maedn_logo": ,
    "ingame_rules_button": ,
    "ingame_help_button": ,
    "help_image_1": ,
    "rules_image_1": ,
    "back_arrow_image": ,
    "player_arrow_up": ,
    "player_arrow_down": ,
}
'''


class ImagePackJSON:
    image_pack_name: str
    image_dictionary: dict

    def __init__(self, image_pack_name: str):
        self.image_pack_name = image_pack_name
        self.create_image_dictionary()
        self.create_json_file()

    # Pawn_1, Pawn_2, ... need to be provided as images in the respective player's color
    def create_image_dictionary(self):
        if self.image_pack_name == "default":
            self.image_dictionary = {
                "pawn_image": 'images/Pawn_.png',
                "background_image_game": 'images/GameField.jpg',
                "background_image_start_screen": 'images/StartScreen.jpg',
                "start_button": 'images/StartButton.png',
                "maedn_logo": 'images/MaednLogo.png',
                "ingame_rules_button": 'images/RulesButtonIngame.png',
                "ingame_help_button": 'images/HelpButtonIngame.png',
                "help_image_1": 'images/HelpImage1.png',
                "rules_image_1": 'images/RulesImage1.png',
                "back_arrow_image": 'images/BackArrow.png',
                "player_arrow_up": 'images/PlayerArrowUp.png',
                "player_arrow_down": 'images/PlayerArrowDown.png',
            }
        # if nothing applies set it to default
        else:
            self.image_dictionary = {
                "pawn_image": 'images/Pawn_.png',
                "background_image_game": 'images/GameField.jpg',
                "background_image_start_screen": 'images/StartScreen.jpg',
                "start_button": 'images/StartButton.png',
                "maedn_logo": 'images/MaednLogo.png',
                "ingame_rules_button": 'images/RulesButtonIngame.png',
                "ingame_help_button": 'images/HelpButtonIngame.png',
                "help_image_1": 'images/HelpImage1.png',
                "rules_image_1": 'images/RulesImage1.png',
                "back_arrow_image": 'images/BackArrow.png',
                "player_arrow_up": 'images/PlayerArrowUp.png',
                "player_arrow_down": 'images/PlayerArrowDown.png',
            }

    def create_json_file(self):
        # clear existing data
        open("image_pack.txt", "w").close()
        with open('image_pack.txt', 'w') as outfile:
            json.dump(self.image_dictionary, outfile)

