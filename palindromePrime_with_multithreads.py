import httpx
import json
import os
import time
import threading

grp_digits = 0
palindromePrime = None

def increment():
    global grp_digits

    grp_digits += 1

def addInformationPalindromePrime(thread, number_group, number):
    global palindromePrime
    palindromePrime = {
        "thread": thread,
        "number_group": number_group,
        "number": number
    }

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

def threadTask(n_digit, lock, threadName):
    global palindromePrime

    if palindromePrime == None:
        num = json.loads(httpx.get(f'https://api.pi.delivery/v1/pi?start={n_digit}&numberOfDigits=9&radix=10').content)
        num = num['content']

        print(f"\n\nThread Name: {threadName}")
        print(f"Current sequence: {num}")
        print(f"Current number group: {n_digit}")

        if isPalindrome(num):
            print(f"    Palindrome: True\n")
            if isPrime(int(num)):
                lock.acquire()
                addInformationPalindromePrime(threadName, n_digit, num)
                lock.release()
                return
            else:
                print(f"    Prime: False\n")

        else:
            print(f"    Palindrome: False\n")

        lock.acquire()
        increment()
        lock.release()
    else:
        return

def main():
    lock = threading.Lock()

    t1 = threading.Thread(target=threadTask, args=(grp_digits, lock, "Thread_1"))
    t2 = threading.Thread(target=threadTask, args=(grp_digits + 1, lock, "Thread_2"))
    t3 = threading.Thread(target=threadTask, args=(grp_digits + 2, lock, "Thread_3"))
    t4 = threading.Thread(target=threadTask, args=(grp_digits + 3, lock, "Thread_4"))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

if __name__ == '__main__':
    start = time.time()
    while True:
        if palindromePrime == None:
            main()
        else:
            os.system('clear') or None
            threadName = palindromePrime["thread"]
            group = palindromePrime["number_group"]
            number = palindromePrime["number"]

            print("First nine-digit prime Palindrome number in the expansion of pi:\n")
            print(f"Thread: {threadName}")
            print(f"Group_Numbers: {group}")
            print(f"Palindrome_Prime_Number: {number}")
            break
        
    end = time.time()
    print(f"\nRuntime: {end - start}s")
