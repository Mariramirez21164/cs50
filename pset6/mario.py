from cs50 import get_int

def main():
    print("Input the pyramid's height: ")
    
    n = get_int()
    while n < 0 or n > 60:
        print("Error. Please input again: ")
        n = get_int()
    
    for a in range(n):
        for b in range(n-a):
            print(" ", end="")
        for c in range(a+2):
            print("#", end="")
        print("  ", end="")
        for c in range(a+2):
            print("#", end="")
        print("")

if __name__ == "__main__":
    main()