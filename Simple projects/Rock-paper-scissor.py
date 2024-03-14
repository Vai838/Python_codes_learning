import random

print("Welcome to Rock-Paper-Scissor game!")

while True:
    move = input("Choose your move (r for rock, s for scissor and p for paper):")
    valid_moves = ['r', 's', 'p']

    if move not in valid_moves:
        print("Invalid input. Please enter 'r', 'p' or 's'")
    else:
        print("You have chosen: ", move)

        choices = ['rock', 'paper', 'scissor']
        comp_move = random.choice(choices)

        if move == "r":
            move = "rock"
        elif move == "p":
            move = "paper"
        else:  # No need for "elif move == 's':" as it's the only option left
            move = "scissor"

        if comp_move == "rock" and move == "paper":
            print("Computer have chosen rock!\n You win!")
        elif comp_move == "paper" and move == "scissor":
            print("Computer have chosen paper!\n You win!")
        elif comp_move == "scissor" and move == "rock":
            print("Computer have chosen paper!\n You win!")
        elif comp_move == move:  # Simplified draw condition
            print(f"Computer have chosen {comp_move}!\n Draw!")
        else:  # Covers all remaining win cases
            print(f"Computer have chosen {comp_move}!\n You win!")

        inp = input("Do you wish to have another try? (y/n): ")
        if inp != 'y':
            print("You have not chosen 'y'. Thanks for playing with me!. See ya!")
            break

