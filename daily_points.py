import schedule, time, json

def add_points():
    with open('player_info.json', 'r') as openfile: player_info_object = json.load(openfile)
    for index in range(len(player_info_object["players"])):
        try:
            player_info_object["players"][index]["figglebucks"] = int(player_info_object["players"][index]["figglebucks"]) + 5
        except:
            pass
    json_object = json.dumps(player_info_object, indent=2)
    with open("player_info.json", "w") as outfile: outfile.write(json_object)


schedule.every().day.at("00:00").do(add_points)
while True:
    schedule.run_pending()
    time.sleep(1)