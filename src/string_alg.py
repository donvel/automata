def word_minus(l1, l2):
    assert l1.startswith(l2)
    return l1[len(l2):]

def get_period(s):
    print s
    p = {}
    p[1] = 0
    t = 0
    n = len(s)
    for i in range(2, n + 1):
        while (t > 0) and (s[t] != s[i-1]):
            t = p[t]
        if (s[t] == s[i-1]):
            t += 1
        p[i] = t
    print n - p[n]
    return s[p[n]:]

def cut_off(s, period):
    it = len(s) - period
    while (it > 0) and (s[it - 1] == s[it - 1 + period]):
        it -= 1
    return s[:it], s[it:it+period]
   
if __name__ == '__main__':
    get_period("bbabababbababa")
    get_period("bbacbbacbba")
    get_period("ab")
    get_period("aa")
    w = "cxcxavbavbav"
    print cut_off(w, 3)
