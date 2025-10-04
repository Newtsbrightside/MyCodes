# movie = ['Harry Potter','Avenger','Dune']
# new_movie = input('What are you watching? ').split()
# movies = movie + new_movie
# print(movies)
'''def get_score_from_user():
    mid_final_hw = input('Enter the student\' mid-term, final, and homework score (Three Scores e.g. 75 90 80): ').split()
    # Convert each string in the list to float
    mid_final_hw = [float(score) for score in mid_final_hw]
    score = mid_final_hw[0]*0.3 + mid_final_hw[1]*0.4 + mid_final_hw[2]*0.3
    print(f'The student average score is {score}')
    print(f'The student mid-term score is: {mid_final_hw[0]}\nThe final score is: {mid_final_hw[1]}\nThe homework score is: {mid_final_hw[2]}')

get_score_from_user()
#Practice #1
num = int(input('Enter a number: '))
factors = []
for i in range(1, num+1):
    if num % i == 0:
        factors.append(i)
print(factors)'''

#Practice #2
numbers = [int(x) for x in input('Enter numbers separated by spaces: ').split()]
divisor = int(input('Enter a divisor: '))
sum = 0
for number in numbers:
    if number % divisor == 0:
        sum += number
print(f'The sum of numbers divisible by {divisor} is: {sum}')
