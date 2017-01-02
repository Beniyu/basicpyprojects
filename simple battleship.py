import random

#Game User Preparation
def int_create(string):
    number_as_list=[x for x in string if x.isdigit()]
    if number_as_list==[]:
        number_as_list=["0"]
    return int("".join(number_as_list))

#player_amount=int_create(input("1/2 player? "))
#while player_amount!=1 and player_amount!=2:
#    player_amount=int_create(input("1/2 player? "))
player_amount=1
settings={"l1amount":6,"l2amount":4,"l3amount":2,"rang":8}
#settingnames{"l1amount":"Amount of 1-length ships",
#    "l2amount":"Amount of 2-length ships",
#    "l3amount":"Amount of 3-length ships",
#    "rang":"Size of map"}
ship_dict=[]

print("1 - Play\n2 - Settings")
choice=0
while choice!=1 and choice!=2:
    choice=int_create(input(""))
if choice==2:
    while True:
        for setting in settings:
            print("{} - {}".format(setting,settings[setting]))
        print("To change a setting, type it in and type the new variable.")
        print("To finish changing settings, type in 'end'")
        change=input("")
        if change=="end":
            break
        else:
            for setting in settings:
                if setting==change:
                    settings[setting]=int_create(input("Enter the new setting: "))
                
#Game Preparation
def show_board(board):
    for row in board:
        print(" ".join(row))

def test_coord(coord):
    x,y=coord
    if x not in range(settings["rang"]) or y not in range(settings["rang"]):
        return False
    elif real_board[y][x]=="X":
        return False
    else:
        return True

def random_coord():
    x,y=-1,-1
    while test_coord([x,y])==False:
        x=random.randint(0,settings["rang"]-1)
        y=random.randint(0,settings["rang"]-1)
    return x,y
    
def random_direction():
    return random.randint(0,3)
    
def ship_extension(x,y,direction,magnitude):
    if direction==0:
        return x+magnitude,y
    if direction==1:
        return x,y+magnitude
    if direction==2:
        return x-magnitude,y
    if direction==3:
        return x,y-magnitude

def bulk_test_coord(x,y):
    if not len(x)==len(y):
        print("Error within the program.")
    else:
        for coord in range(len(x)):
            if test_coord([x[coord],y[coord]])==False:
                return False
                break
        else:
            return True

def plot_points(x,y,designation):
    if not len(x)==len(y):
        print("Error within the program.")
    else:
        for point_number in range(len(x)):
            real_board[y[point_number]][x[point_number]]=designation

def plot_points2(coords):
    for coord in coords:
        x,y=coord
        board[y][x]="/"

def create_fake_coord_list(amount):
    x=[]
    y=[]
    for coord in range(amount):
        x.append(-1)
        y.append(-1)
    return x,y

def create_coord_list(x,y):
    if not len(x)==len(y):
        print("Error within the program.")
    else:
        coords=[]
        for coord in range(len(x)):
            coords.append([x[coord],y[coord]])
        return coords

board=[]
real_board=[]

for row in range(settings["rang"]):
    board.append(['O']*settings["rang"])
    real_board.append(['O']*settings["rang"])    

if player_amount==1:
    for l1battleship in range(settings["l1amount"]):
        x,y=random_coord()
        ship_dict.append({"condition":"alive","size":1,"coords":[[x,y]]})
        real_board[y][x]="X"

    for l2battleship in range(settings["l2amount"]):
        x,y=create_fake_coord_list(2)
        while bulk_test_coord(x,y)==False:
            x[0],y[0]=random_coord()
            direction=random_direction()
            x[1],y[1]=ship_extension(x[0],y[0],direction,1)
        ship_dict.append({"condition":"alive","size":2,"coords":create_coord_list(x,y)})
        plot_points(x,y,"X")

    for l3battleship in range(settings["l3amount"]):
        x,y=create_fake_coord_list(3)
        while bulk_test_coord(x,y)==False:
            x[0],y[0]=random_coord()
            direction=random_direction()
            x[1],y[1]=ship_extension(x[0],y[0],direction,1)
            x[2],y[2]=ship_extension(x[0],y[0],direction,2)
        ship_dict.append({"condition":"alive","size":3,"coords":create_coord_list(x,y)})
        plot_points(x,y,"X")

#Game Start
def guess(variable,rang):
    coord=int_create(input("Which {}: ".format(variable)))-1
    while coord not in range(rang):
        coord=int_create(input("Invalid number, must be within the range of 1 and {}: ".format(rang)))-1
    return coord
    
def win_check(real_board):
    win=True
    for row in real_board:
        for col in row:
            if col=="X":
                win=False
    return win
    
def ship_check(real_board,ship_dict):
    for ship in ship_dict:
        if ship['condition']=="alive":
            for coord in range(len(ship["coords"])):
                x,y=ship["coords"][coord]
                if real_board[y][x]=="X":
                    break
            else:
                ship['condition']='dead'
                plot_points2(ship["coords"])
                print("You sank a battleship!")
        
turn_counter=0
while True:
    turn_counter+=1
    show_board(board)
    row_guess,col_guess=guess("row",settings["rang"]),guess("column",settings["rang"])
    while board[row_guess][col_guess]=="\\" or board[row_guess][col_guess]=="X" or board[row_guess][col_guess]=="/":
        print("You've already tried this spot.")
        row_guess,col_guess=guess("row",settings["rang"]),guess("column",settings["rang"])
    if real_board[row_guess][col_guess]=="X":
        board[row_guess][col_guess]="\\"
        real_board[row_guess][col_guess]="Y"
        print("You've hit a battleship")
        ship_check(real_board,ship_dict)
        if win_check(real_board)==True:
            break
    else:
        board[row_guess][col_guess]="X"
        print("You missed.")
print("Congratulations, you won!")
print("Your victory took {} turns.".format(turn_counter))
    
    
    
    
