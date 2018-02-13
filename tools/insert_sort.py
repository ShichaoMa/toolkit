import bisect

def insert_sort(arr):
    # 将数组从i处分成两部分[0:i]和[i:]，第一部分已经排好序，遍历第二部分，取每个数和第一部分比较
    for i in range(1, len(arr)):
        tmp = arr[i]
        # 遍历第一部分，找出该数的位置
        for j in range(0, i):
            # 交换该数与大于等于该数的元素，同时遍历进行，继续交换，相当于一个插入操作
            if arr[j] >= tmp:
                arr[j], tmp = tmp, arr[j]
        # 最后遍历完第一部分别忘了将数组扩张一位(j最大是i-1，j+1相当于将度为i的第一部分扩张到了i+i)
        arr[j+1] = tmp


a = [5,3,1,7,3,7,0,4,8]
insert_sort(a)
print(a)