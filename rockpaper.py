import random

def get_computer_choice():
    # Randomly select the computer's choice
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def get_user_choice():
    # Get the user's choice
    user_choice = input("Enter rock, paper, or scissors: ").lower()
    while user_choice not in ['rock', 'paper', 'scissors']:
        user_choice = input("Invalid choice! Please enter rock, paper, or scissors: ").lower()
    return user_choice

def determine_winner(user_choice, computer_choice):
    # Determine the winner based on the choices
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        return 'user'
    else:
        return 'computer'

def play_game():
    user_score = 0
    computer_score = 0

    while True:
        print("\nRock, Paper, Scissors Game!")
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        
        print(f"\nYou chose: {user_choice}")
        print(f"The computer chose: {computer_choice}")
        
        winner = determine_winner(user_choice, computer_choice)
        
        if winner == 'tie':
            print("It's a tie!")
        elif winner == 'user':
            user_score += 1
            print("You win this round!")
        else:
            computer_score += 1
            print("The computer wins this round!")
        
        print(f"\nCurrent Score - You: {user_score} | Computer: {computer_score}")
        
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

    print(f"\nFinal Score - You: {user_score} | Computer: {computer_score}")
    print("Thanks for playing!")

# Start the game
if __name__ == "__main__":
    play_game()
