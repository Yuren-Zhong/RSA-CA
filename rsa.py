import random

def encryptstr(msg, e, n):
    if len(msg) > 128:
        return -1
    l = list(map(ord, msg)) + [0 for i in range(0, 128-len(msg))]

    M = 0
    for i in range(0, 128):
        M = (M << 8) + l[i]

    return expmod(M, e, n)

def decryptstr(C, d, n):
    M = expmod(C, d, n)
    l = [0 for i in range(0, 128)]
    for i in range(0, 128):
        l[127 - i] = M & 255
        M >>= 8
    for i in range(0, 128): 
        if l[127 - i] != 0:
            l = l[0: -i]
            break

    return "".join(list(map(chr, l)))

def miller_rabin(n):
    a = random.randint(2, n-2)

    t = 0
    d = n - 1
    while d & 1 == 0:
        d >>= 1
        t += 1

    x = expmod(a, d, n)
    for i in range(0, t):
        y = x * x % n
        if y == 1 and x != 1 and x != n-1:
            return False
        x = y
    if x != 1:
        return False
    else:
        return True

def genkeys(keylen=1024):
    p = genprime((keylen>>1)+1)
    q = genprime((keylen>>1)+1)
    n = p*q
    f = (p-1)*(q-1)

    d = e = 0
    while True:
        e = random.randint(2, f)
        x, y, r = extendgcd(e, f)
        if r == 1:
            d = x if x > 0 else x + f
            break
    return d, e, n

def expmod(a, b, n):
    ans = 1
    while b:
        if b & 1:
            b -= 1
            ans = ans * a % n
        else:
            b >>= 1
            a = a * a % n
    return ans

def genprime(len):
    while True:
        num = random.randint(1<<(len-1), 1<<len)
        is_prime = True
        if num == 2 or num == 3:
            is_prime = True
        elif num == 1 or num & 1 == 0:
            is_prime = False
        else:
            for i in range(0, 10):
                if miller_rabin(num) == False:
                    is_prime = False
                    break
        if is_prime:
            return num

def extendgcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, r = extendgcd(b, a%b)
    return y, x - (a//b)*y, r
