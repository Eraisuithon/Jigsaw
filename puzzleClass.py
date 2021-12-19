from random import choice
import numpy as np


class Puzzle:
    def __init__(self):
        self.width = 3
        self.height = 3

        self.blank_pos = (self.height - 1, self.width - 1)

        self.state = [[(i + 1) + (j * self.width) for i in range(self.width)] for j in range(self.height)]
        self.state[-1][-1] = None
        self.solution = self.to_string_state(self.state)

        self.n_of_moves = 0

    def show(self, state):
        for row in state:
            for el in row[:-1]:
                if el is None:
                    print("  | ", end='')
                    continue

                print(f"{el} | ", end='')

            if row[-1] is None:
                print()
                continue
            print(row[-1])
        print()

    def move_down(self):
        if self.blank_pos[0] == self.height - 1: return

        y = self.blank_pos[0]
        x = self.blank_pos[1]
        self.state[y][x], self.state[y + 1][x] = self.state[y + 1][x], self.state[y][x]

        self.blank_pos = (y + 1, x)

    def move_up(self):
        if self.blank_pos[0] == 0: return

        y = self.blank_pos[0]
        x = self.blank_pos[1]
        self.state[y][x], self.state[y - 1][x] = self.state[y - 1][x], self.state[y][x]

        self.blank_pos = (y - 1, x)

    def move_right(self):
        if self.blank_pos[1] == self.width - 1: return

        y = self.blank_pos[0]
        x = self.blank_pos[1]
        self.state[y][x], self.state[y][x + 1] = self.state[y][x + 1], self.state[y][x]

        self.blank_pos = (y, x + 1)

    def move_left(self):
        if self.blank_pos[1] == 0: return

        y = self.blank_pos[0]
        x = self.blank_pos[1]
        self.state[y][x], self.state[y][x - 1] = self.state[y][x - 1], self.state[y][x]

        self.blank_pos = (y, x - 1)

    def move_to(self, state):
        self.state = state

        # making blank_pos correct
        for row in range(self.height):
            for col in range(self.width):
                if state[row][col] is None:
                    self.blank_pos = (row, col)
                    return

    def play(self):
        while True:
            self.play_logic()
            puzzle.breadth_first()
            ans = input('Do you want to play again? Y/n\n').upper()
            while ans not in 'YN\n':
                print('Please enter correct')
                ans = input('Do you want to play again? Y/n\n').upper()
            if ans == 'N':
                print('Thanks for playing')
                return

    def play_logic(self):
        self.randomize()
        key_to_move = {'W': self.move_up, 'A': self.move_left, 'S': self.move_down, 'D': self.move_right}
        while True:
            self.show(self.state)
            if self.did_win():
                print("Congrats!!")
                print(f"You made {self.n_of_moves}")
                self.n_of_moves = 0
                return
            move = input('Enter a WASD key and press enter or Q to give up:\n').upper()
            while move not in 'WASDQ':
                move = input('Please enter a valid input: (W/A/S/D/Q)\n').upper()

            if move == 'Q':
                print("Exiting game")
                return

            key_to_move[move]()
            self.n_of_moves += 1

    def breadth_first(self):
        self.randomize()
        first_state = self.to_string_state(self.state)
        queue = []
        explored = {first_state}
        backwards = {}
        while True:
            previous_state = [row[:] for row in self.state]
            to_string_previous = self.to_string_state(previous_state)
            for move in [self.move_up, self.move_left, self.move_down, self.move_right]:
                move()
                string_state = self.to_string_state(self.state)
                copy_of_previous = [row[:] for row in previous_state]
                self.move_to(copy_of_previous)

                if string_state not in explored:
                    queue.append(string_state)
                    explored.add(string_state)
                    backwards[string_state] = to_string_previous
                    if string_state == self.solution:
                        self.show_backwards(backwards)
                        print(f"Computer made {self.n_of_moves - 1} moves")
                        self.n_of_moves = 0
                        return

            if not queue:
                print("Didn't find solution")
                return
            moving_state = queue.pop(0)

            self.move_to(self.to_list_state(moving_state))

    def show_backwards(self, backwards):
        print()
        print()
        print("Computer's turn")
        print()
        solution = [self.solution]
        next_state = backwards.get(self.solution, None)
        while next_state is not None:
            solution.insert(0, next_state)
            next_state = backwards.get(next_state, None)
        for string_state in solution:
            state = self.to_list_state(string_state)
            self.n_of_moves += 1
            self.show(state)

    def did_win(self):
        string_state = self.to_string_state(self.state)
        return string_state == self.solution

    def to_string_state(self, state):
        return ' '.join([str(el) for row in state for el in row])

    def to_list_state(self, state):
        return np.reshape(list(map(lambda x: None if (x == 'None') else int(x), state.strip().split())),
                          (self.width, self.height)).tolist()

    def randomize(self):
        for _ in range(1000):
            choice([self.move_right, self.move_left, self.move_down, self.move_up])()
