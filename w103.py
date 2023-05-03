import sys
import math
if __name__ == "__main__":
    a = int(sys.argv[1]) 
    b = int(sys.argv[2]) 
    c = int(sys.argv[3])
    
    D = b * b - 4 * a * c
    if D > 0:
        print(int(0.5 * (math.sqrt(float(D)) - b) / a))
        print(int(0.5 * (-math.sqrt(float(D)) - b) / a))

