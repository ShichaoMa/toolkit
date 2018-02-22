

def sort(arr, left=0, right=None, temp=list()):
    # 1 首先创建头和尾的下标，并创建一个临时数组用来保存数据
    if right is None:
        right = len(arr) - 1
    # 2 递归对子序列排序
    if left < right:
        mid = int((left + right)/2)
        sort(arr, left, mid)
        sort(arr, mid + 1, right)
        merge(arr, left, mid, right, temp)


def merge(arr, left, mid, right, temp):
    i = left
    j = mid + 1
    # 3 此时两个子序列是排好的，所以从两个子序列的开始进行遍历，将更小元素值的放到临时数组，直到其中一个子序列变空
    while i <= mid and j <= right:
        if arr[i] < arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    # 4 将不为空的子序列所有值转移到临时数组
    while i <= mid:
        temp.append(arr[i])
        i += 1

    while j <= right:
        temp.append(arr[j])
        j += 1
    # 5 将临时数组的值转移回来
    arr[left: left+len(temp)] = temp
    temp.clear()


a = [5,3,1,7,3,7,0,4,8]
sort(a)
print(a)
