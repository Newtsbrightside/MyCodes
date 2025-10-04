'''a = int(input('What is your number? '))
b = int(input('What is your number? '))
c = int(input('What is your number? 1'))
x1 = (-b + (((b ** 2) - (4 * (a * c))) ** 0.5)) / (2*a)
x2 = (-b - (((b ** 2) - (4 * (a * c))) ** 0.5)) / (2*a)
print('The result of your Quadratic Formula equation is, ',x1,'and',x2 )

user_pesos = int(input('How much do you have in pesos? '))
user_soles = int(input('How much do you have in soles? '))
user_reais = int(input('How much do you have in reais? '))
pesos_to_usd = user_pesos / 4012.36
soles_to_usd = user_soles / 3.53
reais_to_usd = user_reais / 5.46
total_usd = reais_to_usd + soles_to_usd + pesos_to_usd
print(total_usd)

butterflies = 10
beetles = 12
ladybugs = 20

print('I caught ' + str(butterflies) + ' 🦋 butterflies!')
print('I caught ' + str(beetles) + ' 🪲 beetles!')
print('I caught ' + str(ladybugs) + ' 🐞 ladybugs!')
total = butterflies + beetles + ladybugs
print('I caught ' + str(total) + ' total bugs!')

height = int(input("What's your height? "))
credits = int(input("How much credits do you have? "))
if height >= 137 and credits >= 10:
  print('Enjoy the ride!')
elif height < 137 and credits >= 10:
  print('You are not tall enough to ride.')
elif height >= 137 and credits < 10:
  print("You don't have enough credits.")
else:
  print("Sorry, but you don't meet the\n requirements to enjoy this ride.")

#Magic 8 Ball
import random
num = random.randint(1, 9)
if num == 1:
  num = 'Yes - definitely.'
elif num == 2:
  num = 'It is decidedly so.'
elif num == 3:
  num = 'Without a doubt.'
elif num == 4:
  num = 'Reply hazy, try again.'
elif num == 5:
  num = 'Ask again later.'
elif num == 6:
  num = 'Better not tell you now.'
elif num == 7:
  num = 'My sources say no.'
elif num == 8:
  num = 'Outlook not so good.'
else:
  num = 'Very doubtful.'
question = input('What is your question? ')
print('The Magic 8 Ball says: ' + str(num))

# Write code below 💖
# Write code below 💖
q1 = int(input('Q1) Do you like Dawn or Dusk? \n1) Dawn \n2) Dusk'))
q2 = int(input('Q2) When I’m dead, I want people to remember me as: \n1) The Good\n2) The Great\n3) The Wise\n4) The Bold'))
q3 = int(input('Q3) Which kind of instrument most pleases your ear? \n1) The violin\n2) The trumpet\n3) The piano\n4) The drum'))
gryffindor = 0
ravenclaw = 0
hufflepuff = 0
slytherin = 0
if q1 == 1:
  gryffindor += 1
  ravenclaw += 1
elif q1 == 2:
  hufflepuff += 1
  slytherin += 1
else:
  print('Wrong input.')
if q2 == 1:
  hufflepuff += 2
elif q2 == 2:
  slytherin += 2
elif q2 == 3:
  ravenclaw += 2
elif q2 == 4:
  gryffindor += 2
else:
  print('Wrong input.')
if q3 == 1:
  slytherin += 4
elif q3 == 2:
  hufflepuff += 4
elif q3 == 3:
  ravenclaw += 4
elif q3 == 4:
  gryffindor += 4
print('Your Score: \nGryffindor: ',str(gryffindor),'\nSlytherin: ',str(slytherin),'\nHufflepuff: ',str(hufflepuff),'\nRavenclaw: ',str(ravenclaw))
if gryffindor > slytherin and gryffindor > hufflepuff and gryffindor > ravenclaw:
  print("You're a Gryffindor!")
elif slytherin > gryffindor and slytherin > hufflepuff and slytherin > ravenclaw:
  print("You're a Slytherin!")
elif hufflepuff > gryffindor and hufflepuff > slytherin and hufflepuff > ravenclaw:
  print("You're a Hufflepuff!")
elif ravenclaw > hufflepuff and ravenclaw > gryffindor and ravenclaw > slytherin:
  print("You're a Ravenclaw!")'''

'''month = int(input('What\'s the month: '))
if month in range(1,4):
  print('Winter 🌨️')
elif month in range(4,7):
  print('Spring 🌱')
elif month in range(7,10): 
  print('Summer 🌻')
elif month in range(10,13):
  print('Autumn 🍂')
else:
  print('Invalid')'''

'''user_weight = float(input("What's your Earth weight? "))
user_planet = int(input("what's your planet destination (in numbers)? "))
if user_planet == 1:
  print('Your weight in Mercury will be: ',user_weight * 0.38)
elif user_planet == 2:
  print('Your weight in Venus will be: ',user_weight * 0.91)
elif user_planet == 3:
  print('Your weight in Mars will be: ',user_weight * 0.38)
elif user_planet == 4:
  print('Your weight in Jupiter will be: ',user_weight * 2.53)
elif user_planet == 5:
  print('Your weight in Saturn will be: ',user_weight * 1.07)
elif user_planet == 6:
  print('Your weight in Uranus is: ',user_weight * 0.89)
elif user_planet == 7:
  print('Your weight in Neptune is: ',user_weight * 1.14)
else:
  print('Invalid planet number.')

user_weight = float(input("What's your Earth weight? "))
user_planet = int(input("what's your planet destination (in numbers)? "))
if user_planet == 1:
  destination_weight = user_weight * 0.38
  print('Your weight in Mercury will be: ',destination_weight)
elif user_planet == 2:
  destination_weight = user_weight * 0.91
  print('Your weight in Venus will be: ',destination_weight)
elif user_planet == 3:
  destination_weight = user_weight * 0.38
  print('Your weight in Mars will be: ',destination_weight)
elif user_planet == 4:
  destination_weight = user_weight * 2.53
  print('Your weight in Jupiter will be: ',destination_weight)
elif user_planet == 5:
  destination_weight = user_weight * 1.07
  print('Your weight in Saturn will be: ',destination_weight)
elif user_planet == 6:
  destination_weight = user_weight * 0.89
  print('Your weight in Uranus is: ',destination_weight)
elif user_planet == 7:
  destination_weight = user_weight * 1.14
  print('Your weight in Neptune is: ',destination_weight)'''

'''print('BANK OF CODÉDEX')

pin = int(input('Enter your PIN: '))

while pin != 2710:
  pin = int(input('Incorrect PIN. Enter your PIN again: '))

if pin == 2710:
  print('PIN accepted!')'''
'''guess = 0
tries = 0

while guess != 6:
  guess = int(input("Guess the number:  "))
  tries += 1
  if tries == 5:
    print('You failed to guess it.')
    break
if guess == 6:
  print('You guessed it in',tries,'tries!')'''
for i in range(99,0,-1):
  print(f'{i} bottles of beer on the wall')
  print(f'{i} bottles of beer')
  print(f'Take one down, pass it around')
  print(f'{i} bottles of beer on the wall')