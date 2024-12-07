import random
from tkinter import *
from tkinter import messagebox
import math


# Class to manage the Tic Tac Toe game (Command Line)
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Initialize an empty board
        self.current_winner = None  # Track the winner

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


# Base player class
class Player:
    def __init__(self, letter, name):
        self.letter = letter
        self.name = name

    def get_move(self, game):
        pass


# Human player class
class HumanPlayer(Player):
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.name + "'s turn. Input move (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


# Computer player class with difficulty levels
class ComputerPlayer(Player):
    def __init__(self, letter, difficulty):
        super().__init__(letter, "Computer")
        self.difficulty = difficulty  # Difficulty: easy, medium, hard

    def get_move(self, game):
        if self.difficulty == "easy":
            return random.choice(game.available_moves())
        elif self.difficulty == "medium":
            if random.random() < 0.5:  # 50% chance to play optimally
                return self.minimax(game, self.letter)['position']
            else:
                return random.choice(game.available_moves())
        elif self.difficulty == "hard":
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}

        if not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best


# Command Line Game Logic
def play_command_line():
    name = input("Enter your name: ")
    player_letter = 'X'
    computer_letter = 'O'
    difficulty = input("Choose AI difficulty: easy, medium, hard: ").lower()

    x_player = HumanPlayer(player_letter, name)
    o_player = ComputerPlayer(computer_letter, difficulty)
    t = TicTacToe()
    TicTacToe.print_board_nums()

    letter = 'X'
    while t.empty_squares():
        square = x_player.get_move(t) if letter == 'X' else o_player.get_move(t)
        if t.make_move(square, letter):
            print(f'{letter} makes a move to square {square}')
            t.print_board()
            if t.current_winner:
                print(f'{letter} wins!')
                return
            letter = 'O' if letter == 'X' else 'X'
    print("It's a tie!")


# GUI Logic with difficulty
class TicTacToeGUI:
    def __init__(self):
        self.Player1 = 'X'
        self.stop_game = False
        self.difficulty = "easy"  # Default difficulty
        self.root = Tk()
        self.root.title("Tic Tac Toe - GUI")
        self.setup_menu()
        self.b = [[0 for _ in range(3)] for _ in range(3)]
        self.states = [[0 for _ in range(3)] for _ in range(3)]
        self.setup_board()
        self.root.mainloop()

    def setup_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        submenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Difficulty", menu=submenu)
        submenu.add_command(label="Easy", command=lambda: self.set_difficulty("easy"))
        submenu.add_command(label="Medium", command=lambda: self.set_difficulty("medium"))
        submenu.add_command(label="Hard", command=lambda: self.set_difficulty("hard"))

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        messagebox.showinfo("Difficulty", f"Difficulty set to {difficulty.capitalize()}")

    def setup_board(self):
        for i in range(3):
            for j in range(3):
                self.b[i][j] = Button(
                    height=4, width=8, font=("Helvetica", "20"),
                    command=lambda r=i, c=j: self.clicked(r, c))
                self.b[i][j].grid(row=i, column=j)

    def clicked(self, r, c):
        if self.states[r][c] == 0 and not self.stop_game:
            self.b[r][c].configure(text=self.Player1)
            self.states[r][c] = self.Player1
            if not self.check_if_win():
                self.Player1 = 'O' if self.Player1 == 'X' else 'X'
                self.ai_move()

    def ai_move(self):
        if not self.stop_game:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.states[r][c] == 0]
            if empty_cells:
                if self.difficulty == "easy":
                    r, c = random.choice(empty_cells)
                elif self.difficulty == "medium":
                    if random.random() < 0.5:
                        r, c = random.choice(empty_cells)
                    else:
                        r, c = self.best_move()
                else:
                    r, c = self.best_move()

                self.b[r][c].configure(text=self.Player1)
                self.states[r][c] = self.Player1
                self.Player1 = 'O' if self.Player1 == 'X' else 'X'
                self.check_if_win()

    def best_move(self):
        # Simplified for GUI: Selects the first empty cell
        for r in range(3):
            for c in range(3):
                if self.states[r][c] == 0:
                    return r, c

    def check_if_win(self):
        for i in range(3):
            if self.states[i][0] == self.states[i][1] == self.states[i][2] != 0 or \
               self.states[0][i] == self.states[1][i] == self.states[2][i] != 0 or \
               self.states[0][0] == self.states[1][1] == self.states[2][2] != 0 or \
               self.states[0][2] == self.states[1][1] == self.states[2][0] != 0:
                self.stop_game = True
                messagebox.showinfo("Winner", f"{self.Player1} Wins!")
                return True
        if all(self.states[i][j] != 0 for i in range(3) for j in range(3)):
            self.stop_game = True
            messagebox.showinfo("Tie", "It's a tie!")
            return True
        return False


# Main Menu
def main():
    choice = input("Choose mode: 1 for Command Line, 2 for GUI: ")
    if choice == '1':
        play_command_line()
    elif choice == '2':
        TicTacToeGUI()


if __name__ == '__main__':
    main()

