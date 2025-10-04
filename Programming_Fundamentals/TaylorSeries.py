import math
print("This program approximates the mathematical constant e using its Taylor series expansion.")
print("The series is given by: e = 1 + 1/1! + 1/2! + 1/3! + ... + 1/n!")
print("You will be prompted to enter the number of terms (n) to include in the approximation.")
print("The more terms you include, the closer the approximation will be to the actual value of e.")
print("Let's get started!")
print("="*50)

def approximate_e(n):

    e_value = 0.0
    
    for i in range(n + 1):
        # Calculate each term: 1/i!
        term = 1 / math.factorial(i)
        e_value += term
    
    return e_value

def main():
    # Get input from user
    n = int(input("Enter the number of terms (n): "))
    
    # Calculate approximation
    result = approximate_e(n)
    
    # Display results
    print(f"Approximation of e using {n} terms: {result}")
    print(f"Actual value of e: {math.e}")
    print(f"Difference: {abs(math.e - result)}")
    print("="*50)
    print("Thank you for using the Taylor series approximation program!")

# Run the program
if __name__ == "__main__":
    main()