import itertools
import random
from copy import deepcopy
import random 


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count: 
            return self.cells 
        else: 
            return []


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0: 
            return self.cells 
        else: 
            return []
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells: 
            self.cells.discard(cell)
            self.count -= 1 



    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: 
            self.cells.discard(cell)
            

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)
        #2 
        self.mark_safe(cell)
        #3 
        close_cells = self.return_close_cells(cell)
        cells = set()
        for cc in close_cells: 
            if cc in self.mines: 
                count -= 1 
            elif cc in self.safes or cc in self.moves_made: 
                pass 
            else: 
                cells.add(cc)

        new_sentence = Sentence(cells, count)
        if len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)
        #4 
        self.iterate_knowledge()

        #5 
        self.subset_knowledge()





    def iterate_knowledge(self):
        indicator = False 
        knowledge_copy = deepcopy(self.knowledge)
        for sentence in knowledge_copy: 
            mine_cells = sentence.known_mines()
            for m in mine_cells: 
                self.mark_mine(m)
                indicator = True
            safe_cells = sentence.known_safes()
            for s in safe_cells: 
                self.mark_safe(s)
                indicator = True 
            if len(sentence.cells) == 0: 
                self.knowledge.remove(sentence)
        if indicator == True: 
            self.iterate_knowledge()


    def subset_knowledge(self): 
        indicator = False
        knowledge_copy = deepcopy(self.knowledge)
        for sentence in knowledge_copy: 
            for sentence_1 in knowledge_copy: 
                if sentence_1.cells.issubset(sentence.cells) and sentence.cells != sentence_1.cells: 
                    new_count = sentence.count - sentence_1.count 
                    new_cells = sentence.cells - sentence_1.cells 
                    if len(new_cells) > 0: 
                        new_sentence = Sentence(new_cells, new_count)
                        self.knowledge.append(new_sentence)
                        indicator = True 
        if indicator == True: 
            self.iterate_knowledge()



    def return_close_cells(self, cell): 
        """
        return cells one from the cell inputted

        """
        close_cells = set()
        rows = [i for i in range(cell[0] -1 ,cell[0]+2) if i >= 0 and i < self.width ]
        cols = [i for i in range(cell[1] -1 ,cell[1]+2) if i >= 0 and i < self.height ]
        for r in rows: 
            for c in cols:
                if (r,c) != cell:
                    close_cells.add((r,c))
        return close_cells
                    



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in self.safes - self.moves_made:
            return i 

        else: 
            return None 

    def make_random_move(self, ind = 0):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        width_seq = [i for i in range(self.width)]
        height_seq = [i for i in range(self.height)]
        if ind > 10: 
            return None 
        else:
            i = random.choice(width_seq)
            j = random.choice(height_seq)
            if (i,j) in self.mines or (i,j) in self.moves_made: 
                ind += 1
                self.make_random_move(ind)
            else: 
                return (i,j)

