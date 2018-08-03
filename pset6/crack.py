import sys
import crypt


def main():
    if len(sys.argv) == 2:
        hashedPwd = sys.argv[1]
    else:
        print("Usage: python crack.py 'hash'")
        return 1

    charset = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    salt = '50'

    # For loop that compares each character's hash against the entered password's hash. #
    # The next for loops adds 1 char before performing the hashing function and then compare. #

    for i in range(len(charset)):
        # Initialize 'pwd' with charset[i] to go over the entire charset.
        pwd = charset[i]
        # If the (pwd + salt) hash == input hash = PROFIT!
        if (crypt.crypt(pwd, salt)) == hashedPwd:
            print("CRACKED!")
            print(f"The password is: {pwd}")
            sys.exit()

    for i in range(len(charset)):
        for j in range(len(charset)):
            pwd = charset[i] + charset[j]
            if (crypt.crypt(pwd, salt)) == hashedPwd:
                print("CRACKED!")
                print(f"The password is: {pwd}")
                sys.exit()

    for i in range(len(charset)):
        for j in range(len(charset)):
            for k in range(len(charset)):
                pwd = charset[i] + charset[j] + charset[k]
                if (crypt.crypt(pwd, salt)) == hashedPwd:
                    print("CRACKED!")
                    print(f"The password is: {pwd}")
                    sys.exit()

    for i in range(len(charset)):
        for j in range(len(charset)):
            for k in range(len(charset)):
                for m in range(len(charset)):
                    pwd = charset[i] + charset[j] + charset[k] + charset[m]
                    if (crypt.crypt(pwd, salt)) == hashedPwd:
                        print("CRACKED!")
                        print(f"The password is: {pwd}")
                        sys.exit()

    for i in range(len(charset)):
        for j in range(len(charset)):
            for k in range(len(charset)):
                for m in range(len(charset)):
                    for n in range(len(charset)):
                        pwd = charset[i] + charset[j] + charset[k] + charset[m] + charset[n]
                        if (crypt.crypt(pwd, salt)) == hashedPwd:
                            print("CRACKED!")
                            print(f"The password is: {pwd}")
                            sys.exit()

    ## TODO ##
    '''
        - Find the way to use less repetitive code by implementing (maybe) a recursive solution.
        - The solution in for loops 4 and 5 takes too much time and sometimes freezes the cpu. 
    '''
    ## RESULTS ##
    '''
        anushree:50xcIMJ0y.RXo	YES
        brian:50mjprEcqC/ts	    CA
        bjbrown:50GApilQSG3E2	UPenn
        lloyd:50n0AAUD.pL8g	    lloyd
        malan:50CcfIk1QrPr6 	maybe
        maria:509nVI8B9VfuA	    TF
        natmelo:50JIIyhDORqMU	nope
        ROFL = 50JGnXUgaafgc	ROFL
        stelios:51u8F0dkeDSbY	NO   
        zamyla:50cI2vYkF0YU2	LOL
    '''

if __name__ == "__main__":
    main()