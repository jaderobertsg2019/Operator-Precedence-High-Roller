import json
import datetime
class JsonHandle:
    def __init__(self, playername: str):
        self.playername = playername
        try:
            with open('player_info.json', 'r') as openfile: self.player_info_object = json.load(openfile)
            self.add_player_if_unique()
        except:
            newfile = {"players": []}
            with open("player_info.json", "w") as json_file:
                json.dump(newfile, json_file)

    #check_figglebucks
    #subtract_figglebucks

    def check_figglebucks(self, point_requirement):
        index = self.calc_index()
        try:
            return self.player_info_object["players"][index]["figglebucks"]
        except:
            self.player_info_object["players"][index]["figglebucks"] = point_requirement
            json_object = json.dumps(self.player_info_object, indent=2)
            with open("player_info.json", "w") as outfile: outfile.write(json_object)
            return self.player_info_object["players"][index]["figglebucks"]
        
    def update_figglebucks(self, update_val):
        index = self.calc_index()
        self.player_info_object["players"][index]["figglebucks"] = int(self.player_info_object["players"][index]["figglebucks"]) + update_val
        json_object = json.dumps(self.player_info_object, indent=2)
        with open("player_info.json", "w") as outfile: outfile.write(json_object)

    def add_player_if_unique(self):
        unique = True
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i]["username"] == self.playername:
                unique = False
        if unique:
            self.player_info_object["players"].append({"username": self.playername, "gambling": "False"})
            json_object = json.dumps(self.player_info_object, indent=2) 
            with open("player_info.json", "w") as outfile: outfile.write(json_object)
        pass

    def add_roll(self, die: str, roll: int, timestamp: datetime.datetime):
        index = self.calc_index()
        try:
            self.player_info_object["players"][index]["rolls"].append({
            "die": die, 
            "roll": roll,
            "timestamp": timestamp
            })
        except:
            self.player_info_object["players"][index]["rolls"] = [{
            "die": die, 
            "roll": roll,
            "timestamp": timestamp
            }]
        json_object = json.dumps(self.player_info_object, indent=2) 
        with open("player_info.json", "w") as outfile: outfile.write(json_object)

    def calc_index(self):
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i]["username"] == self.playername: 
                return i
        else: return None

    def gambling(self):
        index = self.calc_index()
        return self.player_info_object["players"][index]["gambling"] == "True"

    def update_json_gambling(self, gambling: bool):
        index = self.calc_index()
        if (gambling != None):
            self.player_info_object["players"][index]["gambling"] = str(gambling)
        json_object = json.dumps(self.player_info_object, indent=2)
        with open("player_info.json", "w") as outfile: outfile.write(json_object)

    def get_rolls(self):
        index = self.calc_index()
        try:
            return self.player_info_object["players"][index]["rolls"]
        except:
            return None