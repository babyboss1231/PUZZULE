#PythonGeeks - Import Modules
import random
import pygame
import sys

def main():
    global Frame_Speed_Clock, DIS_PlaySurf
    pygame.init()
    Frame_Speed_Clock = pygame.time.Clock()
    DIS_PlaySurf = pygame.display.set_mode((Window_Width, Window_Height))
 
    X_mouse  = 0 
    Y_mouse = 0 
    pygame.display.set_caption('Memory Game by PythonGeeks')
 
    Board = Randomized_Board()
    Boxes_revealed = GenerateData_RevealedBoxes(False)
 
    first_Selection = None  
    DIS_PlaySurf.fill(BackGround_color)
    Start_Game(Board)
 
    while True: 
        mouse_Clicked = False
 
        DIS_PlaySurf.fill(BackGround_color) 
        Draw_Board(Board, Boxes_revealed)
 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                X_mouse, Y_mouse = event.pos
            elif event.type == MOUSEBUTTONUP:
                X_mouse, Y_mouse = event.pos
                mouse_Clicked = True
 
        x_box, y_box = Box_Pixel(X_mouse, Y_mouse)
        if x_box != None and y_box != None:
            if not Boxes_revealed[x_box][y_box]:
                Draw_HighlightBox(x_box, y_box)
            if not Boxes_revealed[x_box][y_box] and mouse_Clicked:
                Reveal_Boxes_Animation(Board, [(x_box, y_box)])
                Boxes_revealed[x_box][y_box] = True 
                if first_Selection == None: 
                    first_Selection = (x_box, y_box)
                else:
                    icon1shape, icon1color = get_Shape_Color(Board, first_Selection[0], first_Selection[1])
                    icon2shape, icon2color = get_Shape_Color(Board, x_box, y_box)
 
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000) 
                        Cover_Boxes_Animation(Board, [(first_Selection[0], first_Selection[1]), (x_box, y_box)])
                        Boxes_revealed[first_Selection[0]][first_Selection[1]] = False
                        Boxes_revealed[x_box][y_box] = False
                    elif Won(Boxes_revealed): 
                        Game_Won(Board)
                        pygame.time.wait(2000)
 
                        Board = Randomized_Board()
                        Boxes_revealed = GenerateData_RevealedBoxes(False)
                        Draw_Board(Board, Boxes_revealed)
                        pygame.display.update()
                        pygame.time.wait(1000)
 
                        Start_Game (Board)
                    first_Selection = None 
        pygame.display.update()
        Frame_Speed_Clock.tick(Frame_Speed)

def GenerateData_RevealedBoxes(val):
    Boxes_revealed = []
    for i in range(Border_Width):
        Boxes_revealed.append([val] * Border_Height)
    return Boxes_revealed
def Randomized_Board():
    icon = []
    for color in All_Colors:
        for shape in All_Shapes:
            icon.append( (shape, color) )
 
    random.shuffle(icon) 
    num_IconsUsed = int(Border_Width * Border_Height / 2) 
    icon = icon[:num_IconsUsed] * 2 
    random.shuffle(icon)
 
    board = []
    for x in range(Border_Width):
        column = []
        for y in range(Border_Height):
            column.append(icon[0])
            del icon[0] 
        board.append(column)
    return board
def Split_Groups(group_Size, List):
    result = []
    for i in range(0, len(List), group_Size):
        result.append(List[i:i + group_Size])
    return result
def leftTop_Coord(x_box, y_box):
    left = x_box * (Box_Size + Gap_Size) + X_margin
    top = y_box * (Box_Size + Gap_Size) + Y_margin
    return (left, top)
 
def Box_Pixel(x, y):
    for x_box in range(Border_Width):
        for y_box in range(Border_Height):
            left, top = leftTop_Coord(x_box, y_box)
            box_Rect = pygame.Rect(left, top, Box_Size, Box_Size)
            if box_Rect.collidepoint(x, y):
                return (x_box, y_box)
    return (None, None)
def Draw_Icon(shape, color, x_box, y_box):
    quarter = int(Box_Size * 0.25) 
    half    = int(Box_Size * 0.5)  
 
    left, top = leftTop_Coord(x_box, y_box) 
 
    if shape == CIRCLE:
        pygame.draw.circle(DIS_PlaySurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DIS_PlaySurf, BackGround_color, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DIS_PlaySurf, color, (left + quarter, top + quarter, Box_Size - half, Box_Size - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DIS_PlaySurf, color, ((left + half, top), (left + Box_Size - 1, top + half), (left + half, top + Box_Size - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, Box_Size, 4):
            pygame.draw.line(DIS_PlaySurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(DIS_PlaySurf, color, (left + i, top + Box_Size - 1), (left + Box_Size - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DIS_PlaySurf, color, (left, top + quarter, Box_Size, half))
 
def get_Shape_Color(board, x_box, y_box):
    return board[x_box][y_box][0], board[x_box][y_box][1]
def Box_Cover(board, boxes, coverage):
    for box in boxes:
        left, top = leftTop_Coord(box[0], box[1])
        pygame.draw.rect(DIS_PlaySurf, BackGround_color, (left, top, Box_Size, Box_Size))
        shape, color = get_Shape_Color(board, box[0], box[1])
        Draw_Icon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DIS_PlaySurf, Box_Color, (left, top, coverage, Box_Size))
    pygame.display.update()
    Frame_Speed_Clock.tick(Frame_Speed
def Reveal_Boxes_Animation(board, boxesToReveal):
    for coverage in range(Box_Size, (-Speed_Reveal) - 1, -Speed_Reveal):
        Box_Cover(board, boxesToReveal, coverage)
 
def Cover_Boxes_Animation(board, boxesToCover):
    for coverage in range(0, Box_Size + Speed_Reveal, Speed_Reveal):
        Box_Cover(board, boxesToCover, coverage)
def Draw_Board(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for x_box in range(Border_Width):
        for y_box in range(Border_Height):
            left, top = leftTop_Coord(x_box, y_box)
            if not revealed[x_box][y_box]:                pygame.draw.rect(DIS_PlaySurf, Box_Color, (left, top, Box_Size, Box_Size))
            else:
                shape, color = get_Shape_Color(board, x_box, y_box)
                Draw_Icon(shape, color, x_box, y_box)
 
def Draw_HighlightBox(x_box, y_box):
    left, top = leftTop_Coord(x_box, y_box)
    pygame.draw.rect(DIS_PlaySurf, HighLight_Color, (left - 5, top - 5, Box_Size + 10, Box_Size + 10), 4)

def Start_Game(board):
    covered_Boxes = GenerateData_RevealedBoxes(False)
    boxes = []
    for x in range(Border_Width):
        for y in range(Border_Height):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    box_Groups = Split_Groups(8, boxes)
 
    Draw_Board(board, covered_Boxes)
    for boxGroup in box_Groups:
        Reveal_Boxes_Animation(board, boxGroup)
        Cover_Boxes_Animation(board, boxGroup)
    def Game_Won (board):
    coveredBoxes = GenerateData_RevealedBoxes(True)
    color_1 = Light_BackGround_color
    color_2 = BackGround_color
 
    for i in range(13):
        color_1, color_2 = color_2, color_1 
        DIS_PlaySurf.fill(color_1)
        Draw_Board(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
 
def Won(Boxes_revealed):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in Boxes_revealed:
        if False in i:
            return False 
    return True
Python Memory Puzzle Game – Create Flipping Tiles Game
by PythonGeeks Team

Boost Your Career with In-demand Skills - Start Now!

Memory Puzzle Game is the most popular best memory game or brain exercise. It helps in enhancing the concentration of the player and improves memory. Let’s build the Memory Puzzle Game in python.

Python Memory Puzzle Game Project Details
The player clicks on the tile to reveal the tile and when two identical tiles are revealed the effect goes up and score increases. To complete the game the user must reveal all pairs of shapes. After the game is completed, the number of moves needed to complete the game is also displayed on the screen.

Project Prerequisites
This project requires good knowledge of python and the pygame module. The Pygame module contains a graphics library which is used across many programming languages for building the Graphical user interface which is a GUI.

Download Python Memory Puzzle Game Code
Please download the source code of Python Memory Puzzle / Flipping Tiles Game from the following link: Python Memory Puzzle Game Code

Steps to Build a Python Memory Puzzle Game Project
Below are the step to develop python memory puzzle tile flipping game from scratch:

Import Modules
Creating main function
Creating Revealed box function
Creating a board
Splitting a list into lists
Create coordinate function
Converting to pixel coordinates to box coordinates
Draw icon and synthetic sugar
Drawing box cover
Revealing and covering animation
Drawing entire board and Highlight
Start the game animation
Creating function for game won
Rest of the code
Step 1- Importing Modules
#PythonGeeks - Import Modules
import random
import pygame
import sys
from pygame.locals import *
Code Explanation-
Random module – Random module is an in-built module of Python which is to generate random words from list[].
pygame – This module is used to create games. Consist of graphics and sound libraries.
sys – sys module provides functions used to manipulate different parts of the python runtime environment.
Step 2- Creating main function
def main():
    global Frame_Speed_Clock, DIS_PlaySurf
    pygame.init()
    Frame_Speed_Clock = pygame.time.Clock()
    DIS_PlaySurf = pygame.display.set_mode((Window_Width, Window_Height))
 
    X_mouse  = 0 
    Y_mouse = 0 
    pygame.display.set_caption('Memory Game by PythonGeeks')
 
    Board = Randomized_Board()
    Boxes_revealed = GenerateData_RevealedBoxes(False)
 
    first_Selection = None  
    DIS_PlaySurf.fill(BackGround_color)
    Start_Game(Board)
 
    while True: 
        mouse_Clicked = False
 
        DIS_PlaySurf.fill(BackGround_color) 
        Draw_Board(Board, Boxes_revealed)
 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                X_mouse, Y_mouse = event.pos
            elif event.type == MOUSEBUTTONUP:
                X_mouse, Y_mouse = event.pos
                mouse_Clicked = True
 
        x_box, y_box = Box_Pixel(X_mouse, Y_mouse)
        if x_box != None and y_box != None:
            if not Boxes_revealed[x_box][y_box]:
                Draw_HighlightBox(x_box, y_box)
            if not Boxes_revealed[x_box][y_box] and mouse_Clicked:
                Reveal_Boxes_Animation(Board, [(x_box, y_box)])
                Boxes_revealed[x_box][y_box] = True 
                if first_Selection == None: 
                    first_Selection = (x_box, y_box)
                else:
                    icon1shape, icon1color = get_Shape_Color(Board, first_Selection[0], first_Selection[1])
                    icon2shape, icon2color = get_Shape_Color(Board, x_box, y_box)
 
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000) 
                        Cover_Boxes_Animation(Board, [(first_Selection[0], first_Selection[1]), (x_box, y_box)])
                        Boxes_revealed[first_Selection[0]][first_Selection[1]] = False
                        Boxes_revealed[x_box][y_box] = False
                    elif Won(Boxes_revealed): 
                        Game_Won(Board)
                        pygame.time.wait(2000)
 
                        Board = Randomized_Board()
                        Boxes_revealed = GenerateData_RevealedBoxes(False)
                        Draw_Board(Board, Boxes_revealed)
                        pygame.display.update()
                        pygame.time.wait(1000)
 
                        Start_Game (Board)
                    first_Selection = None 
        pygame.display.update()
        Frame_Speed_Clock.tick(Frame_Speed)
Code Explanation-
main() – Function where the main part of the game belongs. Then declare global variables.
pygame.init – Initializing the pygame window.
X_mouse – Used to store x coordinates of mouse events.
Y_mouse – Used to store y coordinates of mouse events.
set.caption() – Setting title of the game window
board() – Stored the icons in it.
randomized _board() returns the structure representing the state of the board and GenerateData_RevealedBoxesreturns covered boxes.
first_Selection = It stores the (x, y) of the first box clicked.
.fill – For filling the background color.
Mouse_clicked – On the iteration of the while loop it will store the boolean value true or false.
Draw_Board – Draw the current state of board.
Here we are creating an event handling loop. It is inside the game loop that returns the objects by calling pygame_event_get(). For terminating the program we have to write the quit object. Otherwise there are two events mousemotion and mousebuttonup. In mousebuttonup event, mouse_clicked should be set to true.
Then we have created an if else condition in which we set the mouse currently on the box, box_reveal function will set the box as a reveal. Then check the match between the first selection and current box selection. If icons don’t match, re-cover up both the selections.
By calling won(Box_revealed) function checks if all pairs found. Then reset the board.
Reply the start game animation by calling start_Game() function.
At the end, redraw the screen and wait for the clock tick.
Step 3- Creating Revealed box function
def GenerateData_RevealedBoxes(val):
    Boxes_revealed = []
    for i in range(Border_Width):
        Boxes_revealed.append([val] * Border_Height)
    return Boxes_revealed
Code Explanation-
GenerateData_revealedBoxes() – Creating reveal box function that creates the list of boolean values and passes the val parameter to the function.
Boxes_revealed() – Creating empty list.
Here Inner list represents the columns of the board not the horizontal rows. And create a loop that will create columns and then append them to Boxes_revealed, it has val parameter and Border_height each.
Step 4- Creating a board
#PythonGeeks- Creating a board
 
def Randomized_Board():
    icon = []
    for color in All_Colors:
        for shape in All_Shapes:
            icon.append( (shape, color) )
 
    random.shuffle(icon) 
    num_IconsUsed = int(Border_Width * Border_Height / 2) 
    icon = icon[:num_IconsUsed] * 2 
    random.shuffle(icon)
 
    board = []
    for x in range(Border_Width):
        column = []
        for y in range(Border_Height):
            column.append(icon[0])
            del icon[0] 
        board.append(column)
    return board
Code Explanation-
Randomized_Board() – Function which has a list of tuples. Where tuples have two values, icon’s color and icon’s shape, we have to make sure that only and only two icons of each type.
Here we have created nested for loop which go through each and every possible shape and color.
random.shuffle() – It is useful to randomize the order of the icons list.
num_IconsUsed – It calculates how many icons are needed.
Now we are creating a board structure that will place icons randomly on the board. We have created a for loop, for every column on the board we have created a list of randomly selected icons. As we add icons in the column we will remove or delete the assigned icons from the list.
Step 5- Splitting a list into lists
#PythonGeeks- Splitting a list into lists
 
def Split_Groups(group_Size, List):
    result = []
    for i in range(0, len(List), group_Size):
        result.append(List[i:i + group_Size])
    return result
Code Explanation-
Here we are splitting the list of lists where the inner list has group size in it. Result is the empty list and we are creating for loop which contains range(0, 20, 8).
For the three iterations of the for loop this will give i variable values as 0,8,16.
Step 6- Create coordinate function
#PythonGeeks- Create coordinate function
 
def leftTop_Coord(x_box, y_box):
    left = x_box * (Box_Size + Gap_Size) + X_margin
    top = y_box * (Box_Size + Gap_Size) + Y_margin
    return (left, top)
Code Explanation-
leftTop_coord() – This function is useful to take box coordinates and returns pixel coordinates.
Step 7- Converting to pixel coordinates to box coordinates
#PythonGeeks- Converting to pixel coordinates to box coordinates
 
def Box_Pixel(x, y):
    for x_box in range(Border_Width):
        for y_box in range(Border_Height):
            left, top = leftTop_Coord(x_box, y_box)
            box_Rect = pygame.Rect(left, top, Box_Size, Box_Size)
            if box_Rect.collidepoint(x, y):
                return (x_box, y_box)
    return (None, None)
Code Explanation-
Box_pixel() – This function converts the pixel coordinates to box coordinates.
Rect – Rect object have a collidepoint method which passes x and y and returns true if the coordinate is inside the rect’s area object.
If collidepoint () returns True, we know that we have found a box that has been clicked on or moved on and will return the box coordinates. If no one returns true then the function will return (none,none).
Step 8- Draw icon and synthetic sugar
#PythonGeeks- Draw icon and synthetic sugar
 
def Draw_Icon(shape, color, x_box, y_box):
    quarter = int(Box_Size * 0.25) 
    half    = int(Box_Size * 0.5)  
 
    left, top = leftTop_Coord(x_box, y_box) 
 
    if shape == CIRCLE:
        pygame.draw.circle(DIS_PlaySurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DIS_PlaySurf, BackGround_color, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DIS_PlaySurf, color, (left + quarter, top + quarter, Box_Size - half, Box_Size - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DIS_PlaySurf, color, ((left + half, top), (left + Box_Size - 1, top + half), (left + half, top + Box_Size - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, Box_Size, 4):
            pygame.draw.line(DIS_PlaySurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(DIS_PlaySurf, color, (left + i, top + Box_Size - 1), (left + Box_Size - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DIS_PlaySurf, color, (left, top + quarter, Box_Size, half))
 
def get_Shape_Color(board, x_box, y_box):
    return board[x_box][y_box][0], board[x_box][y_box][1]
Code Explanation-
Draw_icon() – This function draws the icon using parameter shape color x_box and y_box.
The X and Y coordinates of the left and upper top edge of the box can be found by calling the function of the leftTopCoordsOfBox().
Using if else conditions draw the shape of icons circle, square, diamond, lines, oval etc using the pygame module tools.
Icon Shape value for x, y spot is stored in board[x][y][0]
Icon Color value for x, y spot is stored in board[x][y][1]
Step 9- Drawing box cover
#PythonGeeks- Drawing box cover
 
def Box_Cover(board, boxes, coverage):
    for box in boxes:
        left, top = leftTop_Coord(box[0], box[1])
        pygame.draw.rect(DIS_PlaySurf, BackGround_color, (left, top, Box_Size, Box_Size))
        shape, color = get_Shape_Color(board, box[0], box[1])
        Draw_Icon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DIS_PlaySurf, Box_Color, (left, top, coverage, Box_Size))
    pygame.display.update()
    Frame_Speed_Clock.tick(Frame_Speed)
Code Explanation-
Box_cover() – This function contains three parameters: board, boxes, coverage.
It Draws the boxes being covered/revealed. Boxes are the list of two items listed, which have the X and Y coordinate of the box.
leftTop_coord() – This function is useful to take box coordinates and returns pixel coordinates.
In the if condition it will only draw the cover if there is any coverage.
And then it will display the python memory game window.
Step 10- Revealing and covering animation
#PythonGeeks- Revealing and covering animation
def Reveal_Boxes_Animation(board, boxesToReveal):
    for coverage in range(Box_Size, (-Speed_Reveal) - 1, -Speed_Reveal):
        Box_Cover(board, boxesToReveal, coverage)
 
def Cover_Boxes_Animation(board, boxesToCover):
    for coverage in range(0, Box_Size + Speed_Reveal, Speed_Reveal):
        Box_Cover(board, boxesToCover, coverage)
Code Explanation-
Reveal_boxes_Animation() and Cover_Boxes_animation() are the functions for drawing an icon with varying amount of coverage by the white boxes. And using for loop we can do box reveal animation and box cover animation.
Step 11- Drawing entire board and Highlight
#PythonGeeks- Drawing entire board and Highlight
 
def Draw_Board(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for x_box in range(Border_Width):
        for y_box in range(Border_Height):
            left, top = leftTop_Coord(x_box, y_box)
            if not revealed[x_box][y_box]:                pygame.draw.rect(DIS_PlaySurf, Box_Color, (left, top, Box_Size, Box_Size))
            else:
                shape, color = get_Shape_Color(board, x_box, y_box)
                Draw_Icon(shape, color, x_box, y_box)
 
def Draw_HighlightBox(x_box, y_box):
    left, top = leftTop_Coord(x_box, y_box)
    pygame.draw.rect(DIS_PlaySurf, HighLight_Color, (left - 5, top - 5, Box_Size + 10, Box_Size + 10), 4)
Code Explanation-
Draw_board() – Draw the entire board and call draw_icon function for each box on board.
Here we write a nested for loop for X and Y coordinates of boxes, and will draw a white square or draw icons at the location.
When we hover over the particular box, a yellow outline appears outside the box using pygame.draw.rect function.
Step 12- Start the game animation
#PythonGeeks- Start the game animation
def Start_Game(board):
    covered_Boxes = GenerateData_RevealedBoxes(False)
    boxes = []
    for x in range(Border_Width):
        for y in range(Border_Height):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    box_Groups = Split_Groups(8, boxes)
 
    Draw_Board(board, covered_Boxes)
    for boxGroup in box_Groups:
        Reveal_Boxes_Animation(board, boxGroup)
        Cover_Boxes_Animation(board, boxGroup)
Code Explanation-
The animation will play at the start of the memory puzzle which gives the player a quick hint where the icons are located on the board.
Boxes variable created a list with possible spaces on the board and then nested for loop will add (X, Y) tuples to a list.
Randomly reveal the boxes 8 at a time by calling the function split_groups.
random.shuffle() – This function will randomly shuffle the order of the tuples in the boxes list and we will reveal and cover-up boxes 8 by 8.
Step 13- Creating function for game won
#PythonGeeks- Creating function for game won
 
def Game_Won (board):
    coveredBoxes = GenerateData_RevealedBoxes(True)
    color_1 = Light_BackGround_color
    color_2 = BackGround_color
 
    for i in range(13):
        color_1, color_2 = color_2, color_1 
        DIS_PlaySurf.fill(color_1)
        Draw_Board(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
 
def Won(Boxes_revealed):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in Boxes_revealed:
        if False in i:
            return False 
    return True
Code Explanation-
Once the player has unveiled all the boxes by matching all the pairs on the board, we want to congratulate them on lighting the background color.
The loop will draw a color contrast to the color1 of the background color and draw a board over it.
However, for each loop repetition, the values ​​in color1 and color2 will be replaced individually.
The player wins a game in which all the matching icons are matched. If even one false number is in the displayed boxes, then we know there are still incomparable icons on the board.
Returns True if all the boxes have been revealed, otherwise False
Step 14- Rest of code
Frame_Speed = 30 
Window_Width = 640 
Window_Height = 480
Speed_Reveal = 8 
Box_Size = 40 
Gap_Size = 10 
Border_Width = 10 
Border_Height = 7 
 
assert (Border_Width * Border_Height) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
X_margin = int((Window_Width - (Border_Width * (Box_Size + Gap_Size))) / 2)
Y_margin = int((Window_Height - (Border_Height * (Box_Size + Gap_Size))) / 2)
 
#            R    G    B
Gray     = (100, 100, 100)
Navyblue = ( 60,  60, 100)
White    = (255, 255, 255)
Red      = (255,   0,   0)
Green    = (  0, 255,   0)
Blue     = (  0,   0, 255)
Yellow   = (255, 255,   0)
Orange   = (255, 128,   0)
Purple   = (255,   0, 255)
Cyan     = (  0, 255, 255)
 
BackGround_color = Gray
Light_BackGround_color = Navyblue
Box_Color = Cyan
HighLight_Color = Yellow
 
CIRCLE = 'circle'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
 
All_Colors = (Red, Green, Blue, Yellow, Orange, Purple, Cyan)
All_Shapes = (CIRCLE, SQUARE, DIAMOND, LINES, OVAL)
assert len(All_Colors)* len(All_Shapes) * 2 >= Border_Width * Border_Height, "Board is too big for the number of shapes/colors defined.”
 
if __name__ == '__main__':
    main()