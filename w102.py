import sys

N = int(sys.argv[1])

def string(number):
    string = ''
    for j in range(0, N - number):
        string += ' '
    for j in range(0, number):
        string += '#'
    print(string)
       
if __name__ == "__main__":
    for i in range(1, N + 1):
        string(i)
