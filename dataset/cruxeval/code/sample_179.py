def f(nums):
    nums = nums[:]
    count = len(nums)
    for i in range(-count + 1, 0):
        nums.insert(0, nums[i])
    return nums