import os

# gets width/height, is stored in width_height.txt
os.system("python get_width_height.py")
# gets bomb count, is stored in bomb_count.txt
os.system("python get_bomb_count.py")
# obtains width/height from txt file
with open('width_height.txt', 'r') as f:
    str_width_height = f.read()
    width_height = int(str_width_height)
    f.close()
# obtains bomb count from txt file
with open('bomb_count.txt', 'r') as f:
    str_bomb_count = f.read()
    bomb_count = int(str_width_height)
    f.close()
# AI plays the game until stopped
while True:
    # gets current state of the game, placed in json file
    os.system("python get_all_cells.py")
    # AI gets what tile to click next, placed in result.txt
    os.system(f"python evaluator.py test {width_height} {bomb_count}")
    # gets result from txt file
    with open('result.txt', 'r') as f:
        str_result = f.read()
        str_results = str_result.split(",")
        inst1 = int(str_results[0])
        inst2 = int(str_results[1])
        f.close()
    # then clicks the calculated tile
    os.system(f"python click_cell.py --x {inst2} --y {width_height - 1 - inst1}")
    # checks if the game is over or not, placed in game_active.txt
    os.system("python get_game_state.py")
    # gets if game is over from txt file
    with open('game_active.txt', 'r') as f:
        str_game_active = f.read()
        print(str_game_active)
        if str_game_active == "true":
            game_active = True
        else:
            game_active = False
        f.close()
    # restarts the game if game is over
    if game_active:
        os.system("python restart.py")


        