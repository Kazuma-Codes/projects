import random # used to get random values

while True:
    choices = ["rock", "paper","scissor"]
    player = None

    computer = random.choice(choices) # allows the program to select a random value of the list
    while player not in choices :
        player = input("enter rock, paper, scissor: ").lower()


    print("computer picks "+computer)
    print("player picks "+player)
    if computer == player:
     print("draw")
    elif computer == "rock" :
        if player == "scissor" :
            print ("you lose") 
        if player == "paper" :
            print ("you win")

    elif computer == "scissor" :
        if player == "paper" :
            print ("you lose") 
        if player == "rock" :
            print ("you win")

    elif computer == "paper" :
        if player == "scissor" :
            print ("you win") 
        if player == "rock" :
            print ("you lose")

    play_again = input("play again Y/N: ").lower()
    if play_again != "y":
        break
print("Bye")