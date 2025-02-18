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
def suggest_next_equation(previous_guesses, feedback, equation_pool):
    # Step 1: Filter the equation pool based on feedback
    filtered_pool = filter_equations_again(equation_pool, previous_guesses, feedback)
    
    # Step 2: Rank equations by information gain
    ranked_equations = rank_equations(filtered_pool)
    
    # Step 3: Return the equation with the highest score
    return ranked_equations[0]

def filter_equations_again(equation_pool, previous_guesses, feedback):
    filtered_pool = []
    for equation in equation_pool:
        if matches_feedback(equation, previous_guesses, feedback):
            filtered_pool.append(equation)
    return filtered_pool

def matches_feedback(equation, previous_guesses, feedback):
    # Implement logic to check if the equation matches all feedback constraints
    pass

def rank_equations(equation_pool):
    ranked = []
    for equation in equation_pool:
        score = calculate_information_gain(equation, equation_pool)
        ranked.append((equation, score))

    # Sort by score in descending order
    ranked.sort(key=lambda x: x[1], reverse=True)
    return [eq for eq, score in ranked]

def calculate_information_gain(equation, equation_pool):
    """
    Calculate the information gain of a given equation by simulating feedback scenarios
    and counting how many equations in the pool would remain valid for each scenario.
    """
    from collections import defaultdict
    import math

    # Simulate all possible feedback scenarios for the given equation
    feedback_counts = defaultdict(int)

    for possible_equation in equation_pool:
        # Simulate feedback for this equation compared to the possible_equation
        feedback = simulate_feedback(equation, possible_equation)
        feedback_counts[feedback] += 1

    # Calculate the entropy of the feedback distribution
    total_equations = len(equation_pool)
    entropy = 0.0

    for count in feedback_counts.values():
        probability = count / total_equations
        entropy -= probability * math.log2(probability)

    # The information gain is the entropy of the feedback distribution
    return entropy

def simulate_feedback(guess, target):
    """
    Simulate feedback for a guess compared to a target equation.
    Returns a tuple representing the feedback:
    - Correct characters in the correct position
    - Correct characters in the wrong position
    - Incorrect characters
    """
    correct_position = []
    correct_char_wrong_position = []
    incorrect_characters = []

    for i in range(len(guess)):
        if guess[i] == target[i]:
            correct_position.append((guess[i], i))
        elif guess[i] in target:
            correct_char_wrong_position.append((guess[i], i))
        else:
            incorrect_characters.append(guess[i])

    return (tuple(correct_position), tuple(correct_char_wrong_position), tuple(incorrect_characters))

def main():
    clues = ["1", "*", "5", "0"]  # All the entered clused that you know appear in the final result. right num in wrong position and right in right position. Order does not matter. Doesn't need to include the = since all include that.
    known_positions = ["", "", "", "", "", "", "", "5"] #Only includes the right number in the right position. If the = is in the right spot, place that here.
    known_wrong_positions = [[""], ["1"], ["*"], ["*", "5"], ["="], ["=", "1"], ["0"], ["1"]] #Place results from attempts here. Create a list for each slot based on the accumulated clues 
    known_wrong = ["2", "+", "3", "4", "6", "7"] #Enter all the numbers and operators that you know aren't in the final result.
    print("Generating equations...")
    print("Clues:", clues)
    # equations = generate_equations()
    equations = open('./nerdle.txt', 'r').read().splitlines()
    possible_solutions = filter_equations(equations, clues, known_positions, known_wrong, known_wrong_positions)
    
    print("Possible solutions:", len(possible_solutions))

    ranked_solutions = rank_equations(possible_solutions)
    for solution in ranked_solutions:
        print(solution)
    
    #TODO: Make entering the clues more user friendly
    #TODO: Create an algorithm that can prioritize the most likely solutions

if __name__ == "__main__":
    main()
