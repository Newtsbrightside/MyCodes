def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
print('Welcome to Goldbach Conjecture Checker!')
print('This program will find two prime numbers that sum up to the given even number greater than 2.')
print('='*50)
while True:
    while True:
        N = int(input('Enter an even number larger than 2: '))
        if N > 2 and N % 2 == 0:
            break
        print('Please enter even number larger than 2.')
    for A in range(2,N):
        if is_prime(A):
            B = N - A
            if is_prime(B):
                print(f'{N} = {A} + {B}')
                break
    print('='*50)
    print('Thank you for using this program!')
    if input('Would you like to try another number? (y/n): ').lower().strip() != 'y':
        break
    