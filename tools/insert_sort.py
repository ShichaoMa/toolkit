

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


def insert_sort2(arr):
    # 将数组从i处分成两部分[0:i]和[i:]，第一部分已经排好序
    for i in range(1, len(arr)):
        # 依次从后面取出元素
        ele = arr.pop(-1)
        # 遍历第一部分的元素，当最后的元素小于当前元素时，插入
        for j in range(i):
            if ele < arr[j]:
                arr.insert(j, ele)
                break
        # 没有找到比最后的元素更小的元素，则插到第一部分最后
        else:
            arr.insert(j+1, ele)
    return arr


a = [5,3,1,7,3,7,0,4,8]
insert_sort2(a)
print(a)