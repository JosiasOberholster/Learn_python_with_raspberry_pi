choices = {1:"Start", 2:"Edit", 3:"Quit"}
for key, value in choices.items():
    print("Press ", key, " to ", value)

user_input = input("Enter choice: ")

if user_input in choices.values():
    print("You chose", choices[user_input])
else:
    print("Unknown choice")
