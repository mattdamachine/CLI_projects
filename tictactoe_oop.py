# tictactoe_oop.py, an object-oriented tic tac toe game.
import copy

ALL_SPACES = list('123456789')  # Keys for a TTT board
X, O, BLANK = 'X', 'O', ' '  # Constants for string values

def main():
    ''' Runs a game of tic-tac-toe. '''
    print('Welcome to tic-tac-toe!')
    # Create a TTT board object. 
    if input("Use hint board? (y/n): ").lower().startswith('y'):
        gameBoard = HintBoard()
    else:
        gameBoard = TTTBoard()  
    currentPlayer, nextPlayer = X, O  # X Goes first, 0 goes next.

    while True:
        print(gameBoard.getBoardStr())  # Display board on the screen

        # Keep asking the player until they enter a number 1-9:
        move = None
        while not gameBoard.isValidSpace(move):
            move = input(f'What is {currentPlayer}\'s move (1-9)? ')
        gameBoard.updateBoard(move, currentPlayer)  # Make the move

        # Check if the game is over:
        if gameBoard.isWinner(currentPlayer):  # Check for victory
            print(gameBoard.getBoardStr())
            print(currentPlayer + ' has won the game!')
            break
        elif gameBoard.isBoardFull():  # Check for a tie
            print(gameBoard.getBoardStr())
            print('It\'s a tie!')
            break
        currentPlayer, nextPlayer = nextPlayer, currentPlayer  # Swap turns
	
    print('Thanks for playing!')

class TTTBoard:
    def __init__(self):
        ''' Create a new, blank TTT board '''
        self._spaces = {}  # Board is represented as Python dictionary.
        for space in ALL_SPACES:
            self._spaces[space] = BLANK  # All spaces start as blank

    def getBoardStr(self):
        ''' Return a text-representation of the board. '''
        return f'''
        {self._spaces['1']}|{self._spaces['2']}|{self._spaces['3']} 1 2 3
        -+-+-
        {self._spaces['4']}|{self._spaces['5']}|{self._spaces['6']} 4 5 6
        -+-+-
        {self._spaces['7']}|{self._spaces['8']}|{self._spaces['9']} 7 8 9'''
    
    def isValidSpace(self, move):
        ''' Returns True if the space played is a valid space number
            and the space is blank '''
        return move in ALL_SPACES and self._spaces[move] == BLANK
    
    def isWinner(self, player):
        ''' Return True if player is a winner on this TTTBoard. '''
        s, p = self._spaces, player  # shorter names for syntactic sugar. Yum!
        # Check for 3 marks across the 3 rows, 3 columns, and 2 diagonals.
        return ((s['1'] == s['2'] == s['3'] == p) or # Across the top
            (s['4'] == s['5'] == s['6'] == p) or # Across the middle
            (s['7'] == s['8'] == s['9'] == p) or # Across the bottom
            (s['1'] == s['4'] == s['7'] == p) or # Down the left
            (s['2'] == s['5'] == s['8'] == p) or # Down the middle
            (s['3'] == s['6'] == s['9'] == p) or # Down the right
            (s['1'] == s['5'] == s['9'] == p) or # Diagonal
            (s['3'] == s['5'] == s['7'] == p))   # Diagonal
    
    def isBoardFull(self):
        ''' Return True is every space on the board has been taken. ''' 
        for space in ALL_SPACES:
            if self._spaces[space] == BLANK:
                return False  # If a single space is blank return False
        return True  # No spaces are blank so return True
    
    def updateBoard(self, space, mark):
        ''' Sets the space on the board to mark '''
        self._spaces[space] = mark

class MiniBoard(TTTBoard):
    def getBoardStr(self):
        ''' Return a tiny text-representation of the board. '''
        # Change blank spaces to a '.'
        s = self._spaces  # sugar
        for space in ALL_SPACES:
            if s[space] == BLANK:
                s[space] = '.'

        boardStr = f'''
            {s['1']}{s['2']}{s['3']}  123
            {s['4']}{s['5']}{s['6']}  456
            {s['7']}{s['8']}{s['9']}  789 '''
        
        # Change '.' back to blank spaces in order to work with program
        for space in ALL_SPACES:
            if s[space] == '.':
                s[space] = BLANK
        
        return boardStr
    
class HintBoard(TTTBoard):
    def getBoardStr(self):
        ''' Return a text-representation of the board with hints. '''
        boardStr = super().getBoardStr()  # Call getBoardStr() in TTTBoard.

        XCanWin = False
        OCanWin = False
        originalSpaces = self._spaces  # Backup _spaces.

        for space in ALL_SPACES:  # Check each space:
            # Simulate X moving on this space:
            self._spaces = copy.copy(originalSpaces)  # refresh self._spaces
            if self._spaces[space] == BLANK:
                self._spaces[space] = X
            if self.isWinner(X):
                XCanWin = True

            self._spaces = copy.copy(originalSpaces)  # refresh halfway in the event O can win too
            
            # Simulate O moving on this space
            if self._spaces[space] == BLANK:
                self._spaces[space] = O
            if self.isWinner(O):
                OCanWin = True

        if XCanWin:
            boardStr += '\nX can win in one more move...'
        if OCanWin:
            boardStr += '\nO can win in one more move...'
        self._spaces = originalSpaces  # Set self._spaces to original markup
        return boardStr

if __name__ == '__main__':
    main()