import sys

if __name__ == "__main__":

    digit_string = sys.argv[1]
    s = 0
    for i in range(0,len(digit_string)):
        s += int(digit_string[i])
    print(s)