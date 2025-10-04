import random

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def play_number_guessing():
    while True:
        # Game intro and range selection
        print(f"{CYAN}🎲 Welcome to Number Guessing Game! 🎲{RESET}")
        print(f"{GREEN}I will think of a number and you have to guess it within a limited number of attempts.{RESET}")
        print(f"{GREEN}{'='*50}{RESET}")
        number_range = input(f"{GREEN}Choose a range. \n1) 1-50\n2) 1-100\n3) 1-200\n4) Custom Range\n{RESET}").lower().strip()
        if number_range == '1' or number_range == '1-50':
            max_number = 50
        elif number_range == '2' or number_range == '1-100':
            max_number = 100
        elif number_range == '3' or number_range == '1-200':
            max_number = 200
        elif number_range == '4' or number_range == 'custom range':
            max_number = int(input(f"{GREEN}Enter the maximum number for your custom range (minimum is 10): {RESET}"))
            if max_number < 10:
                print(f"{YELLOW}Custom range minimum is 10. Setting to 10.{RESET}")
                max_number = 10
        else:
            print(f"{YELLOW}Invalid choice. Setting range to 1-100.{RESET}")
            max_number = 100

        # Difficulty selection
        difficulty = input(f"{GREEN}Choose a difficulty. (This means how many attempts you get) \n1) Easy (10 attempts)\n2) Medium (7 attempts)\n3) Hard (5 attempts)\n{RESET}").lower().strip()
        if difficulty == 'easy' or difficulty == '1':
            max_guesses = 10
        elif difficulty == 'medium' or difficulty == '2':
            max_guesses = 7
        elif difficulty == 'hard' or difficulty == '3':
            max_guesses = 5
        else:
            print(f"{YELLOW}Invalid choice. Setting difficulty to Easy.{RESET}")
            max_guesses = 10

        while True:
            # Generate random number for this round
            number = random.randint(1, max_number)
            guess = 0
            guess_count = 0
            print(f"{GREEN}You have {max_guesses} attempts to guess the number. 🤔{RESET}")
            # Guessing loop
            while guess != number and guess_count < max_guesses:
                try:
                    guess = int(input(f"{GREEN}Enter your guess (between 1 and {max_number}): {RESET}"))
                except ValueError:
                    print(f"{RED}❌ Please enter a valid number.{RESET}")
                    continue
                guess_count += 1
                if guess < 1 or guess > max_number:
                    print(f"{YELLOW}⚠️ Your guess is out of bounds! Please guess a number between 1 and {max_number}.{RESET}")
                    continue
                if guess < number:
                    print(f"{YELLOW}⬆️ Too low! You have {max_guesses - guess_count} guesses left.{RESET}")
                elif guess > number:
                    print(f"{YELLOW}⬇️ Too high! You have {max_guesses - guess_count} guesses left.{RESET}")
                else:
                    print(f"{GREEN}{'='*50}{RESET}")
                    print(f"{CYAN}🎉 You got it! The number was {number}! 🎉{RESET}")
                    break
            # Out of guesses
            if guess_count == max_guesses and guess != number:
                print(f"{GREEN}{'='*50}{RESET}")
                print(f"{RED}💀 You've used all your guesses. The number was {number}.{RESET}")
            # Ask to play again, change settings, or quit
            play_again = input(f"{GREEN}Do you want to try again? Or do you want to choose a different range/difficulty? \n1) Try Again\n2) Change Range/Difficulty\n3) Quit\n{RESET}").lower().strip()
            if play_again == '1':
                continue  # Replay with same settings
            if play_again == '2':
                break     # Change range/difficulty
            elif play_again == '3':
                print(f"{GREEN}{'='*50}{RESET}")
                print(f"{CYAN}👋 Thanks for playing! 👋{RESET}")
                exit()    # Exit the game

play_number_guessing()