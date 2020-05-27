import json


class TextColorPack:
    text_color_pack_name: str
    text_color_dict: dict

    def __init__(self, text_color_pack_name: str):
        self.text_color_pack_name = text_color_pack_name
        self.create_text_color_dictionary()
        self.create_json_file()

    def create_text_color_dictionary(self):
        if self.text_color_pack_name == "dark":
            self.text_color_dict = {
                "start_screen_color": (0, 0, 255),  # blue
                "text_info_color": (255, 255, 255),  # white
                "rules_help_color": (255, 255, 255),  # white
            }
        elif self.text_color_pack_name == "meme":
            self.text_color_dict = {
                "start_screen_color": (255, 0, 255),  # blue
                "text_info_color": (255, 0, 0),  # black
                "rules_help_color": (255, 0, 255),  # black
            }
        else:
            # this is the default one
            self.text_color_dict = {
                "start_screen_color": (0, 0, 255),  # blue
                "text_info_color": (0, 0, 0),  # black
                "rules_help_color": (0, 0, 0),  # black
            }

    def create_json_file(self):
        # clear existing data
        open("text_color_pack.txt", "w").close()
        # write new data
        with open('text_color_pack.txt', 'w') as outfile:
            json.dump(self.text_color_dict, outfile)
