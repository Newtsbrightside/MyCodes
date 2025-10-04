#666 Assignment
print("This program calculates the sum of the series 6 + 66 + 666 + ... up to n terms.")
print("For example, if n = 3, the series is 6 + 66 + 666.")
print("Let's try it out!")
print("="*50)
n=int(input("Enter a number (n): "))
value = 0
total = 0
for i in range(n):
    value = value * 10 + 6
    total += value
print("The sum is:", total)
print("="*50)
print("Thank you for using the program!")