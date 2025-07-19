import random

a = int(input("enter a nubmer: "))
b = random.randrange(1,3)
if a == b:
    print("guess correct won ")
print(f"the number is {b}")