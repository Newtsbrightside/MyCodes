#Average Calculator
total = 0
count = 0
print("This program calculates the average of numbers you enter.")
print("If you want to stop entering numbers, type a negative number.")
print("="*50)
while True:
    user_input = input("Enter a number or negative number to finish: ")
    if user_input.lower() == 'done':
        break
    try:
        number = float(user_input)
        if number < 0:
            print("Negative number entered. Stopping input.")
            break
        total += number
        count += 1
    except ValueError:
        print("Invalid input. Please enter a valid number.")
average = total / count
print(f"The average of the entered numbers is: {average:.2f}")
print("="*50)
print("Thank you for using the average calculator!")