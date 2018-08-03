from cs50 import get_string
import sys


def main():
    if len(sys.argv) == 2:  # Check if an arg is passed to the program
        k = sys.argv[1]
        k = int(k)

        print("Plaintext: ", end="")
        s = list(get_string())  # Creates a list from the user's string input

        for i in range(len(s)):
            if s[i].isalpha():  # Check for alphanumerical chars
                if s[i].isupper():  # Check for uppercase chars
                    if k < 26:
                        '''
                            ord function returns the ascii value of an aplhabetical character
                            chr function is the opposite to ord
                        '''
                        s[i] = chr(ord(s[i]) + k)
                    else:
                        s[i] = chr(ord(s[i]) + k % 26)
                elif s[i].islower():  # Check for lowercase chars
                    if k < 26:
                        s[i] = chr(ord(s[i]) + k)
                    else:
                        s[i] = chr(ord(s[i]) + k % 26)
            else:
                s[i] = s[i]

        a = ''
        a = a.join(s)
        print(f"Ciphertext: {a}")

    else:
        print("Usage: python caesar.py k")
        return 1


if __name__ == "__main__":
    main()