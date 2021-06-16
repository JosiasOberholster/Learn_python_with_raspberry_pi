import random

secret = int(random.uniform(0,10))
print("I'm thinking of a number between zero ad ten.", "Can you guess what it is?")
guess = 11

while guess != secret:  
    try:
        guess = int(input("Take a guess: "))
    except ValueError:
        print("Supply a interger, not a character")
    if guess != secret:
        print("You guessed wrong")
    
print("Well done!")