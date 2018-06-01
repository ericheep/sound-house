primes = [2, 1.5, 1.25, 1.75, 1.375, 1.625] # len = 6, 2nd to last index = 4

def get_pair(user_list, index_1):
    first_pair = user_list[index_1:index_1 + 2]
    return first_pair

prime_progression = 0
print(get_pair(primes, prime_progression))

while True:
    direction = input("1. left 2. right: ")
    if direction == '1':
        prime_progression -= 1
        if prime_progression < 0:
            prime_progression = 0
    elif direction == '2':
        prime_progression += 1
        if prime_progression > (len(primes) - 2):
            prime_progression = len(primes) - 2
    prime_pair = get_pair(primes, prime_progression)
    print(prime_pair)