###########################################################
#  Computer Project #11
#
# Two Player Game
# The obejctive of the game is to get 5 pieces of one color in a row
# This can be horizontally, verticaly, diagonally
# Each player is assigned a color, either black or white 
# The board is 15x15 
#
###########################################################


class GoPiece(object):
    ''' 
    Represents the pieces used in the game
    '''
    def __init__(self,color = 'black'):
        ''' 
        Creates a piece
        gives it an attriubte named color
        the only colors are black and white
        '''
        self.__color = color #assigns the name color
        black_white = ('black', 'white') #list containing names
        if color not in black_white:
            raise MyError('Wrong color.')  #for colors other than black and white          
    
    def __str__(self):
        ''' 
        Displays the pieces as the black and white dot
        '''
        if self.__color == 'black':
            return ' ● '
        if self.__color == 'white':
            return ' ○ '
    
    def get_color(self):
        ''' 
        Returns the color of the piece as a string
        '''
        if self.__color == 'black':
            return 'black'
        if self.__color == 'white':
            return 'white'
            
class MyError(Exception):
    def __init__(self,value):
        self.__value = value
    def __str__(self):
        return self.__value

class Gomoku(object):
    ''' 
    Contains methods to set up, display, and play the game
    '''
    def __init__(self,board_size = 15,win_count = 5,current_player = 'black'):
        ''' 
        Checks that the value for the board size, if the player has won, and
        if the current player is using the right colors
        '''
        black_white = ('black', 'white')
        self.__board_size = board_size
        self.__win_count = win_count
        self.__current_player = current_player
        if type(board_size) is not int: #checks to see if the board size is an int
            raise ValueError
        if type(win_count) is not int: #checks to see if the player has reached 5 in a row
            raise ValueError
        if current_player not in black_white: #checks to see if the color of the player is black or white
            raise MyError("Wrong color.")
        self.__go_board = [ [ ' - ' for j in range(self.__board_size)] for i in range(self.__board_size)]
        
    def assign_piece(self,piece,row,col):
        ''' 
        Makes sure that the piece fits on the board
        '''
        self.__piece = piece
        self.__row = int(row)
        self.__col = int(col)
        if int(row) not in range(0, 16): #makes sure the rows are within 1-15
            raise MyError('Invalid position.')
        if int(col) not in range(0, 16): #makes sure the cols are within 1-15
            raise MyError('Invalid position.')    
        if self.__go_board[row-1][col-1] != " - ":#if the position doesnt have a dash in it it's full
            raise MyError('Position is occupied.')
        
        self.__go_board[row-1][col-1] = piece    
            
    def get_current_player(self):
        ''' 
        Returns the player as a string
        '''
        return self.__current_player
    
    def switch_current_player(self):
        ''' 
        Returns black if the white player has gone and vis versa
        '''
        if self.__current_player != 'black': #if the string doesnt equal black then return black
            self.__current_player = 'black'
        else: #if not return white
            self.__current_player = 'white'
            
    def __str__(self):
        s = '\n'
        for i,row in enumerate(self.__go_board):
            s += "{:>3d}|".format(i+1)
            for item in row:
                s += str(item)
            s += "\n"
        line = "___"*self.__board_size
        s += "    " + line + "\n"
        s += "    "
        for i in range(1,self.__board_size+1):
            s += "{:>3d}".format(i)
        s += "\n"
        s += 'Current player: ' + ('●' if self.__current_player == 'black' else '○')
        return s
        
    def current_player_is_winner(self):
        ''' 
        Returns true if the player has reached 5 in a row
        Returns false if the player does not reach 5 in a row
        '''
    
        for col in range(0, self.__board_size - self.__win_count + 1): #horizontal 
            for row in range(0, self.__board_size):
                horizontal = 0
                for k in range(0, self.__win_count): #iterates through the range to wincount
                    try:
                        if self.__go_board[row][col + k].get_color() == self.__current_player: #if the point belongs to the player
                            horizontal += 1
                            if horizontal == 5: #if they've reached 5 in a row horizontally
                                return True
                    except:
                        if self.__go_board[row][col + k] != " - ":
                            return False
                
        for row in range(0, self.__board_size - self.__win_count + 1): #vertical count
            for col in range(0, self.__board_size):
                vertical = 0
                for k in range(0, self.__win_count): #iterates through the range to wincount
                    try:
                        if self.__go_board[row + k][col].get_color() == self.__current_player: #if the point belongs to the player
                            vertical += 1
                            if vertical == 5: #if they've reached 5 in a row vertically
                                return True
                    except:
                        if self.__go_board[row + k][col] != " - ":
                            return False
                            
        for row in range(0, self.__board_size - self.__win_count + 1): #DL count
            for col in range(0, self.__board_size - self.__win_count + 1):
                DL = 0
                for k in range(0, self.__win_count): #iterates through the range to wincount
                    if self.__go_board[row + k][col + k] != " - ":
                        if self.__go_board[row + k][col + k].get_color() == self.__current_player: #if the point belongs to the player
                            DL += 1
                            if DL == 5: #if they've reached 5 in a row diagonally
                                return True
                            
        for row in range(0, self.__board_size - self.__win_count + 1): #DR count
            for col in range(self.__win_count - 1, self.__board_size - self.__win_count + 1):
                DR = 0
                for k in range(0, self.__win_count):
                    if self.__go_board[row + k][col - k] != " - ":
                        if self.__go_board[row + k][col - k].get_color() == self.__current_player: #if the point belongs to the player
                            DR += 1
                            if DR == 5: #if they've reached 5 in a row diagonially
                                return True   
        return False                     
#	steps:
#	1. pick an x, y position
#	2. set a loop k=0, win_count
#	3. check the point (x +k, y) h
#			          (x, y+k) v
#			          (x+k, y+k) dL
#			          (x+k, y-k) dR
#					This one is more difficult because you are subtracting, can’t start at
#                        zero you’d have to start at the win_count
                                
#4 checks
#	- (h) horizontal
#	- (v) vertical
#	- (dL) diagonal left-right
#	- (dR) diagonal right-left
        
        
def main():
    
    board = Gomoku()
    print(board)
    play = input("Input a row then column separated by a comma (q to quit): ")
    while play.lower() != 'q': #if it doesnt want to quit
        play_list = play.strip().split(',') #splits at the comma to isolate the row and col
        try: 
            piece = GoPiece(board.get_current_player())
            if len(play_list) != 2: #if there isnt 2 items in the input
                raise MyError("Incorrect input.")
            if play_list[0].strip("-").isdigit() != True: #need the strip for negative values
                raise MyError("Incorrect input.")
            if play_list[1].strip("-").isdigit() != True: #need the strip for negative values
                raise MyError("Incorrect input.")

            play_list[0] = int(play_list[0]) #assigns the row
            play_list[1] = int(play_list[1]) #assigns the col
            board.assign_piece(piece, play_list[0], play_list[1])
            if board.current_player_is_winner() == True:
                print(board)
                print("{} Wins!".format(board.get_current_player()))
                break
            else:
                board.switch_current_player() #needed to switch players


        except MyError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))
        print(board)
        play = input("Input a row then column separated by a comma (q to quit): ")

if __name__ == '__main__':
    main()
