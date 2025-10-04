import random
import time
import math
class Random:
    def random_number(self, start, end):
        return random.randint(start, end)
rand = Random()
print("Random number between 1 and 10:", rand.random_number(1, 10))
time.sleep(1)
print("Random number between 20 and 30:", rand.random_number(20, 30))
time.sleep(1)
print("Random number between 100 and 200:", rand.random_number(100, 200))


'''
print("Can we go outside today?")
weather = input("Enter the weather (sunny, rainy, snowy, windy): ").strip().lower()
if weather == "sunny":
    print("Yes, it's a great day to go outside!")
elif weather == "rainy":
    print("No, it's better to stay indoors and read a book.")
elif weather == "snowy":
    print("Yes, but make sure to dress warmly!")
elif weather == "windy":
    print("Maybe, but be careful of falling branches.")
else:
    print("I'm not sure about that weather condition.")
    '''
'''

username = ("Fai")
password = ("faiuph2025!")
input_username = input("Enter your username: " ).strip()
input_password = input("Enter your password: " ).strip()
if input_username == username and input_password == password:
    print("Login successful! Welcome back, " + username + ".")
else:
    print("Login failed! Please check your username and password.")
    '''
'''
welcome_message = "Welcome to Age Category Classifier!"
print(welcome_message)
age = int(input("Please enter your age: ").strip())
if age < 0:
    print("Invalid age. Please enter a valid age.")
elif age <= 12:
    print("You are a child.")
elif age <= 19:
    print("You are a teenager.")
elif age <= 64:
    print("You are an adult.")
else:
    print("You are a senior.")
print("Thank you for using the Age Category Classifier!")
'''

'''print("Welcome to Number Comparison Program!")
num1 = float(input("Enter the first number: ").strip())
num2 = float(input("Enter the second number: ").strip())
num3 = float(input("Enter the third number: ").strip())
if num1 >= num2 and num1 >= num3:
    largest = num1
elif num2 >= num1 and num1 >= num3:
    largest = num2
else:
    largest = num3
print("The largest number is:", largest)
print("Thank you for using the Number Comparison Program!")'''

'''# FizzBuzz program
print("Welcome to the FizzBuzz Program!")
number = int(input("Enter a number: ").strip())
if number % 3 == 0 and number % 5 == 0:
    print("FizzBuzz")
elif number % 3 == 0:
    print("Fizz")
elif number % 5 == 0:
    print("Buzz")
else:
    print(number)
print("Thank you for using the FizzBuzz Program!")'''

# Print Number Pattern
'''print("Welcome to the Number Pattern Printer!")
n = int(input("Enter a positive integer: ").strip())
if n <= 0:
    print("Please enter a positive integer.")
else:
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(j, end=" ")
        print()
print("Thank you for using the Number Pattern Printer!")'''

# Count Numbers
'''for i in range(1, 11):
    print(i)
print("Counting complete!")'''

# Print Squares as Asterisks
'''print("Welcome to the Square Printer!")
n = int(input("Enter the size of the square (positive integer): ").strip())
if n <= 0:
    print("Please enter a positive integer.")
else:
    for i in range(n):
        print("* " * n)
print("Thank you for using the Square Printer!")'''

# Print 5 Squares as Asterisks
'''n = 3
for i in range(n):
    print("* " * n)'''

'''def over_nine_thousand(lst):
  i = 0
  if len(lst) == 0:
    return 0
  elif sum(lst) < 9000:
    return sum(lst)
  while i <= 9000:
    for value in lst:
      if i > 9000:
        break
      i += value
    return i
print(over_nine_thousand([8000, 900, 120, 5000]))  # Output: 9020
print(over_nine_thousand([100, 200, 300]))          # Output: 600
print(over_nine_thousand([]))                        # Output: 0'''

'''num = int(input("Enter a number: ").strip())
while num < 10:
    for i in range(num):
        print("*" * num)
    num += 3
    if num >= 10:
        break'''

# Print Number Pattern as Asterisks
'''print("Welcome to the Number Pattern Printer!")
n = int(input("Enter a positive integer: ").strip())
if n <= 0:
    print("Please enter a positive integer.")
else:
    for i in range(1, n + 1):
        print("* " * i)
print("Thank you for using the Number Pattern Printer!")'''

# Practice #3
'''n = int(input("Enter a positive integer: ").strip())
for i in range(1, n + 1):
        print("* " * i)'''

# Practice #4 Factorial
'''n=int(input("Enter a positive integer: ").strip())
factorial=1
for i in range(1,n+1):
    factorial=factorial*i
print("The factorial of",n,"is",factorial)'''

# Practice #5 Counting Vowels
'''vowels = "aeiouAEIOU"
string = input("Enter a string: ").strip()
count = 0
for char in string:
    if char in vowels:
        count += 1
print("Number of vowels in the string:", count)'''

# Practice #6 Fibonacci Sequence
'''n = int(input("Enter the number of terms in the Fibonacci sequence: "))
a, b = 0, 1
print("Fibonacci sequence:")
for _ in range(n):
    print(a, end=" ")
    a, b = b, a + b
print()'''

# Practice #7 Print Maximum Number
'''num = int(input("Enter an integer (or -1 to stop): ").strip())
max_num = None
while num != -1:
    if max_num is None or num > max_num:
        max_num = num
    num = int(input("Enter an integer (or -1 to stop): ").strip())
if max_num is not None:
    print("The maximum number entered is:", max_num)
else:
    print("No numbers were entered.")'''

# The Professor's Solution
'''number = 0
maxnum = -100
while number != -1:
    number = input("Please enter a number: ").strip()
    number = int(number)
    if number >= maxnum:
        maxnum = number
print("The maximum number is:", maxnum)'''

'''import math
method = input(">>>>> Please type in your activation method! ('TanH', 'ReLU', or 'Sigmoid'): <<<<< ").strip().lower()

if method == 'tanh':
    x = int(input("Input an integer to the TanH function: "))
    tanH = ((math.exp(x)) - (math.exp(-x))) / ((math.exp(x)) + (math.exp(-x)))
    print("TanH result:", tanH)
elif method == 'relu':
    x = int(input("Input an integer to the ReLU function: "))
    ReLU = max(0, x)
    print("ReLU result:", ReLU)
elif method == 'sigmoid':
    x = int(input("Input an integer to the sigmoid function: "))
    sigmoid_x = 1 / (1 + math.exp(-x))
    print("Sigmoid result:", sigmoid_x)
else:
    print("Invalid activation method. Please choose 'TanH', 'ReLU', or 'Sigmoid'.")'''

#calculate the area of a rectangle
'''def calculate_area():
    area = length * width
    return area
length = float(input("Enter the length of the rectangle: ").strip())
width = float(input("Enter the width of the rectangle: ").strip())
result = calculate_area()
print("The length of the rectangle is:", length, "and the width is:", width, "so the area is:", result)'''

#calculate division result
'''def calculate_division(divisor, dividend):
    result = dividend / divisor
    return result
divisor_value = float(input("Enter the divisor: ").strip())
dividend_value = float(input("Enter the dividend: ").strip()
division_result = calculate_division(divisor_value, dividend_value)
print("The result of the division is:", division_result)'''

'''def azy_begadang():
    if begadang is True:
        return "Azy butuh tidur 24 jam"
    if begadang is False:
        return "Azy ga butuh tidur"
        
# Test change to trigger Git detection
begadang_apa_ngga = input("Azy begadang? (True/False): ").strip().lower()
begadang = begadang_apa_ngga.startswith('y') or begadang_apa_ngga.startswith('t')
print(azy_begadang())'''