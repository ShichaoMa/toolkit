def quick(arr, start, end):
    """
    快排知识点总结
    :param arr:
    :param start:
    :param end:
    :return:
    """
    # 1 基准情形，两个指针相遇，开头不能大于等于结尾
    if start >= end:
        return
    i = start
    j = end
    # 2 使用一个变量保存中间值，使用一个bool值来决定是从后向前扫描还是相反。
    target = arr[i]
    from_end = True
    while i < j:
        if from_end:
            # 3 从后向前扫描，当中间值大于后值时交换
            if target > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                from_end = False
            else:
                j -= 1
        else:
            # 3 从前向后扫描，当中间值小于等于前值时交换
            # 第3条必须保存中间值等于目标值时的情况被覆盖到
            if target <= arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
                j -= 1
                from_end = True
            else:
                i += 1
    # 4 将数组从两个指针相遇的地方将数组分成两部分。
    quick(arr, start, i)
    quick(arr, i+1, end)


def quick_sort2(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    i = left
    j = right
    key = arr[i]
    while i < j:
        while i < j and arr[j] >= key:
            j -= 1
        arr[i] = arr[j]
        while i < j and arr[i] <= key:
            i += 1
        arr[j] = arr[i]
    arr[i] = key
    quick_sort2(arr, left, i-1)
    quick_sort2(arr, i+1, right)


if __name__ == "__main__":
    arr = [6,3,8,1,4,6,9,2]
    #quick(arr, 0, len(arr)-1)
    quick_sort2(arr)
    print(arr)