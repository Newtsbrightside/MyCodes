print('Welcome to Prime Number Sum Calculator!')
print('This program will sums all the prime numbers between the given two number.')
print('='*30)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

A, B = map(int, input('Input two numbers: ').split())
sum = 0
for n in range(A,B+1):
    if is_prime(n):
        sum += n
print(f'The sum of your prime numbers is, {sum}!')
print('='*30)
print('Thank you for using this program!')