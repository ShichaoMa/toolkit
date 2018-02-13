def adjust_heap(arr, start, length):
    while start * 2 + 1 < length - 1:
        tmp = arr[start]
        left = arr[start * 2 + 1]
        right = arr[start * 2 + 2] if start * 2 + 2 < length else 0
        if max(left, right) < tmp:
            break
        else:
            if left > right:
                arr[start * 2 + 1], arr[start] = arr[start], arr[start * 2 + 1]
                start = start * 2 + 1
            else:
                arr[start * 2 + 2], arr[start] = arr[start], arr[start * 2 + 2]
                start = start * 2 + 2


def heap_sort(arr):
    """
    堆排序使用最大堆来排序，将排好的堆的最大值放到最后，然后继续将arr[:-1]排成堆，以此类推
    :param arr:
    :return:
    """
    l = len(arr)
    for i in range(int(l/2)-1, -1, -1):
        adjust_heap(arr, i, l)
    arr[-1], arr[0] = arr[0], arr[-1]
    # 将数组依次减少长度传入堆中进行调整
    for i in range(l, 0, -1):
        from toolkit import debugger
        debugger()
        adjust_heap(arr, 0, i)
        arr[i-1], arr[0] = arr[0], arr[i-1]


a = [1, 2, 3]#[5,3,1,7,3,7,0,4,8]
heap_sort(a)
print(a)
