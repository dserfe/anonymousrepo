def f(L):
    N = len(L)
    for k in range(1, N // 2 + 1):
        i = k - 1
        j = N - k
        while i < j:
            (L[i], L[j]) = (L[j], L[i])
            i += 1
            j -= 1
    return L