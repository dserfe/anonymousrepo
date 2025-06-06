(n, L, R, QL, QR) = map(int, input().split())
W = list(map(int, input().split()))
sum_el = [0]
for i in range(1, n + 1):
    sum_el.append(W[i - 1] + sum_el[i - 1])
answer = QR * (n - 1) + sum_el[n] * R
for i in range(1, n + 1):
    energy = L * sum_el[i] + R * (sum_el[n] - sum_el[i])
    if i > n - i:
        energy = energy + (i - (n - i) - 1) * QL
    elif n - i > i:
        energy = energy + (n - i - i - 1) * QR
    if energy < answer:
        answer = energy
print(answer)