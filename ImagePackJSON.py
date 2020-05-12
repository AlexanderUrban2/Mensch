import json
'''
Vorlage für weitere dictionaryies:
self.image_dictionary = {
    "pawn_image_path": ,
    "background_image_path": ,
    "background_image_start_screen_path": ,
    "back_arrow_image_path": ,
    "start_button_path": ,
    "maedn_logo_path": ,
    "ingame_rules_button_path": ,
    "ingame_help_button_path": ,
    "help_image_1_path": ,
    "rules_image_1_path": ,
    "player_arrow_up_path": ,
    "player_arrow_dow_path": ,
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
                "pawn_image_path": 'images/Pawn_.png',
                "background_image_str": 'images/GameField.jpg',
                "background_image_start_screen_str": 'images/StartScreen.jpg',
                "back_arrow_image_path": 'images/BackArrow.png',
                "start_button_path": 'images/StartButton.png',
                "maedn_logo_path": 'images/MaednLogo.png',
                "ingame_rules_button_path": 'images/RulesButtonIngame.png',
                "ingame_help_button_path": 'images/HelpButtonIngame.png',
                "help_image_1_path": 'images/HelpImage1.png',
                "rules_image_1_path": 'images/RulesImage1.png',
                "player_arrow_up_path": 'images/PlayerArrowUp.png',
                "player_arrow_dow_path": 'images/PlayerArrowDown.png',
            }
        # if nothing applies set it to default
        else:
            self.image_dictionary = {
                "pawn_image_path": 'images/Pawn_.png',
                "background_image_str": 'images/GameField.jpg',
                "background_image_start_screen_str": 'images/StartScreen.jpg',
                "back_arrow_image_path": 'images/BackArrow.png',
                "start_button_path": 'images/StartButton.png',
                "maedn_logo_path": 'images/MaednLogo.png',
                "ingame_rules_button_path": 'images/RulesButtonIngame.png',
                "ingame_help_button_path": 'images/HelpButtonIngame.png',
                "help_image_1_path": 'images/HelpImage1.png',
                "rules_image_1_path": 'images/RulesImage1.png',
                "player_arrow_up_path": 'images/PlayerArrowUp.png',
                "player_arrow_dow_path": 'images/PlayerArrowDown.png',
            }

    def create_json_file(self):
        # clear existing data
        open("image_pack.txt", "w").close()
        with open('image_pack.txt', 'w') as outfile:
            json.dump(self.image_dictionary, outfile)

