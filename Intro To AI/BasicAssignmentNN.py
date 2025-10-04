import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
def tanh(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))
def relu(x):
    return max(0, x)
def neuron_output(x, w, b, activation="sigmoid"):
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    if activation == "sigmoid":
        return sigmoid(z)
    elif activation == "tanh":
        return tanh(z)
    elif activation == "relu":
        return relu(z)
    else:
        raise ValueError("Unsupported activation function")

print("Basic Neuron Output Calculation with Different Activation Functions")
print("Let's compute the output of a single neuron using sigmoid, tanh, and ReLU activation functions.")
print("=" *60)

while True:
    try:
        x = list(map(float, input("Enter input values (comma-separated): ").strip().split(',')))
        w = list(map(float, input("Enter weight values (comma-separated): ").strip().split(',')))
        b = float(input("Enter bias value: ").strip())
        activation = input("Enter activation function (sigmoid, tanh, relu): ").strip().lower()
        output = neuron_output(x, w, b, activation)
        print(f"\nNeuron output with {activation} activation: {output}")
    except Exception as e:
        print("Error:", e)
        continue

    again = input("Do you want to try again (y/n)? ").strip().lower()
    if again != 'y':
        break

print("=" *60)
print("End of Basic Neuron Output Calculation")
print("Thank you for using the program!")