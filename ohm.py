import random

def generate_question():
    """Generates a random Ohm's Law question."""
    components = ['V', 'I', 'R']
    missing = random.choice(components)
    
    if missing == 'V':
        I = round(random.uniform(0.1, 10), 2)  # Random current (0.1A to 10A)
        R = round(random.uniform(1, 100), 2)   # Random resistance (1Ω to 100Ω)
        answer = round(I * R, 2)
        return f"Current = {I}A, Resistance = {R}Ω. Find Voltage (V)?", answer
    elif missing == 'I':
        V = round(random.uniform(1, 100), 2)   # Random voltage (1V to 100V)
        R = round(random.uniform(1, 100), 2)   # Random resistance (1Ω to 100Ω)
        answer = round(V / R, 2)
        return f"Voltage = {V}V, Resistance = {R}Ω. Find Current (I)?", answer
    else:
        V = round(random.uniform(1, 100), 2)   # Random voltage (1V to 100V)
        I = round(random.uniform(0.1, 10), 2)  # Random current (0.1A to 10A)
        answer = round(V / I, 2)
        return f"Voltage = {V}V, Current = {I}A. Find Resistance (R)?", answer

def play_game():
    """Runs the Ohm's Law Puzzle game."""
    score = 0
    rounds = 5  # Number of rounds per game
    
    print("Welcome to the Ohm's Law Puzzle Game!")
    print("Solve the given Ohm's Law equations correctly to earn points.")
    
    for _ in range(rounds):
        question, correct_answer = generate_question()
        print("\n" + question)
        
        try:
            user_answer = float(input("Your answer: "))
            if abs(user_answer - correct_answer) < 0.1:  # Allowing small margin for floating point rounding
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. The correct answer was {correct_answer}")
        except ValueError:
            print(f"❌ Invalid input. The correct answer was {correct_answer}")
    
    print(f"\nGame Over! Your final score: {score}/{rounds}")
    
if __name__ == "__main__":
    play_game()
