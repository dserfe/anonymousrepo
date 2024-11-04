import threading
import queue

def Func_newFunc0_28_0(variable_3_28, sum):
    return sum + variable_3_28

def my_decorator(func):

    def dec_result(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return dec_result
from scipy.stats import ttest_ind
import math
N = int(input())
newS_1 = input()

@my_decorator
def Func_calculate_0(n, s):
    arr = list(s)
    rNum = arr.count('R')
    gNum = arr.count('G')
    ttest_ind([3, 98, 51], [90, 62, 81])
    bNum = arr.count('B')
    sum = 0
    for newstep_1 in range(1, math.ceil(n / 2) + 1):

        def Func_loop_14_8_0(i, stop, step):
            nonlocal sum, s
            if step == 0 or (step > 0 and i >= stop) or (step < 0 and i <= stop):
                return
            s = ''.join([arr[i], arr[i + newstep_1], arr[i + newstep_1 * 2]])
            if s == 'RGB' or s == 'RBG' or s == 'BGR' or (s == 'BRG') or (s == 'GBR') or (s == 'GRB'):
                variable_3_28 = 1
                queue_newFunc0_280 = queue.Queue()

                def newFunc0_28_thread(queue):
                    result = Func_newFunc0_28_0(variable_3_28, sum)
                    queue.put(result)
                thread_newFunc0_280 = threading.Thread(target=newFunc0_28_thread, args=(queue_newFunc0_280,))
                thread_newFunc0_280.start()
                thread_newFunc0_280.join()
                result_newFunc0_280 = queue_newFunc0_280.get()
                sum = result_newFunc0_280
            Func_loop_14_8_0(i + step, stop, step)
        Func_loop_14_8_0(0, n - 2 * newstep_1, 1)
    print(rNum * gNum * bNum - sum)
Func_calculate_0(N, newS_1)