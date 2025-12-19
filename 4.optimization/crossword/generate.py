import sys
from crossword import *
from PIL import Image, ImageDraw, ImageFont


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For each variable, remove words that don't match its length
        for variable in self.domains:
            # Create a copy of the domain to iterate over (so we can modify the original)
            words_to_remove = []
            for word in self.domains[variable]:
                # If word length doesn't match variable length, mark it for removal
                if len(word) != variable.length:
                    words_to_remove.append(word)
            
            # Remove the words that don't match
            for word in words_to_remove:
                self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlap between x and y
        overlap = self.crossword.overlaps[x, y]
        
        # If there's no overlap, x is already arc consistent with y
        if overlap is None:
            return False
        
        # overlap is (i, j) where x[i] must equal y[j]
        x_index, y_index = overlap
        
        # Track if we made any changes
        revised = False
        words_to_remove = []
        
        # Check each word in x's domain
        for word_x in self.domains[x]:
            # Check if there's any word in y's domain that matches at the overlap
            found_match = False
            for word_y in self.domains[y]:
                # If characters match at the overlap position, we found a match
                if word_x[x_index] == word_y[y_index]:
                    found_match = True
                    break
            
            # If no match found, this word_x must be removed from x's domain
            if not found_match:
                words_to_remove.append(word_x)
                revised = True
        
        # Remove words that have no compatible value in y's domain
        for word in words_to_remove:
            self.domains[x].remove(word)
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize the queue of arcs to process
        queue = []
        
        if arcs is None:
            # Start with all arcs (pairs of variables that overlap)
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y and self.crossword.overlaps[x, y] is not None:
                        queue.append((x, y))
        else:
            # Use the provided arcs
            queue = arcs.copy()
        
        # Process arcs until queue is empty
        while queue:
            x, y = queue.pop(0)
            
            # Try to revise x based on y
            if self.revise(x, y):
                # If we revised x's domain, check if it's empty
                if len(self.domains[x]) == 0:
                    return False
                
                # Add arcs back to queue: for each neighbor z of x (except y),
                # add (z, x) to ensure consistency is maintained
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all variables are in the assignment
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check 1: All words must be distinct
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False
        
        # Check 2: Each word must have the correct length for its variable
        for variable, word in assignment.items():
            if len(word) != variable.length:
                return False
        
        # Check 3: No conflicts between neighboring variables
        for variable1, word1 in assignment.items():
            for variable2, word2 in assignment.items():
                if variable1 == variable2:
                    continue
                
                # Check if they overlap
                overlap = self.crossword.overlaps[variable1, variable2]
                if overlap is not None:
                    x_index, y_index = overlap
                    # If characters don't match at overlap, there's a conflict
                    if word1[x_index] != word2[y_index]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get unassigned neighbors (neighbors not in assignment)
        unassigned_neighbors = [
            neighbor for neighbor in self.crossword.neighbors(var)
            if neighbor not in assignment
        ]
        
        # For each value in var's domain, count how many values it rules out
        # for unassigned neighbors
        value_scores = []
        
        for value in self.domains[var]:
            eliminated_count = 0
            
            # For each unassigned neighbor, count eliminated values
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is not None:
                    var_index, neighbor_index = overlap
                    # Count how many neighbor values are eliminated
                    for neighbor_value in self.domains[neighbor]:
                        if value[var_index] != neighbor_value[neighbor_index]:
                            eliminated_count += 1
            
            value_scores.append((value, eliminated_count))
        
        # Sort by eliminated count (ascending - least constraining first)
        value_scores.sort(key=lambda x: x[1])
        
        # Return just the values in order
        return [value for value, _ in value_scores]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get all unassigned variables
        unassigned = [
            var for var in self.crossword.variables
            if var not in assignment
        ]
        
        # Sort by: 1) minimum remaining values (MRV), 2) highest degree (tie-breaker)
        # We'll use a tuple for sorting: (domain_size, -degree)
        # Negative degree because we want highest degree (largest number)
        unassigned.sort(key=lambda var: (
            len(self.domains[var]),  # MRV: smaller is better
            -len(self.crossword.neighbors(var))  # Degree: larger is better (negative for reverse sort)
        ))
        
        # Return the first one (best according to heuristics)
        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: if assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Try each value in the variable's domain (ordered by heuristic)
        for value in self.order_domain_values(var, assignment):
            # Create a new assignment with this variable-value pair
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            # Check if this assignment is consistent
            if self.consistent(new_assignment):
                # Recursively try to complete the assignment
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        # If no value works, return None (backtrack)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
