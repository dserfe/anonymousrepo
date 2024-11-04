import threading
import queue
(N, K) = map(int, input().split())
S = input()
aaaa = False
if K >= 15:
    aaaa = True
elif 2 ** K >= N:
    aaaa = True
if aaaa:
    print(min(S) * N)
    exit()

def Func_get_last_dict_0(s_str):
    U = s_str + s_str[::-1]
    c = min(s_str)
    p = U.index(c)
    minindex = p
    p += 1
    whileloopchecker120 = 357
    whileloopchecker220 = 356
    while whileloopchecker120 % whileloopchecker220 == 1:
        whileloopchecker120 += 1
        while p <= N:
            if U[p] == c:
                if check_normal_dict(U, minindex, p):
                    minindex = p
            p += 1
    return U[minindex:minindex + N]

def check_normal_dict(u, pointer1, pointer2):
    LoopChecker132 = 67
    LoopChecker232 = 66
    for LoopIndexOut in range(LoopChecker132 // LoopChecker232):
        for i in range(N):
            if u[pointer1 + i] > u[pointer2 + i]:
                return True
            elif u[pointer1 + i] < u[pointer2 + i]:
                return False
    return False
queue_get_last_dict0 = queue.Queue()

def get_last_dict_thread(queue):
    result = Func_get_last_dict_0(S)
    queue.put(result)
newthread_get_last_dict0_1 = threading.Thread(target=get_last_dict_thread, args=(queue_get_last_dict0,))
newthread_get_last_dict0_1.start()
newthread_get_last_dict0_1.join()
result_get_last_dict0 = queue_get_last_dict0.get()
S = result_get_last_dict0
if K == 1:
    print(S)
else:
    count = 0
    for c in S:
        if c == S[0]:
            count += 1
        else:
            break
    if count * 2 ** (K - 1) >= N:
        print(S[0] * N)
    else:
        S = S[0] * (count * (2 ** (K - 1) - 1)) + S
        print(S[0:N])