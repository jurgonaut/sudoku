import random

board = [
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"],
    ["X","X","X","X","X","X","X","X","X"]
]

class Number:
    def __init__(self):
        self.num = 0
        self.pos_x = 0
        self.pos_y = 0
        self.available_pos = []
        self.vizited_pos = []

    def get_next_pos(self):
        pos = []
        tmp = []
        if not self.vizited_pos:
            tmp = self.available_pos
        else:
            for i, v in enumerate(self.available_pos):
                found = False
                for j, k in enumerate(self.vizited_pos):
                    if self.vizited_pos[j][0] == self.available_pos[i][0] and self.vizited_pos[j][1] == self.available_pos[i][1]:
                        found = True
                        break
                if not found:
                    tmp.append(self.available_pos[i])

        if not tmp:
            return -1

        if len(tmp) == 1:
            pos = tmp[0]
        else:
            i = random.randint(0 , len(tmp) -1)
            pos = tmp[i]

        self.vizited_pos.append(pos)

        return [pos[0], pos[1]]

class HiddenCandidate:
    def __init__(self):
        self.num = 0
        self.occurrences = 0
        self.positions = []
        self.pair = 0

    def __repr__(self):
        return str(self.num) + " " + str(self.occurrences) + " " + str(self.positions) + " " + str(self.pair) + "\n"

    def __str__(self):
        return str(self.occurrences) + " " + str(self.positions) + " " + str(self.pair) + "\n"

class BoxBoundaries:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

    def __repr__(self):
        return "start x: " + str(self.start_x) + " end x: " + str(self.end_x) + " start y: " + str(self.start_y) + " end y: " + str(self.end_y)

    def __str__(self):
        return "start x: " + str(self.start_x) + " end x: " + str(self.end_x) + " start y: " + str(self.start_y) + " end y: " + str(self.end_y)
        

class SudokuFiller:
    def __init__(self, b):
        self.board = b
        # array for storing past moves of numbers
        self.past_moves = []
        # current row, when "curr_number" reaches 9 we increment this, when "curr_number" goes below
        # 1 we decrement
        self.curr_row = 0
        # current number in row, from 1-9
        self.curr_number = 1
        # variable that starts the backtraking
        self.backtrack = False
        # number of steps taken to finish the board
        self.steps = 0

    def print_board(self):
        for i in range(0,9):
            print self.board[i]

    def generate(self):
        while self.curr_row < 9:
            if self.curr_row > 8 and self.curr_number > 9:
                break

            empty_box = self.get_free_pos()

            if not empty_box or self.backtrack:
                found = False
                while not found:
                    past = self.past_moves[-1]
                    self.curr_number -= 1
                    self.check_edges()

                    self.board[past.pos_y][past.pos_x] = "X"

                    next = past.get_next_pos()

                    if next == -1:
                        new = []
                        for i, v in enumerate(self.past_moves):
                            if not i == len(self.past_moves) -1:
                                new.append(self.past_moves[i])
                        self.past_moves = new
                        self.steps += 1
                    else:
                        past.pos_y = next[0]
                        past.pos_x = next[1]

                        self.board[past.pos_y][past.pos_x] = self.curr_number
                        self.past_moves[-1] = past

                        self.curr_number += 1
                        self.check_edges()

                        found = True
                        self.backtrack = False
                        self.steps += 1

            else:
                a = []
                for i, v in enumerate(empty_box):
                    a.append([self.curr_row, empty_box[i]])

                n = Number()
                n.num = self.curr_number
                n.available_pos = a
                next = n.get_next_pos()

                if next == -1:
                    self.backtrack = True
                else:
                    n.pos_y = next[0]
                    n.pos_x = next[1]

                    self.past_moves.append(n)

                    self.board[n.pos_y][n.pos_x] = self.curr_number

                    self.curr_number += 1
                    self.check_edges()
                    self.steps += 1
        
    def generate_recursive(self):
        if self.curr_row > 8:
            return

        empty_box = self.get_free_pos()

        if not empty_box or self.backtrack:
            found = False
            while not found:
                past = self.past_moves[-1]
                self.curr_number -= 1
                self.check_edges()

                self.board[past.pos_y][past.pos_x] = "X"

                next = past.get_next_pos()

                if next == -1:
                    new = []
                    for i, v in enumerate(self.past_moves):
                        if not i == len(self.past_moves) -1:
                            new.append(self.past_moves[i])
                    self.past_moves = new
                    self.steps += 1
                else:
                    past.pos_y = next[0]
                    past.pos_x = next[1]

                    self.board[past.pos_y][past.pos_x] = self.curr_number
                    self.past_moves[-1] = past

                    self.curr_number += 1
                    self.check_edges()

                    found = True
                    self.backtrack = False
                    self.steps += 1
                    self.generate_recursive()

        else:
            a = []
            for i, v in enumerate(empty_box):
                a.append([self.curr_row, empty_box[i]])

            n = Number()
            n.num = self.curr_number
            n.available_pos = a
            next = n.get_next_pos()

            if next == -1:
                self.backtrack = True
            else:
                n.pos_y = next[0]
                n.pos_x = next[1]

                self.past_moves.append(n)

                self.board[n.pos_y][n.pos_x] = self.curr_number

                self.curr_number += 1
                self.check_edges()
                self.steps += 1
                self.generate_recursive()

    def check_edges(self):
        if self.curr_number < 1:
            self.curr_number = 9
            self.curr_row -= 1

        if self.curr_number > 9:
            self.curr_row += 1
            self.curr_number = 1

        if self.curr_row < 0:
            self.curr_row = 0

    def get_free_pos(self):
        available_pos = []
        available_pos = self.get_free_box()

        return available_pos

    def get_free_box(self):
        possible_pos = []
        available_pos = []
        possible_pos = self.get_free_row()

        if not possible_pos:
            return available_pos
        else:
            for i, v in enumerate(possible_pos):
                found = False
                start_x = 0
                end_x = 0
                start_y = 0
                end_y = 0

                if self.curr_row < 3:
                    start_y = 0
                    end_y = 2
                elif self.curr_row > 2 and self.curr_row < 6:
                    start_y = 3
                    end_y = 5
                elif self.curr_row > 5:
                    start_y = 6
                    end_y = 8
                
                if possible_pos[i] < 3:
                    start_x = 0
                    end_x = 2
                elif possible_pos[i] > 2 and possible_pos[i] < 6:
                    start_x = 3
                    end_x = 5
                elif possible_pos[i] > 5:
                    start_x = 6
                    end_x = 8

                for j in range(start_y, end_y +1):
                        for l in range(start_x, end_x +1):
                            if self.board[j][l] == self.curr_number:
                                found = True

                if not found:
                    available_pos.append(possible_pos[i])

            return available_pos

    def get_free_row(self):
        possible_pos = []
        available_pos = []
        possible_pos = self.get_empty_pos()

        if not possible_pos:
            return available_pos
        else:
            for i, v in enumerate(possible_pos):
                if self.curr_row == 0:
                    available_pos.append(possible_pos[i])

                else:
                    found = False
                    j = self.curr_row
                    while j >= 0:
                        if self.board[j][possible_pos[i]] == self.curr_number:
                            found = True
                        j -= 1

                    if not found:
                        available_pos.append(possible_pos[i])

            return available_pos

    def get_empty_pos(self):
        available_pos = []
        for i, v in enumerate(self.board[self.curr_row]):
            if self.board[self.curr_row][i] == "X":
                available_pos.append(i)
        
        return available_pos

class SudokuGenerator:
    def __init__(self, b):
        self.solved_board = b
        self.finished_board = b
        self.available_numbers = [
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []]
        ]

    def print_available_numbers(self):
        header = ""
        for m in range(0, 9):
            if m == 0:
                header += 11*(" ") + str(m + 1)
            else:
                header += 19*(" ") + str(m + 1)
        print header

        for i in range(0, len(self.available_numbers)):
            row = ""
            pos = str(i + 1)
            for j in range(0, len(self.available_numbers[i])):
                spaces = ""
                length = 9 - len(self.available_numbers[i][j])
                for l in range(0, length):
                    spaces += "  "
                if not self.available_numbers[i][j]:
                    spaces = "                  "
                pos += " |"
                for k in range(0, len(self.available_numbers[i][j])):
                    pos += str(self.available_numbers[i][j][k]) + ","
                pos += spaces
            row = pos + "|"
            print 179*("-")
            print row
        print 179*("-")

    def print_board(self):
        for i in range(0, len(self.finished_board)):
            row = "| "
            print 41*("-")
            for j in range (0, len(self.finished_board[i])):
                if j % 3 == 0 and j != 0:
                    row += "| "
                    row += str(self.finished_board[i][j]) + " | "
                else:
                    row += str(self.finished_board[i][j]) + " | "
            if i % 3 == 0 and i != 0:
                print 41*("-")
            print row
            
        print 41*("-")

    def print_board_yx(self, y, x):
        print self.finished_board[y][x]

    def test_board(self):
        """
        self.finished_board = [
            [ 6 , 5 , 3 ,"X", 8 ,"X", 9 , 1 , 2 ], # 4 7
            [ 2 , 8 , 7 , 9 , 1 , 6 , 4 , 5 , 3 ], #
            [ 1 , 4 , 9 , 5 , 3 , 2 , 8 , 7 , 6 ], #
            [ 7 , 2 , 1 , 6 , 4 , 9 , 3 , 8 , 5 ], #
            [ 3 , 9 , 5 , 8 , 2 ,"X", 6 , 4 ,"X"], # 1 7
            [ 4 , 6 , 8 ,"X", 5 , 3 , 2 , 9 ,"X"], # 7 1
            [ 5 , 3 , 6 ,"X", 9 , 8 , 7 , 2 , 4 ], # 1
            [ 8 , 7 , 4 , 2 , 6 , 5 , 1 , 3 , 9 ], #
            [ 9 , 1 , 2 , 3 , 7 , 4 , 5 , 6 , 8 ]  #
        ]
        """
        
        self.finished_board = [
            [ 6 , 8 , 7 ,"X","X", 4 , 5 , 2 , 3 ], # 
            [ 9 , 5 , 3 ,"X","X", 2 , 6 , 1 , 4 ], #
            [ 1 , 4 , 2 , 3 , 5 , 6 , 9 , 7 , 8 ], #
            [ 3 , 1 ,"X","X","X", 7 , 2 , 4 , 6 ], #
            [ 7 , 6 ,"X","X","X","X", 3 ,"X", 5 ], # 
            ["X", 2 ,"X","X","X","X", 7 ,"X", 1 ], # 
            ["X", 9 , 6 ,"X","X", 1 ,"X", 3 , 2 ], # 
            [ 2 , 3 ,"X","X","X","X","X", 5 , 4 ], #
            ["X", 7 ,"X","X","X","X","X", 6 , 9 ]  #
        ]
        """
        self.finished_board = [
            ["X","X","X", 1 ,"X", 5 ,"X", 6 , 8 ], # 
            ["X","X","X","X","X","X", 7 ,"X", 1 ], #
            [ 9 ,"X", 1 ,"X","X","X","X", 3 ,"X"], #
            ["X","X", 7 ,"X", 2 , 6 ,"X","X","X"], #
            [ 5 ,"X","X","X","X","X","X","X", 3 ], # 
            ["X","X","X", 8 , 7 ,"X", 4 ,"X","X"], # 
            ["X", 3 ,"X","X","X","X", 8 ,"X", 5 ], # 
            [ 1 ,"X", 5 ,"X","X","X","X","X","X"], #
            [ 7 , 9 ,"X", 4 ,"X", 1 ,"X","X","X"]  #
        ]
        """

    def get_box_boundaries(self, y, x):
        boundaries = BoxBoundaries()

        if x < 3:
            boundaries.start_x = 0
            boundaries.end_x = 2
        elif x > 2 and x < 6:
            boundaries.start_x = 3
            boundaries.end_x = 5
        elif x > 5:
            boundaries.start_x = 6
            boundaries.end_x = 8
        
        if y < 3:
            boundaries.start_y = 0
            boundaries.end_y = 2
        elif y > 2 and y < 6:
            boundaries.start_y = 3
            boundaries.end_y = 5
        elif y > 5:
            boundaries.start_y = 6
            boundaries.end_y = 8

        return boundaries

    def get_numbers_in_box(self, y, x):
        nums_in_box = [0,0,0,0,0,0,0,0,0]

        if self.finished_board[y][x] != "X":
            return [9,9,9,9,9,9,9,9,9]

        start_x = 0
        end_x = 0
        start_y = 0
        end_y = 0
        if x < 3:
            start_x = 0
            end_x = 2
        elif x > 2 and x < 6:
            start_x = 3
            end_x = 5
        elif x > 5:
            start_x = 6
            end_x = 8
        
        if y < 3:
            start_y = 0
            end_y = 2
        elif y > 2 and y < 6:
            start_y = 3
            end_y = 5
        elif y > 5:
            start_y = 6
            end_y = 8

        for m in range(start_y, end_y +1):
            for n in range(start_x, end_x +1):
                if self.finished_board[m][n] != "X":
                    nums_in_box[self.finished_board[m][n] - 1] = self.finished_board[m][n]
            
        return nums_in_box

    def get_numbers_in_col(self, y, x):
        nums_in_col = [0,0,0,0,0,0,0,0,0]
        
        if self.finished_board[y][x] != "X":
            return [9,9,9,9,9,9,9,9,9]

        for i in range(0, 9):
            if not self.finished_board[i][x] == "X":
                nums_in_col[self.finished_board[i][x] - 1] = self.finished_board[i][x]
        return nums_in_col

    def get_numbers_in_row(self, y, x):
        nums_in_row = [0,0,0,0,0,0,0,0,0]
        
        if self.finished_board[y][x] != "X":
            return [9,9,9,9,9,9,9,9,9]

        for i in range(0, 9):
            if not self.finished_board[y][i] == "X":
                nums_in_row[self.finished_board[y][i] - 1] = self.finished_board[y][i]
        return nums_in_row

    def update_availible_numbers(self, y, x):
        available_numbers = []

        nums_in_box = self.get_numbers_in_box(y, x)
        #print nums_in_box
        nums_in_col = self.get_numbers_in_col(y, x)
        #print nums_in_col
        nums_in_row = self.get_numbers_in_row(y, x)
        #print nums_in_row

        for i in range(0, 9):
            if nums_in_row[i] == 0 and nums_in_col[i] == 0 and nums_in_box[i] == 0:
                available_numbers.append(i + 1)

        self.available_numbers[y][x] = available_numbers

    def update_availible_numbers_all(self):
        for i in range(0, 9):
            for j in range(0,9):
                self.update_availible_numbers(i, j)

    def find_naked_pairs(self):
        boundaries = self.get_box_boundaries(4,4)
        candidates = []
        for i in range(boundaries.start_y, boundaries.end_y + 1):
                for j in range(boundaries.start_x, boundaries.end_x + 1):
                    if len(self.available_numbers[i][j]) == 2:
                        candidates.append(self.available_numbers[i][j])
        
        #candidates = [[8,9],[1,2],[5,6],[8,9]]
        for i in range(len(candidates)):
            j = i + 1
            while j < len(candidates):
                if candidates[j] == candidates[i]:
                    print "found pair at " + str(j) + " " + str(i)
                j += 1

    def find_pairs(self):
        nums_in_box = self.get_numbers_in_box(8,4)
        print nums_in_box
        missing_nums = []
        candidates = []
        for i in range(len(nums_in_box)):
            if nums_in_box[i] == 0:
                missing_nums.append(i + 1)
        print missing_nums

        boundaries = self.get_box_boundaries(8,4)

        for k in range(len(missing_nums)):
            num = HiddenCandidate()
            num.num = missing_nums[k]
            for i in range(boundaries.start_y, boundaries.end_y + 1):
                for j in range(boundaries.start_x, boundaries.end_x + 1):
                    #print len(self.available_numbers[i][j])
                    for l in range(len(self.available_numbers[i][j])):
                        if self.available_numbers[i][j][l] == num.num:
                            num.occurrences += 1
                            num.positions.append([i, j])
            if num.occurrences == 2:
                candidates.append(num)
        print(candidates)
        print "***************"

        for i in range(len(candidates)):
            for j in range(len(candidates[i].positions)):
                print candidates[i].positions[j]
                k = i + 1
                while k < len(candidates):
                    for l in range(len(candidates[k].positions)):
                        if candidates[k].positions[l] == candidates[i].positions[j]:
                            candidates[i].pair += 1
                            candidates[k].pair += 1
                            print "found at " + str(i) + " " + str(j) + " " + str(k) + " " + str(l)
                    k += 1

        print "***************"
        print(candidates)

    def find_open_singles(self):
        for i in range(0, 9):
            nums_in_row = [0,0,0,0,0,0,0,0,0]
            free_pos_row = []
            number_row = 0
            overflow_row = False

            nums_in_col = [0,0,0,0,0,0,0,0,0]
            free_pos_col = []
            number_col = 0
            overflow_col = False

            # check row for single numbers
            for j in range(0, 9):
                if self.finished_board[i][j] != "X":
                    nums_in_row[self.finished_board[i][j] - 1] = self.finished_board[i][j]
                else:
                    if len(free_pos_row) > 0:
                        print "more than one in a row"
                        overflow_row = True
                    else:
                        free_pos_row.append([i,j])

            if not overflow_row and free_pos_row:
                for k in range(0, len(nums_in_row)):
                    if nums_in_row[k] == 0:
                        number_row = k + 1
                        self.available_numbers[free_pos_row[0][0]][free_pos_row[0][1]] = [number_row]

            # check column for single numbers
            for l in range(0, 9):
                if self.finished_board[l][i] != "X":
                    nums_in_col[self.finished_board[l][i] - 1] = self.finished_board[l][i]
                else:
                    if len(free_pos_col) > 0:
                        print "more than one in col"
                        overflow_col = True
                    free_pos_col.append([l,i])

            if not overflow_col:
                found_duplicate = False
                for h in range(0, len(nums_in_col)):
                    if nums_in_col[h] == 0:
                        number_col = h + 1
                        # check if number already added when checked rows
                        for i in range(len(self.available_numbers[free_pos_col[0][0]][free_pos_col[0][1]])):
                            if self.available_numbers[free_pos_col[0][0]][free_pos_col[0][1]][i] == number_col:
                                found_duplicate = True
                        if not found_duplicate:
                            self.available_numbers[free_pos_col[0][0]][free_pos_col[0][1]].append(number_col)   

if __name__ == "__main__":
    fill = SudokuFiller(board)
    
    print "---------------------------------"
    print "|    generate board iterative   |"
    print "---------------------------------"
    fill.generate()
    fill.print_board()
    print "steps " + str(fill.steps)
    print "--------------------------------"

    
    """
    print "----------------------------------"
    print "|    generate board recursive    |"
    print "----------------------------------"
    fill.generate_recursive()
    fill.print_board()
    print "steps " + str(fill.steps)
    print "--------------------------------"
    """

    """
    board = SudokuGenerator(fill.board)
    board.test_board()
    board.print_board()
    #board.update_availible_numbers(5, 3)
    #board.update_availible_numbers(0, 5)
    #board.update_availible_numbers(8, 0)
    board.update_availible_numbers_all()
    #board.print_board_yx(8,0)
    board.print_available_numbers()
    board.find_pairs()
    #board.find_naked_pairs()
    """