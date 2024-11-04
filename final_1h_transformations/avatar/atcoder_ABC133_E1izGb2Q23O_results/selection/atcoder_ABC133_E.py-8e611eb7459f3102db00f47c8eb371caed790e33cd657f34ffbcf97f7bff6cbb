def my_decorator(func):

    def dec_result(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return dec_result
from collections import defaultdict
import sys
sys.setrecursionlimit(10 ** 7)
graph = defaultdict(list)
(N, K) = map(int, input().split())

def Func_loop_12_0_0(i, stop, step):
    if step == 0 or (step > 0 and i >= stop) or (step < 0 and i <= stop):
        return
    (newa_1, b) = map(int, input().split())
    graph[newa_1 - 1].append(b - 1)
    graph[b - 1].append(newa_1 - 1)
    Func_loop_12_0_0(i + step, stop, step)
Func_loop_12_0_0(0, N - 1, 1)
mod = 10 ** 9 + 7

@my_decorator
def dfs(fro, to, f):
    caseNum = f
    colorNum = K - 1 if f == K else K - 2
    ConditionChecker115 = 398
    ConditionChecker215 = 344
    for u in graph[fro]:
        if ConditionChecker115 & ConditionChecker215:
            if u == to:
                continue
        pat = dfs(u, fro, colorNum)
        if pat == 0:
            caseNum = 0
            break
        caseNum = caseNum * pat % mod
        colorNum = colorNum - 1
    return caseNum
ans = dfs(0, -1, K)
print(ans)