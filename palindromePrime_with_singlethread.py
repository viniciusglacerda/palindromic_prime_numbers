import httpx
import json
import os
import time

def getNumber(n_start, length_group, number_base = 10):
  num = json.loads(httpx.get(f'https://api.pi.delivery/v1/pi?start={n_start}&numberOfDigits={length_group}&radix={number_base}').content)
  num = num['content']
  return num

def getGroupNumbers(string_, start_position, length_group):
  new_string = ""
  for position in range(0, length_group):
    new_string = new_string + string_[start_position + position]
  
  return new_string


def isPalindrome(string):
    for i in range(0, int(len(string)/2)): 
        if string[i] != string[len(string)-i-1]:
            return False
    return True

def isPrime(number):
    if (number <= 1): 
        return False
        
    if (number <= 3):
        return True
    
    if (number % 2 == 0 or number % 3 == 0): 
        return False

    i = 5
    while(i * i <= number): 
        if (number % i == 0 or number % (i + 2) == 0): 
            return False
        i = i + 6
    return True

def main():
    start = time.time()

    os.system('clear') or None
    print("Calculating palindrome and Prime within the decimal expansion of PI")

    # grp_digits = 4129318
    grp_digits = 0
    length_search = 1000
    length_group = 9
    num = getNumber(grp_digits, length_search)
    indice = 0

    print(num)
    while True:
        os.system('clear') or None
        try:
          if indice == (len(num) - length_group):
            num = getNumber(grp_digits, length_search)
            indice = 0
          else:
          
            group = getGroupNumbers(num, indice, length_group)

            print(f"Current sequence: {group}")
            print(f"Current number group: {grp_digits}")

            if isPalindrome(group):
                print(f"    Palindrome: True\n")
                if isPrime(int(group)):
                    os.system('clear') or None
                    print("\n\n##########################################################################################################")
                    print(f"\n    The first palindrome and prime number within the expansion of pi is: {group}")
                    print("\n##########################################################################################################")
                    break

                else:
                    print(f"    Prime: False\n")
            else:
                print(f"    Palindrome: False\n")
            
            indice += 1
            grp_digits += 1

          # time.sleep(0.1)
        except Exception as error:
            print(f"Error: {error}\n")
            print(f"Last sequence: {group}")
            print(f"Last number group: {grp_digits}")
            break

    end = time.time()
    print(f"Runtime: {end - start}s")


if __name__ == '__main__':
    main()