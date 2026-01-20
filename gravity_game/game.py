
def gravity_decorator(insert_method):
    """
    Decorator that applies a gravity effect to a game board 
    after a piece is inserted.
    Input:
        insert_method (function): The original method that 
        inserts a piece into the board.
    Output:
        function: A wrapped version of the insert method 
        with gravity applied.
    """
    def wrapper(self, board, column):
        if insert_method(self, board, column) == True:
            # Iterate over each column from right to left
            # and over each row from second-to-last upwards
            for col in range(board.columns - 1, -1, -1):
                for row in range(board.rows - 2, -1, -1):
                    # Check if cell below the current one is empty
                    for offset in range((board.rows - 1) - row, 0, -1):
                        if board.grid[row + offset][col] == " ":
                            board.grid[row + offset][col] = board.grid[row][col]
                            board.grid[row][col] = " "
                            # Stop once the piece has fallen to lowest empty spot
                            break 
            return True
        return False  # Return False if insertion failed
    return wrapper


class Board:
    def __init__(self, rows, columns):
        """
        Initializes a board with the given number of rows
        and columns.
        Input:
            rows (int): Number of rows in the board.
            columns (int): Number of columns in the board.
        """
        self.rows = rows
        self.columns = columns
        self.grid = [[" " for column in range(columns)] for row in range(rows)]

    def __repr__(self):
        """
        Returns:
            board_output (str): String representation
            of the board.
        """
        # Generate column headers with centered numbers
        position = [str(number).center(4) for number in range(1, self.columns, 1)]
        # Manually append last column number to avoid trailing whitespaces
        coordinates = " " + "".join(position) + " " + str(self.columns)

        # Adjust spacing for the last 3-digit row number to prevent misalignment
        if self.rows > 99:
            coordinates = " " + "".join(position) + str(self.columns)

        # Create horizontal edge line
        horizontal_edge = "\n" + self.columns * "+---" + "+" + "\n"

        # Build each row of the board with vertical dividers
        expanded_board = []
        for row_values in self.grid:
            expanded_cell = ["|" + cell_value.center(3) for cell_value in row_values]
            expanded_row = "".join(expanded_cell)
            expanded_board.append(expanded_row)

        # Combine rows with horizontal edges
        patterned_rows = ("|" + horizontal_edge).join(expanded_board)

        # Final board string
        board_representation = (
            coordinates + horizontal_edge + patterned_rows + "|" + horizontal_edge
        )
        return board_representation

    def __getitem__(self, index):
        """
        Allows direct access to a row in the board using indexing.
        """
        return self.grid[index]


class Piece:
    def __init__(self, symbol):
        """
        Initializes a game piece with a specific symbol.
        Args:
            symbol (str): The character representing the piece (e.g., 'X' or 'O').
        """
        self.symbol = symbol

    def insert(self, board, column):
        """
        Attempts to insert the piece into the specified column of the board.
        Args:
            board (Board): The game board where the piece will be placed.
            column (int): The 1-based index of the column to insert the piece into.
        Returns:
            bool: True if the piece was successfully inserted, False otherwise.
        """
        if column > board.columns:
            return False

        column_index = column - 1  # Convert to 0-based index

        # Start from the bottom row and move upward
        for row in range(board.rows - 1, -1, -1):
            if board.grid[row][column_index] == " ":
                # Place the piece in the first available empty cell
                board.grid[row][column_index] = self.symbol
                return True  # Exit after successful insertion

        return False


class Player:
    def __init__(self, name, symbol):
        """
        Initializes a Player with a name, a default symbol,
        and an empty list of pieces.
        """
        self.name = name
        self.symbol = symbol
        self.pieces = []

    def add_piece(self, symbol, quantity):
        """
        Adds a specified number of pieces with the given symbol
        to the player's collection.
        Input:
            symbol (str): The symbol to assign to each piece.
            quantity (int): The number of pieces to add.
        """
        for i in range(quantity):
            if symbol == "B":
                piece = BombPiece(symbol)
            elif symbol == "T":
                piece = TeleportPiece(symbol)
            else:
                piece = Piece(symbol)
                
            self.pieces.append(piece)

    def choose_piece(self):
        """
        Prompts the player to choose a piece and a column to play.
        Returns:
            list or None: A list containing the selected Piece object
            and the chosen column (as a string), or None
            if no matching piece is found.
        """
        print(self)  # Display the player's current pieces

        # Prompt the player for input and strip any surrounding whitespace
        piece_information = (
            input("Choose a piece to play (symbol and column): ")
        ).strip()

        # Extract the symbol (first character) and column (remaining characters)
        piece_chosen = piece_information[0]
        piece_column = int(piece_information[1:].strip())

        # Search for a piece with the matching symbol
        for piece in self.pieces:
            if piece.symbol == piece_chosen:
                # Remove the selected piece from the player's collection
                selected_piece = piece
                self.pieces.remove(piece)
                return [selected_piece, piece_column]

        return None

    def __repr__(self):
        """
        Returns:
            str: A formatted string listing the player's pieces
            by symbol and count.
        """
        distinct_symbol_list = []

        # Collect all unique symbols from the player's pieces
        for piece in self.pieces:
            if piece.symbol not in distinct_symbol_list:
                distinct_symbol_list.append(piece.symbol)

        # Sort the symbols alphabetically
        distinct_symbol_list.sort()

        # Count how many pieces the player has for each symbol
        quantity_dict = {}
        for distinct_symbol in distinct_symbol_list:
            quantity = 0
            for piece in self.pieces:
                if distinct_symbol == piece.symbol:
                    quantity += 1
            quantity_dict[distinct_symbol] = quantity

        # Format the output string
        string = [f"{x}: {quantity_dict[x]}" for x in quantity_dict]
        return f"{self.name}'s pieces -> " + ", ".join(string)


class Game:
    def __init__(self, rows, columns):
        """
        Initializes the Game with a board of specified size and 
        sets up player tracking.
        Args:
            rows (int): Number of rows in the game board.
            columns (int): Number of columns in the game board.
        """
        self.board = Board(rows, columns)
        self.players = []
        self.current_player = None

    def setup(self):
        """
        Sets up game by collecting player names and symbols,
        validating input, assigning pieces, and determining who starts.
        """
        valid_player_1 = False
        valid_player_2 = False

        # Get valid input for Player 1
        while valid_player_1 == False:
            player_1_input = input("Enter player one's name and symbol: ")
            if len(player_1_input) >= 3:
                if player_1_input[-1] != " " and player_1_input[-2] == " ":
                    valid_player_1 = True

        # Player name is everything up to the penultimate character
        player_1_name = player_1_input[:-2]
        player_1_symbol = player_1_input[-1]
        player_1 = Player(player_1_name, player_1_symbol)
        self.player_1 = player_1
        self.players.append(player_1)

        # Get valid input for Player 2
        while valid_player_2 == False:
            player_2_input = input("Enter player two's name and symbol: ")
            if len(player_2_input) >= 3:
                if (
                    player_2_input[-1] != " "
                    and player_2_input[-1] != player_1_symbol
                    and player_2_input[-2] == " "
                ):
                    valid_player_2 = True

        player_2_name = player_2_input[:-2]
        player_2_symbol = player_2_input[-1]
        player_2 = Player(player_2_name, player_2_symbol)
        self.player_2 = player_2
        self.players.append(player_2)

        # Distribute pieces evenly between players
        pieces_quantity = (self.board.rows * self.board.columns) // 2
        player_2.add_piece(player_2_symbol, pieces_quantity)

        # Give player 1 additional piece for odd size boards
        if (self.board.rows * self.board.columns) % 2 == 1:
            pieces_quantity += 1
        self.player_1.add_piece(player_1_symbol, pieces_quantity)

        # Players receive 1 bomb for every 20 cells
        bomb_quantity = (self.board.rows * self.board.columns) // 20
        # Players receive 1 teleport piece for every 10 cells
        teleport_quantity = (self.board.rows * self.board.columns) // 10

        player_1.add_piece("B", bomb_quantity)
        player_1.add_piece("T", teleport_quantity)

        player_2.add_piece("B", bomb_quantity)
        player_2.add_piece("T", teleport_quantity)

        # Player 1 starts the game
        self.current_player = self.players[0]

    def change_player(self):
        """
        Switches the current player to the other player.
        """
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def check_win(self):
        """
        Checks the board for a win condition in all directions:
        horizontal, vertical, and both diagonals.
        
        Returns:
            str or bool: "Player 1" or "Player 2" if a win is found, otherwise False.
        """
        winner_1 = False
        winner_2 = False
        for row in range(0, self.board.rows):
            for column in range(0, self.board.columns):

                # Horizontal check for 4 consecutive symbols
                count_player_1_horizontal = 0
                count_player_2_horizontal = 0
                for i in range(column, column + 4, 1):
                    try:
                        if self.board.grid[row][i] == self.player_1.symbol:
                            count_player_1_horizontal += 1
                        if self.board.grid[row][i] == self.player_2.symbol:
                            count_player_2_horizontal += 1
                    except IndexError:
                        break
                
                if count_player_1_horizontal == 4 and count_player_2_horizontal == 4 :
                    winner_1 = True
                    winner_2 = True
                elif count_player_1_horizontal == 4:
                    winner_1 = True
                elif count_player_2_horizontal == 4:
                    winner_2 = True
                
                # Vertical check for 4 consecutive symbols
                count_player_1_vertical = 0
                count_player_2_vertical = 0
                for i in range(row, row + 4, 1):
                    try:
                        if self.board.grid[i][column] == self.player_1.symbol:
                            count_player_1_vertical += 1
                        if self.board.grid[i][column] == self.player_2.symbol:
                            count_player_2_vertical += 1
                    except IndexError:
                        break
                
                if count_player_1_vertical == 4 and count_player_2_vertical == 4 :
                    winner_1 = True
                    winner_2 = True
                elif count_player_1_vertical == 4:
                    winner_1 = True
                elif count_player_2_vertical == 4:
                    winner_2 = True
                
                # Diagonal down-right check
                count_player_1_down_right = 0
                count_player_2_down_right = 0
                for i in range(column, column + 4, 1):
                    try:
                        if (self.board.grid[row + (i - column)][i] == self.player_1.symbol):
                            count_player_1_down_right += 1
                        if (self.board.grid[row + (i - column)][i]== self.player_2.symbol):
                            count_player_2_down_right += 1
                    except IndexError:
                        break

                if count_player_1_down_right == 4 and count_player_2_down_right == 4 :
                    winner_1 = True
                    winner_2 = True
                elif count_player_1_down_right == 4:
                    winner_1 = True
                elif count_player_2_down_right == 4:
                    winner_2 = True
                
                # Diagonal up-right check
                count_player_1_up_right = 0
                count_player_2_up_right = 0
                for i in range(column, column + 4, 1):
                    try:
                        if (self.board.grid[row - (i - column)][i]== self.player_1.symbol):
                            count_player_1_up_right += 1
                        if (self.board.grid[row - (i - column)][i] == self.player_2.symbol):
                            count_player_2_up_right += 1
                    except IndexError:
                        break
                
                if count_player_1_up_right == 4 and count_player_2_up_right == 4 :
                    winner_1 = True
                    winner_2 = True
                elif count_player_1_up_right == 4:
                    winner_1 = True
                elif count_player_2_up_right == 4:
                    winner_2 = True
                
        if winner_1 and winner_2:
            return "Both"  
        elif winner_1:
            return "Player 1"
        elif winner_2:
            return "Player 2"
        
        # If neither win
        return False 

    def begin(self, start=True):
        """
        Starts or continues the game loop. Handles player turns, 
        piece selection, win/draw detection, and switching players.
        Args:
            start (bool): Triggers setup() if first call to begin.
        """
        if start == True:
            self.setup()

        print(self.board)

        inserted_piece = False
        # Keep asking user for valid piece and position choice if invalid
        while inserted_piece == False:
            is_valid_piece = self.current_player.choose_piece()
            if is_valid_piece != None:
                selected_piece = is_valid_piece[0]
                selected_column = is_valid_piece[1]
                inserted_piece = selected_piece.insert(self.board, selected_column)

        # Check for win
        if self.check_win() == "Player 1":
            print(f"{self.player_1.name} wins!")
            print(self.board)
            return
        if self.check_win() == "Player 2":
            print(f"{self.player_2.name} wins!")
            print(self.board)
            return

        if self.check_win() == "Both":
            print(f"It was a draw!")
            print(self.board)
            return

        # Check for full board
        else:
            is_empty = False
            for row in self.board.grid:
                for cell in row:
                    if cell == " ":
                        is_empty = True
            if is_empty == False:
                print("It was a draw!")
                print(self.board)
                return

            # Check for empty hands
            if self.player_1.pieces == [] and self.player_2.pieces == []:
                print("It was a draw!")
                print(self.board)
                return

            # Switch player turn and continue game 
            self.change_player()
            self.begin(False)


class BombPiece(Piece):
    """
    A special game piece that clears a 3x3 area centered 
    on its position, when inserted.
    Inherits from the base Piece class.
    """
    def __init__(self, symbol= "B"):
        """
        Initialize the BombPiece with a default symbol 'B'.
        """
        super().__init__(symbol)

    @gravity_decorator
    def insert(self, board, column):
        """
        Inserts the BombPiece into the specified column of the board, 
        which clears a 3x3 area centered on the bomb's location.
        Input:
            board (Board): The game board object.
            column (int): The column 1-base index where the piece should be inserted.
        Returns:
            bool: True if the piece was successfully inserted and exploded, False otherwise.
        """
        if super().insert(board, column) == True:
            # Find the location of the Bomb on the board
            found = False
            for row in range(0, board.rows):
                for col in range(0, board.columns):
                    if board.grid[row][col] == "B":
                        row_index = row
                        col_index = col
                        found = True
                        break
                if found:
                    break
            
            # Clear the 3x3 area centered on the bomb
            for i in range(col_index - 1, col_index + 2):
                try:
                    board.grid[row_index - 1][i] = ' '
                except IndexError:
                    continue
            for i in range(col_index - 1, col_index + 2):
                try:
                    board.grid[row_index][i] = ' '
                except IndexError:
                    continue
            for i in range(col_index - 1, col_index + 2):
                try:
                    board.grid[row_index + 1][i] = ' '
                except IndexError:
                    continue

            return True
            
        return False
        

class TeleportPiece(Piece):
    """
    A special game piece that swaps its position 
    with the mirrored position across the center of the board.
    Inherits from the base Piece class.
    """
    def __init__(self, symbol= "T"):
        """
        Initialize the TeleportPiece with a default symbol 'T'.
        """
        super().__init__(symbol)

    @gravity_decorator
    def insert(self, board, column):
        """
        Inserts the TeleportPiece into the specified column of the board.
        If successfully inserted, it swaps its position with the mirrored position
        across the center of the board.
        Input:
            board (Board): The game board object.
            column (int): The column 1-based index where the piece should be inserted.
        Returns:
            bool: True if the piece was successfully inserted and teleported, False otherwise.
        """
        if super().insert(board, column) == True:
            # Find location of Teleport 
            found = False
            for row in range(0, board.rows):
                for col in range(0, board.columns):
                    if board.grid[row][col] == "T":
                        row_index = row
                        col_index = col
                        found = True
                        break
                if found:
                    break

            # Calculate the mirrored position across the center of the board
            mid_column = board.columns // 2
            mid_row = board.rows // 2

            offset_vertical = row_index - mid_row
            offset_horizontal = col_index - mid_column

            mirrored_row = mid_row - offset_vertical
            mirrored_col = mid_column - offset_horizontal

            # Override Teleport piece with the mirrored position
            mirrored_piece = board.grid[mirrored_row][mirrored_col]
            board.grid[row_index][col_index] = mirrored_piece
            
            # Update replaced board index to empty
            board.grid[mirrored_row][mirrored_col] = ' '
            
            return True
            
        return False



game = Game(5, 5)
game.begin()