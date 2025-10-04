'''i = 0

while i < 6:
  j = 0
  while j < 6:
    print(i * j)
    j = j + 1
  i = i + 1'''


'''import random

lucky_number = random.randint(1, 9)
not_found = True

while not_found:
  for i in range(1, 10):
    if i == lucky_number:
      not_found = False
      break
    else:
      print(i)

print(f"Yay I got my lucky number {lucky_number}! 🍀")'''

'''for i in range(10,0,-1):
    print(i)
print("Happy New Year! 🎉")'''

'''import random
not_snakeeyes = True
while not_snakeeyes:
  die1 = random.randint(1,6)
  die2 = random.randint(1,6)
  total = die1 + die2
  while total != 2:
   print('Nope')
   break
  if total == 2:
    print('Snake eyes!')
    not_snakeeyes = False

for i in range(1,25):
  print ('* ' * i)

number = int(input('What\'s your number? '))
total = 0
for i in range(number + 1):
  i = i * i
  total += i
print(total)'''

'''Friends = ['Wipi', 'Yunus', 'Ghazi']
print(Friends[-1])
'''
'''
todo = ['🏦 Get quarters.','🧺 Do laundry.','🌳 Take a walk.','💈 Get a haircut.','🍵 Make some tea.','💻 Complete Lists chapter.','💖 Call mom.','📺 Watch My Hero Academia.']
print(todo[0])
print(todo[1])
print(todo[2:6])'''
'''movie_names_july = ['Madagascar','Oppenheinmer','Barbie','Kung Fu Panda']
movie_names_july.append('Jurrasic Park')
movie_names_july.copy()
movie_names_august = ['Mission Impossible','Spiderman','Insidious']
movie_names_july.extend(movie_names_august)
movie_names_july.remove('Madagascar')
movie_names_july.sort()
movie_names_july.reverse()
movie_names_july.insert(2,'The Little Mermaid')
movie_names_july.pop(0)
movie_names_july.index('Oppenheinmer')
print( movie_names_july.count('Barbie'))
print( movie_names_july.count('Spiderman'))
print(movie_names_july[4])
print(movie_names_july)
print(len(movie_names_july))
print(min(movie_names_july))
print(max(movie_names_july))
print(movie_names_july[2:5])
print(movie_names_july[:4])
print(movie_names_july[3:])
print(movie_names_july[-1])
print(movie_names_july[-3:])
print(movie_names_july[::2])
print(movie_names_july[1::2])
print(movie_names_july[::-1])
movie_names_july.clear()
print(movie_names_july)
# Write code below 💖
books = ['Harry Potter','1984','The Fault in Our Stars','The Mom Test','Life in Code']
books.append('Pachinko')
books.remove('1984')
books.pop(1)
print(books)'''
# Write code below 💖
# dna_sequence = ['GCT','AGC','AGG','TAA','ACT','CAT','TAT','CCC','ACG','GAA','ACC','GGA']
# item_to_find = 'TT'
# item_found = False
# for i in dna_sequence:
#     if i == item_to_find:
#       item_found = True
# if item_found == True:
#   print('Item Found!')
# else:
#   print('Item not found.')
from Programming_Fundamentals import TaylorSeries
import math
