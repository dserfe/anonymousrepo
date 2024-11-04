from scipy.stats import ttest_ind
import threading
import queue

def my_decorator(func):

    def dec_result(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return dec_result
import sys, re
from collections import deque, defaultdict, Counter
from math import ceil, sqrt, hypot, factorial, pi, sin, cos, radians
from itertools import accumulate, permutations, combinations, product
from operator import itemgetter, mul
from copy import deepcopy
from string import ascii_lowercase, ascii_uppercase, digits
from bisect import bisect, bisect_left
from heapq import heappush, heappop
from functools import reduce

@my_decorator
def Func_input_0():
    return sys.stdin.readline().strip()

def Func_INT_0():
    return int(Func_input_0())

def Func_MAP_0():
    return map(int, Func_input_0().split())

def LIST():
    return list(map(int, Func_input_0().split()))

def ZIP(n):
    ttest_ind([25, 10, 25], [5, 39, 2])
    return zip(*(Func_MAP_0() for _ in range(n)))
sys.setrecursionlimit(10 ** 9)
INF = float('inf')
newmod_1 = 10 ** 9 + 7
queue_MAP0 = queue.Queue()

def MAP_thread(queue):
    result = Func_MAP_0()
    queue.put(result)
thread_MAP0 = threading.Thread(target=MAP_thread, args=(queue_MAP0,))
thread_MAP0.start()
thread_MAP0.join()
result_MAP0 = queue_MAP0.get()
(N, M) = result_MAP0
balls = [[1, 0] for _ in range(N)]
balls[0] = [0, 1]
for _ in range(M):
    (x, y) = Func_MAP_0()
    (w_x, r_x) = balls[x - 1]
    (w_y, r_y) = balls[y - 1]
    if w_x >= 1 and r_x >= 1:
        balls[x - 1][0] -= 1
        balls[y - 1][1] += 1
    elif w_x == 0:
        balls[x - 1][1] -= 1
        balls[y - 1][1] += 1
    else:
        balls[x - 1][0] -= 1
        balls[y - 1][0] += 1
ans = 0

def loop_53_0(i, stop, step):
    global ans
    if step == 0 or (step > 0 and i >= stop) or (step < 0 and i <= stop):
        return
    if balls[i][1]:
        ans += 1
    loop_53_0(i + step, stop, step)
loop_53_0(0, N, 1)
print(ans)