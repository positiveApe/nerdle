import itertools
import re

def generate_equations():
    operators = ['+', '-', '*', '/', '=']
    numbers = [str(i) for i in range(10)]
    equations = []

    # Generate all possible combinations of numbers and operators
    for comb in itertools.product(numbers + operators, repeat=8):
        equation = ''.join(comb)
        if is_valid_equation(equation):
            equations.append(equation)
            print(equation)
            # Open a file in append mode
            with open('nerdle.txt', 'a') as file:
                file.write('\n' + equation)
    
    return equations

def is_valid_equation(equation):
    try:
        # Split the equation into left and right parts
        left, right = equation.split('=')
        
        # Ensure the left side contains at least one valid operator (+, -, *, /)
        if not re.search(r"[+\-*/]", left):
            return False
        
        # Ensure the formula doesn't contain illegal sequences (** or // or ++ or --)
        if re.search(r"(\*\*|//|\+\+|--)", left):
            return False
        
        # Ensure the formula doesn't contain illegal sequences (** or // or ++ or --)
        if re.search(r"(\*\*|//|\+\+|--|-\+|\+-|\*\+|\+\*|-\*|\*-|-/|/-|/\+|\+/)", left):
            return False

        # Ensure the formula doesn't contain illegal sequences (** or // or ++ or --)
        if "*0" in left or "*0/" in left or "+0/" in left or "-0/" in left or "+0" in left or "-0" in left:
            return False
        
        # Ensure the right side contains no operators (+, -, *, /)
        if re.search(r"[+\-*/]", right):
            return False
        
        if left.strip().startswith(("+", "-", "00", "0")):
            return False
        
        if re.search(r"\b0\d+", right.strip()):
            return False
        
        # Evaluate both sides and check if they are equal
        return eval(left) == int(right)
    except:
        return False

def filter_equations(equations, clues, known_positions, known_wrong, known_wrong_positions):
    filtered = []
    for eq in equations:
        if matches_clues(eq, clues, known_positions, known_wrong, known_wrong_positions):
            filtered.append(eq)
    return filtered

def matches_clues(equation, clues, known_positions, known_wrong, known_wrong_positions):
    for clue in clues:
        if clue not in equation:
            return False
    for wrong in known_wrong:
        if wrong in equation:
            return False

    for i, char in enumerate(known_wrong_positions):
        if equation[i] in known_wrong_positions[i]:
            return False
    
    for i, char in enumerate(known_positions):
        if known_positions[i] == "":
            continue
        if known_positions[i] != equation[i]:
            return False
    return True

def main():
    clues = ["1", "*", "2", "0"]  # Example clues
    known_positions = ["", "", "", "", "", "1", "", ""]
    known_wrong_positions = [[""], ["*"], ["2"], ["*", "1"], ["="], ["="], ["0"], ["1"]]
    known_wrong = ["7", "+", "6", "3", "4", "5"]
    print("Generating equations...")
    print("Clues:", clues)
    # equations = generate_equations()
    equations = open('nerdle.txt', 'r').read().splitlines()
    possible_solutions = filter_equations(equations, clues, known_positions, known_wrong, known_wrong_positions)
    
    print("Possible solutions:")
    for solution in possible_solutions:
        print(solution)

if __name__ == "__main__":
    main()
